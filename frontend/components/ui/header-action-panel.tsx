type HeaderActionPanelProps = {
  actions?: React.ReactNode;
  children?: React.ReactNode;
  title: string;
};

export function HeaderActionPanel({
  actions,
  children,
  title,
}: HeaderActionPanelProps) {
  return (
    <div className="grid min-w-[280px] gap-4 rounded-[22px] border border-border-subtle bg-white/72 p-4 text-sm text-text-secondary shadow-[0_16px_40px_rgba(28,39,56,0.08)]">
      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
        {title}
      </p>
      {children ? <div className="space-y-3">{children}</div> : null}
      {actions ? <div className="flex flex-wrap gap-3">{actions}</div> : null}
    </div>
  );
}
