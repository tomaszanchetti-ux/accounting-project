from __future__ import annotations

import json
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from app.core.db import get_db_connection
from app.schemas.runs import (
    ExpectedTotalUsedRecord,
    RunExceptionRecord,
    RunPayrollLineRecord,
    RunRecord,
    RunResultRecord,
    UploadedFileRecord,
)


class RunsRepositoryProtocol(Protocol):
    def create_run(
        self,
        *,
        run_label: str,
        period: str,
        legal_entity_scope: str | None = None,
        tolerance_profile_label: str | None = None,
        rules_version: str | None = None,
    ) -> RunRecord: ...

    def get_run(self, run_id: str) -> RunRecord | None: ...

    def update_run_status(
        self,
        run_id: str,
        *,
        status: str,
        overall_status: str | None = None,
        completed_at: datetime | None = None,
        error_message: str | None = None,
    ) -> RunRecord | None: ...

    def upsert_uploaded_file(
        self,
        *,
        run_id: str,
        file_name: str,
        file_type: str,
        source_kind: str,
        storage_path: str,
        storage_bucket: str | None = None,
    ) -> UploadedFileRecord: ...

    def list_uploaded_files(self, run_id: str) -> list[UploadedFileRecord]: ...

    def persist_run_execution(
        self,
        *,
        run_id: str,
        expected_totals_used: list[ExpectedTotalUsedRecord],
        results: list[RunResultRecord],
        exceptions: list[RunExceptionRecord],
        payroll_lines: list[RunPayrollLineRecord],
        final_status: str,
        overall_status: str,
        source_file_name: str | None,
        record_count: int,
        concept_count: int,
        run_metrics: dict[str, str | int | float | bool | None],
        completed_at: datetime,
    ) -> RunRecord: ...

    def list_results(self, run_id: str) -> list[RunResultRecord]: ...

    def get_result(self, run_id: str, result_id: str) -> RunResultRecord | None: ...

    def list_exceptions(
        self,
        run_id: str,
        *,
        result_id: str | None = None,
    ) -> list[RunExceptionRecord]: ...

    def list_payroll_lines(
        self,
        run_id: str,
        *,
        concept_code_normalized: str | None = None,
    ) -> list[RunPayrollLineRecord]: ...


