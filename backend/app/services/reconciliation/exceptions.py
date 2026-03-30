from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pandas as pd

from app.schemas import (
    DuplicateRecordDetectionResult,
    InvalidDataQualityDetectionResult,
    MisclassifiedConceptDetectionResult,
    MissingExpectedTotalDetectionResult,
    MissingPopulationDetectionResult,
    OutlierAmountDetectionResult,
    OutOfPeriodDetectionResult,
    ReconciliationExceptionItem,
    SignErrorDetectionResult,
    UnmappedConceptDetectionResult,
)
from app.schemas.reconciliation import DataFrameLike
from app.services.reconciliation.aggregate import build_observed_totals
from app.services.reconciliation.base import build_reconcilable_payroll_base
from app.services.reconciliation.concepts import _normalize_text_key
from app.services.reconciliation.validation import validate_expected_totals

INVALID_REASON_METADATA: dict[str, dict[str, str | bool]] = {
    "invalid_amount": {
        "blocking": True,
        "observation": "Amount is missing or non-interpretable for reconciliation.",
        "severity": "critical",
    },
    "invalid_posting_date": {
        "blocking": True,
        "observation": "Posting date is missing or invalid, so temporal validation is unreliable.",
        "severity": "critical",
    },
    "missing_or_invalid_payroll_period": {
        "blocking": True,
        "observation": (
            "Payroll period is missing or invalid and the record cannot be "
            "placed in scope safely."
        ),
        "severity": "critical",
    },
    "missing_concept": {
        "blocking": True,
        "observation": (
            "Concept information is missing, so the record cannot be "
            "classified or reconciled."
        ),
        "severity": "critical",
    },
    "missing_employee_id": {
        "blocking": False,
        "observation": (
            "Employee ID is missing, which breaks traceability even if the "
            "amount is otherwise interpretable."
        ),
        "severity": "medium",
    },
}

EXCEPTION_PRIORITY_ORDER = [
    "Invalid Amount / Data Quality Issue",
    "Out-of-Period Record",
    "Unmapped Concept",
    "Duplicate Record",
    "Missing Expected Total",
    "Missing Record / Missing Population",
    "Sign Error",
    "Outlier Amount",
    "Misclassified Concept",
]

EXCEPTION_SEVERITY_DEFAULTS = {
    "Invalid Amount / Data Quality Issue": "critical",
    "Out-of-Period Record": "high",
    "Unmapped Concept": "high",
    "Duplicate Record": "high",
    "Missing Expected Total": "high",
    "Missing Record / Missing Population": "high",
    "Sign Error": "medium",
    "Outlier Amount": "medium",
    "Misclassified Concept": "low",
}


def _load_dataframe(source: DataFrameLike | pd.DataFrame) -> pd.DataFrame:
    if isinstance(source, pd.DataFrame):
        return source.copy()

    return pd.read_csv(Path(source))


def detect_invalid_data_quality_issues(
    payroll_source: DataFrameLike | pd.DataFrame,
    concept_master_source: DataFrameLike,
    target_period: str,
) -> InvalidDataQualityDetectionResult:
    reconciliable_base = build_reconcilable_payroll_base(
        payroll_source,
        concept_master_source,
        target_period=target_period,
    ).reconciliable_base.copy()
    invalid_records = reconciliable_base.loc[~reconciliable_base["is_valid_record"]].copy()

    rows: list[dict[str, object]] = []
    for record in invalid_records.itertuples(index=False):
        record_invalid_reasons = list(record.invalid_reasons)
        for issue_code in record_invalid_reasons:
            metadata = INVALID_REASON_METADATA.get(
                issue_code,
                {
                    "blocking": True,
                    "observation": "Unexpected data quality issue detected.",
                    "severity": "critical",
                },
            )
            rows.append(
                {
                    "exception_type": "Invalid Amount / Data Quality Issue",
                    "record_id": getattr(record, "record_id", None),
                    "employee_id": getattr(record, "employee_id", None),
                    "concept_code": getattr(record, "concept_code", None),
                    "concept_code_normalized": getattr(
                        record,
                        "concept_code_normalized",
                        None,
                    ),
                    "payroll_period_normalized": getattr(
                        record,
                        "payroll_period_normalized",
                        None,
                    ),
                    "issue_code": issue_code,
                    "severity": metadata["severity"],
                    "blocking": bool(metadata["blocking"]),
                    "observation": metadata["observation"],
                }
            )

    exceptions = pd.DataFrame(rows)
    if exceptions.empty:
        exceptions = pd.DataFrame(
            columns=[
                "exception_type",
                "record_id",
                "employee_id",
                "concept_code",
                "concept_code_normalized",
                "payroll_period_normalized",
                "issue_code",
                "severity",
                "blocking",
                "observation",
            ]
        )

    blocking_issue_count = (
        int(exceptions["blocking"].sum()) if not exceptions.empty else 0
    )
    non_blocking_issue_count = (
        int((~exceptions["blocking"]).sum()) if not exceptions.empty else 0
    )

    return InvalidDataQualityDetectionResult(
        invalid_exceptions=exceptions,
        invalid_record_count=len(invalid_records),
        blocking_issue_count=blocking_issue_count,
        non_blocking_issue_count=non_blocking_issue_count,
        run_has_blocking_data_quality_issues=blocking_issue_count > 0,
        has_partial_invalidation_only=blocking_issue_count == 0 and len(invalid_records) > 0,
    )


