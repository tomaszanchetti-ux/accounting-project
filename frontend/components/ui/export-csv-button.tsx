"use client";

import { useState } from "react";

import { downloadApiFile } from "@/lib/api/client";
import { cx } from "@/lib/utils/cx";

type ExportCsvButtonProps = {
  fallbackFileName: string;
  href: string;
  idleLabel: string;
  variant?: "primary" | "secondary";
};

const buttonStyles = {
  primary: "bg-surface-ink text-white hover:bg-slate-800",
  secondary:
    "border border-border-subtle bg-surface text-foreground hover:border-surface-ink hover:bg-surface-ink hover:text-white",
} as const;

export function ExportCsvButton({
  fallbackFileName,
  href,
  idleLabel,
  variant = "secondary",
}: ExportCsvButtonProps) {
  const [isDownloading, setIsDownloading] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [statusTone, setStatusTone] = useState<"error" | "info">("info");

  async function handleDownload() {
    if (isDownloading) {
      return;
    }

    setIsDownloading(true);
    setStatusMessage(null);

    try {
      const { blob, filename } = await downloadApiFile(href, fallbackFileName);
      const objectUrl = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = objectUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(objectUrl);

      setStatusTone("info");
      setStatusMessage(`Downloaded ${filename}`);
    } catch (error) {
      setStatusTone("error");
      setStatusMessage(
        error instanceof Error ? error.message : "Export failed.",
      );
    } finally {
      setIsDownloading(false);
    }
  }

  return (
    <div className="space-y-1">
      <button
        className={cx(
          "inline-flex items-center justify-center rounded-full px-4 py-2 text-sm font-semibold transition disabled:cursor-not-allowed disabled:bg-slate-300 disabled:text-slate-600",
          buttonStyles[variant],
        )}
        onClick={handleDownload}
        type="button"
      >
        {isDownloading ? "Exporting..." : idleLabel}
      </button>
      {statusMessage ? (
        <p
          className={cx(
            "max-w-xs text-xs leading-5",
            statusTone === "error" ? "text-status-unreconciled" : "text-text-muted",
          )}
        >
          {statusMessage}
        </p>
      ) : null}
    </div>
  );
}
