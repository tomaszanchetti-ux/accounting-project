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

export type RunSummaryResponse = {
  event_log: RunEventRecord[];
  metrics: Record<string, string | number | boolean | null>;
  preview_results: RunResultRecord[];
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
    throw new Error(await extractApiError(response));
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