def detect_out_of_period_records(
    payroll_source: DataFrameLike | pd.DataFrame,
    concept_master_source: DataFrameLike,
    target_period: str,
) -> OutOfPeriodDetectionResult:
    reconciliable_base = build_reconcilable_payroll_base(
        payroll_source,
        concept_master_source,
        target_period=target_period,
    ).reconciliable_base.copy()
    posting_period = reconciliable_base["posting_period"].astype("string")
    posting_period_out_of_scope = posting_period.notna() & posting_period.ne(target_period)
    out_of_period_mask = reconciliable_base["is_out_of_period"] | posting_period_out_of_scope
    out_of_period_records = reconciliable_base.loc[out_of_period_mask].copy()

    if out_of_period_records.empty:
        empty_exceptions = pd.DataFrame(
            columns=[
                "exception_type",
                "record_id",
                "employee_id",
                "concept_code_normalized",
                "payroll_period_normalized",
                "posting_period",
                "temporal_mismatch_source",
                "estimated_impact_amount",
                "observation",
            ]
        )
        empty_impact = pd.DataFrame(
            columns=[
                "concept_code_normalized",
                "out_of_period_record_count",
                "estimated_impact_amount",
            ]
        )
        return OutOfPeriodDetectionResult(
            out_of_period_exceptions=empty_exceptions,
            impact_by_concept=empty_impact,
            out_of_period_record_count=0,
            total_estimated_impact_amount=0.0,
        )

    temporal_mismatch_source = pd.Series("payroll_period", index=out_of_period_records.index)
    posting_only_mask = ~out_of_period_records["is_out_of_period"] & (
        out_of_period_records["posting_period"].astype("string").ne(target_period)
    )
    both_sources_mask = out_of_period_records["is_out_of_period"] & (
        out_of_period_records["posting_period"].astype("string").ne(target_period)
    )
    temporal_mismatch_source.loc[posting_only_mask] = "posting_date"
    temporal_mismatch_source.loc[both_sources_mask] = "payroll_period_and_posting_date"

    out_of_period_records["exception_type"] = "Out-of-Period Record"
    out_of_period_records["temporal_mismatch_source"] = temporal_mismatch_source
    out_of_period_records["estimated_impact_amount"] = out_of_period_records[
        "amount_for_aggregation"
    ].astype(float)
    out_of_period_records["observation"] = (
        "Record falls outside the target period and is excluded from observed totals."
    )

    exceptions = out_of_period_records[
        [
            "exception_type",
            "record_id",
            "employee_id",
            "concept_code_normalized",
            "payroll_period_normalized",
            "posting_period",
            "temporal_mismatch_source",
            "estimated_impact_amount",
            "observation",
        ]
    ].copy()
    impact_by_concept = (
        out_of_period_records.groupby("concept_code_normalized", as_index=False)
        .agg(
            out_of_period_record_count=("record_id", "count"),
            estimated_impact_amount=("estimated_impact_amount", "sum"),
        )
        .sort_values(
            ["estimated_impact_amount", "concept_code_normalized"],
            ascending=[False, True],
            ignore_index=True,
        )
    )

    return OutOfPeriodDetectionResult(
        out_of_period_exceptions=exceptions,
        impact_by_concept=impact_by_concept,
        out_of_period_record_count=len(exceptions),
        total_estimated_impact_amount=float(exceptions["estimated_impact_amount"].sum()),
    )


