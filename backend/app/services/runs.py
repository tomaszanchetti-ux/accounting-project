from __future__ import annotations

import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from io import BytesIO, StringIO
from pathlib import Path
from typing import Protocol
from uuid import uuid4

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.core.settings import get_settings
from app.repositories.runs import RunsRepositoryProtocol
from app.schemas import ReconciliationEngineInput, ToleranceProfile
from app.schemas.runs import (
    ConceptAnalysisEvidenceSummary,
    ConceptAnalysisHeader,
    ConceptAnalysisKpis,
    ConceptAnalysisPayload,
    DrilldownFilterContext,
    DrilldownSummary,
    ExpectedTotalUsedRecord,
    RunCreateRequest,
    RunDrilldownResponse,
    RunEventRecord,
    RunExceptionRecord,
    RunExecuteRequest,
    RunExecuteResponse,
    RunFileReferenceRequest,
    RunPayrollLineRecord,
    RunRecord,
    RunResponse,
    RunResultDetailResponse,
    RunResultRecord,
    RunResultsResponse,
    RunSummaryResponse,
    UploadedFileRecord,
    UploadedFileResponse,
)
from app.services.reconciliation import (
    run_reconciliation_engine,
    validate_expected_totals,
    validate_payroll_schema,
)
from app.services.storage import (
    build_storage_path,
    download_file_from_bucket,
    upload_file_to_bucket,
)

RULES_VERSION_DEFAULT = "engine-v1"


@dataclass(frozen=True)
class RunExportArtifact:
    content: bytes
    filename: str
    media_type: str = "text/csv; charset=utf-8"


class RunNotFoundError(Exception):
    pass


class RunResultNotFoundError(Exception):
    pass


class StorageGatewayProtocol(Protocol):
    def build_input_path(self, run_id: str, filename: str) -> str: ...

    def upload_input_file(
        self,
        *,
        run_id: str,
        filename: str,
        file_bytes: bytes,
        content_type: str,
    ) -> tuple[str, str]: ...

    def download_file(self, bucket_name: str, storage_path: str) -> bytes: ...


class SupabaseStorageGateway:
    def __init__(self) -> None:
        self.settings = get_settings()

    def build_input_path(self, run_id: str, filename: str) -> str:
        return build_storage_path(run_id, filename, artifact_type="inputs")

    def upload_input_file(
        self,
        *,
        run_id: str,
        filename: str,
        file_bytes: bytes,
        content_type: str,
    ) -> tuple[str, str]:
        storage_path = self.build_input_path(run_id, filename)
        upload_file_to_bucket(
            self.settings.storage_bucket_raw_inputs,
            storage_path,
            file_bytes,
            content_type=content_type,
        )
        return self.settings.storage_bucket_raw_inputs, storage_path

    def download_file(self, bucket_name: str, storage_path: str) -> bytes:
        return download_file_from_bucket(bucket_name, storage_path)


