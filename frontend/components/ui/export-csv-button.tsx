"use client";

import { ExportFileButton } from "@/components/ui/export-file-button";

type ExportCsvButtonProps = {
  fallbackFileName: string;
  href: string;
  idleLabel: string;
  variant?: "primary" | "secondary";
};

export function ExportCsvButton(props: ExportCsvButtonProps) {
  return <ExportFileButton {...props} />;
}