class PsycopgRunsRepository:
    _schema_initialized = False

    def ensure_schema(self) -> None:
        if PsycopgRunsRepository._schema_initialized:
            return

        schema_path = Path(__file__).resolve().parents[1] / "models" / "runs_schema.sql"
        sql_script = schema_path.read_text(encoding="utf-8")
        statements = [statement.strip() for statement in sql_script.split(";") if statement.strip()]

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                for statement in statements:
                    cursor.execute(statement)
            connection.commit()

        PsycopgRunsRepository._schema_initialized = True

    def create_run(
        self,
        *,
        run_label: str,
        period: str,
        legal_entity_scope: str | None = None,
        tolerance_profile_label: str | None = None,
        rules_version: str | None = None,
    ) -> RunRecord:
        self.ensure_schema()
        created_at = datetime.now(timezone.utc)
        run_id = str(uuid4())

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO reconciliation_runs (
                        id,
                        run_label,
                        period,
                        status,
                        legal_entity_scope,
                        tolerance_profile_label,
                        rules_version,
                        created_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING *
                    """,
                    (
                        run_id,
                        run_label,
                        period,
                        "DRAFT",
                        legal_entity_scope,
                        tolerance_profile_label,
                        rules_version,
                        created_at,
                    ),
                )
                row = cursor.fetchone()
            connection.commit()

        return _parse_run_row(row)

    def get_run(self, run_id: str) -> RunRecord | None:
        self.ensure_schema()
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM reconciliation_runs WHERE id = %s",
                    (run_id,),
                )
                row = cursor.fetchone()

        return _parse_run_row(row) if row else None

    def update_run_status(
        self,
        run_id: str,
        *,
        status: str,
        overall_status: str | None = None,
        completed_at: datetime | None = None,
        error_message: str | None = None,
    ) -> RunRecord | None:
        self.ensure_schema()
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE reconciliation_runs
                    SET
                        status = %s,
                        overall_status = COALESCE(%s, overall_status),
                        completed_at = COALESCE(%s, completed_at),
                        error_message = %s
                    WHERE id = %s
                    RETURNING *
                    """,
                    (
                        status,
                        overall_status,
                        completed_at,
                        error_message,
                        run_id,
                    ),
                )
                row = cursor.fetchone()
            connection.commit()

        return _parse_run_row(row) if row else None

    def upsert_uploaded_file(
        self,
        *,
        run_id: str,
        file_name: str,
        file_type: str,
        source_kind: str,
        storage_path: str,
        storage_bucket: str | None = None,
    ) -> UploadedFileRecord:
        self.ensure_schema()
        uploaded_at = datetime.now(timezone.utc)
        file_id = str(uuid4())

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO uploaded_files (
                        id,
                        run_id,
                        file_name,
                        file_type,
                        source_kind,
                        storage_bucket,
                        storage_path,
                        uploaded_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (run_id, file_type)
                    DO UPDATE SET
                        id = EXCLUDED.id,
                        file_name = EXCLUDED.file_name,
                        source_kind = EXCLUDED.source_kind,
                        storage_bucket = EXCLUDED.storage_bucket,
                        storage_path = EXCLUDED.storage_path,
                        uploaded_at = EXCLUDED.uploaded_at
                    RETURNING *
                    """,
                    (
                        file_id,
                        run_id,
                        file_name,
                        file_type,
                        source_kind,
                        storage_bucket,
                        storage_path,
                        uploaded_at,
                    ),
                )
                row = cursor.fetchone()
            connection.commit()

        return _parse_uploaded_file_row(row)

    def list_uploaded_files(self, run_id: str) -> list[UploadedFileRecord]:
        self.ensure_schema()
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM uploaded_files
                    WHERE run_id = %s
                    ORDER BY uploaded_at ASC
                    """,
                    (run_id,),
                )
                rows = cursor.fetchall()

        return [_parse_uploaded_file_row(row) for row in rows]

    def persist_run_execution(
        self,
        *,
        run_id: str,
        expected_totals_used: list[ExpectedTotalUsedRecord],
        results: list[RunResultRecord],
        exceptions: list[RunExceptionRecord],
        payroll_lines: list[RunPayrollLineRecord],
        final_status: str,
        overall_status: str,
        source_file_name: str | None,
        record_count: int,
        concept_count: int,
        run_metrics: dict[str, str | int | float | bool | None],
        completed_at: datetime,
    ) -> RunRecord:
        self.ensure_schema()

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM expected_totals_used WHERE run_id = %s",
                    (run_id,),
                )
                cursor.execute(
                    "DELETE FROM reconciliation_exceptions WHERE run_id = %s",
                    (run_id,),
                )
                cursor.execute(
                    "DELETE FROM reconciliation_results WHERE run_id = %s",
                    (run_id,),
                )
                cursor.execute(
                    "DELETE FROM run_payroll_lines WHERE run_id = %s",
                    (run_id,),
                )

                if expected_totals_used:
                    cursor.executemany(
                        """
                        INSERT INTO expected_totals_used (
                            id,
                            run_id,
                            period,
                            concept_code_normalized,
                            expected_amount,
                            currency,
                            legal_entity
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        [
                            (
                                item.id,
                                item.run_id,
                                item.period,
                                item.concept_code_normalized,
                                item.expected_amount,
                                item.currency,
                                item.legal_entity,
                            )
                            for item in expected_totals_used
                        ],
                    )

                if results:
                    cursor.executemany(
                        """
                        INSERT INTO reconciliation_results (
                            id,
                            run_id,
                            period,
                            concept_code_normalized,
                            concept_name_normalized,
                            observed_amount,
                            expected_amount,
                            absolute_diff,
                            relative_diff_pct,
                            status,
                            record_count,
                            employee_count,
                            invalid_record_count,
                            legal_entity,
                            summary_explanation,
                            recommended_action,
                            explained_amount_estimate,
                            impacted_records_count,
                            impacted_employees_count
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s
                        )
                        """,
                        [
                            (
                                item.id,
                                item.run_id,
                                item.period,
                                item.concept_code_normalized,
                                item.concept_name_normalized,
                                item.observed_amount,
                                item.expected_amount,
                                item.absolute_diff,
                                item.relative_diff_pct,
                                item.status,
                                item.record_count,
                                item.employee_count,
                                item.invalid_record_count,
                                item.legal_entity,
                                item.summary_explanation,
                                item.recommended_action,
                                item.explained_amount_estimate,
                                item.impacted_records_count,
                                item.impacted_employees_count,
                            )
                            for item in results
                        ],
                    )

                if exceptions:
                    cursor.executemany(
                        """
                        INSERT INTO reconciliation_exceptions (
                            id,
                            run_id,
                            result_id,
                            record_id,
                            employee_id,
                            concept_scope,
                            exception_type,
                            severity,
                            scope_level,
                            estimated_impact_amount,
                            observation,
                            confidence,
                            created_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        [
                            (
                                item.id,
                                item.run_id,
                                item.result_id,
                                item.record_id,
                                item.employee_id,
                                item.concept_scope,
                                item.exception_type,
                                item.severity,
                                item.scope_level,
                                item.estimated_impact_amount,
                                item.observation,
                                item.confidence,
                                item.created_at,
                            )
                            for item in exceptions
                        ],
                    )

                if payroll_lines:
                    cursor.executemany(
                        """
                        INSERT INTO run_payroll_lines (
                            id,
                            run_id,
                            record_id,
                            employee_id,
                            employee_name,
                            legal_entity,
                            country,
                            cost_center,
                            payroll_period,
                            posting_date,
                            concept_code_raw,
                            concept_code_normalized,
                            concept_name_raw,
                            concept_name_normalized,
                            amount,
                            currency,
                            is_valid,
                            exception_flags,
                            invalid_reasons
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s::jsonb, %s::jsonb
                        )
                        """,
                        [
                            (
                                item.id,
                                item.run_id,
                                item.record_id,
                                item.employee_id,
                                item.employee_name,
                                item.legal_entity,
                                item.country,
                                item.cost_center,
                                item.payroll_period,
                                item.posting_date,
                                item.concept_code_raw,
                                item.concept_code_normalized,
                                item.concept_name_raw,
                                item.concept_name_normalized,
                                item.amount,
                                item.currency,
                                item.is_valid,
                                json.dumps(item.exception_flags),
                                json.dumps(item.invalid_reasons),
                            )
                            for item in payroll_lines
                        ],
                    )

                cursor.execute(
                    """
                    UPDATE reconciliation_runs
                    SET
                        status = %s,
                        overall_status = %s,
                        source_file_name = %s,
                        record_count = %s,
                        concept_count = %s,
                        run_metrics = %s::jsonb,
                        completed_at = %s,
                        error_message = NULL
                    WHERE id = %s
                    RETURNING *
                    """,
                    (
                        final_status,
                        overall_status,
                        source_file_name,
                        record_count,
                        concept_count,
                        json.dumps(run_metrics),
                        completed_at,
                        run_id,
                    ),
                )
                row = cursor.fetchone()
            connection.commit()

        return _parse_run_row(row)

    def list_results(self, run_id: str) -> list[RunResultRecord]:
        self.ensure_schema()
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM reconciliation_results
                    WHERE run_id = %s
                    ORDER BY
                        CASE status
                            WHEN 'Invalid / Incomplete' THEN 1
                            WHEN 'Unreconciled' THEN 2
                            WHEN 'Minor Difference' THEN 3
                            ELSE 4
                        END,
                        ABS(absolute_diff) DESC,
                        concept_code_normalized ASC
                    """,
                    (run_id,),
                )
                rows = cursor.fetchall()

        return [_parse_result_row(row) for row in rows]

    def get_result(self, run_id: str, result_id: str) -> RunResultRecord | None:
        self.ensure_schema()
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM reconciliation_results
                    WHERE run_id = %s AND id = %s
                    """,
                    (run_id, result_id),
                )
                row = cursor.fetchone()

        return _parse_result_row(row) if row else None

    def list_exceptions(
        self,
        run_id: str,
        *,
        result_id: str | None = None,
    ) -> list[RunExceptionRecord]:
        self.ensure_schema()
        sql = """
            SELECT *
            FROM reconciliation_exceptions
            WHERE run_id = %s
        """
        params: list[object] = [run_id]
        if result_id:
            sql += " AND result_id = %s"
            params.append(result_id)
        sql += """
            ORDER BY
                COALESCE(estimated_impact_amount, 0) DESC,
                exception_type ASC
        """

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(params))
                rows = cursor.fetchall()

        return [_parse_exception_row(row) for row in rows]

    def list_payroll_lines(
        self,
        run_id: str,
        *,
        concept_code_normalized: str | None = None,
    ) -> list[RunPayrollLineRecord]:
        self.ensure_schema()
        sql = """
            SELECT *
            FROM run_payroll_lines
            WHERE run_id = %s
        """
        params: list[object] = [run_id]
        if concept_code_normalized:
            sql += " AND concept_code_normalized = %s"
            params.append(concept_code_normalized)
        sql += " ORDER BY ABS(COALESCE(amount, 0)) DESC, record_id ASC"

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(params))
                rows = cursor.fetchall()

        return [_parse_payroll_line_row(row) for row in rows]


