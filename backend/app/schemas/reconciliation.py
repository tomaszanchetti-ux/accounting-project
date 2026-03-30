from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

import pandas as pd

DataFrameLike = pd.DataFrame | str | Path


@dataclass(slots=True)
class ToleranceProfile:
    label: str = "mvp-default"
    absolute_minor_threshold: Decimal | None = None
    relative_minor_threshold_pct: Decimal | None = None


@dataclass(slots=True)
class ValidationIssue:
    code: str
    message: str
    blocking: bool
    column: str | None = None


@dataclass(slots=True)
class PayrollSchemaValidationResult:
    columns_detected: list[str]
    missing_required_columns: list[str] = field(default_factory=list)
    missing_recommended_columns: list[str] = field(default_factory=list)
    errors: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)

    @property
    def is_blocking(self) -> bool:
        return any(issue.blocking for issue in self.errors)

    @property
    def is_valid(self) -> bool:
        return not self.is_blocking


@dataclass(slots=True)
class PayrollRecordValidationResult:
    validated_records: pd.DataFrame
    total_records: int
    valid_record_count: int
    invalid_record_count: int
    validation_errors: list[ValidationIssue] = field(default_factory=list)
    validation_warnings: list[ValidationIssue] = field(default_factory=list)


@dataclass(slots=True)
class ExpectedTotalsValidationResult:
    filtered_expected_totals: pd.DataFrame
    target_period: str
    columns_detected: list[str]
    missing_required_columns: list[str] = field(default_factory=list)
    missing_expected_concepts: list[str] = field(default_factory=list)
    validation_errors: list[ValidationIssue] = field(default_factory=list)
    validation_warnings: list[ValidationIssue] = field(default_factory=list)

    @property
    def is_blocking(self) -> bool:
        return any(issue.blocking for issue in self.validation_errors)

    @property
    def is_valid(self) -> bool:
        return not self.is_blocking


@dataclass(slots=True)
class PayrollNormalizationResult:
    normalized_records: pd.DataFrame
    column_mapping: dict[str, str]


@dataclass(slots=True)
class PayrollPeriodNormalizationResult:
    normalized_records: pd.DataFrame
    target_period: str
    in_target_period_count: int
    out_of_period_count: int


@dataclass(slots=True)
class ConceptNormalizationResult:
    normalized_records: pd.DataFrame
    mapped_record_count: int
    unmapped_record_count: int


@dataclass(slots=True)
class PayrollSignNormalizationResult:
    normalized_records: pd.DataFrame
    unexpected_sign_count: int


@dataclass(slots=True)
class ReconcilablePayrollBaseResult:
    reconciliable_base: pd.DataFrame
    eligible_record_count: int
    invalid_record_count: int
    out_of_period_count: int
    unmapped_record_count: int


@dataclass(slots=True)
class ObservedTotalsInclusionPolicy:
    include_valid_mapped_records: bool = True
    exclude_out_of_period_records: bool = True
    exclude_unmapped_records: bool = True
    exclude_invalid_records: bool = True


@dataclass(slots=True)
class DrilldownPreparationResult:
    prepared_base: pd.DataFrame
    traceable_record_count: int


@dataclass(slots=True)
class ObservedTotalsResult:
    observed_totals: pd.DataFrame
    total_groups: int
    segmented_by_legal_entity: bool = False


@dataclass(slots=True)
class ComparisonBaseResult:
    comparison_base: pd.DataFrame
    missing_expected_count: int


@dataclass(slots=True)
class DifferenceCalculationResult:
    comparison_with_diffs: pd.DataFrame


@dataclass(slots=True)
class InvalidDataQualityDetectionResult:
    invalid_exceptions: pd.DataFrame
    invalid_record_count: int
    blocking_issue_count: int
    non_blocking_issue_count: int
    run_has_blocking_data_quality_issues: bool
    has_partial_invalidation_only: bool


@dataclass(slots=True)
class OutOfPeriodDetectionResult:
    out_of_period_exceptions: pd.DataFrame
    impact_by_concept: pd.DataFrame
    out_of_period_record_count: int
    total_estimated_impact_amount: float


@dataclass(slots=True)
class UnmappedConceptDetectionResult:
    unmapped_exceptions: pd.DataFrame
    impact_by_raw_concept: pd.DataFrame
    unmapped_record_count: int
    total_estimated_impact_amount: float


@dataclass(slots=True)
class DuplicateRecordDetectionResult:
    duplicate_exceptions: pd.DataFrame
    impact_by_concept: pd.DataFrame
    duplicate_record_count: int
    duplicate_group_count: int
    total_estimated_duplicate_impact_amount: float


