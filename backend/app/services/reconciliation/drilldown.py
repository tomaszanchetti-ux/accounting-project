from __future__ import annotations

import pandas as pd

from app.schemas import DrilldownPreparationResult
from app.schemas.reconciliation import DataFrameLike
from app.services.reconciliation.base import build_reconcilable_payroll_base


def prepare_reconcilable_base_for_drilldown(
    payroll_source: DataFrameLike | pd.DataFrame,
    concept_master_source: DataFrameLike,
    target_period: str,
) -> DrilldownPreparationResult:
    base = build_reconcilable_payroll_base(
        payroll_source,
        concept_master_source,
        target_period=target_period,
    ).reconciliable_base.copy()

    base["drilldown_join_key"] = base["record_id"].astype("string")
    base["employee_join_key"] = base["employee_id"].astype("string")
    base["concept_period_join_key"] = (
        base["payroll_period_normalized"].astype("string")
        + "::"
        + base["concept_code_normalized"].astype("string")
    )

    return DrilldownPreparationResult(
        prepared_base=base,
        traceable_record_count=int(base["drilldown_join_key"].notna().sum()),
    )
