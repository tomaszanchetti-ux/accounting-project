import { AppHeader } from "@/components/ui/app-header";
import { LoadingBlock } from "@/components/ui/loading-block";

export function DrilldownLoading() {
  return (
    <div className="space-y-6">
      <AppHeader
        eyebrow="Drill-down"
        subtitle="Loading record-level evidence, filters and anomaly summary."
        title="Preparing detailed records."
      />
      <section className="grid gap-4 lg:grid-cols-[1.05fr_0.95fr]">
        <LoadingBlock className="h-52 border border-border-subtle" />
        <LoadingBlock className="h-52 border border-border-subtle" />
      </section>
      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <LoadingBlock className="h-32 border border-border-subtle" />
        <LoadingBlock className="h-32 border border-border-subtle" />
        <LoadingBlock className="h-32 border border-border-subtle" />
        <LoadingBlock className="h-32 border border-border-subtle" />
      </section>
      <LoadingBlock className="h-24 border border-border-subtle" />
      <LoadingBlock className="h-[480px] border border-border-subtle" />
    </div>
  );
}