class RunsService:
    def __init__(
        self,
        repository: RunsRepositoryProtocol,
        storage_gateway: StorageGatewayProtocol | None = None,
    ):
        self.repository = repository
        self.storage_gateway = storage_gateway or SupabaseStorageGateway()

    def create_run(self, request: RunCreateRequest) -> RunResponse:
        run = self.repository.create_run(
            run_label=request.run_label,
            period=request.period,
            legal_entity_scope=request.legal_entity_scope,
            tolerance_profile_label=request.tolerance_profile_label,
            rules_version=request.rules_version,
        )
        return RunResponse(run=run)

    def register_file_reference(
        self,
        run_id: str,
        request: RunFileReferenceRequest,
    ) -> UploadedFileResponse:
        run = self.repository.get_run(run_id)
        if not run:
            raise RunNotFoundError(run_id)

        uploaded_file = self.repository.upsert_uploaded_file(
            run_id=run_id,
            file_name=request.file_name,
            file_type=request.file_type,
            source_kind=request.source_kind,
            storage_path=request.storage_path,
            storage_bucket=request.storage_bucket,
        )

        current_status = run.status
        if current_status == "DRAFT":
            current_status = "INPUT_VALIDATED"
            self.repository.update_run_status(run_id, status=current_status)

        return UploadedFileResponse(uploaded_file=uploaded_file)

    def upload_file_bytes(
        self,
        run_id: str,
        *,
        file_name: str,
        file_type: str,
        file_bytes: bytes,
        content_type: str,
    ) -> UploadedFileResponse:
        run = self.repository.get_run(run_id)
        if not run:
            raise RunNotFoundError(run_id)

        storage_bucket, storage_path = self.storage_gateway.upload_input_file(
            run_id=run_id,
            filename=file_name,
            file_bytes=file_bytes,
            content_type=content_type,
        )

        uploaded_file = self.repository.upsert_uploaded_file(
            run_id=run_id,
            file_name=file_name,
            file_type=file_type,
            source_kind="supabase_storage",
            storage_path=storage_path,
            storage_bucket=storage_bucket,
        )

        if run.status == "DRAFT":
            self.repository.update_run_status(run_id, status="INPUT_VALIDATED")

        return UploadedFileResponse(uploaded_file=uploaded_file)

    def execute_run(
        self,
        run_id: str,
        request: RunExecuteRequest | None = None,
    ) -> RunExecuteResponse:
        del request
        run = self.repository.get_run(run_id)
        if not run:
            raise RunNotFoundError(run_id)

        uploaded_files = {
            uploaded.file_type: uploaded
            for uploaded in self.repository.list_uploaded_files(run_id)
        }

        payroll_file = uploaded_files.get("payroll")
        expected_totals_file = uploaded_files.get("expected_totals")
        concept_master_file = uploaded_files.get("concept_master")
        employee_reference_file = uploaded_files.get("employee_reference")

        missing_types = [
            required_type
            for required_type, uploaded in (
                ("payroll", payroll_file),
                ("expected_totals", expected_totals_file),
                ("concept_master", concept_master_file),
            )
            if uploaded is None
        ]
        if missing_types:
            invalid_run = self.repository.update_run_status(
                run_id,
                status="INVALID_INPUT",
                completed_at=datetime.now(timezone.utc),
                error_message=(
                    "Missing required file references for run execution: "
                    + ", ".join(missing_types)
                ),
            )
            return RunExecuteResponse(
                run=invalid_run or run,
                message="Run could not start because required input references are missing.",
            )

        self.repository.update_run_status(run_id, status="PROCESSING", error_message=None)

        try:
            payroll_source = self._load_uploaded_source(payroll_file)
            expected_totals_source = self._load_uploaded_source(expected_totals_file)
            concept_master_source = self._load_uploaded_source(concept_master_file)
            employee_reference_source = (
                self._load_uploaded_source(employee_reference_file)
                if employee_reference_file
                else None
            )

            payroll_schema_validation = validate_payroll_schema(payroll_source)
            expected_totals_validation = validate_expected_totals(
                expected_totals_source,
                target_period=run.period,
            )

            blocking_messages = [
                issue.message for issue in payroll_schema_validation.errors if issue.blocking
            ] + [
                issue.message
                for issue in expected_totals_validation.validation_errors
                if issue.blocking
            ]
            if blocking_messages:
                invalid_run = self.repository.update_run_status(
                    run_id,
                    status="INVALID_INPUT",
                    completed_at=datetime.now(timezone.utc),
                    error_message=" | ".join(blocking_messages),
                )
                return RunExecuteResponse(
                    run=invalid_run or run,
                    message="Run finished with invalid input.",
                )

            tolerance_profile = ToleranceProfile(
                label=run.tolerance_profile_label or "mvp-default"
            )
            engine_result = run_reconciliation_engine(
                ReconciliationEngineInput(
                    payroll=payroll_source,
                    expected_totals=expected_totals_source,
                    concept_master=concept_master_source,
                    employee_reference=employee_reference_source,
                    target_period=run.period,
                    legal_entity=run.legal_entity_scope,
                    tolerance_profile=tolerance_profile,
                )
            )

            completed_at = datetime.now(timezone.utc)
            result_rows = _build_result_records(run_id, engine_result)
            result_id_by_concept = {
                row.concept_code_normalized: row.id for row in result_rows
            }
            exception_rows = _build_exception_records(
                run_id=run_id,
                engine_result=engine_result,
                result_id_by_concept=result_id_by_concept,
                created_at=completed_at,
            )
            expected_totals_used = _build_expected_totals_used_records(
                run_id=run_id,
                source=expected_totals_source,
                target_period=run.period,
            )
            payroll_lines = _build_payroll_line_records(
                run_id=run_id,
                engine_result=engine_result,
                exception_rows=exception_rows,
            )

            overall_status = str(engine_result.run_metrics["overall_run_status"])
            final_status = (
                "RECONCILED"
                if overall_status == "reconciled"
                else "RECONCILED_WITH_EXCEPTIONS"
            )
            updated_run = self.repository.persist_run_execution(
                run_id=run_id,
                expected_totals_used=expected_totals_used,
                results=result_rows,
                exceptions=exception_rows,
                payroll_lines=payroll_lines,
                final_status=final_status,
                overall_status=overall_status,
                source_file_name=payroll_file.file_name,
                record_count=len(payroll_lines),
                concept_count=len(result_rows),
                run_metrics=engine_result.run_metrics,
                completed_at=completed_at,
            )

            return RunExecuteResponse(
                run=updated_run,
                message="Run executed and persisted successfully.",
            )
        except FileNotFoundError as error:
            invalid_run = self.repository.update_run_status(
                run_id,
                status="INVALID_INPUT",
                completed_at=datetime.now(timezone.utc),
                error_message=str(error),
            )
            return RunExecuteResponse(
                run=invalid_run or run,
                message="Run failed because one referenced input file could not be found.",
            )
        except Exception as error:
            failed_run = self.repository.update_run_status(
                run_id,
                status="FAILED",
                completed_at=datetime.now(timezone.utc),
                error_message=str(error),
            )
            if failed_run is not None:
                raise RuntimeError(str(error)) from error
            raise

    def _load_uploaded_source(
        self,
        uploaded_file: UploadedFileRecord | None,
    ) -> Path | pd.DataFrame | None:
        if uploaded_file is None:
            return None

        if uploaded_file.source_kind == "local_path":
            path = Path(uploaded_file.storage_path)
            if not path.exists():
                raise FileNotFoundError(
                    f"Referenced local file does not exist: {uploaded_file.storage_path}"
                )
            return path

        if not uploaded_file.storage_bucket:
            raise FileNotFoundError(
                f"Missing storage bucket for uploaded file reference: {uploaded_file.file_name}"
            )

        file_bytes = self.storage_gateway.download_file(
            uploaded_file.storage_bucket,
            uploaded_file.storage_path,
        )
        return pd.read_csv(BytesIO(file_bytes))

    def get_summary(self, run_id: str) -> RunSummaryResponse:
        run = self.repository.get_run(run_id)
        if not run:
            raise RunNotFoundError(run_id)

        results = self.repository.list_results(run_id)
        uploaded_files = self.repository.list_uploaded_files(run_id)
        return RunSummaryResponse(
            run=run,
            metrics=run.run_metrics,
            preview_results=results[:5],
            event_log=_build_run_event_log(run, uploaded_files, results),
        )

    def list_results(self, run_id: str) -> RunResultsResponse:
        run = self.repository.get_run(run_id)
        if not run:
            raise RunNotFoundError(run_id)

        results = self.repository.list_results(run_id)
        return RunResultsResponse(
            run=run,
            total_results=len(results),
            results=results,
        )

    def get_result_detail(self, run_id: str, result_id: str) -> RunResultDetailResponse:
        run = self.repository.get_run(run_id)
        if not run:
            raise RunNotFoundError(run_id)

        result = self.repository.get_result(run_id, result_id)
        if not result:
            raise RunResultNotFoundError(result_id)

        exceptions = self.repository.list_exceptions(run_id, result_id=result_id)
        uploaded_files = self.repository.list_uploaded_files(run_id)
        return RunResultDetailResponse(
            run=run,
            result=result,
            exceptions=exceptions,
            concept_analysis=_build_concept_analysis_payload(result, exceptions),
            event_log=_build_run_event_log(run, uploaded_files, [result]),
        )

    def get_drilldown(self, run_id: str, result_id: str) -> RunDrilldownResponse:
        run = self.repository.get_run(run_id)
        if not run:
            raise RunNotFoundError(run_id)

        result = self.repository.get_result(run_id, result_id)
        if not result:
            raise RunResultNotFoundError(result_id)

        exceptions = self.repository.list_exceptions(run_id, result_id=result_id)
        exception_record_ids = {
            exception.record_id for exception in exceptions if exception.record_id
        }
        rows = [
            row
            for row in self.repository.list_payroll_lines(run_id)
            if (
                row.concept_code_normalized == result.concept_code_normalized
                or row.record_id in exception_record_ids
            )
        ]
        uploaded_files = self.repository.list_uploaded_files(run_id)
        return RunDrilldownResponse(
            run=run,
            result=result,
            total_rows=len(rows),
            summary=_build_drilldown_summary(result, rows),
            filter_context=_build_drilldown_filter_context(rows),
            rows=rows,
            event_log=_build_run_event_log(run, uploaded_files, [result]),
        )

    def export_summary_csv(self, run_id: str) -> RunExportArtifact:
        run = self.repository.get_run(run_id)
        if not run:
            raise RunNotFoundError(run_id)

        results = self.repository.list_results(run_id)
        buffer = StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=[
                "run_label",
                "period",
                "concept_code",
                "concept_name",
                "expected_amount",
                "observed_amount",
                "absolute_diff",
                "relative_diff_pct",
                "status",
                "explanation_preview",
            ],
        )
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "run_label": run.run_label,
                    "period": result.period,
                    "concept_code": result.concept_code_normalized,
                    "concept_name": result.concept_name_normalized,
                    "expected_amount": str(result.expected_amount),
                    "observed_amount": str(result.observed_amount),
                    "absolute_diff": str(result.absolute_diff),
                    "relative_diff_pct": (
                        ""
                        if result.relative_diff_pct is None
                        else str(result.relative_diff_pct)
                    ),
                    "status": result.status,
                    "explanation_preview": result.summary_explanation or "",
                }
            )

        return RunExportArtifact(
            content=buffer.getvalue().encode("utf-8"),
            filename=(
                f"reconciliation-summary-{_slugify_filename(run.run_label)}-"
                f"{run.period}.csv"
            ),
        )

    def export_exception_detail_csv(
        self,
        run_id: str,
        result_id: str,
    ) -> RunExportArtifact:
        run = self.repository.get_run(run_id)
        if not run:
            raise RunNotFoundError(run_id)

        result = self.repository.get_result(run_id, result_id)
        if not result:
            raise RunResultNotFoundError(result_id)

        rows = self.repository.list_payroll_lines(
            run_id,
            concept_code_normalized=result.concept_code_normalized,
        )
        buffer = StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=[
                "run_label",
                "period",
                "record_id",
                "employee_id",
                "employee_name",
                "legal_entity",
                "concept_code",
                "concept_name",
                "amount",
                "currency",
                "exception_type",
                "observation",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "run_label": run.run_label,
                    "period": row.payroll_period or result.period,
                    "record_id": row.record_id,
                    "employee_id": row.employee_id or "",
                    "employee_name": row.employee_name or "",
                    "legal_entity": row.legal_entity or "",
                    "concept_code": row.concept_code_normalized or "",
                    "concept_name": row.concept_name_normalized or "",
                    "amount": "" if row.amount is None else str(row.amount),
                    "currency": row.currency or "",
                    "exception_type": _serialize_row_exception_types(row),
                    "observation": _build_row_observation(row),
                }
            )

        return RunExportArtifact(
            content=buffer.getvalue().encode("utf-8"),
            filename=(
                "exception-detail-"
                f"{_slugify_filename(run.run_label)}-"
                f"{result.period}-"
                f"{_slugify_filename(result.concept_code_normalized)}.csv"
            ),
        )

    def export_exception_detail_pdf(
        self,
        run_id: str,
        result_id: str,
    ) -> RunExportArtifact:
        run = self.repository.get_run(run_id)
        if not run:
            raise RunNotFoundError(run_id)

        result = self.repository.get_result(run_id, result_id)
        if not result:
            raise RunResultNotFoundError(result_id)

        exceptions = self.repository.list_exceptions(run_id, result_id=result_id)
        rows = self.repository.list_payroll_lines(
            run_id,
            concept_code_normalized=result.concept_code_normalized,
        )
        concept_analysis = _build_concept_analysis_payload(result, exceptions)
        drilldown_summary = _build_drilldown_summary(result, rows)

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=16 * mm,
            bottomMargin=16 * mm,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#132033"),
            spaceAfter=8,
        )
        section_style = ParagraphStyle(
            "SectionTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#132033"),
            spaceAfter=6,
            spaceBefore=10,
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#334155"),
        )
        small_style = ParagraphStyle(
            "Small",
            parent=body_style,
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#64748B"),
        )

        story = [
            Paragraph("Accounting Reconciliation Report", title_style),
            Paragraph(
                (
                    f"Run: {run.run_label} | Period: {run.period} | "
                    f"Concept: {result.concept_code_normalized}"
                ),
                small_style,
            ),
            Spacer(1, 6),
            Paragraph("Concept summary", section_style),
            Paragraph(
                concept_analysis.summary_statement
                or "No summary statement is available for this concept.",
                body_style,
            ),
            Spacer(1, 8),
            Paragraph("Recommended action", section_style),
            Paragraph(
                concept_analysis.recommended_action
                or "Review the concept-level evidence and confirm the supporting records.",
                body_style,
            ),
            Spacer(1, 8),
            Paragraph("Key metrics", section_style),
            _build_pdf_table(
                [
                    ["Metric", "Value"],
                    ["Status", result.status],
                    ["Expected total", _format_currency_like(result.expected_amount)],
                    ["Observed total", _format_currency_like(result.observed_amount)],
                    ["Absolute difference", _format_currency_like(result.absolute_diff)],
                    ["Difference %", _format_percentage_like(result.relative_diff_pct)],
                    ["Records analyzed", str(result.record_count)],
                    [
                        "Employees affected",
                        str(result.impacted_employees_count or result.employee_count),
                    ],
                ],
                col_widths=[55 * mm, 95 * mm],
            ),
            Paragraph("Top causes", section_style),
        ]

        if concept_analysis.top_causes:
            top_cause_rows = [["Cause", "Impact", "Confidence"]]
            for cause in concept_analysis.top_causes[:3]:
                top_cause_rows.append(
                    [
                        cause.exception_type,
                        _format_currency_like(cause.estimated_impact_amount),
                        _format_percentage_from_confidence(cause.confidence),
                    ]
                )
            story.append(_build_pdf_table(top_cause_rows, col_widths=[85 * mm, 35 * mm, 30 * mm]))
        else:
            story.append(Paragraph("No ranked causes were returned for this concept.", body_style))

        story.extend(
            [
                Paragraph("Evidence summary", section_style),
                _build_pdf_table(
                    [
                        ["Measure", "Value"],
                        [
                            "Total exceptions",
                            str(concept_analysis.evidence_summary.total_exceptions),
                        ],
                        [
                            "Rows with evidence",
                            str(concept_analysis.evidence_summary.records_with_exception),
                        ],
                        [
                            "Employees with exception",
                            str(concept_analysis.evidence_summary.employees_with_exception),
                        ],
                        ["Rows in deep dive", str(len(rows))],
                        [
                            "Total amount",
                            _format_currency_like(drilldown_summary.total_amount),
                        ],
                    ],
                    col_widths=[55 * mm, 95 * mm],
                ),
                Paragraph("Sample records", section_style),
            ]
        )

        sample_rows = [["Record", "Employee", "Amount", "Exceptions"]]
        for row in rows[:12]:
            sample_rows.append(
                [
                    row.record_id,
                    row.employee_name or row.employee_id or "Unknown",
                    _format_currency_like(row.amount),
                    _serialize_row_exception_types(row) or "None",
                ]
            )
        story.append(
            _build_pdf_table(
                sample_rows,
                col_widths=[30 * mm, 55 * mm, 28 * mm, 52 * mm],
                small=True,
            )
        )

        story.extend(
            [
                Spacer(1, 8),
                Paragraph(
                    (
                        f"Generated from run {run.id} on "
                        f"{_format_datetime_for_report(run.completed_at)}."
                    ),
                    small_style,
                ),
            ]
        )

        doc.build(story)

        return RunExportArtifact(
            content=buffer.getvalue(),
            filename=(
                "reconciliation-report-"
                f"{_slugify_filename(run.run_label)}-"
                f"{result.period}-"
                f"{_slugify_filename(result.concept_code_normalized)}.pdf"
            ),
            media_type="application/pdf",
        )

