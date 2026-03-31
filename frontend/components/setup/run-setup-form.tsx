import { ExpectedTotalsPreview } from "@/components/setup/expected-totals-preview";
import { RunValidationSummary } from "@/components/setup/run-validation-summary";
import { UploadBox, type UploadBoxState } from "@/components/setup/upload-box";
import { NoticeBanner } from "@/components/ui/notice-banner";
import { StatusPill } from "@/components/ui/status-pill";
import type { ExpectedTotalsPreviewRow } from "@/lib/utils/csv";

type RunSetupFormProps = {
  executeDisabled: boolean;
  executeLabel: string;
  expectedTotalsRows: ExpectedTotalsPreviewRow[];
  expectedTotalsSourceLabel: string;
  feedback?: {
    detail?: string;
    message: string;
    tone: "error" | "info" | "success" | "warning";
  };
  onExecute: () => void;
  onExpectedTotalsAmountChange: (conceptCode: string, nextAmount: string) => void;
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
  executeDisabled,
  executeLabel,
  expectedTotalsRows,
  expectedTotalsSourceLabel,
  feedback,
  onExecute,
  onExpectedTotalsAmountChange,
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
  setupParameters,
  supportFilesReady,
}: RunSetupFormProps) {
  const runReadyLabel = readyToExecute ? "Ready to run" : "Waiting for required files";

  return (
    <div className="space-y-6">
      {feedback ? (
        <NoticeBanner
          detail={feedback.detail}
          message={feedback.message}
          tone={feedback.tone}
        />
      ) : null}

      <section className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-6 rounded-[24px] border border-border-subtle bg-white/70 p-5">
          <div className="space-y-3">
            <div className="flex flex-wrap items-center gap-3">
              <h2 className="text-2xl font-semibold tracking-[-0.03em] text-foreground">
                New reconciliation run
              </h2>
              <StatusPill tone={readyToExecute ? "ready" : "warning"}>
                {readyToExecute ? "Ready" : "In progress"}
              </StatusPill>
            </div>
            <p className="max-w-2xl text-sm leading-6 text-text-secondary">
              Start with the essentials: period, payroll file, expected totals
              and one clear action to run the reconciliation.
            </p>
            <div className="flex flex-wrap gap-2 text-sm text-text-secondary">
              <span className="rounded-full border border-border-subtle bg-surface px-3 py-1.5">
                1. Upload payroll
              </span>
              <span className="rounded-full border border-border-subtle bg-surface px-3 py-1.5">
                2. Confirm totals
              </span>
              <span className="rounded-full border border-border-subtle bg-surface px-3 py-1.5">
                3. Run reconciliation
              </span>
            </div>
          </div>

          <label className="space-y-2">
            <span className="text-sm font-semibold text-foreground">Period</span>
            <input
              className="w-full rounded-2xl border border-border-subtle bg-surface px-4 py-3 text-foreground outline-none transition focus:border-surface-ink"
              onChange={(event) => onUpdatePeriod(event.target.value)}
              placeholder="2026-03"
              value={setupParameters.period}
            />
          </label>

          <UploadBox
            ctaLabel="Upload payroll"
            description="Primary input for the reconciliation. The file is checked in the browser first and then uploaded to the backend."
            onFileSelected={onPayrollUpload}
            state={payrollState}
            title="Payroll file"
          />

          <ExpectedTotalsPreview
            onAmountChange={onExpectedTotalsAmountChange}
            onResetToSeed={onResetExpectedTotalsToDemo}
            rows={expectedTotalsRows}
            sourceLabel={expectedTotalsSourceLabel}
          />

          <div className="rounded-[22px] border border-border-subtle bg-surface p-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="space-y-1">
                <p className="text-sm font-semibold text-foreground">
                  Run status
                </p>
                <p className="text-sm text-text-secondary">{runReadyLabel}</p>
              </div>
              <StatusPill tone={readyToExecute ? "ready" : "warning"}>
                {runReadyLabel}
              </StatusPill>
            </div>
            {payrollDetectedPeriod || payrollDetectedRecords || payrollDetectedConcepts ? (
              <div className="mt-4 grid gap-3 md:grid-cols-3">
                <div className="rounded-[18px] border border-border-subtle bg-white/70 p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.16em] text-text-muted">
                    Records
                  </p>
                  <p className="mt-2 text-2xl font-semibold text-foreground">
                    {payrollDetectedRecords ?? "—"}
                  </p>
                </div>
                <div className="rounded-[18px] border border-border-subtle bg-white/70 p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.16em] text-text-muted">
                    Concepts
                  </p>
                  <p className="mt-2 text-2xl font-semibold text-foreground">
                    {payrollDetectedConcepts ?? "—"}
                  </p>
                </div>
                <div className="rounded-[18px] border border-border-subtle bg-white/70 p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.16em] text-text-muted">
                    Detected period
                  </p>
                  <p className="mt-2 text-2xl font-semibold text-foreground">
                    {payrollDetectedPeriod ?? "Pending"}
                  </p>
                </div>
              </div>
            ) : null}
          </div>

          <details className="rounded-[22px] border border-border-subtle bg-surface p-4">
            <summary className="cursor-pointer list-none text-sm font-semibold text-foreground">
              Advanced settings
            </summary>
            <div className="mt-4 grid gap-4 md:grid-cols-2">
              <label className="space-y-2">
                <span className="text-sm font-semibold text-foreground">
                  Legal entity scope
                </span>
                <input
                  className="w-full rounded-2xl border border-border-subtle bg-white/70 px-4 py-3 text-foreground outline-none transition focus:border-surface-ink"
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
                  className="w-full rounded-2xl border border-border-subtle bg-white/70 px-4 py-3 text-foreground outline-none transition focus:border-surface-ink"
                  onChange={(event) => onUpdateToleranceProfile(event.target.value)}
                  value={setupParameters.toleranceProfileLabel}
                >
                  <option value="mvp-default">MVP default</option>
                  <option value="finance-review">Finance review</option>
                </select>
              </label>
              <label className="space-y-2 md:col-span-2">
                <span className="text-sm font-semibold text-foreground">
                  Exceptions analysis
                </span>
                <div className="flex min-h-[52px] items-center justify-between rounded-2xl border border-border-subtle bg-white/70 px-4 py-3">
                  <div>
                    <p className="text-sm font-medium text-foreground">
                      Keep explanation layer active
                    </p>
                    <p className="text-xs text-text-secondary">
                      Recommended for the simplified MVP flow.
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
          </details>

          <details className="rounded-[22px] border border-border-subtle bg-surface p-4">
            <summary className="cursor-pointer list-none text-sm font-semibold text-foreground">
              Validation and support files
            </summary>
            <div className="mt-4 space-y-6">
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
              <RunValidationSummary
                checks={readyChecks}
                detectedConcepts={payrollDetectedConcepts}
                detectedPeriod={payrollDetectedPeriod}
                detectedRecords={payrollDetectedRecords}
                readyToExecute={readyToExecute}
              />
            </div>
          </details>

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
