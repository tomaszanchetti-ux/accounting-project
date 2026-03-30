"use client";

import { useMemo, useState } from "react";

import {
  createRun,
  executeRun,
  getRunSummary,
  registerRunFileReference,
  uploadRunFile,
  type BackendHealthStatus,
  type RunRecord,
  type RunSummaryResponse,
} from "@/lib/api/client";
import {
  parseExpectedTotalsPreview,
  parsePayrollPreview,
  type ExpectedTotalsPreviewRow,
} from "@/lib/utils/csv";
import { formatDateTime } from "@/lib/utils/format";
import { EmptyState } from "@/components/ui/empty-state";
import { NoticeBanner } from "@/components/ui/notice-banner";
import { RunSetupForm } from "@/components/setup/run-setup-form";
import { RunSummarySnapshot } from "@/components/setup/run-summary-snapshot";

type SetupWorkspaceProps = {
  backendHealth: BackendHealthStatus;
  defaultPeriod: string;
  demoExpectedTotals: ExpectedTotalsPreviewRow[];
  referenceFiles: {
    conceptMasterPath: string;
    employeeReferencePath: string;
    expectedTotalsPath: string;
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

export function SetupWorkspace({
  backendHealth,
  defaultPeriod,
  demoExpectedTotals,
  referenceFiles,
}: SetupWorkspaceProps) {
  const [run, setRun] = useState<RunRecord | null>(null);
  const [summary, setSummary] = useState<RunSummaryResponse | null>(null);
  const [feedback, setFeedback] = useState<FeedbackState>(null);
  const [isPreparingRun, setIsPreparingRun] = useState(false);
  const [isExecuting, setIsExecuting] = useState(false);
  const [payrollState, setPayrollState] = useState<UploadState>(pendingUploadState);
  const [expectedTotalsState, setExpectedTotalsState] = useState<UploadState>({
    helperText: "Demo seed totals will be attached when the run starts.",
    status: "pending",
  });
  const [expectedTotalsRows, setExpectedTotalsRows] =
    useState<ExpectedTotalsPreviewRow[]>(demoExpectedTotals);
  const [expectedTotalsSourceLabel, setExpectedTotalsSourceLabel] = useState(
    "Demo seed reference",
  );
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
        description: "Demo seed expected totals or an uploaded replacement are registered.",
        label: "Expected totals ready",
        ready: expectedTotalsState.status === "uploaded",
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
    expectedTotalsState.status,
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
      message: "Creating run workspace",
      detail: "Registering demo seed references and preparing the setup shell.",
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

      const [expectedTotalsUpload, conceptMasterUpload, employeeReferenceUpload] =
        await Promise.all([
          registerRunFileReference(nextRun.id, {
            file_name: "expected_totals.csv",
            file_type: "expected_totals",
            storage_path: referenceFiles.expectedTotalsPath,
          }),
          registerRunFileReference(nextRun.id, {
            file_name: "concept_master.csv",
            file_type: "concept_master",
            storage_path: referenceFiles.conceptMasterPath,
          }),
          registerRunFileReference(nextRun.id, {
            file_name: "employee_reference.csv",
            file_type: "employee_reference",
            storage_path: referenceFiles.employeeReferencePath,
          }),
        ]);

      setExpectedTotalsState({
        fileName: expectedTotalsUpload.uploaded_file.file_name,
        helperText: "Using demo seed expected totals as default reference.",
        metadata: `Registered ${formatDateTime(
          expectedTotalsUpload.uploaded_file.uploaded_at,
        )}`,
        status: "uploaded",
      });
      setSupportFilesReady({
        conceptMaster: Boolean(conceptMasterUpload.uploaded_file.id),
        employeeReference: Boolean(employeeReferenceUpload.uploaded_file.id),
      });
      setFeedback({
        message: "Run ready for input",
        detail:
          "The setup workspace is active. Upload payroll or replace expected totals if needed.",
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

  async function handleExpectedTotalsUpload(file: File) {
    if (!run) {
      setFeedback({
        message: "Create a run first",
        detail: "The setup needs an active run before files can be attached.",
        tone: "warning",
      });
      return;
    }

    setExpectedTotalsState({
      fileName: file.name,
      helperText: "Uploading expected totals...",
      sizeBytes: file.size,
      status: "loading",
    });

    try {
      const fileText = await file.text();
      const previewRows = parseExpectedTotalsPreview(fileText);
      const response = await uploadRunFile(run.id, "expected_totals", file);

      setExpectedTotalsRows(previewRows);
      setExpectedTotalsSourceLabel("Uploaded expected totals");
      setExpectedTotalsState({
        fileName: response.uploaded_file.file_name,
        helperText: "Expected totals uploaded and replacing the demo reference.",
        metadata: `${previewRows.length} concepts ready`,
        sizeBytes: file.size,
        status: "uploaded",
      });
      setFeedback({
        message: "Expected totals updated",
        detail: "The run will use the uploaded reference file on execution.",
        tone: "success",
      });
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Expected totals upload failed.";
      setExpectedTotalsState({
        fileName: file.name,
        helperText: message,
        sizeBytes: file.size,
        status: "error",
      });
      setFeedback({
        message: "Expected totals upload failed",
        detail: message,
        tone: "error",
      });
    }
  }

  async function resetExpectedTotalsToDemo() {
    if (!run) {
      return;
    }

    setExpectedTotalsState({
      fileName: "expected_totals.csv",
      helperText: "Re-registering demo seed reference...",
      status: "loading",
    });

    try {
      const response = await registerRunFileReference(run.id, {
        file_name: "expected_totals.csv",
        file_type: "expected_totals",
        storage_path: referenceFiles.expectedTotalsPath,
      });

      setExpectedTotalsRows(demoExpectedTotals);
      setExpectedTotalsSourceLabel("Demo seed reference");
      setExpectedTotalsState({
        fileName: response.uploaded_file.file_name,
        helperText: "Demo seed expected totals restored.",
        metadata: `${demoExpectedTotals.length} concepts ready`,
        status: "uploaded",
      });
      setFeedback({
        message: "Demo expected totals restored",
        detail: "The default reference file is active again for this run.",
        tone: "info",
      });
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unable to restore demo seed.";
      setExpectedTotalsState({
        fileName: "expected_totals.csv",
        helperText: message,
        status: "error",
      });
      setFeedback({
        message: "Demo reference could not be restored",
        detail: message,
        tone: "error",
      });
    }
  }

  async function handleExecuteRun() {
    if (!run || isExecuting || !readyToExecute) {
      return;
    }

    setIsExecuting(true);
    setFeedback({
      message: "Executing reconciliation",
      detail: "The backend is processing the run and preparing the summary payload.",
      tone: "info",
    });

    try {
      const execution = await executeRun(run.id);
      setRun(execution.run);
      const nextSummary = await getRunSummary(run.id);
      setSummary(nextSummary);
      setFeedback({
        message: "Run executed successfully",
        detail:
          "Summary payload, preview results and event trace are now available below.",
        tone: "success",
      });
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
          backendReachable={backendHealth.ok}
          executeDisabled={!readyToExecute || isExecuting}
          executeLabel={isExecuting ? "Running reconciliation..." : "Run Reconciliation"}
          expectedTotalsRows={expectedTotalsRows}
          expectedTotalsSourceLabel={expectedTotalsSourceLabel}
          expectedTotalsState={expectedTotalsState}
          feedback={feedback ?? undefined}
          onExecute={handleExecuteRun}
          onExpectedTotalsUpload={handleExpectedTotalsUpload}
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
          run={run}
          setupParameters={setupParameters}
          supportFilesReady={supportFilesReady}
        />
      )}

      {summary ? <RunSummarySnapshot summary={summary} /> : null}
    </div>
  );
}