def _build_expected_totals_used_records(
    *,
    run_id: str,
    source: Path | pd.DataFrame,
    target_period: str,
) -> list[ExpectedTotalUsedRecord]:
    dataframe = source.copy() if isinstance(source, pd.DataFrame) else pd.read_csv(source)
    filtered = dataframe.loc[
        dataframe["payroll_period"].astype("string").str.strip() == target_period
    ].copy()
    if filtered.empty:
        return []

    filtered["concept_code_normalized"] = (
        filtered["concept_code"].astype("string").str.strip().str.upper()
    )
    filtered["currency"] = filtered["currency"].astype("string").str.strip().str.upper()
    filtered["expected_amount"] = pd.to_numeric(
        filtered["expected_amount"],
        errors="coerce",
    )

    records: list[ExpectedTotalUsedRecord] = []
    for row in filtered.itertuples(index=False):
        records.append(
            ExpectedTotalUsedRecord(
                id=str(uuid4()),
                run_id=run_id,
                period=str(target_period),
                concept_code_normalized=str(row.concept_code_normalized),
                expected_amount=Decimal(str(row.expected_amount)),
                currency=str(row.currency),
                legal_entity=(
                    None
                    if not hasattr(row, "legal_entity") or pd.isna(row.legal_entity)
                    else str(row.legal_entity)
                ),
            )
        )

    return records