def detect_unmapped_concept_records(
    payroll_source: DataFrameLike | pd.DataFrame,
    concept_master_source: DataFrameLike,
    target_period: str,
) -> UnmappedConceptDetectionResult:
    reconciliable_base = build_reconcilable_payroll_base(
        payroll_source,
        concept_master_source,
        target_period=target_period,
    ).reconciliable_base.copy()
    unmapped_records = reconciliable_base.loc[reconciliable_base["is_unmapped_concept"]].copy()
    concept_master = _load_dataframe(concept_master_source)

    if unmapped_records.empty:
        empty_exceptions = pd.DataFrame(
            columns=[
                "exception_type",
                "record_id",
                "employee_id",
                "concept_code",
                "concept_name",
                "inferred_concept_scope",
                "payroll_period_normalized",
                "estimated_impact_amount",
                "observation",
            ]
        )
        empty_impact = pd.DataFrame(
            columns=[
                "concept_code",
                "concept_name",
                "unmapped_record_count",
                "estimated_impact_amount",
            ]
        )
        return UnmappedConceptDetectionResult(
            unmapped_exceptions=empty_exceptions,
            impact_by_raw_concept=empty_impact,
            unmapped_record_count=0,
            total_estimated_impact_amount=0.0,
        )

    unmapped_records["exception_type"] = "Unmapped Concept"
    unmapped_records["inferred_concept_scope"] = _infer_unmapped_concept_scope(
        unmapped_records["concept_name"],
        concept_master,
    )
    unmapped_records["estimated_impact_amount"] = unmapped_records[
        "amount_for_aggregation"
    ].astype(float)
    unmapped_records["observation"] = (
        "Record could not be mapped to a normalized concept and is excluded from observed totals."
    )

    exceptions = unmapped_records[
        [
            "exception_type",
            "record_id",
            "employee_id",
            "concept_code",
            "concept_name",
            "inferred_concept_scope",
            "payroll_period_normalized",
            "estimated_impact_amount",
            "observation",
        ]
    ].copy()
    impact_by_raw_concept = (
        unmapped_records.groupby(["concept_code", "concept_name"], as_index=False)
        .agg(
            unmapped_record_count=("record_id", "count"),
            estimated_impact_amount=("estimated_impact_amount", "sum"),
        )
        .sort_values(
            ["estimated_impact_amount", "concept_code"],
            ascending=[False, True],
            ignore_index=True,
        )
    )

    return UnmappedConceptDetectionResult(
        unmapped_exceptions=exceptions,
        impact_by_raw_concept=impact_by_raw_concept,
        unmapped_record_count=len(exceptions),
        total_estimated_impact_amount=float(exceptions["estimated_impact_amount"].sum()),
    )


def detect_duplicate_records(
    payroll_source: DataFrameLike | pd.DataFrame,
    concept_master_source: DataFrameLike,
    target_period: str,
) -> DuplicateRecordDetectionResult:
    reconciliable_base = build_reconcilable_payroll_base(
        payroll_source,
        concept_master_source,
        target_period=target_period,
    ).reconciliable_base.copy()
    eligible = reconciliable_base.loc[
        reconciliable_base["is_valid_record"]
        & ~reconciliable_base["is_unmapped_concept"]
        & ~reconciliable_base["is_out_of_period"]
    ].copy()

    group_columns = [
        "employee_id",
        "payroll_period_normalized",
        "concept_code_normalized",
        "amount_for_aggregation",
        "legal_entity",
    ]
    duplicate_groups = (
        eligible.groupby(group_columns, dropna=False, as_index=False)
        .agg(
            duplicate_group_size=("record_id", "count"),
            duplicate_record_ids=("record_id", lambda values: list(values)),
        )
        .loc[lambda df: df["duplicate_group_size"] > 1]
        .copy()
    )

    if duplicate_groups.empty:
        empty_exceptions = pd.DataFrame(
            columns=[
                "exception_type",
                "record_id",
                "employee_id",
                "concept_code_normalized",
                "payroll_period_normalized",
                "duplicate_group_key",
                "duplicate_group_size",
                "estimated_group_impact_amount",
                "observation",
            ]
        )
        empty_impact = pd.DataFrame(
            columns=[
                "concept_code_normalized",
                "duplicate_group_count",
                "duplicate_record_count",
                "estimated_duplicate_impact_amount",
            ]
        )
        return DuplicateRecordDetectionResult(
            duplicate_exceptions=empty_exceptions,
            impact_by_concept=empty_impact,
            duplicate_record_count=0,
            duplicate_group_count=0,
            total_estimated_duplicate_impact_amount=0.0,
        )

    duplicate_groups["estimated_group_impact_amount"] = (
        duplicate_groups["amount_for_aggregation"].astype(float)
        * (duplicate_groups["duplicate_group_size"] - 1)
    )
    duplicate_groups["duplicate_group_key"] = (
        duplicate_groups["employee_id"].astype("string")
        + "::"
        + duplicate_groups["payroll_period_normalized"].astype("string")
        + "::"
        + duplicate_groups["concept_code_normalized"].astype("string")
        + "::"
        + duplicate_groups["amount_for_aggregation"].astype("string")
        + "::"
        + duplicate_groups["legal_entity"].astype("string")
    )

    exceptions = eligible.merge(
        duplicate_groups[
            group_columns
            + [
                "duplicate_group_size",
                "estimated_group_impact_amount",
                "duplicate_group_key",
            ]
        ],
        on=group_columns,
        how="inner",
    ).copy()
    exceptions["exception_type"] = "Duplicate Record"
    exceptions["observation"] = (
        "Record belongs to a probable duplicate group and may be overstating observed totals."
    )
    exceptions = exceptions[
        [
            "exception_type",
            "record_id",
            "employee_id",
            "concept_code_normalized",
            "payroll_period_normalized",
            "duplicate_group_key",
            "duplicate_group_size",
            "estimated_group_impact_amount",
            "observation",
        ]
    ].copy()

    impact_by_concept = (
        duplicate_groups.groupby("concept_code_normalized", as_index=False)
        .agg(
            duplicate_group_count=("duplicate_group_key", "count"),
            duplicate_record_count=(
                "duplicate_group_size",
                lambda values: int(sum(values)),
            ),
            estimated_duplicate_impact_amount=("estimated_group_impact_amount", "sum"),
        )
        .sort_values(
            ["estimated_duplicate_impact_amount", "concept_code_normalized"],
            ascending=[False, True],
            ignore_index=True,
        )
    )

    return DuplicateRecordDetectionResult(
        duplicate_exceptions=exceptions,
        impact_by_concept=impact_by_concept,
        duplicate_record_count=len(exceptions),
        duplicate_group_count=len(duplicate_groups),
        total_estimated_duplicate_impact_amount=float(
            duplicate_groups["estimated_group_impact_amount"].sum()
        ),
    )


