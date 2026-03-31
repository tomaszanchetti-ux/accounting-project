type EmptyStateProps = {
  action: React.ReactNode;
};

export function EmptyState({ action }: EmptyStateProps) {
  return (
    <section className="grid gap-6 rounded-[24px] border border-border-subtle bg-white/70 p-6 lg:grid-cols-[1.3fr_0.7fr] lg:p-8">
      <div className="space-y-5">
        <div className="space-y-3">
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-text-muted">
            New Reconciliation
          </p>
          <h2 className="text-3xl font-semibold tracking-[-0.03em] text-foreground">
            Start with the files and the run.
          </h2>
          <p className="max-w-2xl text-base leading-7 text-text-secondary">
            The simplified MVP starts from one task: prepare the payroll input,
            confirm the expected totals and launch the run without extra setup
            noise.
          </p>
        </div>
        <div className="flex flex-wrap gap-3 text-sm text-text-secondary">
          <span className="rounded-full border border-border-subtle bg-surface px-3 py-2">
            Upload payroll
          </span>
          <span className="rounded-full border border-border-subtle bg-surface px-3 py-2">
            Confirm totals
          </span>
          <span className="rounded-full border border-border-subtle bg-surface px-3 py-2">
            Run reconciliation
          </span>
        </div>
      </div>
      <div className="rounded-[20px] bg-surface-ink p-5 text-white">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-300">
          What happens next
        </p>
        <div className="mt-4 space-y-3 text-sm leading-6 text-slate-200">
          <p>1. Create the run shell in the background.</p>
          <p>2. Attach `payroll.csv` and `expected_totals.csv`.</p>
          <p>3. Run the reconciliation and open the results.</p>
        </div>
        <div className="mt-6">{action}</div>
      </div>
    </section>
  );
}
