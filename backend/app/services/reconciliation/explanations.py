from __future__ import annotations

from decimal import Decimal

import pandas as pd

from app.schemas import ConceptExplanation, ExplanationCause, ReconciliationSummaryRow
from app.schemas.reconciliation import ReconciliationExceptionItem

CAUSE_TITLES = {
    "Invalid Amount / Data Quality Issue": "Data quality issues detected",
    "Out-of-Period Record": "Out-of-period records detected",
    "Unmapped Concept": "Unmapped concept lines detected",
    "Duplicate Record": "Probable duplicate records detected",
    "Missing Expected Total": "Expected total is missing",
    "Missing Record / Missing Population": "Missing eligible population detected",
    "Outlier Amount": "Outlier amount detected",
}

RECOMMENDATION_BY_EXCEPTION = {
    "Invalid Amount / Data Quality Issue": (
        "Review the raw payroll lines with invalid critical fields before relying "
        "on this concept."
    ),
    "Out-of-Period Record": (
        "Review payroll lines booked outside the target period and confirm whether "
        "they should be reclassified or excluded."
    ),
    "Unmapped Concept": (
        "Review raw concept labels and extend the mapping only where the match is "
        "operationally safe."
    ),
    "Duplicate Record": (
        "Review repeated employee and concept combinations to confirm whether "
        "duplicate posting occurred."
    ),
    "Missing Expected Total": (
        "Add or validate the expected total for this concept before using the "
        "comparison as a control."
    ),
    "Missing Record / Missing Population": (
        "Review eligible employees missing from the observed population and "
        "confirm whether payroll coverage is incomplete."
    ),
    "Outlier Amount": (
        "Review the dominant outlier line first and confirm whether the amount "
        "is valid or needs adjustment."
    ),
}


def build_concept_explanations(
    summary_rows: list[ReconciliationSummaryRow],
    ranked_exception_causes: pd.DataFrame,
    structured_exceptions: list[ReconciliationExceptionItem],
) -> list[ConceptExplanation]:
    explanations: list[ConceptExplanation] = []
    structured_by_concept = _group_structured_exceptions_by_concept(structured_exceptions)

    for summary_row in summary_rows:
        concept_scope = summary_row.concept_code_normalized
        concept_ranked = ranked_exception_causes.loc[
            ranked_exception_causes["concept_scope"] == concept_scope
        ].copy()
        concept_structured = structured_by_concept.get(concept_scope, [])
        probable_causes = [
            _build_explanation_cause(row) for row in concept_ranked.itertuples(index=False)
        ]
        recommendation = (
            RECOMMENDATION_BY_EXCEPTION.get(probable_causes[0].exception_type)
            if probable_causes
            else None
        )
        explained_amount = (
            Decimal(str(concept_ranked["estimated_impact_amount"].sum()))
            if not concept_ranked.empty
            else None
        )
        impacted_records_count = len(
            {item.record_id for item in concept_structured if item.record_id}
        )
        impacted_employees_count = len(
            {item.employee_id for item in concept_structured if item.employee_id}
        )

        explanations.append(
            ConceptExplanation(
                concept_code_normalized=concept_scope,
                summary_statement=_build_summary_statement(summary_row),
                probable_causes=probable_causes,
                recommended_action=recommendation,
                explained_amount_estimate=explained_amount,
                impacted_records_count=impacted_records_count,
                impacted_employees_count=impacted_employees_count,
            )
        )

    return explanations


def _build_summary_statement(summary_row: ReconciliationSummaryRow) -> str:
    diff_abs = abs(summary_row.absolute_diff)
    direction = "above" if summary_row.absolute_diff > 0 else "below"
    if summary_row.status == "Invalid / Incomplete":
        return (
            f"{summary_row.concept_code_normalized} for {summary_row.period} could not be "
            "fully assessed because the available data is incomplete or invalid."
        )
    if summary_row.status == "Reconciled":
        return (
            f"{summary_row.concept_code_normalized} for {summary_row.period} is reconciled "
            "within the MVP tolerance."
        )
    if summary_row.status == "Minor Difference":
        return (
            f"{summary_row.concept_code_normalized} for {summary_row.period} shows a minor "
            f"difference: observed is EUR {direction_amount(summary_row.absolute_diff)} "
            f"vs expected by EUR {diff_abs}."
        )
    return (
        f"{summary_row.concept_code_normalized} for {summary_row.period} is unreconciled: "
        f"observed is EUR {direction} expected by EUR {diff_abs}."
    )


def _build_explanation_cause(row: pd.Series | object) -> ExplanationCause:
    exception_type = str(row.exception_type)
    evidence_count = int(row.exception_count)
    impact = Decimal(str(row.estimated_impact_amount))
    confidence = Decimal(str(row.confidence))
    detail = _build_cause_detail(
        exception_type=exception_type,
        evidence_count=evidence_count,
        estimated_impact_amount=impact,
        impact_quality=str(row.impact_quality),
    )
    return ExplanationCause(
        exception_type=exception_type,
        title=CAUSE_TITLES.get(exception_type, exception_type),
        detail=detail,
        estimated_impact_amount=impact,
        evidence_count=evidence_count,
        confidence=confidence,
    )


def _build_cause_detail(
    *,
    exception_type: str,
    evidence_count: int,
    estimated_impact_amount: Decimal,
    impact_quality: str,
) -> str:
    if exception_type == "Duplicate Record":
        return (
            f"Detected {evidence_count} probable duplicate records with "
            f"{impact_quality} impact around EUR {estimated_impact_amount}."
        )
    if exception_type == "Missing Record / Missing Population":
        return (
            f"Detected {evidence_count} eligible employees missing from the observed "
            f"population, with estimated impact around EUR {estimated_impact_amount}."
        )
    if exception_type == "Outlier Amount":
        return (
            f"Detected {evidence_count} dominant outlier records, with estimated "
            f"excess impact around EUR {estimated_impact_amount}."
        )
    if exception_type == "Invalid Amount / Data Quality Issue":
        return (
            f"Detected {evidence_count} data quality issues affecting the reliability "
            "of this concept."
        )
    return (
        f"Detected {evidence_count} records or units linked to this cause, with "
        f"{impact_quality} impact around EUR {estimated_impact_amount}."
    )


def _group_structured_exceptions_by_concept(
    structured_exceptions: list[ReconciliationExceptionItem],
) -> dict[str, list[ReconciliationExceptionItem]]:
    grouped: dict[str, list[ReconciliationExceptionItem]] = {}
    for item in structured_exceptions:
        if not item.concept_scope:
            continue
        grouped.setdefault(item.concept_scope, []).append(item)
    return grouped


def direction_amount(value: Decimal) -> str:
    return "above" if value > 0 else "below"