def detect_missing_expected_totals(
    payroll_source: DataFrameLike | pd.DataFrame,
    expected_totals_source: DataFrameLike,
    concept_master_source: DataFrameLike,
    target_period: str,
) -> MissingExpectedTotalDetectionResult:
    observed = build_observed_totals(
        payroll_source,
        concept_master_source,
        target_period=target_period,
    ).observed_totals.copy()
    expected_validation = validate_expected_totals(
        expected_totals_source,
        target_period=target_period,
        observed_concepts=observed["concept_code_normalized"].tolist(),
    )
    expected = expected_validation.filtered_expected_totals.copy()
    expected["concept_code"] = expected["concept_code"].astype("string").str.strip()
    expected_concepts = set(expected["concept_code"].tolist())

    missing_expected = observed.loc[
        ~observed["concept_code_normalized"].astype("string").isin(expected_concepts)
    ].copy()

    if missing_expected.empty:
        empty = pd.DataFrame(
            columns=[
                "exception_type",
                "period",
                "concept_code_normalized",
                "concept_name_normalized",
                "observed_amount",
                "observation",
            ]
        )
        return MissingExpectedTotalDetectionResult(
            missing_expected_exceptions=empty,
            missing_expected_count=0,
            total_observed_amount_without_expected=0.0,
        )

    missing_expected["exception_type"] = "Missing Expected Total"
    missing_expected["observation"] = (
        "Observed amount exists but there is no matching expected total for "
        "this reconciliation unit."
    )
    exceptions = missing_expected[
        [
            "exception_type",
            "period",
            "concept_code_normalized",
            "concept_name_normalized",
            "observed_amount",
            "observation",
        ]
    ].copy()

    return MissingExpectedTotalDetectionResult(
        missing_expected_exceptions=exceptions,
        missing_expected_count=len(exceptions),
        total_observed_amount_without_expected=float(exceptions["observed_amount"].sum()),
    )


def detect_outlier_amounts(
    payroll_source: DataFrameLike | pd.DataFrame,
    concept_master_source: DataFrameLike,
    target_period: str,
    multiplier_threshold: float = 5.0,
) -> OutlierAmountDetectionResult:
    reconciliable_base = build_reconcilable_payroll_base(
        payroll_source,
        concept_master_source,
        target_period=target_period,
    ).reconciliable_base.copy()
    eligible = reconciliable_base.loc[
        reconciliable_base["is_valid_record"]
        & ~reconciliable_base["is_unmapped_concept"]
        & ~reconciliable_base["is_out_of_period"]
    ].copy()

    if eligible.empty:
        empty_exceptions = pd.DataFrame(
            columns=[
                "exception_type",
                "record_id",
                "employee_id",
                "concept_code_normalized",
                "amount_for_aggregation",
                "concept_median_amount",
                "outlier_ratio_vs_median",
                "estimated_impact_amount",
                "observation",
            ]
        )
        empty_impact = pd.DataFrame(
            columns=[
                "concept_code_normalized",
                "outlier_record_count",
                "estimated_impact_amount",
            ]
        )
        return OutlierAmountDetectionResult(
            outlier_exceptions=empty_exceptions,
            impact_by_concept=empty_impact,
            outlier_record_count=0,
            total_estimated_outlier_impact_amount=0.0,
        )

    eligible["concept_median_amount"] = eligible.groupby("concept_code_normalized")[
        "amount_for_aggregation"
    ].transform("median")
    eligible["outlier_ratio_vs_median"] = (
        eligible["amount_for_aggregation"].astype(float)
        / eligible["concept_median_amount"].replace(0, pd.NA).astype(float)
    )
    outliers = eligible.loc[
        eligible["concept_median_amount"].gt(0)
        & (
            eligible["amount_for_aggregation"].astype(float)
            > eligible["concept_median_amount"].astype(float) * multiplier_threshold
        )
    ].copy()

    if outliers.empty:
        return OutlierAmountDetectionResult(
            outlier_exceptions=pd.DataFrame(
                columns=[
                    "exception_type",
                    "record_id",
                    "employee_id",
                    "concept_code_normalized",
                    "amount_for_aggregation",
                    "concept_median_amount",
                    "outlier_ratio_vs_median",
                    "estimated_impact_amount",
                    "observation",
                ]
            ),
            impact_by_concept=pd.DataFrame(
                columns=[
                    "concept_code_normalized",
                    "outlier_record_count",
                    "estimated_impact_amount",
                ]
            ),
            outlier_record_count=0,
            total_estimated_outlier_impact_amount=0.0,
        )

    outliers["exception_type"] = "Outlier Amount"
    outliers["estimated_impact_amount"] = (
        outliers["amount_for_aggregation"].astype(float)
        - outliers["concept_median_amount"].astype(float)
    )
    outliers["observation"] = (
        "Record amount is materially above the concept median and looks like a dominant outlier."
    )
    exceptions = outliers[
        [
            "exception_type",
            "record_id",
            "employee_id",
            "concept_code_normalized",
            "amount_for_aggregation",
            "concept_median_amount",
            "outlier_ratio_vs_median",
            "estimated_impact_amount",
            "observation",
        ]
    ].copy()
    impact_by_concept = (
        outliers.groupby("concept_code_normalized", as_index=False)
        .agg(
            outlier_record_count=("record_id", "count"),
            estimated_impact_amount=("estimated_impact_amount", "sum"),
        )
        .sort_values(
            ["estimated_impact_amount", "concept_code_normalized"],
            ascending=[False, True],
            ignore_index=True,
        )
    )

    return OutlierAmountDetectionResult(
        outlier_exceptions=exceptions,
        impact_by_concept=impact_by_concept,
        outlier_record_count=len(exceptions),
        total_estimated_outlier_impact_amount=float(
            exceptions["estimated_impact_amount"].sum()
        ),
    )


