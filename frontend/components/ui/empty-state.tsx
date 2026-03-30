type EmptyStateProps = {
  action: React.ReactNode;
};

export function EmptyState({ action }: EmptyStateProps) {
  return (
    <section className="grid gap-6 rounded-[24px] border border-border-subtle bg-white/70 p-6 lg:grid-cols-[1.3fr_0.7fr] lg:p-8">
      <div className="space-y-5">
        <div className="space-y-3">
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-text-muted">
            Setup Flow
          </p>
          <h2 className="text-3xl font-semibold tracking-[-0.03em] text-foreground">
            Start a reconciliation run with just the essentials.
          </h2>
          <p className="max-w-2xl text-base leading-7 text-text-secondary">
            The MVP keeps the first interaction intentionally narrow: define the
            payroll period, attach the payroll file, confirm the expected totals
            reference and launch the run from one controlled workspace.
          </p>
        </div>
        <div className="flex flex-wrap gap-3 text-sm text-text-secondary">
          <span className="rounded-full border border-border-subtle bg-surface px-3 py-2">
            One active run at a time
          </span>
          <span className="rounded-full border border-border-subtle bg-surface px-3 py-2">
            Demo seed references preloaded
          </span>
          <span className="rounded-full border border-border-subtle bg-surface px-3 py-2">
            Ready for upload and execution
          </span>
        </div>
      </div>
      <div className="rounded-[20px] bg-surface-ink p-5 text-white">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-300">
          What happens next
        </p>
        <div className="mt-4 space-y-3 text-sm leading-6 text-slate-200">
          <p>1. Create a run and register the demo reference files.</p>
          <p>2. Upload `payroll.csv` and optionally replace expected totals.</p>
          <p>3. Review readiness and execute reconciliation.</p>
        </div>
        <div className="mt-6">{action}</div>
      </div>
    </section>
  );
}
