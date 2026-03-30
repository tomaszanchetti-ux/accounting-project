import type { RunResultRecord } from "@/lib/api/client";

export type StatusTone = "error" | "incomplete" | "success" | "warning";

type ResultStatusMeta = {
  label: string;
  priority: number;
  tone: StatusTone;
};

const resultStatusMetaMap: Record<string, ResultStatusMeta> = {
  "Invalid / Incomplete": {
    label: "Invalid / Incomplete",
    priority: 0,
    tone: "incomplete",
  },
  "Minor Difference": {
    label: "Minor Difference",
    priority: 2,
    tone: "warning",
  },
  Reconciled: {
    label: "Reconciled",
    priority: 3,
    tone: "success",
  },
  Unreconciled: {
    label: "Unreconciled",
    priority: 1,
    tone: "error",
  },
};

const overallRunStatusMetaMap: Record<
  string,
  { description: string; label: string; tone: StatusTone }
> = {
  invalid_incomplete: {
    description:
      "The run could not be fully trusted because one or more inputs or concept results were incomplete.",
    label: "Invalid Input",
    tone: "incomplete",
  },
  minor_difference: {
    description:
      "Most concepts reconciled, but the run still contains explainable differences worth reviewing.",
    label: "Reconciled with Exceptions",
    tone: "warning",
  },
  reconciled: {
    description:
      "The run closed cleanly with the expected totals aligned at concept level.",
    label: "Reconciled",
    tone: "success",
  },
  unreconciled: {
    description:
      "Material differences remain open and should be reviewed before closing the period.",
    label: "Attention Required",
    tone: "error",
  },
};

export function getResultStatusMeta(status: string | null | undefined): ResultStatusMeta {
  if (!status) {
    return {
      label: "Unknown",
      priority: 4,
      tone: "incomplete",
    };
  }

  return (
    resultStatusMetaMap[status] ?? {
      label: status,
      priority: 4,
      tone: "incomplete",
    }
  );
}

export function getOverallRunStatusMeta(status: string | null | undefined) {
  if (!status) {
    return {
      description:
        "The run is available, but its business status is not currently defined in the payload.",
      label: "Status unavailable",
      tone: "incomplete" as const,
    };
  }

  return (
    overallRunStatusMetaMap[status] ?? {
      description:
        "The run completed, but the current status mapping has not been documented in the UI yet.",
      label: status,
      tone: "incomplete" as const,
    }
  );
}

export function sortResultsForSummary(results: RunResultRecord[]) {
  return [...results].sort((left, right) => {
    const leftMeta = getResultStatusMeta(left.status);
    const rightMeta = getResultStatusMeta(right.status);
    if (leftMeta.priority !== rightMeta.priority) {
      return leftMeta.priority - rightMeta.priority;
    }

    const rightDiff = Math.abs(Number.parseFloat(right.absolute_diff) || 0);
    const leftDiff = Math.abs(Number.parseFloat(left.absolute_diff) || 0);
    if (rightDiff !== leftDiff) {
      return rightDiff - leftDiff;
    }

    return left.concept_code_normalized.localeCompare(right.concept_code_normalized);
  });
}
