import Link from "next/link";

import {
  ApiRequestError,
  getRunResults,
  getRunSummary,
} from "@/lib/api/client";
import { sortResultsForSummary } from "@/lib/utils/reconciliation";

import { RunSummaryScreen } from "@/components/summary/run-summary-screen";
import { AppHeader } from "@/components/ui/app-header";
import { AppShell } from "@/components/ui/app-shell";
import { NoticeBanner } from "@/components/ui/notice-banner";
import { StatePanel } from "@/components/ui/state-panel";

type RunSnapshotPageProps = {
  params: Promise<{
    runId: string;
  }>;
};

async function loadRunSummary(runId: string) {
  try {
    const [summary, resultsPayload] = await Promise.all([
      getRunSummary(runId),
      getRunResults(runId),
    ]);

    return {
      results: sortResultsForSummary(resultsPayload.results),
      summary,
    };
  } catch (error) {
    return {
      error:
        error instanceof ApiRequestError
          ? error.message
          : "Unable to load the run summary.",
      notFound: error instanceof ApiRequestError && error.status === 404,
    };
  }
}

export default async function RunSnapshotPage({
  params,
}: RunSnapshotPageProps) {
  const { runId } = await params;
  const summaryState = await loadRunSummary(runId);

  if ("error" in summaryState) {
    return (
      <AppShell>
        <AppHeader
          actions={
            <Link
              className="inline-flex items-center justify-center rounded-full bg-surface-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
              href="/"
            >
              Back to setup
            </Link>
          }
          eyebrow="Run Summary"
          kicker={runId}
          subtitle={
            summaryState.notFound
              ? "The requested run does not exist or is no longer available."
              : "The analytical layer could not be loaded from the backend."
          }
          title={summaryState.notFound ? "Run not found" : "Run summary unavailable"}
        />
        <NoticeBanner
          detail={summaryState.error}
          message={
            summaryState.notFound
              ? "This run is no longer available."
              : "The summary screen failed to load."
          }
          tone={summaryState.notFound ? "warning" : "error"}
        />
        <StatePanel
          action={
            <Link
              className="inline-flex items-center justify-center rounded-full bg-surface-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
              href="/"
            >
              Start from setup
            </Link>
          }
          detail={
            summaryState.notFound
              ? "The app keeps navigation anchored here instead of sending the user to a generic browser-level 404. This makes it clearer that the run context was missing, not that the whole product broke."
              : "The route is still reachable, but the backend did not return a usable summary payload. Returning to setup keeps the workflow moving without leaving the user in an ambiguous state."
          }
          eyebrow={summaryState.notFound ? "Run Not Found" : "Summary Unavailable"}
          title={
            summaryState.notFound
              ? "Return to setup and create or open another run."
              : "Go back to setup while the summary issue is resolved."
          }
          tone={summaryState.notFound ? "warning" : "error"}
        />
      </AppShell>
    );
  }

  const { results, summary } = summaryState;

  return (
    <AppShell>
      {results.length ? (
        <RunSummaryScreen results={results} summary={summary} />
      ) : (
        <>
          <AppHeader
            actions={
              <Link
                className="inline-flex items-center justify-center rounded-full bg-surface-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
                href="/"
              >
                Back to setup
              </Link>
            }
            eyebrow="Run Summary"
            kicker={summary.run.id}
            subtitle="The run is available, but no concept-level results were returned yet."
            title={summary.run.run_label}
          />
          <StatePanel
            action={
              <Link
                className="inline-flex items-center justify-center rounded-full bg-surface-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
                href="/"
              >
                Back to setup
              </Link>
            }
            detail="The run context is valid, but the backend returned no concept-level results yet. This can happen on early execution edges, incomplete persistence or runs that did not produce a visible concept set."
            eyebrow="Empty Summary"
            title="No concept results are available for this run yet."
            tone="warning"
          />
        </>
      )}
    </AppShell>
  );
}
