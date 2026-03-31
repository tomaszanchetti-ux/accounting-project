import type { ExpectedTotalsPreviewRow } from "@/lib/utils/csv";
import { formatCurrency } from "@/lib/utils/format";

type ExpectedTotalsPreviewProps = {
  isLoading?: boolean;
  onAmountChange?: (conceptCode: string, nextAmount: string) => void;
  onResetToSeed?: () => void;
  rows: ExpectedTotalsPreviewRow[];
  sourceLabel: string;
};

export function ExpectedTotalsPreview({
  isLoading,
  onAmountChange,
  onResetToSeed,
  rows,
  sourceLabel,
}: ExpectedTotalsPreviewProps) {
  const isEditable = Boolean(onAmountChange);

  return (
    <section className="rounded-[24px] border border-border-subtle bg-white/70 p-5">
      <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div className="space-y-1">
          <h3 className="text-xl font-semibold text-foreground">
            Expected totals
          </h3>
          <p className="text-sm leading-6 text-text-secondary">
            {isEditable
              ? "Enter the reference amount for each concept. The values start prefilled from the demo seed and can be edited manually."
              : "Quick verification of the reference amounts that will be used during reconciliation."}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <p className="text-sm font-medium text-text-secondary">{sourceLabel}</p>
          {onResetToSeed ? (
            <button
              className="inline-flex items-center justify-center rounded-full border border-border-subtle px-4 py-2 text-sm font-semibold text-foreground transition hover:bg-surface"
              onClick={onResetToSeed}
              type="button"
            >
              Reset seed values
            </button>
          ) : null}
        </div>
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
              rows.map((row) => (
                <tr key={`${row.payrollPeriod}-${row.conceptCode}`}>
                  <td className="px-4 py-3 font-medium text-foreground">
                    {row.conceptCode}
                  </td>
                  <td className="px-4 py-3 text-text-secondary">
                    {row.payrollPeriod}
                  </td>
                  <td className="px-4 py-3 text-right font-mono text-foreground">
                    {isEditable ? (
                      <div className="flex items-center justify-end gap-2">
                        <span className="text-xs text-text-muted">{row.currency}</span>
                        <input
                          className="w-32 rounded-xl border border-border-subtle bg-surface px-3 py-2 text-right font-mono text-sm text-foreground outline-none transition focus:border-surface-ink"
                          inputMode="decimal"
                          onChange={(event) =>
                            onAmountChange?.(row.conceptCode, event.target.value)
                          }
                          value={Number.isFinite(row.expectedAmount) ? row.expectedAmount : 0}
                        />
                      </div>
                    ) : (
                      formatCurrency(row.expectedAmount, row.currency)
                    )}
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
