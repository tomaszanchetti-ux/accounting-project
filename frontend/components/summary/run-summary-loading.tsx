import { AppHeader } from "@/components/ui/app-header";
import { LoadingBlock } from "@/components/ui/loading-block";

export function RunSummaryLoading() {
  return (
    <div className="space-y-6">
      <AppHeader
        eyebrow="Run Summary"
        subtitle="Loading executive status, concept metrics and explanation previews from the backend."
        title="Preparing the run summary."
      />
      <section className="grid gap-4 lg:grid-cols-[1.15fr_0.85fr]">
        <LoadingBlock className="h-64 border border-border-subtle" />
        <LoadingBlock className="h-64 border border-border-subtle" />
      </section>
      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
        <LoadingBlock className="h-32 border border-border-subtle" />
        <LoadingBlock className="h-32 border border-border-subtle" />
        <LoadingBlock className="h-32 border border-border-subtle" />
        <LoadingBlock className="h-32 border border-border-subtle" />
        <LoadingBlock className="h-32 border border-border-subtle" />
      </section>
      <LoadingBlock className="h-[420px] border border-border-subtle" />
    </div>
  );
}
