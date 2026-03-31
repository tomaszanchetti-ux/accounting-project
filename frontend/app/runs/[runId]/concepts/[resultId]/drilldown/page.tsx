import Link from "next/link";

import { ApiRequestError, getRunResultDrilldown } from "@/lib/api/client";

import { DrilldownScreen } from "@/components/drilldown/drilldown-screen";
import { AppHeader } from "@/components/ui/app-header";
import { AppShell } from "@/components/ui/app-shell";
import { NoticeBanner } from "@/components/ui/notice-banner";
import { StatePanel } from "@/components/ui/state-panel";

type DrilldownPageProps = {
  params: Promise<{
    resultId: string;
    runId: string;
  }>;
};

async function loadDrilldown(runId: string, resultId: string) {
  try {
    return {
      drilldown: await getRunResultDrilldown(runId, resultId),
    };
  } catch (error) {
    return {
      error:
        error instanceof ApiRequestError
          ? error.message
          : "Unable to load the drill-down payload.",
      notFound: error instanceof ApiRequestError && error.status === 404,
    };
  }
}

export default async function DrilldownPage({ params }: DrilldownPageProps) {
  const { resultId, runId } = await params;
  const drilldownState = await loadDrilldown(runId, resultId);

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
          eyebrow="Drill-down"
          kicker={resultId}
          subtitle={
            drilldownState.notFound
              ? "The run or concept could not be found for this record-level view."
              : "The drill-down payload could not be loaded from the backend."
          }
          title={
            drilldownState.notFound
              ? "Detailed records not found"
              : "Drill-down unavailable"
          }
        />
        <NoticeBanner
          detail={drilldownState.error}
          message={
            drilldownState.notFound
              ? "This record-level view is no longer available for the selected run."
              : "The drill-down screen failed to load."
          }
          tone={drilldownState.notFound ? "warning" : "error"}
        />
        <StatePanel
          action={
            <div className="flex flex-wrap gap-3">
              <Link
                className="inline-flex items-center justify-center rounded-full bg-surface-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
                href={`/runs/${runId}`}
              >
                Back to summary
              </Link>
              <Link
                className="inline-flex items-center justify-center rounded-full border border-border-subtle bg-white px-4 py-2 text-sm font-semibold text-foreground transition hover:bg-surface"
                href="/"
              >
                Back to setup
              </Link>
            </div>
          }
          detail={
            drilldownState.notFound
              ? "The record-level evidence for this run and concept could not be resolved anymore. The user can step back to a stable summary view instead of landing on an abrupt dead end."
              : "The drill-down route exists but the backend did not return a usable payload. The navigation path stays explicit so the demo can continue from a known-good screen."
          }
          eyebrow={drilldownState.notFound ? "Drill-down Missing" : "Drill-down Load Error"}
          title={
            drilldownState.notFound
              ? "Return to summary and reopen a valid concept."
              : "Go back to a stable screen while drill-down is unavailable."
          }
          tone={drilldownState.notFound ? "warning" : "error"}
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <DrilldownScreen drilldown={drilldownState.drilldown} />
    </AppShell>
  );
}