def _build_result_records(
    run_id: str,
    engine_result,
) -> list[RunResultRecord]:
    explanations_by_concept = {
        explanation.concept_code_normalized: explanation
        for explanation in engine_result.debug_artifacts.concept_explanations
    }
    rows: list[RunResultRecord] = []

    for summary_row in engine_result.summary_rows:
        explanation = explanations_by_concept.get(summary_row.concept_code_normalized)
        rows.append(
            RunResultRecord(
                id=str(uuid4()),
                run_id=run_id,
                period=summary_row.period,
                concept_code_normalized=summary_row.concept_code_normalized,
                concept_name_normalized=summary_row.concept_name_normalized,
                observed_amount=summary_row.observed_amount,
                expected_amount=summary_row.expected_amount,
                absolute_diff=summary_row.absolute_diff,
                relative_diff_pct=summary_row.relative_diff_pct,
                status=summary_row.status,
                record_count=summary_row.record_count,
                employee_count=summary_row.employee_count,
                invalid_record_count=summary_row.invalid_record_count,
                legal_entity=summary_row.legal_entity,
                summary_explanation=(
                    explanation.summary_statement if explanation else None
                ),
                recommended_action=(
                    explanation.recommended_action if explanation else None
                ),
                explained_amount_estimate=(
                    explanation.explained_amount_estimate if explanation else None
                ),
                impacted_records_count=(
                    explanation.impacted_records_count if explanation else None
                ),
                impacted_employees_count=(
                    explanation.impacted_employees_count if explanation else None
                ),
            )
        )

    return rows