@dataclass(slots=True)
class MissingExpectedTotalDetectionResult:
    missing_expected_exceptions: pd.DataFrame
    missing_expected_count: int
    total_observed_amount_without_expected: float


@dataclass(slots=True)
class OutlierAmountDetectionResult:
    outlier_exceptions: pd.DataFrame
    impact_by_concept: pd.DataFrame
    outlier_record_count: int
    total_estimated_outlier_impact_amount: float


@dataclass(slots=True)
class MissingPopulationDetectionResult:
    missing_population_exceptions: pd.DataFrame
    missing_population_record_count: int
    total_estimated_missing_population_impact_amount: float


@dataclass(slots=True)
class SignErrorDetectionResult:
    sign_error_exceptions: pd.DataFrame
    sign_error_record_count: int
    total_estimated_sign_error_impact_amount: float


@dataclass(slots=True)
class MisclassifiedConceptDetectionResult:
    misclassified_exceptions: pd.DataFrame
    misclassified_record_count: int


@dataclass(slots=True)
class ReconciliationExceptionItem:
    exception_type: str
    severity: str
    scope_level: str
    record_id: str | None = None
    concept_scope: str | None = None
    employee_id: str | None = None
    estimated_impact_amount: Decimal | None = None
    observation: str | None = None
    confidence: Decimal | None = None


@dataclass(slots=True)
class ExplanationCause:
    exception_type: str
    title: str
    detail: str
    estimated_impact_amount: Decimal | None = None
    evidence_count: int = 0
    confidence: Decimal | None = None


@dataclass(slots=True)
class ConceptExplanation:
    concept_code_normalized: str
    summary_statement: str
    probable_causes: list[ExplanationCause] = field(default_factory=list)
    recommended_action: str | None = None
    explained_amount_estimate: Decimal | None = None
    impacted_records_count: int = 0
    impacted_employees_count: int = 0


@dataclass(slots=True)
class ReconciliationEngineInput:
    payroll: DataFrameLike
    expected_totals: DataFrameLike
    target_period: str
    concept_master: DataFrameLike | None = None
    employee_reference: DataFrameLike | None = None
    legal_entity: str | None = None
    tolerance_profile: ToleranceProfile | None = None


@dataclass(slots=True)
class ReconciliationSummaryRow:
    period: str
    concept_code_normalized: str
    concept_name_normalized: str
    observed_amount: Decimal
    expected_amount: Decimal
    absolute_diff: Decimal
    relative_diff_pct: Decimal | None
    status: str
    record_count: int
    employee_count: int
    invalid_record_count: int
    legal_entity: str | None = None


@dataclass(slots=True)
class ReconciliationDebugArtifacts:
    normalized_payroll: pd.DataFrame | None = None
    observed_totals: pd.DataFrame | None = None
    expected_totals_filtered: pd.DataFrame | None = None
    invalid_data_quality_exceptions: pd.DataFrame | None = None
    out_of_period_exceptions: pd.DataFrame | None = None
    out_of_period_impact_by_concept: pd.DataFrame | None = None
    unmapped_concept_exceptions: pd.DataFrame | None = None
    unmapped_concept_impact_by_raw_concept: pd.DataFrame | None = None
    duplicate_record_exceptions: pd.DataFrame | None = None
    duplicate_record_impact_by_concept: pd.DataFrame | None = None
    missing_expected_total_exceptions: pd.DataFrame | None = None
    outlier_amount_exceptions: pd.DataFrame | None = None
    outlier_amount_impact_by_concept: pd.DataFrame | None = None
    missing_population_exceptions: pd.DataFrame | None = None
    sign_error_exceptions: pd.DataFrame | None = None
    misclassified_concept_exceptions: pd.DataFrame | None = None
    structured_exceptions: list[ReconciliationExceptionItem] = field(default_factory=list)
    exception_impact_summary: pd.DataFrame | None = None
    ranked_exception_causes: pd.DataFrame | None = None
    concept_explanations: list[ConceptExplanation] = field(default_factory=list)
    validation_errors: list[str] = field(default_factory=list)
    validation_warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ReconciliationEngineResult:
    summary_rows: list[ReconciliationSummaryRow]
    run_metrics: dict[str, int] = field(default_factory=dict)
    debug_artifacts: ReconciliationDebugArtifacts = field(
        default_factory=ReconciliationDebugArtifacts,
    )
