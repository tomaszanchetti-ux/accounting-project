"use client";

import type { RunPayrollLineRecord } from "@/lib/api/client";
import { cx } from "@/lib/utils/cx";
import { formatCurrency } from "@/lib/utils/format";

import { StatusPill } from "@/components/ui/status-pill";

type ExceptionDrilldownTableProps = {
  rows: RunPayrollLineRecord[];
};

function getRowExceptionTone(row: RunPayrollLineRecord) {
  if (row.invalid_reasons.length) {
    return "error" as const;
  }

  if (row.exception_flags.length) {
    return "warning" as const;
  }

  return "success" as const;
}

function getRowObservation(row: RunPayrollLineRecord) {
  if (row.invalid_reasons.length) {
    return row.invalid_reasons.join(" · ");
  }

  if (row.exception_flags.length) {
    return `Detected ${row.exception_flags.length} exception flag${
      row.exception_flags.length > 1 ? "s" : ""
    }.`;
  }

  return "No anomaly persisted for this row.";
}

export function ExceptionDrilldownTable({
  rows,
}: ExceptionDrilldownTableProps) {
  return (
    <div className="overflow-hidden rounded-[24px] border border-border-subtle bg-white/78">
      <div className="overflow-x-auto">
        <table className="min-w-full border-collapse">
          <thead className="bg-surface-strong/70">
            <tr className="text-left text-xs font-semibold uppercase tracking-[0.14em] text-text-muted">
              <th className="px-4 py-4">Record ID</th>
              <th className="px-4 py-4">Employee</th>
              <th className="px-4 py-4">Legal Entity</th>
              <th className="px-4 py-4">Concept</th>
              <th className="px-4 py-4 text-right">Amount</th>
              <th className="px-4 py-4">Period</th>
              <th className="px-4 py-4">Exception Type</th>
              <th className="px-4 py-4">Observation</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => {
              const tone = getRowExceptionTone(row);
              const anomalyLabels = row.invalid_reasons.length
                ? row.invalid_reasons
                : row.exception_flags;

              return (
                <tr
                  className={cx(
                    "align-top border-t border-border-subtle/80",
                    tone === "error" && "bg-status-unreconciled/4",
                    tone === "warning" && "bg-status-minor-difference/5",
                  )}
                  key={row.id}
                >
                  <td className="px-4 py-4 font-mono text-xs text-foreground">
                    {row.record_id}
                  </td>
                  <td className="px-4 py-4">
                    <div className="space-y-1">
                      <p className="text-sm font-semibold text-foreground">
                        {row.employee_name ?? "Employee unavailable"}
                      </p>
                      <p className="text-xs text-text-secondary">
                        {row.employee_id ?? "No employee id"}
                      </p>
                    </div>
                  </td>
                  <td className="px-4 py-4 text-sm text-text-secondary">
                    {row.legal_entity ?? "Mixed scope"}
                  </td>
                  <td className="px-4 py-4">
                    <div className="space-y-1">
                      <p className="text-sm font-semibold text-foreground">
                        {row.concept_name_normalized ?? "Unknown concept"}
                      </p>
                      <p className="text-xs text-text-secondary">
                        {row.concept_code_normalized ?? "No concept code"}
                      </p>
                    </div>
                  </td>
                  <td className="px-4 py-4 text-right text-sm font-semibold text-foreground">
                    {formatCurrency(row.amount, row.currency ?? "EUR")}
                  </td>
                  <td className="px-4 py-4 text-sm text-text-secondary">
                    {row.payroll_period ?? "Period unavailable"}
                  </td>
                  <td className="px-4 py-4">
                    <div className="flex max-w-xs flex-wrap gap-2">
                      {anomalyLabels.length ? (
                        anomalyLabels.map((anomalyLabel) => (
                          <StatusPill key={`${row.id}-${anomalyLabel}`} tone={tone}>
                            {anomalyLabel}
                          </StatusPill>
                        ))
                      ) : (
                        <StatusPill tone="success">Clear</StatusPill>
                      )}
                    </div>
                  </td>
                  <td className="px-4 py-4 text-sm leading-6 text-text-secondary">
                    {getRowObservation(row)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
