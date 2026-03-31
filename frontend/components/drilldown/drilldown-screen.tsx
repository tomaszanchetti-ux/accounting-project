"use client";

import Link from "next/link";
import { useDeferredValue, useState } from "react";

import {
  type RunDrilldownResponse,
  type RunPayrollLineRecord,
} from "@/lib/api/client";
import {
  formatCompactNumber,
  formatCurrency,
  formatDateTime,
} from "@/lib/utils/format";
import { getResultStatusMeta } from "@/lib/utils/reconciliation";

import { ExceptionDrilldownTable } from "@/components/drilldown/exception-drilldown-table";
import { AppHeader } from "@/components/ui/app-header";
import { ExportCsvButton } from "@/components/ui/export-csv-button";
import { HeaderActionPanel } from "@/components/ui/header-action-panel";
import { MetricCard } from "@/components/ui/metric-card";
import { NoticeBanner } from "@/components/ui/notice-banner";
import { StatusPill } from "@/components/ui/status-pill";

type DrilldownScreenProps = {
  drilldown: RunDrilldownResponse;
};

type SortOption = "amount_desc" | "anomaly_desc" | "employee_asc";

function rowMatchesException(
  row: RunPayrollLineRecord,
  selectedExceptionType: string,
) {
  if (selectedExceptionType === "all") {
    return true;
  }

  return (
    row.exception_flags.includes(selectedExceptionType) ||
    row.invalid_reasons.includes(selectedExceptionType)
  );
}

function getRowAnomalyRank(row: RunPayrollLineRecord) {
  if (row.invalid_reasons.length) {
    return 2 + row.invalid_reasons.length;
  }

  if (row.exception_flags.length) {
    return 1 + row.exception_flags.length;
  }

  return 0;
}

function getRowAmountValue(row: RunPayrollLineRecord) {
  const parsedAmount = row.amount ? Number.parseFloat(row.amount) : 0;
  return Number.isFinite(parsedAmount) ? Math.abs(parsedAmount) : 0;
}

function getEmployeeSearchTarget(row: RunPayrollLineRecord) {
  return `${row.employee_id ?? ""} ${row.employee_name ?? ""}`.toLowerCase();
}

