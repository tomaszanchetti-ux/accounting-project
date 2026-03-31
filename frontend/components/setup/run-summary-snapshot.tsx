import Link from "next/link";

import { MetricCard } from "@/components/ui/metric-card";
import { StatusPill } from "@/components/ui/status-pill";
import type { RunSummaryResponse } from "@/lib/api/client";
import { formatCurrency, formatDateTime, formatRunStatus } from "@/lib/utils/format";

type RunSummarySnapshotProps = {
  summary: RunSummaryResponse;
};

export function RunSummarySnapshot({ summary }: RunSummarySnapshotProps) {
  return (
    <section className="rounded-[24px] border border-border-subtle bg-surface-ink p-5 text-white md:p-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-3">
            <StatusPill tone="success">Run executed</StatusPill>
            <span className="text-sm text-slate-300">
              {formatRunStatus(summary.run.status)}
            </span>
          </div>
          <div className="space-y-2">
            <h3 className="text-2xl font-semibold tracking-[-0.03em]">
              {summary.run.run_label}
            </h3>
            <p className="text-sm leading-6 text-slate-300">
              Completed {formatDateTime(summary.run.completed_at)} with period{" "}
              {summary.run.period}.
            </p>
          </div>
        </div>
        <Link
          className="inline-flex items-center justify-center rounded-full border border-white/15 px-4 py-2 text-sm font-semibold text-white transition hover:bg-white/10"
          href={`/runs/${summary.run.id}`}
        >
          Open results
        </Link>
      </div>

      <div className="mt-6 grid gap-3 md:grid-cols-4">
        <MetricCard
          label="Reconciled"
          value={String(summary.metrics.concepts_reconciled ?? 0)}
        />
        <MetricCard
          label="Minor diff"
          value={String(summary.metrics.concepts_minor_difference ?? 0)}
        />
        <MetricCard
          label="Unreconciled"
          value={String(summary.metrics.concepts_unreconciled ?? 0)}
        />
        <MetricCard
          label="Observed total"
          value={formatCurrency(summary.metrics.observed_amount_total)}
        />
      </div>

      <div className="mt-6 grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
        <div className="overflow-hidden rounded-[20px] border border-white/10">
          <table className="min-w-full divide-y divide-white/10 text-sm">
            <thead className="bg-white/5 text-left text-slate-300">
              <tr>
                <th className="px-4 py-3 font-medium">Concept</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 text-right font-medium">Diff</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/10">
              {summary.preview_results.map((result) => (
                <tr key={result.id}>
                  <td className="px-4 py-3">
                    <div className="space-y-1">
                      <p className="font-medium text-white">
                        {result.concept_name_normalized}
                      </p>
                      <p className="font-mono text-xs text-slate-400">
                        {result.concept_code_normalized}
                      </p>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-slate-300">{result.status}</td>
                  <td className="px-4 py-3 text-right font-mono text-white">
                    {formatCurrency(result.absolute_diff)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="rounded-[20px] border border-white/10 bg-white/5 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
            Recent run events
          </p>
          <div className="mt-4 space-y-4">
            {summary.event_log.map((event) => (
              <div className="border-l border-white/10 pl-4" key={event.event_code}>
                <p className="text-sm font-semibold text-white">{event.title}</p>
                <p className="mt-1 text-sm leading-6 text-slate-300">
                  {event.detail}
                </p>
                <p className="mt-1 text-xs text-slate-400">
                  {formatDateTime(event.event_at)}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
