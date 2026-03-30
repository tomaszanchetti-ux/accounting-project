from __future__ import annotations

import pandas as pd

from app.schemas import ReconcilablePayrollBaseResult
from app.schemas.reconciliation import DataFrameLike
from app.services.reconciliation.periods import normalize_payroll_periods
from app.services.reconciliation.signs import normalize_payroll_signs
from app.services.reconciliation.validation import validate_payroll_records


def build_reconcilable_payroll_base(
    payroll_source: DataFrameLike | pd.DataFrame,
    concept_master_source: DataFrameLike,
    target_period: str,
) -> ReconcilablePayrollBaseResult:
    record_validation = validate_payroll_records(payroll_source).validated_records.copy()
    period_normalization = normalize_payroll_periods(
        payroll_source,
        target_period=target_period,
    ).normalized_records.copy()
    sign_normalization = normalize_payroll_signs(
        payroll_source,
        concept_master_source,
    ).normalized_records.copy()

    base = sign_normalization.copy()
    base["invalid_reasons"] = record_validation["invalid_reasons"]
    base["is_valid_record"] = record_validation["is_valid_record"]
    base["payroll_period_normalized"] = period_normalization["payroll_period_normalized"]
    base["payroll_period_derived"] = period_normalization["payroll_period_derived"]
    base["payroll_period_is_valid"] = period_normalization["payroll_period_is_valid"]
    base["posting_period"] = period_normalization["posting_period"]
    base["is_target_period"] = period_normalization["is_target_period"]
    base["is_out_of_period"] = period_normalization["is_out_of_period"]

    base["reconciliation_unit_key"] = (
        base["payroll_period_normalized"].astype("string")
        + "::"
        + base["concept_code_normalized"].astype("string")
    )
    base["is_eligible_for_reconciliation"] = (
        base["is_valid_record"] & ~base["is_unmapped_concept"]
    )
    base["quality_status"] = pd.Series(pd.NA, index=base.index, dtype="string")
    base.loc[base["is_valid_record"], "quality_status"] = "valid"
    base.loc[~base["is_valid_record"], "quality_status"] = "invalid"

    base["observability_status"] = pd.Series(pd.NA, index=base.index, dtype="string")
    base.loc[base["is_eligible_for_reconciliation"], "observability_status"] = "eligible"
    base.loc[
        base["is_valid_record"] & base["is_unmapped_concept"],
        "observability_status",
    ] = "valid_with_exception"
    base.loc[~base["is_valid_record"], "observability_status"] = "invalid"

    return ReconcilablePayrollBaseResult(
        reconciliable_base=base,
        eligible_record_count=int(base["is_eligible_for_reconciliation"].sum()),
        invalid_record_count=int((~base["is_valid_record"]).sum()),
        out_of_period_count=int(base["is_out_of_period"].sum()),
        unmapped_record_count=int(base["is_unmapped_concept"].sum()),
    )
