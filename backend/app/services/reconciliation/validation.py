from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.schemas import (
    ExpectedTotalsValidationResult,
    PayrollRecordValidationResult,
    PayrollSchemaValidationResult,
    ValidationIssue,
)
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

REQUIRED_EXPECTED_TOTALS_COLUMNS = [
    "payroll_period",
    "concept_code",
    "expected_amount",
    "currency",
]


def _get_string_series(dataframe: pd.DataFrame, column: str) -> pd.Series:
    if column not in dataframe.columns:
        return pd.Series(pd.NA, index=dataframe.index, dtype="string")

    return dataframe[column].astype("string").str.strip()


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


def validate_payroll_records(source: DataFrameLike) -> PayrollRecordValidationResult:
    dataframe = _load_dataframe(source)
    validated = dataframe.copy()

    amount_numeric = pd.to_numeric(validated.get("amount"), errors="coerce")
    posting_date_parsed = pd.to_datetime(
        validated.get("posting_date"),
        errors="coerce",
    )
    payroll_period_raw = _get_string_series(validated, "payroll_period")
    payroll_period_present = payroll_period_raw.notna() & payroll_period_raw.ne("")
    payroll_period_format_valid = payroll_period_raw.str.fullmatch(r"\d{4}-\d{2}", na=False)
    derived_payroll_period = posting_date_parsed.dt.strftime("%Y-%m").astype("string")
    payroll_period_derived = (~payroll_period_present) & derived_payroll_period.notna()
    effective_payroll_period = payroll_period_raw.where(
        payroll_period_present,
        derived_payroll_period,
    )
    effective_payroll_period_valid = effective_payroll_period.str.fullmatch(
        r"\d{4}-\d{2}",
        na=False,
    )

    concept_code_raw = _get_string_series(validated, "concept_code")
    concept_name_raw = _get_string_series(validated, "concept_name")
    employee_id_raw = _get_string_series(validated, "employee_id")

    validated["amount_numeric"] = amount_numeric
    validated["amount_is_valid"] = amount_numeric.notna()
    validated["posting_date_parsed"] = posting_date_parsed
    validated["posting_date_is_valid"] = posting_date_parsed.notna()
    validated["payroll_period_raw"] = payroll_period_raw
    validated["payroll_period_present"] = payroll_period_present
    validated["payroll_period_format_valid"] = payroll_period_format_valid
    validated["derived_payroll_period"] = derived_payroll_period
    validated["payroll_period_derived"] = payroll_period_derived
    validated["effective_payroll_period"] = effective_payroll_period
    validated["effective_payroll_period_is_valid"] = effective_payroll_period_valid
    validated["concept_code_present"] = concept_code_raw.notna() & concept_code_raw.ne("")
    validated["concept_name_present"] = concept_name_raw.notna() & concept_name_raw.ne("")
    validated["concept_present"] = (
        validated["concept_code_present"] | validated["concept_name_present"]
    )
    validated["employee_id_present"] = employee_id_raw.notna() & employee_id_raw.ne("")

    invalid_reason_columns = {
        "invalid_amount": ~validated["amount_is_valid"],
        "invalid_posting_date": ~validated["posting_date_is_valid"],
        "missing_or_invalid_payroll_period": ~validated["effective_payroll_period_is_valid"],
        "missing_concept": ~validated["concept_present"],
        "missing_employee_id": ~validated["employee_id_present"],
    }

    def collect_invalid_reasons(index: int) -> list[str]:
        return [
            reason
            for reason, mask in invalid_reason_columns.items()
            if bool(mask.iloc[index])
        ]

    validated["invalid_reasons"] = [
        collect_invalid_reasons(index) for index in range(len(validated))
    ]
    validated["is_valid_record"] = validated["invalid_reasons"].map(lambda reasons: not reasons)

    invalid_record_count = int((~validated["is_valid_record"]).sum())
    result = PayrollRecordValidationResult(
        validated_records=validated,
        total_records=len(validated),
        valid_record_count=int(validated["is_valid_record"].sum()),
        invalid_record_count=invalid_record_count,
    )

    if invalid_record_count > 0:
        result.validation_warnings.append(
            ValidationIssue(
                code="invalid_records_detected",
                message=(
                    f"Detected {invalid_record_count} payroll records with invalid or "
                    "non-interpretable critical fields."
                ),
                blocking=False,
            )
        )

    return result


def validate_expected_totals(
    source: DataFrameLike,
    target_period: str,
    observed_concepts: list[str] | None = None,
) -> ExpectedTotalsValidationResult:
    dataframe = _load_dataframe(source)
    detected_columns = [str(column).strip() for column in dataframe.columns]
    detected_set = set(detected_columns)

    missing_required = [
        column
        for column in REQUIRED_EXPECTED_TOTALS_COLUMNS
        if column not in detected_set
    ]

    filtered_expected_totals = pd.DataFrame()
    result = ExpectedTotalsValidationResult(
        filtered_expected_totals=filtered_expected_totals,
        target_period=target_period,
        columns_detected=detected_columns,
        missing_required_columns=missing_required,
    )

    for column in missing_required:
        result.validation_errors.append(
            ValidationIssue(
                code="missing_required_expected_totals_column",
                message=f"Missing required expected totals column: {column}",
                blocking=True,
                column=column,
            )
        )

    if missing_required:
        return result

    filtered_expected_totals = dataframe.loc[
        dataframe["payroll_period"].astype("string").str.strip() == target_period
    ].copy()
    result.filtered_expected_totals = filtered_expected_totals

    if filtered_expected_totals.empty:
        result.validation_errors.append(
            ValidationIssue(
                code="missing_target_period_in_expected_totals",
                message=(
                    "Expected totals does not contain rows for the requested "
                    f"target period: {target_period}"
                ),
                blocking=True,
                column="payroll_period",
            )
        )
        return result

    expected_concepts = set(
        filtered_expected_totals["concept_code"].astype("string").str.strip().tolist()
    )

    if observed_concepts:
        normalized_observed = sorted(
            {
                str(concept).strip()
                for concept in observed_concepts
                if str(concept).strip()
            }
        )
        missing_expected_concepts = [
            concept for concept in normalized_observed if concept not in expected_concepts
        ]
        result.missing_expected_concepts = missing_expected_concepts

        for concept in missing_expected_concepts:
            result.validation_warnings.append(
                ValidationIssue(
                    code="missing_expected_total_for_concept",
                    message=(
                        "Expected totals is missing a reference row for observed "
                        f"concept {concept} in period {target_period}"
                    ),
                    blocking=False,
                    column="concept_code",
                )
            )

    return result
