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
          subtitle="The analytical layer could not be loaded from the backend."
          title="Run summary unavailable"
        />
        <NoticeBanner
          detail={summaryState.error}
          message="The summary screen failed to load."
          tone="error"
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
          <NoticeBanner
            detail="This empty state keeps the run accessible without forcing a not-found page. It covers valid runs with no results, incomplete persistence or early execution edges."
            message="No concept results are available for this run yet."
            tone="warning"
          />
        </>
      )}
    </AppShell>
  );
}