def _parse_run_row(row: dict[str, object]) -> RunRecord:
    return RunRecord(
        id=str(row["id"]),
        run_label=str(row["run_label"]),
        period=str(row["period"]),
        status=str(row["status"]),
        overall_status=_coerce_optional_string(row.get("overall_status")),
        source_file_name=_coerce_optional_string(row.get("source_file_name")),
        record_count=_coerce_optional_int(row.get("record_count")),
        concept_count=_coerce_optional_int(row.get("concept_count")),
        legal_entity_scope=_coerce_optional_string(row.get("legal_entity_scope")),
        tolerance_profile_label=_coerce_optional_string(
            row.get("tolerance_profile_label")
        ),
        rules_version=_coerce_optional_string(row.get("rules_version")),
        run_metrics=_coerce_json_dict(row.get("run_metrics")),
        error_message=_coerce_optional_string(row.get("error_message")),
        created_at=_coerce_datetime(row["created_at"]),
        completed_at=_coerce_optional_datetime(row.get("completed_at")),
    )


def _parse_uploaded_file_row(row: dict[str, object]) -> UploadedFileRecord:
    return UploadedFileRecord(
        id=str(row["id"]),
        run_id=str(row["run_id"]),
        file_name=str(row["file_name"]),
        file_type=str(row["file_type"]),
        source_kind=str(row["source_kind"]),
        storage_bucket=_coerce_optional_string(row.get("storage_bucket")),
        storage_path=str(row["storage_path"]),
        uploaded_at=_coerce_datetime(row["uploaded_at"]),
    )


