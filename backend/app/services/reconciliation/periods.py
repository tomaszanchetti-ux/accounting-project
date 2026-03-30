from __future__ import annotations

import pandas as pd

from app.schemas import PayrollPeriodNormalizationResult
from app.schemas.reconciliation import DataFrameLike
from app.services.reconciliation.normalization import normalize_payroll_base


def normalize_payroll_periods(
    source: DataFrameLike | pd.DataFrame,
    target_period: str,
) -> PayrollPeriodNormalizationResult:
    normalized_base = normalize_payroll_base(source).normalized_records
    normalized = normalized_base.copy()

    payroll_period_raw = (
        normalized["payroll_period"].astype("string").str.strip()
        if "payroll_period" in normalized.columns
        else pd.Series(pd.NA, index=normalized.index, dtype="string")
    )
    posting_period = (
        normalized["posting_date"].dt.strftime("%Y-%m").astype("string")
        if "posting_date" in normalized.columns
        else pd.Series(pd.NA, index=normalized.index, dtype="string")
    )

    payroll_period_format_valid = payroll_period_raw.str.fullmatch(r"\d{4}-\d{2}", na=False)
    payroll_period_from_posting_date = posting_period.where(posting_period.notna())
    payroll_period_normalized = payroll_period_raw.where(
        payroll_period_format_valid,
        payroll_period_from_posting_date,
    )
    payroll_period_derived = (~payroll_period_format_valid) & posting_period.notna()
    payroll_period_is_valid = payroll_period_normalized.str.fullmatch(r"\d{4}-\d{2}", na=False)
    is_target_period = payroll_period_normalized.eq(target_period)
    is_out_of_period = payroll_period_is_valid & ~is_target_period

    normalized["posting_period"] = posting_period
    normalized["payroll_period_normalized"] = payroll_period_normalized
    normalized["payroll_period_derived"] = payroll_period_derived
    normalized["payroll_period_is_valid"] = payroll_period_is_valid
    normalized["is_target_period"] = is_target_period
    normalized["is_out_of_period"] = is_out_of_period

    return PayrollPeriodNormalizationResult(
        normalized_records=normalized,
        target_period=target_period,
        in_target_period_count=int(is_target_period.sum()),
        out_of_period_count=int(is_out_of_period.sum()),
    )
