const defaultApiBaseUrl = "http://localhost:8000";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? defaultApiBaseUrl;

export type BackendHealthStatus = {
  apiBaseUrl: string;
  details?: unknown;
  ok: boolean;
  status: "reachable" | "unreachable";
  summary: string;
};

export type RunStatus =
  | "DRAFT"
  | "INPUT_VALIDATED"
  | "PROCESSING"
  | "RECONCILED"
  | "RECONCILED_WITH_EXCEPTIONS"
  | "FAILED"
  | "INVALID_INPUT";

export type UploadedFileType =
  | "payroll"
  | "expected_totals"
  | "concept_master"
  | "employee_reference";

export type FileSourceKind = "local_path" | "supabase_storage";

export type RunRecord = {
  completed_at: string | null;
  concept_count: number | null;
  created_at: string;
  error_message: string | null;
  id: string;
  legal_entity_scope: string | null;
  overall_status: string | null;
  period: string;
  record_count: number | null;
  rules_version: string | null;
  run_label: string;
  run_metrics: Record<string, string | number | boolean | null>;
  source_file_name: string | null;
  status: RunStatus;
  tolerance_profile_label: string | null;
};

export type UploadedFileRecord = {
  file_name: string;
  file_type: UploadedFileType;
  id: string;
  run_id: string;
  source_kind: FileSourceKind;
  storage_bucket: string | null;
  storage_path: string;
  uploaded_at: string;
};

export type RunResultRecord = {
  absolute_diff: string;
  concept_code_normalized: string;
  concept_name_normalized: string;
  employee_count: number;
  expected_amount: string;
  id: string;
  impacted_employees_count: number | null;
  impacted_records_count: number | null;
  legal_entity: string | null;
  observed_amount: string;
  period: string;
  record_count: number;
  recommended_action?: string | null;
  relative_diff_pct: string | null;
  status: string;
  summary_explanation: string | null;
};

export type RunEventRecord = {
  detail: string;
  event_at: string | null;
  event_code: string;
  status_snapshot: string | null;
  title: string;
};

export type RunSummaryMetrics = {
  concepts_invalid_incomplete?: number | null;
  concepts_minor_difference?: number | null;
  concepts_reconciled?: number | null;
  concepts_unreconciled?: number | null;
  expected_amount_total?: number | string | null;
  observed_amount_total?: number | string | null;
  overall_run_status?: string | null;
  total_concepts?: number | null;
};

export type RunSummaryResponse = {
  event_log: RunEventRecord[];
  metrics: RunSummaryMetrics;
  preview_results: RunResultRecord[];
  run: RunRecord;
};

export type RunResultsResponse = {
  results: RunResultRecord[];
  run: RunRecord;
  total_results: number;
};

export type RunExceptionRecord = {
  concept_scope: string | null;
  confidence: string | null;
  created_at: string;
  employee_id: string | null;
  estimated_impact_amount: string | null;
  exception_type: string;
  id: string;
  observation: string | null;
  record_id: string | null;
  result_id: string | null;
  run_id: string;
  scope_level: string;
  severity: string;
};

export type ConceptAnalysisHeader = {
  concept_code_normalized: string;
  concept_name_normalized: string;
  period: string;
  status: string;
};

export type ConceptAnalysisKpis = {
  absolute_diff: string;
  employee_count: number;
  expected_amount: string;
  explained_amount_estimate: string | null;
  impacted_employees_count: number | null;
  impacted_records_count: number | null;
  observed_amount: string;
  record_count: number;
  relative_diff_pct: string | null;
};

export type ConceptAnalysisEvidenceSummary = {
  employees_with_exception: number;
  records_with_exception: number;
  top_exception_types: string[];
  total_exceptions: number;
};

export type ConceptAnalysisPayload = {
  evidence_summary: ConceptAnalysisEvidenceSummary;
  header: ConceptAnalysisHeader;
  kpis: ConceptAnalysisKpis;
  recommended_action: string | null;
  summary_statement: string | null;
  top_causes: RunExceptionRecord[];
};

export type RunResultDetailResponse = {
  concept_analysis: ConceptAnalysisPayload;
  event_log: RunEventRecord[];
  exceptions: RunExceptionRecord[];
  result: RunResultRecord;
  run: RunRecord;
};

export type RunCreatePayload = {
  legal_entity_scope?: string;
  period: string;
  rules_version?: string;
  run_label: string;
  tolerance_profile_label?: string;
};

export type FileReferencePayload = {
  file_name: string;
  file_type: UploadedFileType;
  source_kind?: FileSourceKind;
  storage_bucket?: string | null;
  storage_path: string;
};

type ApiErrorPayload = {
  detail?: string;
};

type RunResponse = {
  run: RunRecord;
};

type UploadedFileResponse = {
  uploaded_file: UploadedFileRecord;
};

type RunExecuteResponse = {
  message: string;
  run: RunRecord;
};

export class ApiRequestError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiRequestError";
    this.status = status;
  }
}

async function extractApiError(response: Response) {
  try {
    const payload = (await response.json()) as ApiErrorPayload;
    return payload.detail ?? `API request failed with status ${response.status}`;
  } catch {
    return `API request failed with status ${response.status}`;
  }
}

export async function fetchApi<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    cache: "no-store",
  });

  if (!response.ok) {
    throw new ApiRequestError(await extractApiError(response), response.status);
  }

  return (await response.json()) as T;
}

export async function getBackendHealth(): Promise<BackendHealthStatus> {
  try {
    const details = await fetchApi<unknown>("/health");

    return {
      apiBaseUrl: API_BASE_URL,
      details,
      ok: true,
      status: "reachable",
      summary: "Backend reachable desde el frontend.",
    };
  } catch {
    return {
      apiBaseUrl: API_BASE_URL,
      ok: false,
      status: "unreachable",
      summary:
        "Backend aun no disponible. El frontend ya esta listo para conectarse cuando exista /health.",
    };
  }
}

export function createRun(payload: RunCreatePayload) {
  return fetchApi<RunResponse>("/runs", {
    body: JSON.stringify(payload),
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
  });
}

export function registerRunFileReference(
  runId: string,
  payload: FileReferencePayload,
) {
  return fetchApi<UploadedFileResponse>(`/runs/${runId}/upload`, {
    body: JSON.stringify(payload),
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
  });
}

export function uploadRunFile(
  runId: string,
  fileType: UploadedFileType,
  file: File,
) {
  const formData = new FormData();
  formData.set("file", file);
  formData.set("file_type", fileType);

  return fetchApi<UploadedFileResponse>(`/runs/${runId}/upload`, {
    body: formData,
    method: "POST",
  });
}

export function executeRun(runId: string) {
  return fetchApi<RunExecuteResponse>(`/runs/${runId}/execute`, {
    body: JSON.stringify({ force_recompute: true }),
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
  });
}

export function getRunSummary(runId: string) {
  return fetchApi<RunSummaryResponse>(`/runs/${runId}/summary`);
}

export function getRunResults(runId: string) {
  return fetchApi<RunResultsResponse>(`/runs/${runId}/results`);
}

export function getRunResultDetail(runId: string, resultId: string) {
  return fetchApi<RunResultDetailResponse>(`/runs/${runId}/results/${resultId}`);
}