def _build_pdf_table(
    rows: list[list[str]],
    *,
    col_widths: list[float],
    small: bool = False,
) -> Table:
    table = Table(rows, colWidths=col_widths, repeatRows=1)
    font_size = 7 if small else 8
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#132033")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), font_size),
                ("LEADING", (0, 0), (-1, -1), 10),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def _format_currency_like(value: Decimal | str | None) -> str:
    if value in (None, ""):
        return "N/A"

    try:
        number = Decimal(str(value))
    except Exception:
        return str(value)

    return f"EUR {number:,.2f}"


def _format_percentage_like(value: Decimal | str | None) -> str:
    if value in (None, ""):
        return "N/A"

    try:
        number = Decimal(str(value))
    except Exception:
        return str(value)

    return f"{number:.2f}%"


def _format_percentage_from_confidence(value: str | None) -> str:
    if not value:
        return "N/A"

    try:
        number = Decimal(str(value)) * Decimal("100")
    except Exception:
        return value

    return f"{number:.0f}%"


def _format_datetime_for_report(value: datetime | None) -> str:
    if value is None:
        return "an unknown time"

    return value.strftime("%Y-%m-%d %H:%M UTC")


def _build_exception_records(
    *,
    run_id: str,
    engine_result,
    result_id_by_concept: dict[str, str],
    created_at: datetime,
) -> list[RunExceptionRecord]:
    rows: list[RunExceptionRecord] = []
    for exception in engine_result.debug_artifacts.structured_exceptions:
        rows.append(
            RunExceptionRecord(
                id=str(uuid4()),
                run_id=run_id,
                result_id=result_id_by_concept.get(exception.concept_scope or ""),
                record_id=exception.record_id,
                employee_id=exception.employee_id,
                concept_scope=exception.concept_scope,
                exception_type=exception.exception_type,
                severity=exception.severity,
                scope_level=exception.scope_level,
                estimated_impact_amount=exception.estimated_impact_amount,
                observation=exception.observation,
                confidence=exception.confidence,
                created_at=created_at,
            )
        )
    return rows


