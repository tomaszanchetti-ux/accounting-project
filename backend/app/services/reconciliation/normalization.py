from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from app.schemas import PayrollNormalizationResult
from app.schemas.reconciliation import DataFrameLike

_COLUMN_ALIAS_MAP = {
    "recordid": "record_id",
    "employeeid": "employee_id",
    "employeename": "employee_name",
    "legalentity": "legal_entity",
    "costcentre": "cost_center",
    "costcenter": "cost_center",
    "payrollperiod": "payroll_period",
    "postingdate": "posting_date",
    "conceptcode": "concept_code",
    "conceptname": "concept_name",
}

_STRING_COLUMNS = [
    "record_id",
    "employee_id",
    "employee_name",
    "legal_entity",
    "country",
    "cost_center",
    "payroll_period",
    "concept_code",
    "concept_name",
    "currency",
]

_UPPERCASE_COLUMNS = ["concept_code", "currency"]


def _load_dataframe(source: DataFrameLike) -> pd.DataFrame:
    if isinstance(source, pd.DataFrame):
        return source.copy()

    return pd.read_csv(Path(source))


def _canonicalize_column_name(name: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    collapsed = cleaned.replace("_", "")
    return _COLUMN_ALIAS_MAP.get(collapsed, cleaned)


def normalize_payroll_base(source: DataFrameLike) -> PayrollNormalizationResult:
    dataframe = _load_dataframe(source)
    column_mapping = {
        str(column): _canonicalize_column_name(str(column)) for column in dataframe.columns
    }
    normalized = dataframe.rename(columns=column_mapping).copy()

    for column in _STRING_COLUMNS:
        if column not in normalized.columns:
            continue

        normalized[column] = (
            normalized[column]
            .astype("string")
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    for column in _UPPERCASE_COLUMNS:
        if column in normalized.columns:
            normalized[column] = normalized[column].str.upper()

    if "amount" in normalized.columns:
        normalized["amount"] = pd.to_numeric(normalized["amount"], errors="coerce")

    if "posting_date" in normalized.columns:
        normalized["posting_date"] = pd.to_datetime(
            normalized["posting_date"],
            errors="coerce",
        )

    return PayrollNormalizationResult(
        normalized_records=normalized,
        column_mapping=column_mapping,
    )