export function DrilldownScreen({ drilldown }: DrilldownScreenProps) {
  const [selectedExceptionType, setSelectedExceptionType] = useState("all");
  const [selectedLegalEntity, setSelectedLegalEntity] = useState("all");
  const [employeeQuery, setEmployeeQuery] = useState("");
  const [sortBy, setSortBy] = useState<SortOption>("anomaly_desc");
  const deferredEmployeeQuery = useDeferredValue(employeeQuery.trim().toLowerCase());

  const statusMeta = getResultStatusMeta(drilldown.result.status);
  const shouldShowLegalEntityFilter =
    drilldown.filter_context.legal_entities.length > 1;
  const filteredRows = drilldown.rows
    .filter((row) => rowMatchesException(row, selectedExceptionType))
    .filter((row) =>
      selectedLegalEntity === "all" ? true : row.legal_entity === selectedLegalEntity,
    )
    .filter((row) =>
      deferredEmployeeQuery
        ? getEmployeeSearchTarget(row).includes(deferredEmployeeQuery)
        : true,
    )
    .sort((left, right) => {
      if (sortBy === "amount_desc") {
        return getRowAmountValue(right) - getRowAmountValue(left);
      }

      if (sortBy === "employee_asc") {
        return (left.employee_id ?? "").localeCompare(right.employee_id ?? "");
      }

      const anomalyRankDiff = getRowAnomalyRank(right) - getRowAnomalyRank(left);
      if (anomalyRankDiff !== 0) {
        return anomalyRankDiff;
      }

      return getRowAmountValue(right) - getRowAmountValue(left);
    });

  const impactedEmployees = new Set(
    drilldown.rows
      .filter((row) => row.exception_flags.length || row.invalid_reasons.length)
      .map((row) => row.employee_id ?? row.employee_name ?? row.record_id),
  ).size;

  return (
    <div className="space-y-6">
      <AppHeader
        actions={
          <HeaderActionPanel
            actions={
              <>
                <ExportCsvButton
                  fallbackFileName={`exception-detail-${drilldown.result.concept_code_normalized.toLowerCase()}-${drilldown.run.period}.csv`}
                  href={`/runs/${drilldown.run.id}/results/${drilldown.result.id}/exports/detail`}
                  idleLabel="Export detail CSV"
                />
                <Link
                  className="inline-flex items-center justify-center rounded-full border border-border-subtle bg-white px-4 py-2 text-sm font-semibold text-foreground transition hover:border-surface-ink hover:bg-surface-ink hover:text-white"
                  href={`/runs/${drilldown.run.id}/concepts/${drilldown.result.id}`}
                >
                  Back to concept
                </Link>
                <Link
                  className="inline-flex items-center justify-center rounded-full bg-surface-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
                  href={`/runs/${drilldown.run.id}`}
                >
                  Back to summary
                </Link>
              </>
            }
            title="Drill-down Context"
          >
            <div className="flex items-center gap-2">
              <StatusPill tone={statusMeta.tone}>{statusMeta.label}</StatusPill>
              <span className="font-medium text-foreground">{drilldown.run.period}</span>
            </div>
            <p className="max-w-xs leading-6 text-text-secondary">
              {drilldown.run.run_label}
            </p>
            <div className="space-y-1 font-mono text-xs text-text-muted">
              <p>{drilldown.run.id}</p>
              <p>{drilldown.run.source_file_name ?? "Source file pending"}</p>
              <p>{drilldown.run.rules_version ?? "rules unavailable"}</p>
            </div>
          </HeaderActionPanel>
        }
        eyebrow="Drill-down"
        kicker={drilldown.result.concept_code_normalized}
        subtitle="This workspace turns the concept explanation into record-level evidence so the user can validate where the difference sits, who it touches and what anomaly pattern deserves review first."
        title={`Detailed records for ${drilldown.result.concept_name_normalized}`}
      />

      <section className="grid gap-4 lg:grid-cols-[1.05fr_0.95fr]">
        <article className="rounded-[24px] border border-border-subtle bg-surface-ink p-5 text-white md:p-6">
          <div className="flex flex-wrap items-center gap-3">
            <StatusPill tone={statusMeta.tone}>{statusMeta.label}</StatusPill>
            <span className="text-sm text-slate-300">{drilldown.result.period}</span>
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Run
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                {drilldown.run.run_label}
              </p>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Processed File
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                {drilldown.run.source_file_name ?? "No source file recorded"}
              </p>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Review focus
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                Prioritize anomalous rows first, then scan clean rows only if
                balance confirmation is still needed.
              </p>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Recommended next step
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                {drilldown.result.recommended_action ?? "Review the detailed records."}
              </p>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Rules Version
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                {drilldown.run.rules_version ?? "Rules version unavailable"}
              </p>
            </div>
          </div>
        </article>

        <article className="rounded-[24px] border border-border-subtle bg-white/72 p-5 md:p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            Evidence summary
          </p>
          <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-foreground">
            The table below is the auditable evidence layer for this concept.
          </h2>
          <p className="mt-3 text-sm leading-6 text-text-secondary">
            Use the filters to isolate a specific anomaly family or employee. The
            default order keeps the rows with the strongest anomaly signal first.
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            {drilldown.summary.exception_types_present.length ? (
              drilldown.summary.exception_types_present.map((exceptionType) => (
                <StatusPill key={exceptionType} tone="warning">
                  {exceptionType}
                </StatusPill>
              ))
            ) : (
              <StatusPill tone="success">No persisted anomalies</StatusPill>
            )}
          </div>
        </article>
      </section>

      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          label="Impacted Records"
          value={formatCompactNumber(drilldown.summary.rows_with_exception)}
        />
        <MetricCard
          label="Employees Affected"
          value={formatCompactNumber(
            drilldown.result.impacted_employees_count ?? impactedEmployees,
          )}
        />
        <MetricCard
          label="Total Rows"
          value={formatCompactNumber(drilldown.total_rows)}
        />
        <MetricCard
          label="Total Amount"
          value={formatCurrency(drilldown.summary.total_amount)}
        />
      </section>

      <NoticeBanner
        detail="This drill-down stays intentionally analytical: no edits, no approvals and no remediation workflow. The goal is to validate evidence fast and export it later."
        message="Review context first, then use the table to confirm the exact rows behind the difference."
        tone="info"
      />

      <section className="grid gap-4 xl:grid-cols-[0.95fr_1.05fr]">
        <article className="rounded-[24px] border border-border-subtle bg-white/75 p-5 md:p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            Traceability
          </p>
          <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-foreground">
            Every row in this view comes from persisted payroll evidence.
          </h2>
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <MetricCard
              label="Run Record Count"
              value={formatCompactNumber(drilldown.run.record_count)}
            />
            <MetricCard
              label="Completed At"
              value={formatDateTime(drilldown.run.completed_at)}
            />
          </div>
        </article>

        <article className="rounded-[24px] border border-border-subtle bg-white/72 p-5 md:p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            Run Events
          </p>
          <div className="mt-4 space-y-4">
            {drilldown.event_log.slice(-3).map((event) => (
              <div className="border-l border-border-subtle pl-4" key={event.event_code}>
                <p className="text-sm font-semibold text-foreground">{event.title}</p>
                <p className="mt-1 text-sm leading-6 text-text-secondary">
                  {event.detail}
                </p>
                <p className="mt-1 text-xs text-text-muted">
                  {formatDateTime(event.event_at)}
                </p>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="rounded-[24px] border border-border-subtle bg-white/72 p-5 md:p-6">
        <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
              Filters and Ordering
            </p>
            <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-foreground">
              Reduce noise before reviewing line-level evidence.
            </h2>
          </div>
          <p className="max-w-xl text-sm leading-6 text-text-secondary">
            Filters are intentionally light. They narrow the evidence set without
            turning the MVP into a transaction workspace.
          </p>
        </div>

        <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          <label className="space-y-2">
            <span className="text-xs font-semibold uppercase tracking-[0.14em] text-text-muted">
              Exception Type
            </span>
            <select
              className="w-full rounded-[18px] border border-border-subtle bg-surface px-4 py-3 text-sm text-foreground outline-none transition focus:border-surface-ink"
              onChange={(event) => setSelectedExceptionType(event.target.value)}
              value={selectedExceptionType}
            >
              <option value="all">All anomalies</option>
              {drilldown.filter_context.available_exception_types.map((exceptionType) => (
                <option key={exceptionType} value={exceptionType}>
                  {exceptionType}
                </option>
              ))}
            </select>
          </label>

          <label className="space-y-2">
            <span className="text-xs font-semibold uppercase tracking-[0.14em] text-text-muted">
              Employee
            </span>
            <input
              className="w-full rounded-[18px] border border-border-subtle bg-surface px-4 py-3 text-sm text-foreground outline-none transition placeholder:text-text-muted focus:border-surface-ink"
              onChange={(event) => setEmployeeQuery(event.target.value)}
              placeholder="Search by id or name"
              value={employeeQuery}
            />
          </label>

          {shouldShowLegalEntityFilter ? (
            <label className="space-y-2">
              <span className="text-xs font-semibold uppercase tracking-[0.14em] text-text-muted">
                Legal Entity
              </span>
              <select
                className="w-full rounded-[18px] border border-border-subtle bg-surface px-4 py-3 text-sm text-foreground outline-none transition focus:border-surface-ink"
                onChange={(event) => setSelectedLegalEntity(event.target.value)}
                value={selectedLegalEntity}
              >
                <option value="all">All legal entities</option>
                {drilldown.filter_context.legal_entities.map((legalEntity) => (
                  <option key={legalEntity} value={legalEntity}>
                    {legalEntity}
                  </option>
                ))}
              </select>
            </label>
          ) : null}

          <label className="space-y-2">
            <span className="text-xs font-semibold uppercase tracking-[0.14em] text-text-muted">
              Order By
            </span>
            <select
              className="w-full rounded-[18px] border border-border-subtle bg-surface px-4 py-3 text-sm text-foreground outline-none transition focus:border-surface-ink"
              onChange={(event) => setSortBy(event.target.value as SortOption)}
              value={sortBy}
            >
              <option value="anomaly_desc">Anomaly severity</option>
              <option value="amount_desc">Highest amount</option>
              <option value="employee_asc">Employee ID</option>
            </select>
          </label>
        </div>

        <div className="mt-4 flex flex-wrap items-center gap-3 text-sm text-text-secondary">
          <span className="rounded-full border border-border-subtle bg-surface px-3 py-2">
            Showing {formatCompactNumber(filteredRows.length)} of{" "}
            {formatCompactNumber(drilldown.total_rows)} rows
          </span>
          <button
            className="inline-flex items-center justify-center rounded-full border border-border-subtle bg-white px-3 py-2 font-semibold text-foreground transition hover:border-surface-ink hover:bg-surface-ink hover:text-white"
            onClick={() => {
              setSelectedExceptionType("all");
              setSelectedLegalEntity("all");
              setEmployeeQuery("");
              setSortBy("anomaly_desc");
            }}
            type="button"
          >
            Reset filters
          </button>
        </div>
      </section>

      {!drilldown.total_rows ? (
        <section className="rounded-[24px] border border-border-subtle bg-white/72 p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            No persisted records
          </p>
          <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-foreground">
            This concept does not have drill-down rows available yet.
          </h2>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-text-secondary">
            The run and concept context are still available, but the backend did
            not return persisted line-level rows for this concept. This protects
            the user from landing on a broken or ambiguous table.
          </p>
        </section>
      ) : filteredRows.length ? (
        <ExceptionDrilldownTable rows={filteredRows} />
      ) : (
        <section className="rounded-[24px] border border-border-subtle bg-white/72 p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            No matching rows
          </p>
          <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-foreground">
            The current filters hide every record in this concept.
          </h2>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-text-secondary">
            Clear one or more filters to restore the persisted evidence set. This
            empty state makes it explicit that the result is filter-driven, not a
            missing dataset.
          </p>
        </section>
      )}
    </div>
  );
}