def _parse_result_row(row: dict[str, object]) -> RunResultRecord:
    return RunResultRecord(
        id=str(row["id"]),
        run_id=str(row["run_id"]),
        period=str(row["period"]),
        concept_code_normalized=str(row["concept_code_normalized"]),
        concept_name_normalized=str(row["concept_name_normalized"]),
        observed_amount=_coerce_decimal(row["observed_amount"]),
        expected_amount=_coerce_decimal(row["expected_amount"]),
        absolute_diff=_coerce_decimal(row["absolute_diff"]),
        relative_diff_pct=_coerce_optional_decimal(row.get("relative_diff_pct")),
        status=str(row["status"]),
        record_count=int(row["record_count"]),
        employee_count=int(row["employee_count"]),
        invalid_record_count=int(row.get("invalid_record_count") or 0),
        legal_entity=_coerce_optional_string(row.get("legal_entity")),
        summary_explanation=_coerce_optional_string(row.get("summary_explanation")),
        recommended_action=_coerce_optional_string(row.get("recommended_action")),
        explained_amount_estimate=_coerce_optional_decimal(
            row.get("explained_amount_estimate")
        ),
        impacted_records_count=_coerce_optional_int(row.get("impacted_records_count")),
        impacted_employees_count=_coerce_optional_int(
            row.get("impacted_employees_count")
        ),
    )


