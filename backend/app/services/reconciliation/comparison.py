from __future__ import annotations

import pandas as pd

from app.schemas import ComparisonBaseResult, DifferenceCalculationResult
from app.schemas.reconciliation import DataFrameLike
from app.services.reconciliation.aggregate import build_observed_totals
from app.services.reconciliation.validation import validate_expected_totals


def build_comparison_base(
    payroll_source: DataFrameLike | pd.DataFrame,
    expected_totals_source: DataFrameLike,
    concept_master_source: DataFrameLike,
    target_period: str,
) -> ComparisonBaseResult:
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
    expected = expected.rename(
        columns={
            "payroll_period": "period",
            "concept_code": "concept_code_normalized",
            "expected_amount": "expected_amount",
        }
    )

    comparison = observed.merge(
        expected[["period", "concept_code_normalized", "expected_amount", "currency"]],
        on=["period", "concept_code_normalized"],
        how="left",
    )
    comparison["has_expected_reference"] = comparison["expected_amount"].notna()

    return ComparisonBaseResult(
        comparison_base=comparison,
        missing_expected_count=int((~comparison["has_expected_reference"]).sum()),
    )


def calculate_differences(
    payroll_source: DataFrameLike | pd.DataFrame,
    expected_totals_source: DataFrameLike,
    concept_master_source: DataFrameLike,
    target_period: str,
) -> DifferenceCalculationResult:
    comparison = build_comparison_base(
        payroll_source,
        expected_totals_source,
        concept_master_source,
        target_period=target_period,
    ).comparison_base.copy()

    comparison["absolute_diff"] = comparison["observed_amount"] - comparison["expected_amount"]
    comparison["relative_diff_pct"] = (
        comparison["absolute_diff"] / comparison["expected_amount"].abs() * 100
    )
    comparison.loc[
        comparison["expected_amount"].isna() | comparison["expected_amount"].eq(0),
        "relative_diff_pct",
    ] = pd.NA
    comparison["absolute_diff"] = comparison["absolute_diff"].round(2)
    comparison["relative_diff_pct"] = comparison["relative_diff_pct"].round(4)

    return DifferenceCalculationResult(comparison_with_diffs=comparison)
