import { AppHeader } from "@/components/ui/app-header";
import { AppShell } from "@/components/ui/app-shell";
import { HeaderActionPanel } from "@/components/ui/header-action-panel";
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
          <HeaderActionPanel title="Workspace Status">
            <div className="flex items-center gap-2">
              <StatusPill tone={backendHealth.ok ? "ready" : "warning"}>
                {backendHealth.ok ? "API live" : "API offline"}
              </StatusPill>
              <span className="font-medium text-foreground">Demo workspace ready</span>
            </div>
            <p className="max-w-xs leading-6">{backendHealth.summary}</p>
            <p className="font-mono text-xs text-text-muted">
              {backendHealth.apiBaseUrl}
            </p>
          </HeaderActionPanel>
        }
        eyebrow="Accounting Reconciliation MVP"
        kicker="Demo Seed & Run Setup"
        subtitle="A controlled workspace to recreate the canonical demo run, validate readiness and move from setup into summary without operational noise."
        title="Prepare the canonical walkthrough in one place."
      />

      <SetupWorkspace
        backendHealth={backendHealth}
        defaultPeriod={demoSetupBundle.defaultPeriod}
        demoExpectedTotals={demoSetupBundle.expectedTotals}
        seedFiles={demoSetupBundle.seedFiles}
      />
    </AppShell>
  );
}