def _build_payroll_line_records(
    *,
    run_id: str,
    engine_result,
    exception_rows: list[RunExceptionRecord],
) -> list[RunPayrollLineRecord]:
    base = engine_result.debug_artifacts.normalized_payroll
    if base is None or base.empty:
        return []

    exception_flags_by_record: dict[str, set[str]] = defaultdict(set)
    for exception in exception_rows:
        if exception.record_id:
            exception_flags_by_record[exception.record_id].add(exception.exception_type)

    rows: list[RunPayrollLineRecord] = []
    for row in base.itertuples(index=False):
        record_id = str(getattr(row, "record_id"))
        posting_date = getattr(row, "posting_date", None)
        if pd.isna(posting_date):
            posting_date = None
        elif hasattr(posting_date, "date"):
            posting_date = posting_date.date()

        invalid_reasons = getattr(row, "invalid_reasons", [])
        if not isinstance(invalid_reasons, list):
            invalid_reasons = list(invalid_reasons) if invalid_reasons else []

        rows.append(
            RunPayrollLineRecord(
                id=str(uuid4()),
                run_id=run_id,
                record_id=record_id,
                employee_id=_optional_string(getattr(row, "employee_id", None)),
                employee_name=_optional_string(getattr(row, "employee_name", None)),
                legal_entity=_optional_string(getattr(row, "legal_entity", None)),
                country=_optional_string(getattr(row, "country", None)),
                cost_center=_optional_string(getattr(row, "cost_center", None)),
                payroll_period=_optional_string(
                    getattr(row, "payroll_period_normalized", None)
                ),
                posting_date=posting_date,
                concept_code_raw=_optional_string(getattr(row, "concept_code", None)),
                concept_code_normalized=_optional_string(
                    getattr(row, "concept_code_normalized", None)
                ),
                concept_name_raw=_optional_string(getattr(row, "concept_name", None)),
                concept_name_normalized=_optional_string(
                    getattr(row, "concept_name_normalized", None)
                ),
                amount=_optional_decimal(getattr(row, "amount", None)),
                currency=_optional_string(getattr(row, "currency", None)),
                is_valid=bool(getattr(row, "is_valid_record", False)),
                exception_flags=sorted(exception_flags_by_record.get(record_id, set())),
                invalid_reasons=[str(reason) for reason in invalid_reasons],
            )
        )

    return rows


