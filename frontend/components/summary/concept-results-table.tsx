import Link from "next/link";

import type { RunResultRecord } from "@/lib/api/client";
import { formatCurrency, formatPercentage } from "@/lib/utils/format";
import { getResultStatusMeta } from "@/lib/utils/reconciliation";

import { StatusPill } from "@/components/ui/status-pill";

type ConceptResultsTableProps = {
  results: RunResultRecord[];
  runId: string;
};

export function ConceptResultsTable({
  results,
  runId,
}: ConceptResultsTableProps) {
  return (
    <section className="overflow-hidden rounded-[24px] border border-border-subtle bg-white/72">
      <div className="flex flex-col gap-3 border-b border-border-subtle px-5 py-5 md:flex-row md:items-end md:justify-between">
        <div className="space-y-2">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            Concepts
          </p>
          <h2 className="text-2xl font-semibold tracking-[-0.03em] text-foreground">
            Open the concepts that still need review.
          </h2>
        </div>
        <p className="max-w-md text-sm leading-6 text-text-secondary">
          The default order pushes unreconciled and high-materiality concepts to the
          top so you can move straight into the details.
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-[1080px] text-sm">
          <colgroup>
            <col className="w-[24%]" />
            <col className="w-[10%]" />
            <col className="w-[10%]" />
            <col className="w-[10%]" />
            <col className="w-[8%]" />
            <col className="w-[10%]" />
            <col className="w-[20%]" />
            <col className="w-[8%]" />
          </colgroup>
          <thead className="border-b border-border-subtle bg-surface-strong/55 text-left text-text-secondary">
            <tr>
              <th className="px-5 py-3.5 font-semibold">Concept</th>
              <th className="px-4 py-3.5 text-right font-semibold">Expected</th>
              <th className="px-4 py-3.5 text-right font-semibold">Observed</th>
              <th className="px-4 py-3.5 text-right font-semibold">Diff</th>
              <th className="px-4 py-3.5 text-right font-semibold">Diff %</th>
              <th className="px-4 py-3.5 font-semibold">Status</th>
              <th className="px-4 py-3.5 font-semibold">Summary</th>
              <th className="px-5 py-3.5 text-right font-semibold">Details</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle">
            {results.map((result) => {
              const statusMeta = getResultStatusMeta(result.status);

              return (
                <tr className="align-top hover:bg-surface/70" key={result.id}>
                  <td className="px-5 py-4.5">
                    <div className="space-y-1">
                      <p className="text-[15px] font-semibold leading-6 text-foreground">
                        {result.concept_name_normalized}
                      </p>
                      <div className="flex flex-wrap items-center gap-2 text-xs text-text-muted">
                        <span className="font-mono">
                          {result.concept_code_normalized}
                        </span>
                        <span>{result.record_count} records</span>
                        <span>{result.employee_count} employees</span>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-4.5 text-right font-mono text-[13px] text-foreground">
                    {formatCurrency(result.expected_amount)}
                  </td>
                  <td className="px-4 py-4.5 text-right font-mono text-[13px] text-foreground">
                    {formatCurrency(result.observed_amount)}
                  </td>
                  <td className="px-4 py-4.5 text-right font-mono text-[13px] text-foreground">
                    {formatCurrency(result.absolute_diff)}
                  </td>
                  <td className="px-4 py-4.5 text-right font-mono text-[13px] text-foreground">
                    {formatPercentage(result.relative_diff_pct)}
                  </td>
                  <td className="px-4 py-4.5">
                    <StatusPill tone={statusMeta.tone}>{statusMeta.label}</StatusPill>
                  </td>
                  <td className="px-4 py-4.5">
                    <p className="max-w-md text-sm leading-6 text-text-secondary">
                      {result.summary_explanation ??
                        "No explanation available for this concept yet."}
                    </p>
                  </td>
                  <td className="px-5 py-4.5 text-right">
                    <Link
                      className="inline-flex items-center justify-center rounded-full border border-border-subtle bg-surface px-4 py-2 text-sm font-semibold text-foreground transition hover:border-surface-ink hover:bg-surface-ink hover:text-white"
                      href={`/runs/${runId}/concepts/${result.id}`}
                    >
                      View details
                    </Link>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}
