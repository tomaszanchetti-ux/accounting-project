import { AppHeader } from "@/components/ui/app-header";
import { AppShell } from "@/components/ui/app-shell";
import { SetupWorkspace } from "@/components/setup/setup-workspace";
import { StatusPill } from "@/components/ui/status-pill";
import { getBackendHealth } from "@/lib/api/client";
import { getDemoSetupBundle } from "@/lib/setup/demo-seed";

export default async function Home() {
  const [backendHealth, demoSetupBundle] = await Promise.all([
    getBackendHealth(),
    getDemoSetupBundle(),
  ]);

  return (
    <AppShell>
      <AppHeader
        actions={
          <div className="flex flex-col gap-3 rounded-[20px] border border-border-subtle bg-white/60 p-4 text-sm text-text-secondary">
            <div className="flex items-center gap-2">
              <StatusPill tone={backendHealth.ok ? "ready" : "warning"}>
                {backendHealth.ok ? "API live" : "API offline"}
              </StatusPill>
              <span className="font-medium">EPIC 05 active</span>
            </div>
            <p className="max-w-xs leading-6">{backendHealth.summary}</p>
            <p className="font-mono text-xs text-text-muted">
              {backendHealth.apiBaseUrl}
            </p>
          </div>
        }
        eyebrow="Accounting Reconciliation MVP"
        kicker="UI Foundation & Setup Flow"
        subtitle="A single enterprise-style workspace to create a run, attach payroll inputs, validate readiness and launch reconciliation without exposing technical complexity."
        title="Prepare a new reconciliation run with confidence."
      />

      <SetupWorkspace
        backendHealth={backendHealth}
        defaultPeriod={demoSetupBundle.defaultPeriod}
        demoExpectedTotals={demoSetupBundle.expectedTotals}
        referenceFiles={demoSetupBundle.referenceFiles}
      />
    </AppShell>
  );
}
