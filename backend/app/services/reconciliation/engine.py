from __future__ import annotations

from decimal import Decimal
from math import isnan

from app.schemas import (
    ReconciliationDebugArtifacts,
    ReconciliationEngineInput,
    ReconciliationEngineResult,
    ReconciliationSummaryRow,
)
from app.services.reconciliation.base import build_reconcilable_payroll_base
from app.services.reconciliation.comparison import assign_reconciliation_status


def build_run_summary_metrics(
    summary_rows: list[ReconciliationSummaryRow],
) -> dict[str, int | float | str]:
    reconciled = sum(1 for row in summary_rows if row.status == "Reconciled")
    minor = sum(1 for row in summary_rows if row.status == "Minor Difference")
    unreconciled = sum(1 for row in summary_rows if row.status == "Unreconciled")
    invalid = sum(1 for row in summary_rows if row.status == "Invalid / Incomplete")

    overall_status = "reconciled"
    if invalid > 0:
        overall_status = "invalid_incomplete"
    elif unreconciled > 0:
        overall_status = "unreconciled"
    elif minor > 0:
        overall_status = "minor_difference"

    return {
        "concepts_reconciled": reconciled,
        "concepts_minor_difference": minor,
        "concepts_unreconciled": unreconciled,
        "concepts_invalid_incomplete": invalid,
        "total_concepts": len(summary_rows),
        "overall_run_status": overall_status,
        "observed_amount_total": float(sum(row.observed_amount for row in summary_rows)),
        "expected_amount_total": float(sum(row.expected_amount for row in summary_rows)),
    }


def run_reconciliation_engine(
    engine_input: ReconciliationEngineInput,
) -> ReconciliationEngineResult:
    base_result = build_reconcilable_payroll_base(
        engine_input.payroll,
        engine_input.concept_master,
        target_period=engine_input.target_period,
    )
    comparison = assign_reconciliation_status(
        engine_input.payroll,
        engine_input.expected_totals,
        engine_input.concept_master,
        target_period=engine_input.target_period,
    ).comparison_with_diffs

    summary_rows: list[ReconciliationSummaryRow] = []
    for row in comparison.itertuples(index=False):
        relative_diff_pct = None
        if row.relative_diff_pct is not None and not isnan(row.relative_diff_pct):
            relative_diff_pct = Decimal(str(row.relative_diff_pct))

        summary_rows.append(
            ReconciliationSummaryRow(
                period=str(row.period),
                concept_code_normalized=str(row.concept_code_normalized),
                concept_name_normalized=str(row.concept_name_normalized),
                observed_amount=Decimal(str(row.observed_amount)),
                expected_amount=Decimal(str(row.expected_amount)),
                absolute_diff=Decimal(str(row.absolute_diff)),
                relative_diff_pct=relative_diff_pct,
                status=str(row.status),
                record_count=int(row.record_count),
                employee_count=int(row.employee_count),
                invalid_record_count=0,
            )
        )

    return ReconciliationEngineResult(
        summary_rows=summary_rows,
        run_metrics=build_run_summary_metrics(summary_rows),
        debug_artifacts=ReconciliationDebugArtifacts(
            normalized_payroll=base_result.reconciliable_base.copy(),
            observed_totals=comparison.copy(),
            expected_totals_filtered=None,
            validation_errors=[],
            validation_warnings=[],
        ),
    )
