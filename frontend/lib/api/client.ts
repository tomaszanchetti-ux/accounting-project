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

export async function fetchApi<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
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

