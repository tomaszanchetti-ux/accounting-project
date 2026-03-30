import Link from "next/link";

import {
  ApiRequestError,
  getRunResultDetail,
} from "@/lib/api/client";

import { ConceptAnalysisScreen } from "@/components/concept/concept-analysis-screen";
import { AppHeader } from "@/components/ui/app-header";
import { AppShell } from "@/components/ui/app-shell";
import { NoticeBanner } from "@/components/ui/notice-banner";

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
      </AppShell>
    );
  }

  return (
    <AppShell>
      <ConceptAnalysisScreen detail={conceptState.detail} />
    </AppShell>
  );
}
