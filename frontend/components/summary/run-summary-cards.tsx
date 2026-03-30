import type { RunResultRecord, RunSummaryMetrics } from "@/lib/api/client";
import { formatCompactNumber, formatCurrency } from "@/lib/utils/format";

import { MetricCard } from "@/components/ui/metric-card";

type RunSummaryCardsProps = {
  metrics: RunSummaryMetrics;
  results: RunResultRecord[];
};

function calculateReconciledAmount(results: RunResultRecord[]) {
  return results
    .filter((result) => result.status === "Reconciled")
    .reduce(
      (total, result) => total + (Number.parseFloat(result.observed_amount) || 0),
      0,
    );
}

function calculatePendingExplanation(results: RunResultRecord[]) {
  return results
    .filter((result) => result.status !== "Reconciled")
    .reduce(
      (total, result) => total + Math.abs(Number.parseFloat(result.absolute_diff) || 0),
      0,
    );
}

export function RunSummaryCards({ metrics, results }: RunSummaryCardsProps) {
  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
      <MetricCard
        hint="Concepts aligned against expected totals."
        label="Concepts Reconciled"
        value={formatCompactNumber(metrics.concepts_reconciled)}
      />
      <MetricCard
        hint="Concepts with low-severity differences that still need review."
        label="Minor Differences"
        value={formatCompactNumber(metrics.concepts_minor_difference)}
      />
      <MetricCard
        hint="Concepts still materially open at the end of the run."
        label="Unreconciled Concepts"
        value={formatCompactNumber(metrics.concepts_unreconciled)}
      />
      <MetricCard
        hint="Observed amount already aligned inside reconciled concepts."
        label="Total Amount Reconciled"
        value={formatCurrency(calculateReconciledAmount(results))}
      />
      <MetricCard
        hint="Absolute amount still waiting for explanation across non-reconciled concepts."
        label="Amount Pending Explanation"
        value={formatCurrency(calculatePendingExplanation(results))}
      />
    </section>
  );
}
