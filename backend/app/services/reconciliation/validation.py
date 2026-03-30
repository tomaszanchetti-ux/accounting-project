from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.schemas import PayrollSchemaValidationResult, ValidationIssue
from app.schemas.reconciliation import DataFrameLike

REQUIRED_PAYROLL_COLUMNS = [
    "record_id",
    "employee_id",
    "payroll_period",
    "posting_date",
    "concept_code",
    "amount",
    "currency",
]

RECOMMENDED_PAYROLL_COLUMNS = [
    "employee_name",
    "legal_entity",
    "country",
    "cost_center",
    "concept_name",
]


def _load_dataframe(source: DataFrameLike) -> pd.DataFrame:
    if isinstance(source, pd.DataFrame):
        return source.copy()

    return pd.read_csv(Path(source))


def validate_payroll_schema(source: DataFrameLike) -> PayrollSchemaValidationResult:
    dataframe = _load_dataframe(source)
    detected_columns = [str(column).strip() for column in dataframe.columns]
    detected_set = set(detected_columns)

    missing_required = [
        column for column in REQUIRED_PAYROLL_COLUMNS if column not in detected_set
    ]
    missing_recommended = [
        column for column in RECOMMENDED_PAYROLL_COLUMNS if column not in detected_set
    ]

    result = PayrollSchemaValidationResult(
        columns_detected=detected_columns,
        missing_required_columns=missing_required,
        missing_recommended_columns=missing_recommended,
    )

    for column in missing_required:
        result.errors.append(
            ValidationIssue(
                code="missing_required_column",
                message=f"Missing required payroll column: {column}",
                blocking=True,
                column=column,
            )
        )

    for column in missing_recommended:
        result.warnings.append(
            ValidationIssue(
                code="missing_recommended_column",
                message=f"Missing recommended payroll column: {column}",
                blocking=False,
                column=column,
            )
        )

    return result
