import Link from "next/link";

import {
  ApiRequestError,
  getRunResultDetail,
} from "@/lib/api/client";

import { ConceptAnalysisScreen } from "@/components/concept/concept-analysis-screen";
import { AppHeader } from "@/components/ui/app-header";
import { AppShell } from "@/components/ui/app-shell";
import { NoticeBanner } from "@/components/ui/notice-banner";
import { StatePanel } from "@/components/ui/state-panel";

type ConceptAnalysisPageProps = {
  params: Promise<{
    resultId: string;
    runId: string;
  }>;
};

async function loadConceptAnalysis(runId: string, resultId: string) {
  try {
    return {
      detail: await getRunResultDetail(runId, resultId),
    };
  } catch (error) {
    return {
      error:
        error instanceof ApiRequestError
          ? error.message
          : "Unable to load the concept analysis payload.",
      notFound: error instanceof ApiRequestError && error.status === 404,
    };
  }
}

export default async function ConceptAnalysisPage({
  params,
}: ConceptAnalysisPageProps) {
  const { resultId, runId } = await params;
  const conceptState = await loadConceptAnalysis(runId, resultId);

  if ("error" in conceptState) {
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
          eyebrow="Concept Analysis"
          kicker={resultId}
          subtitle={
            conceptState.notFound
              ? "The concept was not found inside this run."
              : "The concept analysis payload could not be loaded."
          }
          title={
            conceptState.notFound
              ? "Concept not found"
              : "Concept analysis unavailable"
          }
        />
        <NoticeBanner
          detail={conceptState.error}
          message={
            conceptState.notFound
              ? "This concept is no longer available for the selected run."
              : "The concept analysis screen failed to load."
          }
          tone={conceptState.notFound ? "warning" : "error"}
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
            conceptState.notFound
              ? "The selected concept result could not be resolved inside this run anymore. The user can step back to summary without losing the broader run context."
              : "The route is available but the backend did not return a valid concept analysis payload. The recovery path stays visible so the user can continue navigating the demo."
          }
          eyebrow={conceptState.notFound ? "Concept Missing" : "Concept Load Error"}
          title={
            conceptState.notFound
              ? "Use the summary to open another concept."
              : "Return to a stable screen and try again from there."
          }
          tone={conceptState.notFound ? "warning" : "error"}
        />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <ConceptAnalysisScreen detail={conceptState.detail} />
    </AppShell>
  );
}
