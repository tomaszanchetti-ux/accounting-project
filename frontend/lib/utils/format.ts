export function formatCurrency(
  value: boolean | number | string | null | undefined,
  currency = "EUR",
) {
  const numericValue =
    typeof value === "string" ? Number.parseFloat(value) : value ?? 0;

  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency,
    maximumFractionDigits: 2,
  }).format(
    typeof numericValue === "number" && Number.isFinite(numericValue)
      ? numericValue
      : 0,
  );
}

export function formatDateTime(value: string | null | undefined) {
  if (!value) {
    return "Pending";
  }

  const date = new Date(value);

  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export function formatPercentage(
  value: boolean | number | string | null | undefined,
  digits = 2,
) {
  if (value === null || value === undefined || value === "") {
    return "N/A";
  }

  const numericValue =
    typeof value === "string" ? Number.parseFloat(value) : Number(value);
  if (!Number.isFinite(numericValue)) {
    return "N/A";
  }

  return `${numericValue.toFixed(digits)}%`;
}

export function formatCompactNumber(value: number | string | null | undefined) {
  if (value === null || value === undefined || value === "") {
    return "0";
  }

  const numericValue =
    typeof value === "string" ? Number.parseFloat(value) : Number(value);
  if (!Number.isFinite(numericValue)) {
    return "0";
  }

  return new Intl.NumberFormat("en-GB", {
    maximumFractionDigits: 0,
  }).format(numericValue);
}

export function formatFileSize(bytes: number | null | undefined) {
  if (!bytes) {
    return "Unknown size";
  }

  if (bytes < 1024) {
    return `${bytes} B`;
  }

  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }

  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function formatRunStatus(status: string | null | undefined) {
  if (!status) {
    return "Draft";
  }

  return status
    .toLowerCase()
    .split("_")
    .map((chunk) => chunk.charAt(0).toUpperCase() + chunk.slice(1))
    .join(" ");
}
