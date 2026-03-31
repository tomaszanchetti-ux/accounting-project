"use client";

import { useId } from "react";

import { StatusPill } from "@/components/ui/status-pill";
import { cx } from "@/lib/utils/cx";
import { formatFileSize } from "@/lib/utils/format";

export type UploadBoxState = {
  fileName?: string;
  helperText?: string;
  metadata?: string;
  sizeBytes?: number;
  status: "error" | "loading" | "pending" | "uploaded";
};

type UploadBoxProps = {
  accept?: string;
  ctaLabel: string;
  description: string;
  disabled?: boolean;
  onFileSelected?: (file: File) => void;
  secondaryAction?: React.ReactNode;
  state: UploadBoxState;
  title: string;
};

const toneByStatus = {
  error: "error",
  loading: "executing",
  pending: "pending",
  uploaded: "ready",
} as const;

const labelByStatus = {
  error: "Error",
  loading: "Uploading",
  pending: "Pending",
  uploaded: "Ready",
} as const;

export function UploadBox({
  accept = ".csv,text/csv",
  ctaLabel,
  description,
  disabled,
  onFileSelected,
  secondaryAction,
  state,
  title,
}: UploadBoxProps) {
  const inputId = useId();

  return (
    <section
      className={cx(
        "rounded-[22px] border p-5 transition-colors",
        state.status === "uploaded"
          ? "border-status-reconciled/25 bg-status-reconciled/5"
          : "border-border-subtle bg-white/70",
      )}
    >
      <div className="flex flex-col gap-4">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="space-y-2">
            <h3 className="text-lg font-semibold text-foreground">{title}</h3>
            <p className="max-w-xl text-sm leading-6 text-text-secondary">
              {description}
            </p>
          </div>
          <StatusPill tone={toneByStatus[state.status]}>
            {labelByStatus[state.status]}
          </StatusPill>
        </div>

        <div className="rounded-[18px] border border-dashed border-border-subtle bg-surface px-4 py-5">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div className="space-y-1">
              <p className="text-sm font-medium text-foreground">
                {state.fileName ?? "No file selected yet"}
              </p>
              <p className="text-sm text-text-secondary">
                {state.helperText ?? "Upload a CSV file to continue."}
              </p>
              {state.metadata ? (
                <p className="font-mono text-xs text-text-muted">
                  {state.metadata}
                  {state.sizeBytes ? ` • ${formatFileSize(state.sizeBytes)}` : ""}
                </p>
              ) : null}
            </div>
            {onFileSelected ? (
              <div className="flex flex-wrap gap-3">
                <label
                  className={cx(
                    "inline-flex cursor-pointer items-center justify-center rounded-full px-4 py-2 text-sm font-semibold transition",
                    disabled
                      ? "cursor-not-allowed bg-slate-300 text-slate-600"
                      : "bg-surface-ink text-white hover:bg-slate-800",
                  )}
                  htmlFor={inputId}
                >
                  {ctaLabel}
                </label>
                <input
                  accept={accept}
                  className="sr-only"
                  disabled={disabled}
                  id={inputId}
                  onChange={(event) => {
                    const selectedFile = event.target.files?.[0];
                    if (selectedFile) {
                      onFileSelected(selectedFile);
                    }
                    event.currentTarget.value = "";
                  }}
                  type="file"
                />
                {secondaryAction}
              </div>
            ) : (
              secondaryAction
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
