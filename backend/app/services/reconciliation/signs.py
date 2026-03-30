from __future__ import annotations

import pandas as pd

from app.schemas import PayrollSignNormalizationResult
from app.schemas.reconciliation import DataFrameLike
from app.services.reconciliation.concepts import normalize_payroll_concepts


def normalize_payroll_signs(
    payroll_source: DataFrameLike | pd.DataFrame,
    concept_master_source: DataFrameLike,
) -> PayrollSignNormalizationResult:
    normalized = normalize_payroll_concepts(
        payroll_source,
        concept_master_source,
    ).normalized_records.copy()

    normalized["amount_for_aggregation"] = pd.to_numeric(
        normalized["amount"],
        errors="coerce",
    )
    normalized["amount_absolute"] = normalized["amount_for_aggregation"].abs()
    normalized["amount_sign_observed"] = pd.Series(pd.NA, index=normalized.index, dtype="string")

    positive_mask = normalized["amount_for_aggregation"] > 0
    negative_mask = normalized["amount_for_aggregation"] < 0
    zero_mask = normalized["amount_for_aggregation"] == 0

    normalized.loc[positive_mask, "amount_sign_observed"] = "positive"
    normalized.loc[negative_mask, "amount_sign_observed"] = "negative"
    normalized.loc[zero_mask, "amount_sign_observed"] = "zero"

    normalized["has_unexpected_sign"] = (
        normalized["expected_sign"].notna()
        & normalized["amount_sign_observed"].notna()
        & normalized["amount_sign_observed"].ne("zero")
        & normalized["amount_sign_observed"].ne(normalized["expected_sign"])
    )

    return PayrollSignNormalizationResult(
        normalized_records=normalized,
        unexpected_sign_count=int(normalized["has_unexpected_sign"].sum()),
    )
