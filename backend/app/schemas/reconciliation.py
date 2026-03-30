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
    validation_errors: list[str] = field(default_factory=list)
    validation_warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ReconciliationEngineResult:
    summary_rows: list[ReconciliationSummaryRow]
    run_metrics: dict[str, int] = field(default_factory=dict)
    debug_artifacts: ReconciliationDebugArtifacts = field(
        default_factory=ReconciliationDebugArtifacts,
    )
