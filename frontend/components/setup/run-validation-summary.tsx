import { StatusPill } from "@/components/ui/status-pill";

type ValidationItem = {
  description: string;
  label: string;
  ready: boolean;
};

type RunValidationSummaryProps = {
  checks: ValidationItem[];
  detectedConcepts: number | null;
  detectedPeriod: string | null;
  detectedRecords: number | null;
  readyToExecute: boolean;
};

export function RunValidationSummary({
  checks,
  detectedConcepts,
  detectedPeriod,
  detectedRecords,
  readyToExecute,
}: RunValidationSummaryProps) {
  return (
    <section className="rounded-[24px] border border-border-subtle bg-white/70 p-5">
      <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
        <div className="space-y-1">
          <h3 className="text-xl font-semibold text-foreground">
            Readiness checks
          </h3>
          <p className="max-w-2xl text-sm leading-6 text-text-secondary">
            Readiness stays visible on screen so the setup never feels like a
            black box.
          </p>
        </div>
        <StatusPill tone={readyToExecute ? "ready" : "warning"}>
          {readyToExecute ? "Ready to run" : "Needs attention"}
        </StatusPill>
      </div>

      <div className="mt-5 grid gap-3 md:grid-cols-2">
        {checks.map((check) => (
          <article
            className="rounded-[18px] border border-border-subtle bg-surface p-4"
            key={check.label}
          >
            <div className="flex items-center justify-between gap-3">
              <p className="text-sm font-semibold text-foreground">{check.label}</p>
              <StatusPill tone={check.ready ? "ready" : "warning"}>
                {check.ready ? "Ready" : "Missing"}
              </StatusPill>
            </div>
            <p className="mt-2 text-sm leading-6 text-text-secondary">
              {check.description}
            </p>
          </article>
        ))}
      </div>

      <div className="mt-5 grid gap-3 md:grid-cols-3">
        <article className="rounded-[18px] border border-border-subtle bg-surface p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-text-muted">
            Records detected
          </p>
          <p className="mt-2 text-2xl font-semibold text-foreground">
            {detectedRecords ?? "—"}
          </p>
        </article>
        <article className="rounded-[18px] border border-border-subtle bg-surface p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-text-muted">
            Concepts detected
          </p>
          <p className="mt-2 text-2xl font-semibold text-foreground">
            {detectedConcepts ?? "—"}
          </p>
        </article>
        <article className="rounded-[18px] border border-border-subtle bg-surface p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-text-muted">
            Detected period
          </p>
          <p className="mt-2 text-2xl font-semibold text-foreground">
            {detectedPeriod ?? "Pending"}
          </p>
        </article>
      </div>
    </section>
  );
}