def _build_concept_analysis_payload(
    result: RunResultRecord,
    exceptions: list[RunExceptionRecord],
) -> ConceptAnalysisPayload:
    top_exception_types = _unique_preserving_order(
        [exception.exception_type for exception in exceptions]
    )[:3]
    records_with_exception = len({item.record_id for item in exceptions if item.record_id})
    employees_with_exception = len(
        {item.employee_id for item in exceptions if item.employee_id}
    )
    top_causes = _build_ranked_top_causes(exceptions)

    return ConceptAnalysisPayload(
        header=ConceptAnalysisHeader(
            concept_code_normalized=result.concept_code_normalized,
            concept_name_normalized=result.concept_name_normalized,
            period=result.period,
            status=result.status,
        ),
        kpis=ConceptAnalysisKpis(
            observed_amount=result.observed_amount,
            expected_amount=result.expected_amount,
            absolute_diff=result.absolute_diff,
            relative_diff_pct=result.relative_diff_pct,
            record_count=result.record_count,
            employee_count=result.employee_count,
            impacted_records_count=result.impacted_records_count,
            impacted_employees_count=result.impacted_employees_count,
            explained_amount_estimate=result.explained_amount_estimate,
        ),
        summary_statement=result.summary_explanation,
        top_causes=top_causes,
        recommended_action=result.recommended_action,
        evidence_summary=ConceptAnalysisEvidenceSummary(
            total_exceptions=len(exceptions),
            top_exception_types=top_exception_types,
            records_with_exception=records_with_exception,
            employees_with_exception=employees_with_exception,
        ),
    )


def _build_ranked_top_causes(
    exceptions: list[RunExceptionRecord],
    limit: int = 3,
) -> list[RunExceptionRecord]:
    if not exceptions:
        return []

    aggregated_by_type: dict[str, dict[str, object]] = {}
    for exception in exceptions:
        exception_type = exception.exception_type
        impact_amount = exception.estimated_impact_amount or Decimal("0")
        confidence = exception.confidence or Decimal("0")
        current = aggregated_by_type.get(exception_type)
        if current is None:
            aggregated_by_type[exception_type] = {
                "representative": exception,
                "estimated_impact_amount": impact_amount,
                "confidence_total": confidence,
                "confidence_count": 1 if exception.confidence is not None else 0,
            }
            continue

        current["estimated_impact_amount"] = (
            current["estimated_impact_amount"] + impact_amount
        )
        if exception.confidence is not None:
            current["confidence_total"] = current["confidence_total"] + confidence
            current["confidence_count"] = current["confidence_count"] + 1

        representative = current["representative"]
        representative_impact = representative.estimated_impact_amount or Decimal("0")
        representative_confidence = representative.confidence or Decimal("0")
        if (
            impact_amount > representative_impact
            or (
                impact_amount == representative_impact
                and confidence > representative_confidence
            )
        ):
            current["representative"] = exception

    ranked_groups = sorted(
        aggregated_by_type.values(),
        key=lambda item: (
            item["estimated_impact_amount"],
            (
                item["confidence_total"] / item["confidence_count"]
                if item["confidence_count"]
                else Decimal("0")
            ),
        ),
        reverse=True,
    )[:limit]

    ranked_top_causes: list[RunExceptionRecord] = []
    for group in ranked_groups:
        representative = group["representative"]
        confidence_count = group["confidence_count"]
        average_confidence = (
            group["confidence_total"] / confidence_count
            if confidence_count
            else representative.confidence
        )
        ranked_top_causes.append(
            representative.model_copy(
                update={
                    "estimated_impact_amount": group["estimated_impact_amount"],
                    "confidence": average_confidence,
                }
            )
        )

    return ranked_top_causes