def detect_missing_population(
    payroll_source: DataFrameLike | pd.DataFrame,
    expected_totals_source: DataFrameLike,
    concept_master_source: DataFrameLike,
    employee_reference_source: DataFrameLike | pd.DataFrame | None,
    target_period: str,
) -> MissingPopulationDetectionResult:
    if employee_reference_source is None:
        return MissingPopulationDetectionResult(
            missing_population_exceptions=pd.DataFrame(
                columns=[
                    "exception_type",
                    "concept_code_normalized",
                    "missing_employee_id",
                    "estimated_impact_amount",
                    "observation",
                ]
            ),
            missing_population_record_count=0,
            total_estimated_missing_population_impact_amount=0.0,
        )

    employee_reference = _load_dataframe(employee_reference_source)
    employee_reference["employee_id"] = (
        employee_reference["employee_id"].astype("string").str.strip()
    )
    employee_reference["payroll_period"] = (
        employee_reference["payroll_period"].astype("string").str.strip()
    )

    childcare_reference = employee_reference.loc[
        employee_reference["payroll_period"].eq(target_period)
        & employee_reference["is_childcare_eligible"].fillna(False).astype(bool)
    ].copy()
    if childcare_reference.empty:
        return MissingPopulationDetectionResult(
            missing_population_exceptions=pd.DataFrame(
                columns=[
                    "exception_type",
                    "concept_code_normalized",
                    "missing_employee_id",
                    "estimated_impact_amount",
                    "observation",
                ]
            ),
            missing_population_record_count=0,
            total_estimated_missing_population_impact_amount=0.0,
        )

    reconciliable_base = build_reconcilable_payroll_base(
        payroll_source,
        concept_master_source,
        target_period=target_period,
    ).reconciliable_base.copy()
    childcare_observed = reconciliable_base.loc[
        reconciliable_base["is_valid_record"]
        & ~reconciliable_base["is_unmapped_concept"]
        & ~reconciliable_base["is_out_of_period"]
        & reconciliable_base["concept_code_normalized"].astype("string").eq("CHILDCARE")
    ].copy()
    observed_employee_ids = set(
        childcare_observed["employee_id"].astype("string").str.strip().tolist()
    )
    missing_reference = childcare_reference.loc[
        ~childcare_reference["employee_id"].isin(observed_employee_ids)
    ].copy()

    if missing_reference.empty:
        return MissingPopulationDetectionResult(
            missing_population_exceptions=pd.DataFrame(
                columns=[
                    "exception_type",
                    "concept_code_normalized",
                    "missing_employee_id",
                    "estimated_impact_amount",
                    "observation",
                ]
            ),
            missing_population_record_count=0,
            total_estimated_missing_population_impact_amount=0.0,
        )

    observed_total = float(childcare_observed["amount_for_aggregation"].sum())
    expected_validation = validate_expected_totals(
        expected_totals_source,
        target_period=target_period,
    )
    expected_rows = expected_validation.filtered_expected_totals.copy()
    childcare_expected_rows = expected_rows.loc[
        expected_rows["concept_code"].astype("string").str.strip().eq("CHILDCARE")
    ]
    expected_total = (
        float(childcare_expected_rows.iloc[0]["expected_amount"])
        if not childcare_expected_rows.empty
        else observed_total
    )
    absolute_diff = max(expected_total - observed_total, 0.0)
    expected_per_eligible = (
        expected_total / len(childcare_reference) if len(childcare_reference) > 0 else 0.0
    )
    raw_estimated_impact = expected_per_eligible * len(missing_reference)
    bounded_estimated_impact = min(raw_estimated_impact, absolute_diff)
    per_employee_impact = (
        bounded_estimated_impact / len(missing_reference)
        if len(missing_reference) > 0
        else 0.0
    )

    missing_reference["exception_type"] = "Missing Record / Missing Population"
    missing_reference["concept_code_normalized"] = "CHILDCARE"
    missing_reference["missing_employee_id"] = missing_reference["employee_id"]
    missing_reference["estimated_impact_amount"] = per_employee_impact
    missing_reference["observation"] = (
        "Eligible employee is missing from observed CHILDCARE records for the target period."
    )
    exceptions = missing_reference[
        [
            "exception_type",
            "concept_code_normalized",
            "missing_employee_id",
            "estimated_impact_amount",
            "observation",
        ]
    ].copy()

    return MissingPopulationDetectionResult(
        missing_population_exceptions=exceptions,
        missing_population_record_count=len(exceptions),
        total_estimated_missing_population_impact_amount=float(
            exceptions["estimated_impact_amount"].sum()
        ),
    )


