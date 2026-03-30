import { AppHeader } from "@/components/ui/app-header";
import { LoadingBlock } from "@/components/ui/loading-block";

export function ConceptAnalysisLoading() {
  return (
    <div className="space-y-6">
      <AppHeader
        eyebrow="Concept Analysis"
        subtitle="Loading concept-level KPIs, explanation blocks and evidence summary."
        title="Preparing concept analysis."
      />
      <section className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
        <LoadingBlock className="h-64 border border-border-subtle" />
        <LoadingBlock className="h-64 border border-border-subtle" />
      </section>
      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        <LoadingBlock className="h-32 border border-border-subtle" />
        <LoadingBlock className="h-32 border border-border-subtle" />
        <LoadingBlock className="h-32 border border-border-subtle" />
        <LoadingBlock className="h-32 border border-border-subtle" />
        <LoadingBlock className="h-32 border border-border-subtle" />
        <LoadingBlock className="h-32 border border-border-subtle" />
      </section>
      <section className="grid gap-4 xl:grid-cols-2">
        <LoadingBlock className="h-[360px] border border-border-subtle" />
        <LoadingBlock className="h-[360px] border border-border-subtle" />
      </section>
    </div>
  );
}
