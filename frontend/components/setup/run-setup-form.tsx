import { ExpectedTotalsPreview } from "@/components/setup/expected-totals-preview";
import { RunValidationSummary } from "@/components/setup/run-validation-summary";
import { UploadBox, type UploadBoxState } from "@/components/setup/upload-box";
import { MetricCard } from "@/components/ui/metric-card";
import { NoticeBanner } from "@/components/ui/notice-banner";
import { StatusPill } from "@/components/ui/status-pill";
import type { RunRecord } from "@/lib/api/client";
import type { ExpectedTotalsPreviewRow } from "@/lib/utils/csv";

type RunSetupFormProps = {
  backendReachable: boolean;
  executeDisabled: boolean;
  executeLabel: string;
  expectedTotalsRows: ExpectedTotalsPreviewRow[];
  expectedTotalsSourceLabel: string;
  expectedTotalsState: UploadBoxState;
  feedback?: {
    detail?: string;
    message: string;
    tone: "error" | "info" | "success" | "warning";
  };
  onExecute: () => void;
  onExpectedTotalsUpload: (file: File) => void;
  onPayrollUpload: (file: File) => void;
  onResetExpectedTotalsToDemo: () => void;
  onUpdateIncludeExceptions: (checked: boolean) => void;
  onUpdateLegalEntityScope: (value: string) => void;
  onUpdatePeriod: (value: string) => void;
  onUpdateToleranceProfile: (value: string) => void;
  payrollDetectedConcepts: number | null;
  payrollDetectedPeriod: string | null;
  payrollDetectedRecords: number | null;
  payrollState: UploadBoxState;
  readyChecks: Array<{
    description: string;
    label: string;
    ready: boolean;
  }>;
  readyToExecute: boolean;
  run: RunRecord;
  setupParameters: {
    includeExceptionsAnalysis: boolean;
    legalEntityScope: string;
    period: string;
    toleranceProfileLabel: string;
  };
  supportFilesReady: {
    conceptMaster: boolean;
    employeeReference: boolean;
  };
};

