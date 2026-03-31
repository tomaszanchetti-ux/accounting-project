"use client";

import { useRouter } from "next/navigation";
import { useMemo, useState } from "react";

import {
  createRun,
  executeRun,
  uploadRunFile,
  type BackendHealthStatus,
  type RunRecord,
} from "@/lib/api/client";
import {
  parsePayrollPreview,
  serializeExpectedTotalsPreview,
  type ExpectedTotalsPreviewRow,
} from "@/lib/utils/csv";
import { EmptyState } from "@/components/ui/empty-state";
import { NoticeBanner } from "@/components/ui/notice-banner";
import { RunSetupForm } from "@/components/setup/run-setup-form";

type SetupWorkspaceProps = {
  backendHealth: BackendHealthStatus;
  defaultPeriod: string;
  demoExpectedTotals: ExpectedTotalsPreviewRow[];
  seedFiles: {
    conceptMaster: {
      content: string;
      fileName: string;
    };
    employeeReference: {
      content: string;
      fileName: string;
    };
    expectedTotals: {
      content: string;
      fileName: string;
    };
  };
};

type FeedbackState = {
  detail?: string;
  message: string;
  tone: "error" | "info" | "success" | "warning";
} | null;

type UploadState = {
  fileName?: string;
  helperText?: string;
  metadata?: string;
  sizeBytes?: number;
  status: "error" | "loading" | "pending" | "uploaded";
};

const pendingUploadState: UploadState = {
  helperText: "No file registered yet.",
  status: "pending",
};

function buildRunLabel(period: string) {
  return `Payroll reconciliation ${period}`;
}

function buildSeedFile(fileName: string, content: string) {
  return new File([content], fileName, { type: "text/csv" });
}

function buildExpectedTotalsFile(rows: ExpectedTotalsPreviewRow[]) {
  return new File(
    [serializeExpectedTotalsPreview(rows)],
    "expected_totals_manual.csv",
    { type: "text/csv" },
  );
}

function buildExecutionFeedback(run: RunRecord): NonNullable<FeedbackState> | null {
  if (run.status === "INVALID_INPUT") {
    return {
      message: "Run requires corrected inputs",
      detail:
        run.error_message ??
        "One or more required files are missing or inconsistent for the selected period.",
      tone: "error",
    };
  }

  if (run.status === "FAILED") {
    return {
      message: "Run failed during execution",
      detail:
        run.error_message ??
        "The run stopped because of a technical error. Review the inputs and try again.",
      tone: "error",
    };
  }

  return null;
}

