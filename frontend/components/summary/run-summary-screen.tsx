import Link from "next/link";

import { type RunResultRecord, type RunSummaryResponse } from "@/lib/api/client";
import { formatCurrency, formatDateTime, formatRunStatus } from "@/lib/utils/format";
import { getOverallRunStatusMeta } from "@/lib/utils/reconciliation";

import { ConceptResultsTable } from "@/components/summary/concept-results-table";
import { RunSummaryCards } from "@/components/summary/run-summary-cards";
import { AppHeader } from "@/components/ui/app-header";
import { ExportCsvButton } from "@/components/ui/export-csv-button";
import { HeaderActionPanel } from "@/components/ui/header-action-panel";
import { NoticeBanner } from "@/components/ui/notice-banner";
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
                idleLabel="Export summary CSV"
                variant="primary"
              />
            }
            title="Run Context"
          >
            <div className="flex items-center gap-2">
              <StatusPill tone={overallStatus.tone}>{overallStatus.label}</StatusPill>
              <span className="font-medium text-foreground">
                {formatRunStatus(summary.run.status)}
              </span>
            </div>
            <p className="max-w-xs leading-6">{overallStatus.description}</p>
            <div className="space-y-1 font-mono text-xs text-text-muted">
              <p>{summary.run.id}</p>
              <p>{summary.run.source_file_name ?? "Source file pending"}</p>
              <p>{summary.run.rules_version ?? "rules unavailable"}</p>
            </div>
          </HeaderActionPanel>
        }
        eyebrow="Run Summary"
        kicker={summary.run.run_label}
        subtitle="This screen answers the four executive questions the MVP must solve first: did the run close well, how many concepts reconciled, where the biggest differences sit and how material the open problem still is."
        title="Read the period in one pass, then drill into the concepts that need explanation."
      />

      <section className="grid gap-4 lg:grid-cols-[1.15fr_0.85fr]">
        <article className="rounded-[24px] border border-border-subtle bg-surface-ink p-5 text-white md:p-6">
          <div className="flex flex-wrap items-center gap-3">
            <StatusPill tone={overallStatus.tone}>{overallStatus.label}</StatusPill>
            <span className="text-sm text-slate-300">
              {summary.metrics.total_concepts ?? results.length} concepts reviewed
            </span>
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
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
                File Processed
              </p>
              <p className="text-base leading-7 text-slate-100">
                {summary.run.source_file_name ?? "No source file recorded"}
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
                Observed vs Expected
              </p>
              <p className="text-base leading-7 text-slate-100">
                {formatCurrency(summary.metrics.observed_amount_total)} against{" "}
                {formatCurrency(summary.metrics.expected_amount_total)}
              </p>
            </div>
          </div>
        </article>

        <article className="rounded-[24px] border border-border-subtle bg-white/72 p-5 md:p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            Traceability
          </p>
          <div className="mt-4 space-y-4">
            {summary.event_log.map((event) => (
              <div className="border-l border-border-subtle pl-4" key={event.event_code}>
                <p className="text-sm font-semibold text-foreground">{event.title}</p>
                <p className="mt-1 text-sm leading-6 text-text-secondary">
                  {event.detail}
                </p>
                <p className="mt-1 text-xs text-text-muted">
                  {formatDateTime(event.event_at)}
                </p>
              </div>
            ))}
          </div>
        </article>
      </section>

      <RunSummaryCards metrics={summary.metrics} results={results} />

      <NoticeBanner
        detail="The table is intentionally data-first: status, materiality and explanation preview come before dense controls or filters."
        message="The default summary path is executive first and detail second."
        tone="info"
      />

      <ConceptResultsTable results={results} runId={summary.run.id} />

      <section className="flex flex-wrap items-center justify-between gap-3 rounded-[24px] border border-border-subtle bg-white/70 p-5">
        <div className="space-y-1">
          <p className="text-sm font-semibold text-foreground">
            Ready to continue from explanation into records?
          </p>
          <p className="text-sm leading-6 text-text-secondary">
            Concept Analysis and Drill-down now preserve the same run context,
            traceability framing and export path so the review can move from
            executive view into evidence without losing continuity.
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
