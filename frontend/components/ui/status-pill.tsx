import { cx } from "@/lib/utils/cx";

const toneMap: Record<string, string> = {
  draft: "border-slate-500/20 bg-slate-500/10 text-slate-700",
  error: "border-status-unreconciled/20 bg-status-unreconciled/10 text-status-unreconciled",
  executing:
    "border-status-processing/20 bg-status-processing/10 text-status-processing",
  incomplete: "border-status-invalid/20 bg-status-invalid/10 text-status-invalid",
  info: "border-status-processing/20 bg-status-processing/10 text-status-processing",
  pending: "border-slate-500/20 bg-slate-500/10 text-slate-700",
  ready:
    "border-status-reconciled/20 bg-status-reconciled/10 text-status-reconciled",
  success:
    "border-status-reconciled/20 bg-status-reconciled/10 text-status-reconciled",
  warning:
    "border-status-minor-difference/20 bg-status-minor-difference/10 text-status-minor-difference",
};

type StatusPillProps = {
  children: React.ReactNode;
  tone?: keyof typeof toneMap;
};

export function StatusPill({
  children,
  tone = "info",
}: StatusPillProps) {
  return (
    <span
      className={cx(
        "inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold tracking-[0.12em] uppercase",
        toneMap[tone],
      )}
    >
      {children}
    </span>
  );
}
