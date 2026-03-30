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
from app.services.reconciliation.exceptions import (
    build_exception_impact_summary,
    build_ranked_exception_causes,
    build_structured_exception_items,
    detect_duplicate_records,
    detect_invalid_data_quality_issues,
    detect_misclassified_concepts,
    detect_missing_expected_totals,
    detect_missing_population,
    detect_out_of_period_records,
    detect_outlier_amounts,
    detect_sign_errors,
    detect_unmapped_concept_records,
)
from app.services.reconciliation.explanations import build_concept_explanations


def build_run_summary_metrics(
    summary_rows: list[ReconciliationSummaryRow],
    invalid_record_count: int = 0,
    blocking_data_quality_issue_count: int = 0,
    non_blocking_data_quality_issue_count: int = 0,
    run_has_blocking_data_quality_issues: bool = False,
    has_partial_invalidation_only: bool = False,
    out_of_period_record_count: int = 0,
    out_of_period_total_estimated_impact_amount: float = 0.0,
    unmapped_record_count: int = 0,
    unmapped_total_estimated_impact_amount: float = 0.0,
    duplicate_record_count: int = 0,
    duplicate_group_count: int = 0,
    duplicate_total_estimated_impact_amount: float = 0.0,
    missing_expected_total_count: int = 0,
    missing_expected_total_observed_amount: float = 0.0,
    outlier_record_count: int = 0,
    outlier_total_estimated_impact_amount: float = 0.0,
    missing_population_record_count: int = 0,
    missing_population_total_estimated_impact_amount: float = 0.0,
    sign_error_record_count: int = 0,
    misclassified_record_count: int = 0,
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
        "invalid_record_count": invalid_record_count,
        "blocking_data_quality_issue_count": blocking_data_quality_issue_count,
        "non_blocking_data_quality_issue_count": non_blocking_data_quality_issue_count,
        "run_has_blocking_data_quality_issues": run_has_blocking_data_quality_issues,
        "has_partial_invalidation_only": has_partial_invalidation_only,
        "out_of_period_record_count": out_of_period_record_count,
        "out_of_period_total_estimated_impact_amount": (
            out_of_period_total_estimated_impact_amount
        ),
        "unmapped_record_count": unmapped_record_count,
        "unmapped_total_estimated_impact_amount": unmapped_total_estimated_impact_amount,
        "duplicate_record_count": duplicate_record_count,
        "duplicate_group_count": duplicate_group_count,
        "duplicate_total_estimated_impact_amount": duplicate_total_estimated_impact_amount,
        "missing_expected_total_count": missing_expected_total_count,
        "missing_expected_total_observed_amount": missing_expected_total_observed_amount,
        "outlier_record_count": outlier_record_count,
        "outlier_total_estimated_impact_amount": outlier_total_estimated_impact_amount,
        "missing_population_record_count": missing_population_record_count,
        "missing_population_total_estimated_impact_amount": (
            missing_population_total_estimated_impact_amount
        ),
        "sign_error_record_count": sign_error_record_count,
        "misclassified_record_count": misclassified_record_count,
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
    invalid_detection = detect_invalid_data_quality_issues(
        engine_input.payroll,
        engine_input.concept_master,
        target_period=engine_input.target_period,
    )
    out_of_period_detection = detect_out_of_period_records(
        engine_input.payroll,
        engine_input.concept_master,
        target_period=engine_input.target_period,
    )
    unmapped_detection = detect_unmapped_concept_records(
        engine_input.payroll,
        engine_input.concept_master,
        target_period=engine_input.target_period,
    )
    duplicate_detection = detect_duplicate_records(
        engine_input.payroll,
        engine_input.concept_master,
        target_period=engine_input.target_period,
    )
    missing_expected_detection = detect_missing_expected_totals(
        engine_input.payroll,
        engine_input.expected_totals,
        engine_input.concept_master,
        target_period=engine_input.target_period,
    )
    outlier_detection = detect_outlier_amounts(
        engine_input.payroll,
        engine_input.concept_master,
        target_period=engine_input.target_period,
    )
    missing_population_detection = detect_missing_population(
        engine_input.payroll,
        engine_input.expected_totals,
        engine_input.concept_master,
        engine_input.employee_reference,
        target_period=engine_input.target_period,
    )
    sign_error_detection = detect_sign_errors(
        engine_input.payroll,
        engine_input.concept_master,
        target_period=engine_input.target_period,
    )
    misclassified_detection = detect_misclassified_concepts(
        engine_input.payroll,
        engine_input.concept_master,
        target_period=engine_input.target_period,
    )
    structured_exceptions = build_structured_exception_items(
        invalid_detection=invalid_detection,
        out_of_period_detection=out_of_period_detection,
        unmapped_detection=unmapped_detection,
        duplicate_detection=duplicate_detection,
        missing_expected_detection=missing_expected_detection,
        outlier_detection=outlier_detection,
        missing_population_detection=missing_population_detection,
        sign_error_detection=sign_error_detection,
        misclassified_detection=misclassified_detection,
    )
    exception_impact_summary = build_exception_impact_summary(structured_exceptions)
    ranked_exception_causes = build_ranked_exception_causes(structured_exceptions)

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

    concept_explanations = build_concept_explanations(
        summary_rows,
        ranked_exception_causes,
        structured_exceptions,
    )

    return ReconciliationEngineResult(
        summary_rows=summary_rows,
        run_metrics=build_run_summary_metrics(
            summary_rows,
            invalid_record_count=invalid_detection.invalid_record_count,
            blocking_data_quality_issue_count=invalid_detection.blocking_issue_count,
            non_blocking_data_quality_issue_count=invalid_detection.non_blocking_issue_count,
            run_has_blocking_data_quality_issues=(
                invalid_detection.run_has_blocking_data_quality_issues
            ),
            has_partial_invalidation_only=invalid_detection.has_partial_invalidation_only,
            out_of_period_record_count=out_of_period_detection.out_of_period_record_count,
            out_of_period_total_estimated_impact_amount=(
                out_of_period_detection.total_estimated_impact_amount
            ),
            unmapped_record_count=unmapped_detection.unmapped_record_count,
            unmapped_total_estimated_impact_amount=(
                unmapped_detection.total_estimated_impact_amount
            ),
            duplicate_record_count=duplicate_detection.duplicate_record_count,
            duplicate_group_count=duplicate_detection.duplicate_group_count,
            duplicate_total_estimated_impact_amount=(
                duplicate_detection.total_estimated_duplicate_impact_amount
            ),
            missing_expected_total_count=(
                missing_expected_detection.missing_expected_count
            ),
            missing_expected_total_observed_amount=(
                missing_expected_detection.total_observed_amount_without_expected
            ),
            outlier_record_count=outlier_detection.outlier_record_count,
            outlier_total_estimated_impact_amount=(
                outlier_detection.total_estimated_outlier_impact_amount
            ),
            missing_population_record_count=(
                missing_population_detection.missing_population_record_count
            ),
            missing_population_total_estimated_impact_amount=(
                missing_population_detection.total_estimated_missing_population_impact_amount
            ),
            sign_error_record_count=sign_error_detection.sign_error_record_count,
            misclassified_record_count=(
                misclassified_detection.misclassified_record_count
            ),
        ),
        debug_artifacts=ReconciliationDebugArtifacts(
            normalized_payroll=base_result.reconciliable_base.copy(),
            observed_totals=comparison.copy(),
            expected_totals_filtered=None,
            invalid_data_quality_exceptions=invalid_detection.invalid_exceptions.copy(),
            out_of_period_exceptions=out_of_period_detection.out_of_period_exceptions.copy(),
            out_of_period_impact_by_concept=out_of_period_detection.impact_by_concept.copy(),
            unmapped_concept_exceptions=unmapped_detection.unmapped_exceptions.copy(),
            unmapped_concept_impact_by_raw_concept=(
                unmapped_detection.impact_by_raw_concept.copy()
            ),
            duplicate_record_exceptions=duplicate_detection.duplicate_exceptions.copy(),
            duplicate_record_impact_by_concept=(
                duplicate_detection.impact_by_concept.copy()
            ),
            missing_expected_total_exceptions=(
                missing_expected_detection.missing_expected_exceptions.copy()
            ),
            outlier_amount_exceptions=outlier_detection.outlier_exceptions.copy(),
            outlier_amount_impact_by_concept=(
                outlier_detection.impact_by_concept.copy()
            ),
            missing_population_exceptions=(
                missing_population_detection.missing_population_exceptions.copy()
            ),
            sign_error_exceptions=sign_error_detection.sign_error_exceptions.copy(),
            misclassified_concept_exceptions=(
                misclassified_detection.misclassified_exceptions.copy()
            ),
            structured_exceptions=structured_exceptions,
            exception_impact_summary=exception_impact_summary.copy(),
            ranked_exception_causes=ranked_exception_causes.copy(),
            concept_explanations=concept_explanations,
            validation_errors=[],
            validation_warnings=[],
        ),
    )
