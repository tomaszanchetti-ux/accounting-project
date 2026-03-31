import Link from "next/link";

import { type RunResultRecord, type RunSummaryResponse } from "@/lib/api/client";
import { formatCurrency, formatDateTime, formatRunStatus } from "@/lib/utils/format";
import { getOverallRunStatusMeta } from "@/lib/utils/reconciliation";

import { ConceptResultsTable } from "@/components/summary/concept-results-table";
import { RunSummaryCards } from "@/components/summary/run-summary-cards";
import { AppHeader } from "@/components/ui/app-header";
import { ExportCsvButton } from "@/components/ui/export-csv-button";
import { HeaderActionPanel } from "@/components/ui/header-action-panel";
import { StatusPill } from "@/components/ui/status-pill";

type RunSummaryScreenProps = {
  results: RunResultRecord[];
  summary: RunSummaryResponse;
};

export function RunSummaryScreen({
  results,
  summary,
}: RunSummaryScreenProps) {
  const overallStatus = getOverallRunStatusMeta(summary.metrics.overall_run_status);

  return (
    <div className="space-y-6">
      <AppHeader
        actions={
          <HeaderActionPanel
            actions={
              <ExportCsvButton
                fallbackFileName={`reconciliation-summary-${summary.run.period}.csv`}
                href={`/runs/${summary.run.id}/exports/summary`}
                idleLabel="Export summary"
                variant="primary"
              />
            }
            title="Results"
          >
            <div className="flex items-center gap-2">
              <StatusPill tone={overallStatus.tone}>{overallStatus.label}</StatusPill>
              <span className="font-medium text-foreground">
                {formatRunStatus(summary.run.status)}
              </span>
            </div>
            <p className="max-w-xs leading-6">{overallStatus.description}</p>
          </HeaderActionPanel>
        }
        eyebrow="Run Summary"
        kicker={summary.run.run_label}
        subtitle="Review the status of the run, scan the main differences and open the concepts that need attention."
        title="Results at a glance."
      />

      <section className="rounded-[24px] border border-border-subtle bg-surface-ink p-5 text-white md:p-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-3">
            <StatusPill tone={overallStatus.tone}>{overallStatus.label}</StatusPill>
            <span className="text-sm text-slate-300">
              {summary.metrics.total_concepts ?? results.length} concepts reviewed
            </span>
          </div>
          <p className="text-sm text-slate-300">
            File: {summary.run.source_file_name ?? "No source file recorded"}
          </p>
        </div>
        <div className="mt-4 grid gap-4 md:grid-cols-4">
          <div className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
              Period
            </p>
            <p className="text-2xl font-semibold tracking-[-0.03em]">
              {summary.run.period}
            </p>
          </div>
          <div className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
              Completed At
            </p>
            <p className="text-base leading-7 text-slate-100">
              {formatDateTime(summary.run.completed_at)}
            </p>
          </div>
          <div className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
              Observed
            </p>
            <p className="text-base leading-7 text-slate-100">
              {formatCurrency(summary.metrics.observed_amount_total)}
            </p>
          </div>
          <div className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
              Expected
            </p>
            <p className="text-base leading-7 text-slate-100">
              {formatCurrency(summary.metrics.expected_amount_total)}
            </p>
          </div>
        </div>
      </section>

      <RunSummaryCards metrics={summary.metrics} results={results} />
      <ConceptResultsTable results={results} runId={summary.run.id} />

      <section className="flex flex-wrap items-center justify-between gap-3 rounded-[24px] border border-border-subtle bg-white/70 p-5">
        <div className="space-y-1">
          <p className="text-sm font-semibold text-foreground">
            Need to review a concept in detail?
          </p>
          <p className="text-sm leading-6 text-text-secondary">
            Open any row from the summary table to continue into the detailed review flow.
          </p>
        </div>
        <Link
          className="inline-flex items-center justify-center rounded-full bg-surface-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
          href="/"
        >
          Back to setup
        </Link>
      </section>
    </div>
  );
}
