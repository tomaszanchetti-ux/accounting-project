import { cx } from "@/lib/utils/cx";

type StatePanelProps = {
  action?: React.ReactNode;
  detail: string;
  eyebrow: string;
  title: string;
  tone?: "error" | "info" | "warning";
};

const toneStyles = {
  error: "border-status-unreconciled/20 bg-status-unreconciled/5",
  info: "border-border-subtle bg-white/72",
  warning: "border-status-minor/25 bg-status-minor/5",
} as const;

export function StatePanel({
  action,
  detail,
  eyebrow,
  title,
  tone = "info",
}: StatePanelProps) {
  return (
    <section
      className={cx(
        "rounded-[24px] border p-6",
        toneStyles[tone],
      )}
    >
      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
        {eyebrow}
      </p>
      <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-foreground">
        {title}
      </h2>
      <p className="mt-3 max-w-2xl text-sm leading-6 text-text-secondary">
        {detail}
      </p>
      {action ? <div className="mt-5">{action}</div> : null}
    </section>
  );
}