def detect_sign_errors(
    payroll_source: DataFrameLike | pd.DataFrame,
    concept_master_source: DataFrameLike,
    target_period: str,
) -> SignErrorDetectionResult:
    reconciliable_base = build_reconcilable_payroll_base(
        payroll_source,
        concept_master_source,
        target_period=target_period,
    ).reconciliable_base.copy()
    sign_errors = reconciliable_base.loc[
        reconciliable_base["is_valid_record"]
        & ~reconciliable_base["is_unmapped_concept"]
        & ~reconciliable_base["is_out_of_period"]
        & reconciliable_base["has_unexpected_sign"]
    ].copy()

    if sign_errors.empty:
        return SignErrorDetectionResult(
            sign_error_exceptions=pd.DataFrame(
                columns=[
                    "exception_type",
                    "record_id",
                    "employee_id",
                    "concept_code_normalized",
                    "estimated_impact_amount",
                    "observation",
                ]
            ),
            sign_error_record_count=0,
            total_estimated_sign_error_impact_amount=0.0,
        )

    sign_errors["exception_type"] = "Sign Error"
    sign_errors["estimated_impact_amount"] = sign_errors["amount_absolute"].astype(float)
    sign_errors["observation"] = (
        "Observed sign differs from the expected sign configured for the concept."
    )
    exceptions = sign_errors[
        [
            "exception_type",
            "record_id",
            "employee_id",
            "concept_code_normalized",
            "estimated_impact_amount",
            "observation",
        ]
    ].copy()

    return SignErrorDetectionResult(
        sign_error_exceptions=exceptions,
        sign_error_record_count=len(exceptions),
        total_estimated_sign_error_impact_amount=float(
            exceptions["estimated_impact_amount"].sum()
        ),
    )


def detect_misclassified_concepts(
    payroll_source: DataFrameLike | pd.DataFrame,
    concept_master_source: DataFrameLike,
    target_period: str,
    configured_raw_concept_codes: set[str] | None = None,
) -> MisclassifiedConceptDetectionResult:
    configured = {code.strip().upper() for code in configured_raw_concept_codes or set()}
    if not configured:
        return MisclassifiedConceptDetectionResult(
            misclassified_exceptions=pd.DataFrame(
                columns=[
                    "exception_type",
                    "record_id",
                    "concept_code",
                    "suggested_concept_scope",
                    "observation",
                ]
            ),
            misclassified_record_count=0,
        )

    unmapped_detection = detect_unmapped_concept_records(
        payroll_source,
        concept_master_source,
        target_period=target_period,
    )
    candidates = unmapped_detection.unmapped_exceptions.copy()
    candidates["concept_code"] = (
        candidates["concept_code"].astype("string").str.strip().str.upper()
    )
    misclassified = candidates.loc[
        candidates["concept_code"].isin(configured)
        & candidates["inferred_concept_scope"].notna()
    ].copy()

    if misclassified.empty:
        return MisclassifiedConceptDetectionResult(
            misclassified_exceptions=pd.DataFrame(
                columns=[
                    "exception_type",
                    "record_id",
                    "concept_code",
                    "suggested_concept_scope",
                    "observation",
                ]
            ),
            misclassified_record_count=0,
        )

    misclassified["exception_type"] = "Misclassified Concept"
    misclassified["suggested_concept_scope"] = misclassified["inferred_concept_scope"]
    misclassified["observation"] = (
        "Pattern suggests the raw concept may belong to another configured concept scope."
    )
    exceptions = misclassified[
        [
            "exception_type",
            "record_id",
            "concept_code",
            "suggested_concept_scope",
            "observation",
        ]
    ].copy()

    return MisclassifiedConceptDetectionResult(
        misclassified_exceptions=exceptions,
        misclassified_record_count=len(exceptions),
    )


