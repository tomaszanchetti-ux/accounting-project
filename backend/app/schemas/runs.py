from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

RunStatus = Literal[
    "DRAFT",
    "INPUT_VALIDATED",
    "PROCESSING",
    "RECONCILED",
    "RECONCILED_WITH_EXCEPTIONS",
    "FAILED",
    "INVALID_INPUT",
]
OverallRunStatus = Literal[
    "reconciled",
    "minor_difference",
    "unreconciled",
    "invalid_incomplete",
]
UploadedFileType = Literal[
    "payroll",
    "expected_totals",
    "concept_master",
    "employee_reference",
]
FileSourceKind = Literal["local_path", "supabase_storage"]
MetricValue = str | int | float | bool | None


class RunRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    run_label: str
    period: str
    status: RunStatus
    overall_status: str | None = None
    source_file_name: str | None = None
    record_count: int | None = None
    concept_count: int | None = None
    legal_entity_scope: str | None = None
    tolerance_profile_label: str | None = None
    rules_version: str | None = None
    run_metrics: dict[str, MetricValue] = Field(default_factory=dict)
    error_message: str | None = None
    created_at: datetime
    completed_at: datetime | None = None


class UploadedFileRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    run_id: str
    file_name: str
    file_type: UploadedFileType
    source_kind: FileSourceKind
    storage_bucket: str | None = None
    storage_path: str
    uploaded_at: datetime


class ExpectedTotalUsedRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    run_id: str
    period: str
    concept_code_normalized: str
    expected_amount: Decimal
    currency: str
    legal_entity: str | None = None


class RunResultRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    run_id: str
    period: str
    concept_code_normalized: str
    concept_name_normalized: str
    observed_amount: Decimal
    expected_amount: Decimal
    absolute_diff: Decimal
    relative_diff_pct: Decimal | None = None
    status: str
    record_count: int
    employee_count: int
    invalid_record_count: int = 0
    legal_entity: str | None = None
    summary_explanation: str | None = None
    recommended_action: str | None = None
    explained_amount_estimate: Decimal | None = None
    impacted_records_count: int | None = None
    impacted_employees_count: int | None = None


class RunExceptionRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    run_id: str
    result_id: str | None = None
    record_id: str | None = None
    employee_id: str | None = None
    concept_scope: str | None = None
    exception_type: str
    severity: str
    scope_level: str
    estimated_impact_amount: Decimal | None = None
    observation: str | None = None
    confidence: Decimal | None = None
    created_at: datetime


class RunPayrollLineRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    run_id: str
    record_id: str
    employee_id: str | None = None
    employee_name: str | None = None
    legal_entity: str | None = None
    country: str | None = None
    cost_center: str | None = None
    payroll_period: str | None = None
    posting_date: date | None = None
    concept_code_raw: str | None = None
    concept_code_normalized: str | None = None
    concept_name_raw: str | None = None
    concept_name_normalized: str | None = None
    amount: Decimal | None = None
    currency: str | None = None
    is_valid: bool
    exception_flags: list[str] = Field(default_factory=list)
    invalid_reasons: list[str] = Field(default_factory=list)


class RunCreateRequest(BaseModel):
    run_label: str
    period: str
    legal_entity_scope: str | None = None
    tolerance_profile_label: str = "mvp-default"
    rules_version: str = "engine-v1"


class RunFileReferenceRequest(BaseModel):
    file_name: str
    file_type: UploadedFileType
    storage_path: str
    source_kind: FileSourceKind = "local_path"
    storage_bucket: str | None = None


class RunExecuteRequest(BaseModel):
    force_recompute: bool = True


class RunResponse(BaseModel):
    run: RunRecord


class UploadedFileResponse(BaseModel):
    uploaded_file: UploadedFileRecord


class RunExecuteResponse(BaseModel):
    run: RunRecord
    message: str


class RunEventRecord(BaseModel):
    event_code: str
    title: str
    detail: str
    event_at: datetime | None = None
    status_snapshot: str | None = None


class RunSummaryResponse(BaseModel):
    run: RunRecord
    metrics: dict[str, MetricValue] = Field(default_factory=dict)
    preview_results: list[RunResultRecord] = Field(default_factory=list)
    event_log: list[RunEventRecord] = Field(default_factory=list)


class ConceptAnalysisHeader(BaseModel):
    concept_code_normalized: str
    concept_name_normalized: str
    period: str
    status: str


class ConceptAnalysisKpis(BaseModel):
    observed_amount: Decimal
    expected_amount: Decimal
    absolute_diff: Decimal
    relative_diff_pct: Decimal | None = None
    record_count: int
    employee_count: int
    impacted_records_count: int | None = None
    impacted_employees_count: int | None = None
    explained_amount_estimate: Decimal | None = None


class ConceptAnalysisEvidenceSummary(BaseModel):
    total_exceptions: int
    top_exception_types: list[str] = Field(default_factory=list)
    records_with_exception: int = 0
    employees_with_exception: int = 0


class ConceptAnalysisPayload(BaseModel):
    header: ConceptAnalysisHeader
    kpis: ConceptAnalysisKpis
    summary_statement: str | None = None
    top_causes: list[RunExceptionRecord] = Field(default_factory=list)
    recommended_action: str | None = None
    evidence_summary: ConceptAnalysisEvidenceSummary


class RunResultsResponse(BaseModel):
    run: RunRecord
    total_results: int
    results: list[RunResultRecord]


class RunResultDetailResponse(BaseModel):
    run: RunRecord
    result: RunResultRecord
    exceptions: list[RunExceptionRecord] = Field(default_factory=list)
    concept_analysis: ConceptAnalysisPayload
    event_log: list[RunEventRecord] = Field(default_factory=list)


class DrilldownSummary(BaseModel):
    concept_code_normalized: str
    total_rows: int
    total_amount: Decimal | None = None
    rows_with_exception: int = 0
    exception_types_present: list[str] = Field(default_factory=list)


class DrilldownFilterContext(BaseModel):
    available_exception_types: list[str] = Field(default_factory=list)
    legal_entities: list[str] = Field(default_factory=list)
    countries: list[str] = Field(default_factory=list)


class RunDrilldownResponse(BaseModel):
    run: RunRecord
    result: RunResultRecord
    total_rows: int
    summary: DrilldownSummary
    filter_context: DrilldownFilterContext
    rows: list[RunPayrollLineRecord] = Field(default_factory=list)
    event_log: list[RunEventRecord] = Field(default_factory=list)
