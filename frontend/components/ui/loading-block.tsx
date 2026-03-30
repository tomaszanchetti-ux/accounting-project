type LoadingBlockProps = {
  className?: string;
};

export function LoadingBlock({ className = "" }: LoadingBlockProps) {
  return (
    <div
      aria-hidden="true"
      className={`animate-pulse rounded-[20px] bg-slate-200/70 ${className}`.trim()}
    />
  );
}