def build_structured_exception_items(
    *,
    invalid_detection: InvalidDataQualityDetectionResult,
    out_of_period_detection: OutOfPeriodDetectionResult,
    unmapped_detection: UnmappedConceptDetectionResult,
    duplicate_detection: DuplicateRecordDetectionResult,
    missing_expected_detection: MissingExpectedTotalDetectionResult,
    outlier_detection: OutlierAmountDetectionResult,
    missing_population_detection: MissingPopulationDetectionResult,
    sign_error_detection: SignErrorDetectionResult | None = None,
    misclassified_detection: MisclassifiedConceptDetectionResult | None = None,
) -> list[ReconciliationExceptionItem]:
    items: list[ReconciliationExceptionItem] = []

    for row in invalid_detection.invalid_exceptions.itertuples(index=False):
        items.append(
            ReconciliationExceptionItem(
                exception_type=row.exception_type,
                severity=str(row.severity),
                scope_level="record",
                record_id=_normalize_optional_string(row.record_id),
                concept_scope=_normalize_optional_string(row.concept_code_normalized),
                employee_id=_normalize_optional_string(row.employee_id),
                observation=str(row.observation),
                confidence=Decimal("1.0"),
            )
        )

    for row in out_of_period_detection.out_of_period_exceptions.itertuples(index=False):
        items.append(
            ReconciliationExceptionItem(
                exception_type=row.exception_type,
                severity=EXCEPTION_SEVERITY_DEFAULTS[row.exception_type],
                scope_level="record",
                record_id=_normalize_optional_string(row.record_id),
                concept_scope=_normalize_optional_string(row.concept_code_normalized),
                employee_id=_normalize_optional_string(row.employee_id),
                estimated_impact_amount=Decimal(str(row.estimated_impact_amount)),
                observation=str(row.observation),
                confidence=Decimal("1.0"),
            )
        )

    for row in unmapped_detection.unmapped_exceptions.itertuples(index=False):
        items.append(
            ReconciliationExceptionItem(
                exception_type=row.exception_type,
                severity=EXCEPTION_SEVERITY_DEFAULTS[row.exception_type],
                scope_level="record",
                record_id=_normalize_optional_string(row.record_id),
                concept_scope=(
                    _normalize_optional_string(row.inferred_concept_scope)
                    or _normalize_optional_string(row.concept_code)
                ),
                employee_id=_normalize_optional_string(row.employee_id),
                estimated_impact_amount=Decimal(str(row.estimated_impact_amount)),
                observation=str(row.observation),
                confidence=Decimal("1.0"),
            )
        )

    for row in duplicate_detection.duplicate_exceptions.itertuples(index=False):
        items.append(
            ReconciliationExceptionItem(
                exception_type=row.exception_type,
                severity=EXCEPTION_SEVERITY_DEFAULTS[row.exception_type],
                scope_level="record",
                record_id=_normalize_optional_string(row.record_id),
                concept_scope=_normalize_optional_string(row.concept_code_normalized),
                employee_id=_normalize_optional_string(row.employee_id),
                estimated_impact_amount=Decimal(str(row.estimated_group_impact_amount)),
                observation=str(row.observation),
                confidence=Decimal("0.75"),
            )
        )

    for row in missing_expected_detection.missing_expected_exceptions.itertuples(index=False):
        items.append(
            ReconciliationExceptionItem(
                exception_type=row.exception_type,
                severity=EXCEPTION_SEVERITY_DEFAULTS[row.exception_type],
                scope_level="concept",
                concept_scope=_normalize_optional_string(row.concept_code_normalized),
                estimated_impact_amount=Decimal(str(row.observed_amount)),
                observation=str(row.observation),
                confidence=Decimal("1.0"),
            )
        )

    for row in outlier_detection.outlier_exceptions.itertuples(index=False):
        items.append(
            ReconciliationExceptionItem(
                exception_type=row.exception_type,
                severity=EXCEPTION_SEVERITY_DEFAULTS[row.exception_type],
                scope_level="record",
                record_id=_normalize_optional_string(row.record_id),
                concept_scope=_normalize_optional_string(row.concept_code_normalized),
                employee_id=_normalize_optional_string(row.employee_id),
                estimated_impact_amount=Decimal(str(row.estimated_impact_amount)),
                observation=str(row.observation),
                confidence=Decimal("0.9"),
            )
        )

    for row in missing_population_detection.missing_population_exceptions.itertuples(
        index=False
    ):
        items.append(
            ReconciliationExceptionItem(
                exception_type=row.exception_type,
                severity=EXCEPTION_SEVERITY_DEFAULTS[row.exception_type],
                scope_level="record",
                concept_scope=_normalize_optional_string(row.concept_code_normalized),
                employee_id=_normalize_optional_string(row.missing_employee_id),
                estimated_impact_amount=Decimal(str(row.estimated_impact_amount)),
                observation=str(row.observation),
                confidence=Decimal("0.85"),
            )
        )

    if sign_error_detection is not None:
        for row in sign_error_detection.sign_error_exceptions.itertuples(index=False):
            items.append(
                ReconciliationExceptionItem(
                    exception_type=row.exception_type,
                    severity=EXCEPTION_SEVERITY_DEFAULTS[row.exception_type],
                    scope_level="record",
                    record_id=_normalize_optional_string(row.record_id),
                    concept_scope=_normalize_optional_string(row.concept_code_normalized),
                    employee_id=_normalize_optional_string(row.employee_id),
                    estimated_impact_amount=Decimal(str(row.estimated_impact_amount)),
                    observation=str(row.observation),
                    confidence=Decimal("0.95"),
                )
            )

    if misclassified_detection is not None:
        for row in misclassified_detection.misclassified_exceptions.itertuples(index=False):
            items.append(
                ReconciliationExceptionItem(
                    exception_type=row.exception_type,
                    severity=EXCEPTION_SEVERITY_DEFAULTS[row.exception_type],
                    scope_level="record",
                    record_id=_normalize_optional_string(row.record_id),
                    concept_scope=_normalize_optional_string(row.suggested_concept_scope),
                    observation=str(row.observation),
                    confidence=Decimal("0.5"),
                )
            )

    priority_map = {
        exception: index for index, exception in enumerate(EXCEPTION_PRIORITY_ORDER)
    }
    return sorted(
        items,
        key=lambda item: (
            priority_map.get(item.exception_type, len(priority_map)),
            item.scope_level,
            item.concept_scope or "",
            item.record_id or "",
            item.employee_id or "",
        ),
    )


