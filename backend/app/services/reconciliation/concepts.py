from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.schemas import ConceptNormalizationResult
from app.schemas.reconciliation import DataFrameLike
from app.services.reconciliation.normalization import normalize_payroll_base


def _load_dataframe(source: DataFrameLike) -> pd.DataFrame:
    if isinstance(source, pd.DataFrame):
        return source.copy()

    return pd.read_csv(Path(source))


def _normalize_text_key(series: pd.Series) -> pd.Series:
    return (
        series.astype("string")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .str.lower()
    )


def normalize_payroll_concepts(
    payroll_source: DataFrameLike | pd.DataFrame,
    concept_master_source: DataFrameLike,
) -> ConceptNormalizationResult:
    payroll = normalize_payroll_base(payroll_source).normalized_records.copy()
    concept_master = _load_dataframe(concept_master_source).copy()

    concept_master["source_concept_code"] = (
        concept_master["source_concept_code"].astype("string").str.strip().str.upper()
    )
    concept_master["source_concept_name_key"] = _normalize_text_key(
        concept_master["source_concept_name"]
    )
    concept_master["is_active"] = concept_master["is_active"].fillna(False).astype(bool)
    active_master = concept_master.loc[concept_master["is_active"]].copy()

    payroll["concept_code"] = payroll["concept_code"].astype("string").str.strip().str.upper()
    payroll["concept_name_key"] = _normalize_text_key(payroll["concept_name"])

    code_lookup = active_master[
        [
            "source_concept_code",
            "normalized_concept_code",
            "normalized_concept_name",
            "concept_category",
            "reconciliation_group",
            "expected_sign",
        ]
    ].drop_duplicates(subset=["source_concept_code"])
    code_lookup = code_lookup.rename(
        columns={
            "source_concept_code": "concept_code",
            "normalized_concept_code": "concept_code_normalized_by_code",
            "normalized_concept_name": "concept_name_normalized_by_code",
            "concept_category": "concept_category_by_code",
            "reconciliation_group": "reconciliation_group_by_code",
            "expected_sign": "expected_sign_by_code",
        }
    )

    normalized = payroll.merge(code_lookup, on="concept_code", how="left")

    name_lookup = active_master[
        [
            "source_concept_name_key",
            "normalized_concept_code",
            "normalized_concept_name",
            "concept_category",
            "reconciliation_group",
            "expected_sign",
        ]
    ].drop_duplicates(subset=["source_concept_name_key"])
    name_lookup = name_lookup.rename(
        columns={
            "normalized_concept_code": "concept_code_normalized_by_name",
            "normalized_concept_name": "concept_name_normalized_by_name",
            "concept_category": "concept_category_by_name",
            "reconciliation_group": "reconciliation_group_by_name",
            "expected_sign": "expected_sign_by_name",
        }
    )

    normalized = normalized.merge(
        name_lookup,
        left_on="concept_name_key",
        right_on="source_concept_name_key",
        how="left",
    )

    normalized["concept_mapping_method"] = pd.Series(pd.NA, index=normalized.index, dtype="string")
    has_code_match = normalized["concept_code_normalized_by_code"].notna()
    has_name_match = normalized["concept_code_normalized_by_name"].notna()

    normalized.loc[has_code_match, "concept_mapping_method"] = "code"
    normalized.loc[~has_code_match & has_name_match, "concept_mapping_method"] = "name"
    normalized.loc[
        normalized["concept_mapping_method"].isna(),
        "concept_mapping_method",
    ] = "unmapped"

    normalized["concept_code_normalized"] = normalized["concept_code_normalized_by_code"].where(
        has_code_match,
        normalized["concept_code_normalized_by_name"],
    )
    normalized["concept_name_normalized"] = normalized["concept_name_normalized_by_code"].where(
        has_code_match,
        normalized["concept_name_normalized_by_name"],
    )
    normalized["concept_category"] = normalized["concept_category_by_code"].where(
        has_code_match,
        normalized["concept_category_by_name"],
    )
    normalized["reconciliation_group"] = normalized["reconciliation_group_by_code"].where(
        has_code_match,
        normalized["reconciliation_group_by_name"],
    )
    normalized["expected_sign"] = normalized["expected_sign_by_code"].where(
        has_code_match,
        normalized["expected_sign_by_name"],
    )
    normalized["is_unmapped_concept"] = normalized["concept_mapping_method"].eq("unmapped")

    drop_columns = [
        "concept_name_key",
        "concept_code_normalized_by_code",
        "concept_name_normalized_by_code",
        "concept_category_by_code",
        "reconciliation_group_by_code",
        "expected_sign_by_code",
        "concept_code_normalized_by_name",
        "concept_name_normalized_by_name",
        "concept_category_by_name",
        "reconciliation_group_by_name",
        "expected_sign_by_name",
        "source_concept_name_key",
    ]
    normalized = normalized.drop(
        columns=[column for column in drop_columns if column in normalized]
    )

    return ConceptNormalizationResult(
        normalized_records=normalized,
        mapped_record_count=int((~normalized["is_unmapped_concept"]).sum()),
        unmapped_record_count=int(normalized["is_unmapped_concept"].sum()),
    )
