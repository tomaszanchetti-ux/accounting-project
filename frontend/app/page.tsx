import { AppHeader } from "@/components/ui/app-header";
import { AppShell } from "@/components/ui/app-shell";
import { SetupWorkspace } from "@/components/setup/setup-workspace";
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
        eyebrow="Accounting Reconciliation"
        kicker="New Run"
        subtitle="Upload the payroll file, confirm the reference totals and run the reconciliation from one simple starting point."
        title="Run a reconciliation in three steps."
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
