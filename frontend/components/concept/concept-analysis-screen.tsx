import Link from "next/link";

import { type RunResultDetailResponse } from "@/lib/api/client";
import {
  formatCompactNumber,
  formatCurrency,
  formatDateTime,
  formatPercentage,
} from "@/lib/utils/format";
import { getResultStatusMeta } from "@/lib/utils/reconciliation";

import { AppHeader } from "@/components/ui/app-header";
import { ExportCsvButton } from "@/components/ui/export-csv-button";
import { HeaderActionPanel } from "@/components/ui/header-action-panel";
import { MetricCard } from "@/components/ui/metric-card";
import { NoticeBanner } from "@/components/ui/notice-banner";
import { StatusPill } from "@/components/ui/status-pill";

type ConceptAnalysisScreenProps = {
  detail: RunResultDetailResponse;
};

export function ConceptAnalysisScreen({ detail }: ConceptAnalysisScreenProps) {
  const statusMeta = getResultStatusMeta(detail.concept_analysis.header.status);
  const topCause = detail.concept_analysis.top_causes[0];

  return (
    <div className="space-y-6">
      <AppHeader
        actions={
          <HeaderActionPanel
            actions={
              <>
                <ExportCsvButton
                  fallbackFileName={`exception-detail-${detail.concept_analysis.header.concept_code_normalized.toLowerCase()}-${detail.run.period}.csv`}
                  href={`/runs/${detail.run.id}/results/${detail.result.id}/exports/detail`}
                  idleLabel="Export detail CSV"
                />
                <Link
                  className="inline-flex items-center justify-center rounded-full border border-border-subtle bg-white px-4 py-2 text-sm font-semibold text-foreground transition hover:border-surface-ink hover:bg-surface-ink hover:text-white"
                  href={`/runs/${detail.run.id}`}
                >
                  Back to summary
                </Link>
                <Link
                  className="inline-flex items-center justify-center rounded-full bg-surface-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
                  href={`/runs/${detail.run.id}/concepts/${detail.result.id}/drilldown`}
                >
                  Open detailed records
                </Link>
              </>
            }
            title="Concept Context"
          >
            <div className="flex items-center gap-2">
              <StatusPill tone={statusMeta.tone}>{statusMeta.label}</StatusPill>
              <span className="font-medium text-foreground">{detail.run.period}</span>
            </div>
            <p className="max-w-xs leading-6 text-text-secondary">
              {detail.run.run_label}
            </p>
            <div className="space-y-1 font-mono text-xs text-text-muted">
              <p>{detail.run.id}</p>
              <p>{detail.run.source_file_name ?? "Source file pending"}</p>
              <p>{detail.run.rules_version ?? "rules unavailable"}</p>
            </div>
          </HeaderActionPanel>
        }
        eyebrow="Concept Analysis"
        kicker={detail.concept_analysis.header.concept_code_normalized}
        subtitle="This view connects numbers, likely causes, evidence framing and the next recommended review action without forcing the user into raw records too early."
        title={detail.concept_analysis.header.concept_name_normalized}
      />

      <section className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
        <article className="rounded-[24px] border border-border-subtle bg-surface-ink p-5 text-white md:p-6">
          <div className="flex flex-wrap items-center gap-3">
            <StatusPill tone={statusMeta.tone}>{statusMeta.label}</StatusPill>
            <span className="text-sm text-slate-300">
              {detail.concept_analysis.header.period}
            </span>
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Run
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                {detail.run.run_label}
              </p>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Processed File
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                {detail.run.source_file_name ?? "No source file recorded"}
              </p>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Completed At
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                {formatDateTime(detail.run.completed_at)}
              </p>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Review focus
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                Start with the top ranked causes, then continue into the detailed
                records if confirmation is needed.
              </p>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Rules Version
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                {detail.run.rules_version ?? "Rules version unavailable"}
              </p>
            </div>
          </div>
        </article>

        <article className="rounded-[24px] border border-border-subtle bg-white/72 p-5 md:p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            Evidence framing
          </p>
          <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-foreground">
            The explanation is rule-based and grounded on observed records.
          </h2>
          <p className="mt-3 text-sm leading-6 text-text-secondary">
            It should be read as probable explanation, not as an irreversible
            statement. The UI surfaces the strongest evidence first so a controller
            can validate it quickly.
          </p>
          <div className="mt-5 grid gap-3 md:grid-cols-2">
            <MetricCard
              label="Highest impact anomaly"
              value={topCause?.exception_type ?? "No anomaly detected"}
            />
            <MetricCard
              label="Top impacted employee"
              value={
                topCause?.employee_id
                  ? `Employee ${topCause.employee_id}`
                  : "No employee singled out"
              }
            />
            <MetricCard
              label="Top impacted legal entity"
              value={detail.result.legal_entity ?? "Mixed scope"}
            />
            <MetricCard
              hint="Rows with at least one exception attached."
              label="Rows With Evidence"
              value={formatCompactNumber(
                detail.concept_analysis.evidence_summary.records_with_exception,
              )}
            />
          </div>
        </article>
      </section>

      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        <MetricCard
          label="Expected Total"
          value={formatCurrency(detail.concept_analysis.kpis.expected_amount)}
        />
        <MetricCard
          label="Observed Total"
          value={formatCurrency(detail.concept_analysis.kpis.observed_amount)}
        />
        <MetricCard
          label="Absolute Difference"
          value={formatCurrency(detail.concept_analysis.kpis.absolute_diff)}
        />
        <MetricCard
          label="Difference %"
          value={formatPercentage(detail.concept_analysis.kpis.relative_diff_pct)}
        />
        <MetricCard
          label="Records Analyzed"
          value={formatCompactNumber(detail.concept_analysis.kpis.record_count)}
        />
        <MetricCard
          label="Employees Affected"
          value={formatCompactNumber(
            detail.concept_analysis.kpis.impacted_employees_count ??
              detail.concept_analysis.evidence_summary.employees_with_exception,
          )}
        />
      </section>

      <section className="grid gap-4 xl:grid-cols-[0.95fr_1.05fr]">
        <article className="rounded-[24px] border border-border-subtle bg-white/75 p-5 md:p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            Summary statement
          </p>
          <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-foreground">
            {detail.concept_analysis.summary_statement ??
              "A summary statement is not available for this concept yet."}
          </h2>
        </article>

        <article className="rounded-[24px] border border-border-subtle bg-surface-strong/55 p-5 md:p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            Recommended next step
          </p>
          <p className="mt-3 text-lg leading-8 text-foreground">
            {detail.concept_analysis.recommended_action ??
              "Review the concept-level evidence and confirm the supporting records before closing the period."}
          </p>
        </article>
      </section>

      <section className="grid gap-4 xl:grid-cols-[1.05fr_0.95fr]">
        <article className="rounded-[24px] border border-border-subtle bg-white/75 p-5 md:p-6">
          <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
                Top Causes
              </p>
              <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-foreground">
                Ranked probable causes behind the difference.
              </h2>
            </div>
            <p className="max-w-sm text-sm leading-6 text-text-secondary">
              Ranking prioritizes estimated impact first and confidence second, while
              keeping the tone sober and review-oriented.
            </p>
          </div>

          <div className="mt-5 space-y-4">
            {detail.concept_analysis.top_causes.length ? (
              detail.concept_analysis.top_causes.map((cause, index) => (
                <article
                  className="rounded-[22px] border border-border-subtle bg-surface p-4"
                  key={cause.id}
                >
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-surface-ink text-sm font-semibold text-white">
                        {index + 1}
                      </span>
                      <div>
                        <p className="font-semibold text-foreground">
                          {cause.exception_type}
                        </p>
                        <p className="text-sm text-text-secondary">
                          Severity {cause.severity} | Scope {cause.scope_level}
                        </p>
                      </div>
                    </div>
                    <div className="text-right text-sm text-text-secondary">
                      <p className="font-mono text-foreground">
                        {cause.estimated_impact_amount
                          ? formatCurrency(cause.estimated_impact_amount)
                          : "Impact N/A"}
                      </p>
                      <p>
                        Confidence{" "}
                        {cause.confidence
                          ? formatPercentage(Number.parseFloat(cause.confidence) * 100, 0)
                          : "N/A"}
                      </p>
                    </div>
                  </div>
                  <p className="mt-4 text-sm leading-6 text-text-secondary">
                    {cause.observation ??
                      "No additional observation was stored for this exception."}
                  </p>
                  <div className="mt-3 flex flex-wrap gap-2 text-xs text-text-muted">
                    {cause.record_id ? (
                      <span className="rounded-full border border-border-subtle bg-white px-3 py-1.5">
                        Record {cause.record_id}
                      </span>
                    ) : null}
                    {cause.employee_id ? (
                      <span className="rounded-full border border-border-subtle bg-white px-3 py-1.5">
                        Employee {cause.employee_id}
                      </span>
                    ) : null}
                    {cause.concept_scope ? (
                      <span className="rounded-full border border-border-subtle bg-white px-3 py-1.5">
                        Scope {cause.concept_scope}
                      </span>
                    ) : null}
                  </div>
                </article>
              ))
            ) : (
              <NoticeBanner
                detail="This concept does not currently expose ranked exception causes, even though the summary result is available."
                message="No ranked causes were returned for this concept."
                tone="warning"
              />
            )}
          </div>
        </article>

        <article className="rounded-[24px] border border-border-subtle bg-white/75 p-5 md:p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            Evidence Summary
          </p>
          <div className="mt-5 space-y-4">
            <div className="rounded-[20px] border border-border-subtle bg-surface p-4">
              <p className="text-sm font-semibold text-foreground">Exception footprint</p>
              <div className="mt-3 grid gap-3 md:grid-cols-2">
                <MetricCard
                  label="Total Exceptions"
                  value={formatCompactNumber(
                    detail.concept_analysis.evidence_summary.total_exceptions,
                  )}
                />
                <MetricCard
                  label="Employees With Exception"
                  value={formatCompactNumber(
                    detail.concept_analysis.evidence_summary.employees_with_exception,
                  )}
                />
                <MetricCard
                  label="Records With Exception"
                  value={formatCompactNumber(
                    detail.concept_analysis.evidence_summary.records_with_exception,
                  )}
                />
                <MetricCard
                  label="Explained Amount Estimate"
                  value={
                    detail.concept_analysis.kpis.explained_amount_estimate
                      ? formatCurrency(
                          detail.concept_analysis.kpis.explained_amount_estimate,
                        )
                      : "Not estimated"
                  }
                />
              </div>
            </div>

            <div className="rounded-[20px] border border-border-subtle bg-surface p-4">
              <p className="text-sm font-semibold text-foreground">
                Top exception types
              </p>
              <div className="mt-3 flex flex-wrap gap-2">
                {detail.concept_analysis.evidence_summary.top_exception_types.length ? (
                  detail.concept_analysis.evidence_summary.top_exception_types.map(
                    (exceptionType) => (
                      <span
                        className="rounded-full border border-border-subtle bg-white px-3 py-1.5 text-xs font-medium text-text-secondary"
                        key={exceptionType}
                      >
                        {exceptionType}
                      </span>
                    ),
                  )
                ) : (
                  <span className="text-sm text-text-secondary">
                    No exception types were returned for this concept.
                  </span>
                )}
              </div>
            </div>

            <div className="rounded-[20px] border border-border-subtle bg-surface-ink p-4 text-white">
              <p className="text-sm font-semibold">Next step</p>
              <p className="mt-2 text-sm leading-6 text-slate-200">
                If the controller needs record-level confirmation, continue to the
                prepared drill-down handoff with run and concept context preserved.
              </p>
              <Link
                className="mt-4 inline-flex items-center justify-center rounded-full border border-white/15 px-4 py-2 text-sm font-semibold text-white transition hover:bg-white/10"
                href={`/runs/${detail.run.id}/concepts/${detail.result.id}/drilldown`}
              >
                Open detailed records
              </Link>
            </div>
          </div>
        </article>
      </section>

      <section className="grid gap-4 xl:grid-cols-[0.95fr_1.05fr]">
        <article className="rounded-[24px] border border-border-subtle bg-white/75 p-5 md:p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            Traceability
          </p>
          <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-foreground">
            The concept view stays anchored to concrete run metadata.
          </h2>
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <MetricCard
              label="Records Analyzed"
              value={formatCompactNumber(detail.result.record_count)}
            />
            <MetricCard
              label="Impacted Rows"
              value={formatCompactNumber(
                detail.result.impacted_records_count ??
                  detail.concept_analysis.evidence_summary.records_with_exception,
              )}
            />
          </div>
        </article>

        <article className="rounded-[24px] border border-border-subtle bg-white/72 p-5 md:p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            Run Events
          </p>
          <div className="mt-4 space-y-4">
            {detail.event_log.slice(-3).map((event) => (
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
    </div>
  );
}