def build_exception_impact_summary(
    structured_exceptions: list[ReconciliationExceptionItem],
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    priority_map = {
        exception: index + 1 for index, exception in enumerate(EXCEPTION_PRIORITY_ORDER)
    }

    for item in structured_exceptions:
        impact_value = (
            float(item.estimated_impact_amount)
            if item.estimated_impact_amount is not None
            else 0.0
        )
        rows.append(
            {
                "concept_scope": item.concept_scope,
                "exception_type": item.exception_type,
                "severity": item.severity,
                "priority_rank": priority_map.get(item.exception_type, len(priority_map) + 1),
                "impact_quality": _resolve_impact_quality(item.exception_type),
                "estimated_impact_amount": impact_value,
                "confidence": (
                    float(item.confidence) if item.confidence is not None else 0.0
                ),
            }
        )

    if not rows:
        return pd.DataFrame(
            columns=[
                "concept_scope",
                "exception_type",
                "severity",
                "priority_rank",
                "impact_quality",
                "exception_count",
                "estimated_impact_amount",
                "confidence",
            ]
        )

    summary = (
        pd.DataFrame(rows)
        .groupby(
            [
                "concept_scope",
                "exception_type",
                "severity",
                "priority_rank",
                "impact_quality",
            ],
            dropna=False,
            as_index=False,
        )
        .agg(
            exception_count=("exception_type", "count"),
            estimated_impact_amount=("estimated_impact_amount", "sum"),
            confidence=("confidence", "mean"),
        )
        .sort_values(
            ["concept_scope", "estimated_impact_amount", "priority_rank"],
            ascending=[True, False, True],
            ignore_index=True,
        )
    )
    return summary


def build_ranked_exception_causes(
    structured_exceptions: list[ReconciliationExceptionItem],
    limit_per_concept: int = 3,
) -> pd.DataFrame:
    impact_summary = build_exception_impact_summary(structured_exceptions)
    if impact_summary.empty:
        return impact_summary

    severity_score_map = {
        "critical": 4,
        "high": 3,
        "medium": 2,
        "low": 1,
    }
    ranked = impact_summary.copy()
    ranked["severity_score"] = ranked["severity"].map(severity_score_map).fillna(0)
    ranked = ranked.sort_values(
        [
            "concept_scope",
            "estimated_impact_amount",
            "severity_score",
            "confidence",
            "priority_rank",
            "exception_count",
        ],
        ascending=[True, False, False, False, True, False],
        ignore_index=True,
    )
    ranked["rank_within_concept"] = ranked.groupby("concept_scope").cumcount() + 1
    ranked = ranked.loc[ranked["rank_within_concept"] <= limit_per_concept].copy()
    return ranked


def _normalize_optional_string(value: object) -> str | None:
    if pd.isna(value):
        return None

    text = str(value).strip()
    return text or None


def _resolve_impact_quality(exception_type: str) -> str:
    if exception_type in {
        "Out-of-Period Record",
        "Unmapped Concept",
        "Missing Expected Total",
    }:
        return "exact"
    if exception_type in {
        "Duplicate Record",
        "Missing Record / Missing Population",
        "Outlier Amount",
    }:
        return "estimated"
    return "not_quantified"


def _infer_unmapped_concept_scope(
    concept_name_series: pd.Series,
    concept_master: pd.DataFrame,
) -> pd.Series:
    if concept_name_series.empty:
        return pd.Series(dtype="string")

    active_master = concept_master.copy()
    active_master["source_concept_name_key"] = _normalize_text_key(
        active_master["source_concept_name"]
    )
    active_master["normalized_concept_code"] = (
        active_master["normalized_concept_code"].astype("string").str.strip()
    )
    raw_keys = _normalize_text_key(concept_name_series)

    inferred: list[str | None] = []
    for raw_key in raw_keys.tolist():
        match = None
        for candidate in active_master.itertuples(index=False):
            source_key = str(candidate.source_concept_name_key)
            if source_key and source_key in raw_key:
                match = str(candidate.normalized_concept_code)
                break
        inferred.append(match)

    return pd.Series(inferred, index=concept_name_series.index, dtype="string")