export function RunSetupForm({
  backendReachable,
  executeDisabled,
  executeLabel,
  expectedTotalsRows,
  expectedTotalsSourceLabel,
  expectedTotalsState,
  feedback,
  onExecute,
  onExpectedTotalsUpload,
  onPayrollUpload,
  onResetExpectedTotalsToDemo,
  onUpdateIncludeExceptions,
  onUpdateLegalEntityScope,
  onUpdatePeriod,
  onUpdateToleranceProfile,
  payrollDetectedConcepts,
  payrollDetectedPeriod,
  payrollDetectedRecords,
  payrollState,
  readyChecks,
  readyToExecute,
  run,
  setupParameters,
  supportFilesReady,
}: RunSetupFormProps) {
  return (
    <div className="space-y-6">
      <section className="grid gap-4 xl:grid-cols-4">
        <MetricCard label="Run ID" value={run.id.slice(0, 8).toUpperCase()} />
        <MetricCard label="Current status" value={run.status} />
        <MetricCard label="Period" value={setupParameters.period} />
        <MetricCard label="API connectivity" value={backendReachable ? "Live" : "Offline"} />
      </section>

      {feedback ? (
        <NoticeBanner
          detail={feedback.detail}
          message={feedback.message}
          tone={feedback.tone}
        />
      ) : null}

      <section className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-6 rounded-[24px] border border-border-subtle bg-white/70 p-5">
          <div className="space-y-1">
            <div className="flex flex-wrap items-center gap-3">
              <h2 className="text-2xl font-semibold tracking-[-0.03em] text-foreground">
                New reconciliation run
              </h2>
              <StatusPill tone={readyToExecute ? "ready" : "warning"}>
                {readyToExecute ? "Ready" : "In progress"}
              </StatusPill>
            </div>
            <p className="max-w-2xl text-sm leading-6 text-text-secondary">
              Keep the setup focused on what matters: target period, payroll
              upload, reference totals and readiness to run.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <label className="space-y-2">
              <span className="text-sm font-semibold text-foreground">Period</span>
              <input
                className="w-full rounded-2xl border border-border-subtle bg-surface px-4 py-3 text-foreground outline-none transition focus:border-surface-ink"
                onChange={(event) => onUpdatePeriod(event.target.value)}
                placeholder="2026-03"
                value={setupParameters.period}
              />
            </label>
            <label className="space-y-2">
              <span className="text-sm font-semibold text-foreground">
                Legal entity scope
              </span>
              <input
                className="w-full rounded-2xl border border-border-subtle bg-surface px-4 py-3 text-foreground outline-none transition focus:border-surface-ink"
                onChange={(event) => onUpdateLegalEntityScope(event.target.value)}
                placeholder="ARD Spain SL"
                value={setupParameters.legalEntityScope}
              />
            </label>
            <label className="space-y-2">
              <span className="text-sm font-semibold text-foreground">
                Tolerance profile
              </span>
              <select
                className="w-full rounded-2xl border border-border-subtle bg-surface px-4 py-3 text-foreground outline-none transition focus:border-surface-ink"
                onChange={(event) => onUpdateToleranceProfile(event.target.value)}
                value={setupParameters.toleranceProfileLabel}
              >
                <option value="mvp-default">MVP default</option>
                <option value="finance-review">Finance review</option>
              </select>
            </label>
            <label className="space-y-2">
              <span className="text-sm font-semibold text-foreground">
                Exceptions analysis
              </span>
              <div className="flex min-h-[52px] items-center justify-between rounded-2xl border border-border-subtle bg-surface px-4 py-3">
                <div>
                  <p className="text-sm font-medium text-foreground">
                    Keep explanation layer active
                  </p>
                  <p className="text-xs text-text-secondary">
                    Recommended for demo and traceability.
                  </p>
                </div>
                <input
                  checked={setupParameters.includeExceptionsAnalysis}
                  className="h-4 w-4 accent-[#132033]"
                  onChange={(event) =>
                    onUpdateIncludeExceptions(event.target.checked)
                  }
                  type="checkbox"
                />
              </div>
            </label>
          </div>

          <UploadBox
            ctaLabel="Upload payroll"
            description="Primary input for the run. The file is parsed client-side for quick readiness checks and then sent to the backend."
            onFileSelected={onPayrollUpload}
            state={payrollState}
            title="Payroll file"
          />

          <UploadBox
            ctaLabel="Replace expected totals"
            description="The run starts with demo seed expected totals, but you can replace them with another CSV if needed."
            onFileSelected={onExpectedTotalsUpload}
            secondaryAction={
              <button
                className="inline-flex items-center justify-center rounded-full border border-border-subtle px-4 py-2 text-sm font-semibold text-foreground transition hover:bg-surface"
                onClick={onResetExpectedTotalsToDemo}
                type="button"
              >
                Use demo seed again
              </button>
            }
            state={expectedTotalsState}
            title="Expected totals"
          />

          <div className="flex flex-col gap-4 rounded-[22px] border border-border-subtle bg-surface p-4 md:flex-row md:items-center md:justify-between">
            <div className="space-y-1">
              <p className="text-sm font-semibold text-foreground">
                Reference files loaded automatically
              </p>
              <p className="text-sm text-text-secondary">
                `concept_master.csv` and `employee_reference.csv` are uploaded
                automatically from the demo seed so setup stays focused.
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <StatusPill tone={supportFilesReady.conceptMaster ? "ready" : "warning"}>
                Concept master
              </StatusPill>
              <StatusPill
                tone={supportFilesReady.employeeReference ? "ready" : "warning"}
              >
                Employee reference
              </StatusPill>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <ExpectedTotalsPreview
            rows={expectedTotalsRows}
            sourceLabel={expectedTotalsSourceLabel}
          />
          <RunValidationSummary
            checks={readyChecks}
            detectedConcepts={payrollDetectedConcepts}
            detectedPeriod={payrollDetectedPeriod}
            detectedRecords={payrollDetectedRecords}
            readyToExecute={readyToExecute}
          />
          <button
            className="inline-flex w-full items-center justify-center rounded-[20px] bg-surface-ink px-5 py-4 text-base font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
            disabled={executeDisabled}
            onClick={onExecute}
            type="button"
          >
            {executeLabel}
          </button>
        </div>
      </section>
    </div>
  );
}