def _build_drilldown_summary(
    result: RunResultRecord,
    rows: list[RunPayrollLineRecord],
) -> DrilldownSummary:
    total_amount = (
        sum(
            ((row.amount or Decimal("0")) for row in rows),
            start=Decimal("0"),
        )
        if rows
        else None
    )
    exception_types_present = _unique_preserving_order(
        [
            exception_type
            for row in rows
            for exception_type in row.exception_flags
        ]
    )
    rows_with_exception = sum(1 for row in rows if row.exception_flags)

    return DrilldownSummary(
        concept_code_normalized=result.concept_code_normalized,
        total_rows=len(rows),
        total_amount=total_amount,
        rows_with_exception=rows_with_exception,
        exception_types_present=exception_types_present,
    )


def _build_drilldown_filter_context(
    rows: list[RunPayrollLineRecord],
) -> DrilldownFilterContext:
    return DrilldownFilterContext(
        available_exception_types=_unique_preserving_order(
            [
                exception_type
                for row in rows
                for exception_type in row.exception_flags
            ]
        ),
        legal_entities=_unique_preserving_order(
            [row.legal_entity for row in rows if row.legal_entity]
        ),
        countries=_unique_preserving_order([row.country for row in rows if row.country]),
    )


def _build_run_event_log(
    run: RunRecord,
    uploaded_files: list[UploadedFileRecord],
    results: list[RunResultRecord],
) -> list[RunEventRecord]:
    events: list[RunEventRecord] = [
        RunEventRecord(
            event_code="run_created",
            title="Run created",
            detail=(
                f"Run {run.run_label} was created for period {run.period}."
            ),
            event_at=run.created_at,
            status_snapshot="DRAFT",
        )
    ]

    for uploaded_file in sorted(uploaded_files, key=lambda item: item.uploaded_at):
        events.append(
            RunEventRecord(
                event_code="file_uploaded",
                title="File associated",
                detail=(
                    f"{uploaded_file.file_type} file {uploaded_file.file_name} was "
                    f"registered via {uploaded_file.source_kind}."
                ),
                event_at=uploaded_file.uploaded_at,
                status_snapshot="INPUT_VALIDATED",
            )
        )

    processing_related_statuses = {
        "PROCESSING",
        "RECONCILED",
        "RECONCILED_WITH_EXCEPTIONS",
        "FAILED",
        "INVALID_INPUT",
    }
    if run.status in processing_related_statuses:
        events.append(
            RunEventRecord(
                event_code="processing_started",
                title="Processing started",
                detail="The run entered processing after the required inputs were available.",
                event_at=run.created_at if run.completed_at is None else run.created_at,
                status_snapshot="PROCESSING",
            )
        )

    if results:
        events.append(
            RunEventRecord(
                event_code="results_persisted",
                title="Results persisted",
                detail=(
                    f"The run persisted {len(results)} concept-level results for "
                    f"period {run.period}."
                ),
                event_at=run.completed_at,
                status_snapshot=run.status,
            )
        )

    if run.status in {"RECONCILED", "RECONCILED_WITH_EXCEPTIONS"}:
        events.append(
            RunEventRecord(
                event_code="run_completed",
                title="Run completed",
                detail=(
                    f"The run finished with business status "
                    f"{run.overall_status or 'unknown'}."
                ),
                event_at=run.completed_at,
                status_snapshot=run.status,
            )
        )
    elif run.status == "INVALID_INPUT":
        events.append(
            RunEventRecord(
                event_code="run_invalid_input",
                title="Run invalidated",
                detail=run.error_message or "The run stopped because the inputs were invalid.",
                event_at=run.completed_at,
                status_snapshot=run.status,
            )
        )
    elif run.status == "FAILED":
        events.append(
            RunEventRecord(
                event_code="run_failed",
                title="Run failed",
                detail=run.error_message or "The run failed because of a technical error.",
                event_at=run.completed_at,
                status_snapshot=run.status,
            )
        )

    return events


def _unique_preserving_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def _optional_string(value: object) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = str(value)
    return text if text else None


def _optional_decimal(value: object) -> Decimal | None:
    if value is None or pd.isna(value):
        return None
    return Decimal(str(value))


def _serialize_row_exception_types(row: RunPayrollLineRecord) -> str:
    anomaly_labels = row.invalid_reasons or row.exception_flags
    return " | ".join(anomaly_labels) if anomaly_labels else "Clear"


def _build_row_observation(row: RunPayrollLineRecord) -> str:
    if row.invalid_reasons:
        return " | ".join(row.invalid_reasons)
    if row.exception_flags:
        count = len(row.exception_flags)
        suffix = "s" if count > 1 else ""
        return f"Detected {count} exception flag{suffix}."
    return "No anomaly persisted for this row."


def _slugify_filename(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "run"
