import { AppShell } from "@/components/ui/app-shell";
import { RunSummaryLoading } from "@/components/summary/run-summary-loading";

export default function Loading() {
  return (
    <AppShell>
      <RunSummaryLoading />
    </AppShell>
  );
}
