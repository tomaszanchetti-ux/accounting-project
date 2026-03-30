import { StatusPill } from "@/components/ui/status-pill";

type AppHeaderProps = {
  actions?: React.ReactNode;
  eyebrow: string;
  kicker?: string;
  subtitle: string;
  title: string;
};

export function AppHeader({
  actions,
  eyebrow,
  kicker,
  subtitle,
  title,
}: AppHeaderProps) {
  return (
    <header className="rounded-[24px] border border-border-subtle bg-surface-strong/65 p-5 md:p-6">
      <div className="flex flex-col gap-6 xl:flex-row xl:items-start xl:justify-between">
        <div className="max-w-3xl space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <StatusPill tone="info">{eyebrow}</StatusPill>
            {kicker ? (
              <span className="text-sm font-medium text-text-secondary">
                {kicker}
              </span>
            ) : null}
          </div>
          <div className="space-y-3">
            <h1 className="max-w-3xl text-4xl font-semibold tracking-[-0.03em] text-balance md:text-5xl">
              {title}
            </h1>
            <p className="max-w-2xl text-base leading-7 text-text-secondary md:text-lg">
              {subtitle}
            </p>
          </div>
        </div>
        {actions ? (
          <div className="flex shrink-0 items-start justify-start xl:justify-end">
            {actions}
          </div>
        ) : null}
      </div>
    </header>
  );
}