export function SetupWorkspace({
  backendHealth,
  defaultPeriod,
  demoExpectedTotals,
  seedFiles,
}: SetupWorkspaceProps) {
  const router = useRouter();
  const [run, setRun] = useState<RunRecord | null>(null);
  const [feedback, setFeedback] = useState<FeedbackState>(null);
  const [isPreparingRun, setIsPreparingRun] = useState(false);
  const [isExecuting, setIsExecuting] = useState(false);
  const [payrollState, setPayrollState] = useState<UploadState>(pendingUploadState);
  const [, setExpectedTotalsState] = useState<UploadState>({
    fileName: "expected_totals_manual.csv",
    helperText: "Seed values loaded and ready to edit.",
    metadata: `${demoExpectedTotals.length} concepts ready`,
    status: "uploaded",
  });
  const [expectedTotalsRows, setExpectedTotalsRows] =
    useState<ExpectedTotalsPreviewRow[]>(demoExpectedTotals);
  const [expectedTotalsSourceLabel, setExpectedTotalsSourceLabel] = useState(
    "Manual entry prefilled from seed",
  );
  const [expectedTotalsDirty, setExpectedTotalsDirty] = useState(true);
  const [setupParameters, setSetupParameters] = useState({
    includeExceptionsAnalysis: true,
    legalEntityScope: "ARD Spain SL",
    period: defaultPeriod,
    toleranceProfileLabel: "mvp-default",
  });
  const [supportFilesReady, setSupportFilesReady] = useState({
    conceptMaster: false,
    employeeReference: false,
  });
  const [payrollDetectedRecords, setPayrollDetectedRecords] = useState<number | null>(
    null,
  );
  const [payrollDetectedConcepts, setPayrollDetectedConcepts] = useState<number | null>(
    null,
  );
  const [payrollDetectedPeriod, setPayrollDetectedPeriod] = useState<string | null>(
    null,
  );

  const readyChecks = useMemo(() => {
    return [
      {
        description: "An active run exists and keeps the setup lifecycle anchored.",
        label: "Run created",
        ready: Boolean(run),
      },
      {
        description: "Expected totals are available and will be synced when the run executes.",
        label: "Expected totals ready",
        ready: expectedTotalsRows.length > 0,
      },
      {
        description: "Payroll CSV must be uploaded before execution.",
        label: "Payroll attached",
        ready: payrollState.status === "uploaded",
      },
      {
        description: "Supporting reference files stay hidden but available in the run.",
        label: "Support files ready",
        ready:
          supportFilesReady.conceptMaster && supportFilesReady.employeeReference,
      },
      {
        description: "Detected payroll period should match the target period.",
        label: "Period aligned",
        ready:
          payrollDetectedPeriod === null ||
          payrollDetectedPeriod === setupParameters.period,
      },
    ];
  }, [
    expectedTotalsRows.length,
    payrollDetectedPeriod,
    payrollState.status,
    run,
    setupParameters.period,
    supportFilesReady.conceptMaster,
    supportFilesReady.employeeReference,
  ]);

  const readyToExecute = readyChecks.every((item) => item.ready);

  async function startRun() {
    if (run || isPreparingRun) {
      return;
    }

    setIsPreparingRun(true);
      setFeedback({
        message: "Creating reconciliation run",
        detail: "Preparing the run and loading the default reference files.",
        tone: "info",
      });

    try {
      const created = await createRun({
        legal_entity_scope: setupParameters.legalEntityScope || undefined,
        period: setupParameters.period,
        run_label: buildRunLabel(setupParameters.period),
        tolerance_profile_label: setupParameters.toleranceProfileLabel,
      });

      const nextRun = created.run;
      setRun(nextRun);

      const [conceptMasterUpload, employeeReferenceUpload] = await Promise.all([
        uploadRunFile(
          nextRun.id,
          "concept_master",
          buildSeedFile(
            seedFiles.conceptMaster.fileName,
            seedFiles.conceptMaster.content,
          ),
        ),
        uploadRunFile(
          nextRun.id,
          "employee_reference",
          buildSeedFile(
            seedFiles.employeeReference.fileName,
            seedFiles.employeeReference.content,
          ),
        ),
      ]);

      setSupportFilesReady({
        conceptMaster: Boolean(conceptMasterUpload.uploaded_file.id),
        employeeReference: Boolean(employeeReferenceUpload.uploaded_file.id),
      });
      setFeedback({
        message: "Run ready",
        detail:
          "Upload the payroll file, confirm the expected totals and run the reconciliation.",
        tone: "success",
      });
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unable to prepare the run.";
      setFeedback({
        message: "Run preparation failed",
        detail: message,
        tone: "error",
      });
    } finally {
      setIsPreparingRun(false);
    }
  }

  async function handlePayrollUpload(file: File) {
    if (!run) {
      setFeedback({
        message: "Create a run first",
        detail: "The setup needs an active run before files can be attached.",
        tone: "warning",
      });
      return;
    }

    setPayrollState({
      fileName: file.name,
      helperText: "Uploading payroll file...",
      sizeBytes: file.size,
      status: "loading",
    });

    try {
      const fileText = await file.text();
      const preview = parsePayrollPreview(fileText);
      const response = await uploadRunFile(run.id, "payroll", file);

      setPayrollDetectedRecords(preview.recordCount);
      setPayrollDetectedConcepts(preview.conceptCount);
      setPayrollDetectedPeriod(preview.detectedPeriod);
      setPayrollState({
        fileName: response.uploaded_file.file_name,
        helperText: "Payroll uploaded and linked to the run.",
        metadata: `${preview.recordCount} rows • ${preview.conceptCount} concepts`,
        sizeBytes: file.size,
        status: "uploaded",
      });
      setFeedback({
        message: "Payroll loaded",
        detail:
          preview.detectedPeriod && preview.detectedPeriod !== setupParameters.period
            ? `Detected payroll period ${preview.detectedPeriod}. Review the target period before execution.`
            : "Payroll file is now part of the active run.",
        tone:
          preview.detectedPeriod && preview.detectedPeriod !== setupParameters.period
            ? "warning"
            : "success",
      });
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Payroll upload failed.";
      setPayrollState({
        fileName: file.name,
        helperText: message,
        sizeBytes: file.size,
        status: "error",
      });
      setFeedback({
        message: "Payroll upload failed",
        detail: message,
        tone: "error",
      });
    }
  }

  function handleExpectedTotalsAmountChange(
    conceptCode: string,
    nextAmount: string,
  ) {
    const parsedAmount = Number.parseFloat(nextAmount);

    setExpectedTotalsRows((current) =>
      current.map((row) =>
        row.conceptCode === conceptCode
          ? {
              ...row,
              expectedAmount: Number.isFinite(parsedAmount) ? parsedAmount : 0,
            }
          : row,
      ),
    );
    setExpectedTotalsDirty(true);
    setExpectedTotalsSourceLabel("Manual entry");
    setExpectedTotalsState({
      fileName: "expected_totals_manual.csv",
      helperText: "Manual values will be synced automatically when you run the reconciliation.",
      metadata: `${expectedTotalsRows.length} concepts ready`,
      status: "uploaded",
    });
  }

  function resetExpectedTotalsToDemo() {
    setExpectedTotalsRows(demoExpectedTotals);
    setExpectedTotalsDirty(true);
    setExpectedTotalsSourceLabel("Manual entry prefilled from seed");
    setExpectedTotalsState({
      fileName: "expected_totals_manual.csv",
      helperText: "Seed values restored. They will be synced automatically when you run the reconciliation.",
      metadata: `${demoExpectedTotals.length} concepts ready`,
      status: "uploaded",
    });
    setFeedback({
      message: "Expected totals restored",
      detail: "The manual values were reset to the default seed amounts.",
      tone: "info",
    });
  }

  async function handleExecuteRun() {
    if (!run || isExecuting || !readyToExecute) {
      return;
    }

    setIsExecuting(true);
      setFeedback({
        message: "Executing reconciliation",
        detail: "The backend is processing the files and preparing the results.",
        tone: "info",
      });

    try {
      if (!expectedTotalsRows.length) {
        throw new Error("Expected totals are required before running reconciliation.");
      }

      if (expectedTotalsDirty) {
        setExpectedTotalsState({
          fileName: "expected_totals_manual.csv",
          helperText: "Syncing manual expected totals...",
          metadata: `${expectedTotalsRows.length} concepts ready`,
          status: "loading",
        });

        const response = await uploadRunFile(
          run.id,
          "expected_totals",
          buildExpectedTotalsFile(expectedTotalsRows),
        );

        setExpectedTotalsState({
          fileName: response.uploaded_file.file_name,
          helperText: "Manual expected totals synced to the run.",
          metadata: `${expectedTotalsRows.length} concepts ready`,
          status: "uploaded",
        });
        setExpectedTotalsDirty(false);
      }

      const execution = await executeRun(run.id);
      setRun(execution.run);
      const executionFeedback = buildExecutionFeedback(execution.run);

      if (executionFeedback) {
        setFeedback(executionFeedback);
        return;
      }
      setFeedback({
        message: "Run executed successfully",
        detail: "Opening the results now.",
        tone: "success",
      });
      router.push(`/runs/${run.id}`);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Run execution failed.";
      setFeedback({
        message: "Run execution failed",
        detail: message,
        tone: "error",
      });
    } finally {
      setIsExecuting(false);
    }
  }

  return (
    <div className="space-y-6">
      {!backendHealth.ok ? (
        <NoticeBanner
          detail={`API base URL: ${backendHealth.apiBaseUrl}`}
          message="Backend is not reachable from the frontend."
          tone="warning"
        />
      ) : null}

      {!run ? (
        <EmptyState
          action={
            <button
              className="inline-flex w-full items-center justify-center rounded-full bg-white px-4 py-3 text-sm font-semibold text-surface-ink transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:bg-slate-300"
              disabled={!backendHealth.ok || isPreparingRun}
              onClick={startRun}
              type="button"
            >
              {isPreparingRun ? "Preparing setup..." : "Start new reconciliation run"}
            </button>
          }
        />
      ) : (
        <RunSetupForm
          executeDisabled={!readyToExecute || isExecuting}
          executeLabel={isExecuting ? "Running reconciliation..." : "Run Reconciliation"}
          expectedTotalsRows={expectedTotalsRows}
          expectedTotalsSourceLabel={expectedTotalsSourceLabel}
          feedback={feedback ?? undefined}
          onExecute={handleExecuteRun}
          onExpectedTotalsAmountChange={handleExpectedTotalsAmountChange}
          onPayrollUpload={handlePayrollUpload}
          onResetExpectedTotalsToDemo={resetExpectedTotalsToDemo}
          onUpdateIncludeExceptions={(checked) =>
            setSetupParameters((current) => ({
              ...current,
              includeExceptionsAnalysis: checked,
            }))
          }
          onUpdateLegalEntityScope={(value) =>
            setSetupParameters((current) => ({
              ...current,
              legalEntityScope: value,
            }))
          }
          onUpdatePeriod={(value) =>
            setSetupParameters((current) => ({
              ...current,
              period: value,
            }))
          }
          onUpdateToleranceProfile={(value) =>
            setSetupParameters((current) => ({
              ...current,
              toleranceProfileLabel: value,
            }))
          }
          payrollDetectedConcepts={payrollDetectedConcepts}
          payrollDetectedPeriod={payrollDetectedPeriod}
          payrollDetectedRecords={payrollDetectedRecords}
          payrollState={payrollState}
          readyChecks={readyChecks}
          readyToExecute={readyToExecute}
          setupParameters={setupParameters}
          supportFilesReady={supportFilesReady}
        />
      )}
    </div>
  );
}
