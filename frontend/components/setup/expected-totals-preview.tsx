import type { ExpectedTotalsPreviewRow } from "@/lib/utils/csv";
import { formatCurrency } from "@/lib/utils/format";

type ExpectedTotalsPreviewProps = {
  isLoading?: boolean;
  rows: ExpectedTotalsPreviewRow[];
  sourceLabel: string;
};

export function ExpectedTotalsPreview({
  isLoading,
  rows,
  sourceLabel,
}: ExpectedTotalsPreviewProps) {
  return (
    <section className="rounded-[24px] border border-border-subtle bg-white/70 p-5">
      <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div className="space-y-1">
          <h3 className="text-xl font-semibold text-foreground">
            Reference totals preview
          </h3>
          <p className="text-sm leading-6 text-text-secondary">
            Quick verification of the reference amounts that will be used during
            reconciliation.
          </p>
        </div>
        <p className="text-sm font-medium text-text-secondary">{sourceLabel}</p>
      </div>

      <div className="mt-5 overflow-hidden rounded-[18px] border border-border-subtle">
        <table className="min-w-full divide-y divide-border-subtle text-sm">
          <thead className="bg-surface text-left text-text-secondary">
            <tr>
              <th className="px-4 py-3 font-medium">Concept</th>
              <th className="px-4 py-3 font-medium">Period</th>
              <th className="px-4 py-3 text-right font-medium">Expected amount</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle bg-white/70">
            {isLoading ? (
              <tr>
                <td className="px-4 py-5 text-text-secondary" colSpan={3}>
                  Loading expected totals preview...
                </td>
              </tr>
            ) : rows.length === 0 ? (
              <tr>
                <td className="px-4 py-5 text-text-secondary" colSpan={3}>
                  No reference totals available yet.
                </td>
              </tr>
            ) : (
              rows.slice(0, 8).map((row) => (
                <tr key={`${row.payrollPeriod}-${row.conceptCode}`}>
                  <td className="px-4 py-3 font-medium text-foreground">
                    {row.conceptCode}
                  </td>
                  <td className="px-4 py-3 text-text-secondary">
                    {row.payrollPeriod}
                  </td>
                  <td className="px-4 py-3 text-right font-mono text-foreground">
                    {formatCurrency(row.expectedAmount, row.currency)}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
