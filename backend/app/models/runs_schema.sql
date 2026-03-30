CREATE TABLE IF NOT EXISTS reconciliation_runs (
    id UUID PRIMARY KEY,
    run_label TEXT NOT NULL,
    period TEXT NOT NULL,
    status TEXT NOT NULL,
    overall_status TEXT NULL,
    source_file_name TEXT NULL,
    record_count INTEGER NULL,
    concept_count INTEGER NULL,
    legal_entity_scope TEXT NULL,
    tolerance_profile_label TEXT NULL,
    rules_version TEXT NULL,
    run_metrics JSONB NOT NULL DEFAULT '{}'::jsonb,
    error_message TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ NULL
);

CREATE TABLE IF NOT EXISTS uploaded_files (
    id UUID PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES reconciliation_runs(id) ON DELETE CASCADE,
    file_name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    source_kind TEXT NOT NULL,
    storage_bucket TEXT NULL,
    storage_path TEXT NOT NULL,
    uploaded_at TIMESTAMPTZ NOT NULL,
    UNIQUE (run_id, file_type)
);

CREATE TABLE IF NOT EXISTS expected_totals_used (
    id UUID PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES reconciliation_runs(id) ON DELETE CASCADE,
    period TEXT NOT NULL,
    concept_code_normalized TEXT NOT NULL,
    expected_amount NUMERIC(18, 4) NOT NULL,
    currency TEXT NOT NULL,
    legal_entity TEXT NULL
);

CREATE TABLE IF NOT EXISTS reconciliation_results (
    id UUID PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES reconciliation_runs(id) ON DELETE CASCADE,
    period TEXT NOT NULL,
    concept_code_normalized TEXT NOT NULL,
    concept_name_normalized TEXT NOT NULL,
    observed_amount NUMERIC(18, 4) NOT NULL,
    expected_amount NUMERIC(18, 4) NOT NULL,
    absolute_diff NUMERIC(18, 4) NOT NULL,
    relative_diff_pct NUMERIC(18, 6) NULL,
    status TEXT NOT NULL,
    record_count INTEGER NOT NULL,
    employee_count INTEGER NOT NULL,
    invalid_record_count INTEGER NOT NULL DEFAULT 0,
    legal_entity TEXT NULL,
    summary_explanation TEXT NULL,
    recommended_action TEXT NULL,
    explained_amount_estimate NUMERIC(18, 4) NULL,
    impacted_records_count INTEGER NULL,
    impacted_employees_count INTEGER NULL
);

CREATE TABLE IF NOT EXISTS reconciliation_exceptions (
    id UUID PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES reconciliation_runs(id) ON DELETE CASCADE,
    result_id UUID NULL REFERENCES reconciliation_results(id) ON DELETE SET NULL,
    record_id TEXT NULL,
    employee_id TEXT NULL,
    concept_scope TEXT NULL,
    exception_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    scope_level TEXT NOT NULL,
    estimated_impact_amount NUMERIC(18, 4) NULL,
    observation TEXT NULL,
    confidence NUMERIC(18, 6) NULL,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS run_payroll_lines (
    id UUID PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES reconciliation_runs(id) ON DELETE CASCADE,
    record_id TEXT NOT NULL,
    employee_id TEXT NULL,
    employee_name TEXT NULL,
    legal_entity TEXT NULL,
    country TEXT NULL,
    cost_center TEXT NULL,
    payroll_period TEXT NULL,
    posting_date DATE NULL,
    concept_code_raw TEXT NULL,
    concept_code_normalized TEXT NULL,
    concept_name_raw TEXT NULL,
    concept_name_normalized TEXT NULL,
    amount NUMERIC(18, 4) NULL,
    currency TEXT NULL,
    is_valid BOOLEAN NOT NULL,
    exception_flags JSONB NOT NULL DEFAULT '[]'::jsonb,
    invalid_reasons JSONB NOT NULL DEFAULT '[]'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_uploaded_files_run_id
    ON uploaded_files (run_id);

CREATE INDEX IF NOT EXISTS idx_expected_totals_used_run_id
    ON expected_totals_used (run_id);

CREATE INDEX IF NOT EXISTS idx_reconciliation_results_run_id
    ON reconciliation_results (run_id);

CREATE INDEX IF NOT EXISTS idx_reconciliation_results_run_status
    ON reconciliation_results (run_id, status);

CREATE INDEX IF NOT EXISTS idx_reconciliation_results_run_concept
    ON reconciliation_results (run_id, concept_code_normalized);

CREATE INDEX IF NOT EXISTS idx_reconciliation_exceptions_run_id
    ON reconciliation_exceptions (run_id);

CREATE INDEX IF NOT EXISTS idx_reconciliation_exceptions_result_id
    ON reconciliation_exceptions (result_id);

CREATE INDEX IF NOT EXISTS idx_run_payroll_lines_run_id
    ON run_payroll_lines (run_id);

CREATE INDEX IF NOT EXISTS idx_run_payroll_lines_run_concept
    ON run_payroll_lines (run_id, concept_code_normalized);
