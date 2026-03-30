type MetricCardProps = {
  hint?: string;
  label: string;
  value: string;
};

export function MetricCard({ hint, label, value }: MetricCardProps) {
  return (
    <article className="rounded-[22px] border border-border-subtle bg-white/70 p-4">
      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
        {label}
      </p>
      <p className="mt-3 text-2xl font-semibold tracking-[-0.02em] text-foreground">
        {value}
      </p>
      {hint ? (
        <p className="mt-2 text-sm leading-6 text-text-secondary">{hint}</p>
      ) : null}
    </article>
  );
}
