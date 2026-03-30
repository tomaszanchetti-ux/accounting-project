import Link from "next/link";
import { notFound } from "next/navigation";

import { RunSummarySnapshot } from "@/components/setup/run-summary-snapshot";
import { AppHeader } from "@/components/ui/app-header";
import { AppShell } from "@/components/ui/app-shell";
import { getRunSummary } from "@/lib/api/client";

type RunSnapshotPageProps = {
  params: Promise<{
    runId: string;
  }>;
};

export default async function RunSnapshotPage({
  params,
}: RunSnapshotPageProps) {
  const { runId } = await params;
  let summary;

  try {
    summary = await getRunSummary(runId);
  } catch {
    notFound();
  }

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
        eyebrow="Run Snapshot"
        kicker={summary.run.id}
        subtitle="Operational snapshot generated from the summary payload exposed by the backend."
        title={summary.run.run_label}
      />
      <RunSummarySnapshot summary={summary} />
    </AppShell>
  );
}
