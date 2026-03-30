import { StatusPill } from "@/components/ui/status-pill";

type NoticeBannerProps = {
  detail?: string;
  message: string;
  tone?: "error" | "info" | "success" | "warning";
};

export function NoticeBanner({
  detail,
  message,
  tone = "info",
}: NoticeBannerProps) {
  return (
    <div className="rounded-[20px] border border-border-subtle bg-white/55 p-4">
      <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
        <div className="space-y-1">
          <p className="text-sm font-semibold text-foreground">{message}</p>
          {detail ? (
            <p className="text-sm leading-6 text-text-secondary">{detail}</p>
          ) : null}
        </div>
        <StatusPill tone={tone}>{tone}</StatusPill>
      </div>
    </div>
  );
}
