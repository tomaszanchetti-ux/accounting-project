import Link from "next/link";

import {
  ApiRequestError,
  getRunResultDetail,
} from "@/lib/api/client";

import { AppHeader } from "@/components/ui/app-header";
import { AppShell } from "@/components/ui/app-shell";
import { MetricCard } from "@/components/ui/metric-card";
import { NoticeBanner } from "@/components/ui/notice-banner";
import { formatCompactNumber, formatCurrency } from "@/lib/utils/format";

type DrilldownHandoffPageProps = {
  params: Promise<{
    resultId: string;
    runId: string;
  }>;
};

async function loadDrilldownHandoff(runId: string, resultId: string) {
  try {
    return {
      detail: await getRunResultDetail(runId, resultId),
    };
  } catch (error) {
    return {
      error:
        error instanceof ApiRequestError
          ? error.message
          : "Unable to prepare the drill-down handoff.",
    };
  }
}

export default async function DrilldownHandoffPage({
  params,
}: DrilldownHandoffPageProps) {
  const { resultId, runId } = await params;
  const drilldownState = await loadDrilldownHandoff(runId, resultId);

  if ("error" in drilldownState) {
    return (
      <AppShell>
        <AppHeader
          actions={
            <Link
              className="inline-flex items-center justify-center rounded-full bg-surface-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
              href={`/runs/${runId}`}
            >
              Back to summary
            </Link>
          }
          eyebrow="Drill-down Handoff"
          kicker={resultId}
          subtitle="The handoff could not load the concept context from the backend."
          title="Drill-down handoff unavailable"
        />
        <NoticeBanner
          detail={drilldownState.error}
          message="The drill-down handoff failed to load."
          tone="error"
        />
      </AppShell>
    );
  }

  const { detail } = drilldownState;

  return (
    <AppShell>
      <AppHeader
        actions={
          <div className="flex flex-wrap gap-3">
            <Link
              className="inline-flex items-center justify-center rounded-full border border-border-subtle bg-white/70 px-4 py-2 text-sm font-semibold text-foreground transition hover:border-surface-ink hover:bg-surface-ink hover:text-white"
              href={`/runs/${runId}/concepts/${resultId}`}
            >
              Back to concept
            </Link>
            <Link
              className="inline-flex items-center justify-center rounded-full bg-surface-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
              href={`/runs/${runId}`}
            >
              Back to summary
            </Link>
          </div>
        }
        eyebrow="Drill-down Handoff"
        kicker={detail.concept_analysis.header.concept_code_normalized}
        subtitle="The record-level workspace belongs to EPIC 07. This route preserves continuity so the user never lands in a dead end after reading the concept explanation."
        title={`Detailed records for ${detail.concept_analysis.header.concept_name_normalized}`}
      />

      <NoticeBanner
        detail="EPIC 06 prepares the transition and preserves run plus concept context. The full record table, filters and exports arrive in the next epic."
        message="Detailed records are intentionally staged for the next implementation layer."
        tone="info"
      />

      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Concept Status" value={detail.result.status} />
        <MetricCard
          label="Absolute Difference"
          value={formatCurrency(detail.result.absolute_diff)}
        />
        <MetricCard
          label="Impacted Records"
          value={formatCompactNumber(
            detail.result.impacted_records_count ?? detail.exceptions.length,
          )}
        />
        <MetricCard
          label="Exceptions Persisted"
          value={formatCompactNumber(detail.exceptions.length)}
        />
      </section>

      <section className="rounded-[24px] border border-border-subtle bg-white/72 p-5 md:p-6">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
          Next operational scope
        </p>
        <div className="mt-4 grid gap-4 lg:grid-cols-[1fr_0.9fr]">
          <div className="space-y-3">
            <h2 className="text-2xl font-semibold tracking-[-0.03em] text-foreground">
              The drill-down experience is queued and context-complete.
            </h2>
            <p className="text-sm leading-6 text-text-secondary">
              When EPIC 07 starts, this route can render the real endpoint
              <span className="mx-1 font-mono">
                GET /runs/{"{run_id}"}/results/{"{result_id}"}/drilldown
              </span>
              without changing the navigation model introduced here.
            </p>
          </div>
          <div className="rounded-[20px] bg-surface-ink p-5 text-white">
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-300">
              Context preserved
            </p>
            <div className="mt-4 space-y-2 text-sm leading-6 text-slate-200">
              <p>Run: {detail.run.run_label}</p>
              <p>Period: {detail.result.period}</p>
              <p>Concept: {detail.result.concept_code_normalized}</p>
              <p>
                Recommended action:{" "}
                {detail.result.recommended_action ?? "Review detailed records"}
              </p>
            </div>
          </div>
        </div>
      </section>
    </AppShell>
  );
}