def _parse_exception_row(row: dict[str, object]) -> RunExceptionRecord:
    return RunExceptionRecord(
        id=str(row["id"]),
        run_id=str(row["run_id"]),
        result_id=_coerce_optional_string(row.get("result_id")),
        record_id=_coerce_optional_string(row.get("record_id")),
        employee_id=_coerce_optional_string(row.get("employee_id")),
        concept_scope=_coerce_optional_string(row.get("concept_scope")),
        exception_type=str(row["exception_type"]),
        severity=str(row["severity"]),
        scope_level=str(row["scope_level"]),
        estimated_impact_amount=_coerce_optional_decimal(
            row.get("estimated_impact_amount")
        ),
        observation=_coerce_optional_string(row.get("observation")),
        confidence=_coerce_optional_decimal(row.get("confidence")),
        created_at=_coerce_datetime(row["created_at"]),
    )


def _parse_payroll_line_row(row: dict[str, object]) -> RunPayrollLineRecord:
    posting_date = row.get("posting_date")
    return RunPayrollLineRecord(
        id=str(row["id"]),
        run_id=str(row["run_id"]),
        record_id=str(row["record_id"]),
        employee_id=_coerce_optional_string(row.get("employee_id")),
        employee_name=_coerce_optional_string(row.get("employee_name")),
        legal_entity=_coerce_optional_string(row.get("legal_entity")),
        country=_coerce_optional_string(row.get("country")),
        cost_center=_coerce_optional_string(row.get("cost_center")),
        payroll_period=_coerce_optional_string(row.get("payroll_period")),
        posting_date=posting_date if isinstance(posting_date, date) else None,
        concept_code_raw=_coerce_optional_string(row.get("concept_code_raw")),
        concept_code_normalized=_coerce_optional_string(
            row.get("concept_code_normalized")
        ),
        concept_name_raw=_coerce_optional_string(row.get("concept_name_raw")),
        concept_name_normalized=_coerce_optional_string(
            row.get("concept_name_normalized")
        ),
        amount=_coerce_optional_decimal(row.get("amount")),
        currency=_coerce_optional_string(row.get("currency")),
        is_valid=bool(row["is_valid"]),
        exception_flags=_coerce_json_list(row.get("exception_flags")),
        invalid_reasons=_coerce_json_list(row.get("invalid_reasons")),
    )


def _coerce_decimal(value: object) -> Decimal:
    return Decimal(str(value))


def _coerce_optional_decimal(value: object) -> Decimal | None:
    if value is None:
        return None
    return Decimal(str(value))


def _coerce_optional_string(value: object) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _coerce_optional_int(value: object) -> int | None:
    if value is None:
        return None
    return int(value)


def _coerce_datetime(value: object) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value))


def _coerce_optional_datetime(value: object) -> datetime | None:
    if value is None:
        return None
    return _coerce_datetime(value)


def _coerce_json_dict(value: object) -> dict[str, str | int | float | bool | None]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    return json.loads(str(value))


def _coerce_json_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(item) for item in json.loads(str(value))]
