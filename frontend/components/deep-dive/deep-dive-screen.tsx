"use client";

import Link from "next/link";
import { useDeferredValue, useState } from "react";

import {
  type RunDrilldownResponse,
  type RunPayrollLineRecord,
  type RunResultDetailResponse,
} from "@/lib/api/client";
import {
  formatCompactNumber,
  formatCurrency,
  formatDateTime,
  formatPercentage,
} from "@/lib/utils/format";
import { getResultStatusMeta } from "@/lib/utils/reconciliation";

import { ExceptionDrilldownTable } from "@/components/drilldown/exception-drilldown-table";
import { AppHeader } from "@/components/ui/app-header";
import { ExportCsvButton } from "@/components/ui/export-csv-button";
import { ExportFileButton } from "@/components/ui/export-file-button";
import { HeaderActionPanel } from "@/components/ui/header-action-panel";
import { MetricCard } from "@/components/ui/metric-card";
import { NoticeBanner } from "@/components/ui/notice-banner";
import { StatusPill } from "@/components/ui/status-pill";

type DeepDiveScreenProps = {
  detail: RunResultDetailResponse;
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

export function DeepDiveScreen({ detail, drilldown }: DeepDiveScreenProps) {
  const [selectedExceptionType, setSelectedExceptionType] = useState("all");
  const [selectedLegalEntity, setSelectedLegalEntity] = useState("all");
  const [employeeQuery, setEmployeeQuery] = useState("");
  const [sortBy, setSortBy] = useState<SortOption>("anomaly_desc");
  const deferredEmployeeQuery = useDeferredValue(employeeQuery.trim().toLowerCase());

  const statusMeta = getResultStatusMeta(detail.concept_analysis.header.status);
  const topCause = detail.concept_analysis.top_causes[0];
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
                  fallbackFileName={`exception-detail-${detail.concept_analysis.header.concept_code_normalized.toLowerCase()}-${detail.run.period}.csv`}
                  href={`/runs/${detail.run.id}/results/${detail.result.id}/exports/detail`}
                  idleLabel="Export evidence CSV"
                />
                <ExportFileButton
                  fallbackFileName={`reconciliation-report-${detail.concept_analysis.header.concept_code_normalized.toLowerCase()}-${detail.run.period}.pdf`}
                  href={`/runs/${detail.run.id}/results/${detail.result.id}/exports/report`}
                  idleLabel="Export PDF report"
                />
                <Link
                  className="inline-flex items-center justify-center rounded-full bg-surface-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
                  href={`/runs/${detail.run.id}`}
                >
                  Back to summary
                </Link>
              </>
            }
            title="Deep Dive"
          >
            <div className="flex items-center gap-2">
              <StatusPill tone={statusMeta.tone}>{statusMeta.label}</StatusPill>
              <span className="font-medium text-foreground">{detail.run.period}</span>
            </div>
            <p className="max-w-xs leading-6 text-text-secondary">
              {detail.run.run_label}
            </p>
          </HeaderActionPanel>
        }
        eyebrow="Deep Dive"
        kicker={detail.concept_analysis.header.concept_code_normalized}
        subtitle="Review the likely causes first, then validate the evidence directly in the detailed records below."
        title={detail.concept_analysis.header.concept_name_normalized}
      />

      <section className="grid gap-4 lg:grid-cols-[1.05fr_0.95fr]">
        <article className="rounded-[24px] border border-border-subtle bg-surface-ink p-5 text-white md:p-6">
          <div className="flex flex-wrap items-center gap-3">
            <StatusPill tone={statusMeta.tone}>{statusMeta.label}</StatusPill>
            <span className="text-sm text-slate-300">
              {detail.concept_analysis.header.period}
            </span>
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Expected Total
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                {formatCurrency(detail.concept_analysis.kpis.expected_amount)}
              </p>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Observed Total
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                {formatCurrency(detail.concept_analysis.kpis.observed_amount)}
              </p>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Absolute Difference
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                {formatCurrency(detail.concept_analysis.kpis.absolute_diff)}
              </p>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Difference %
              </p>
              <p className="mt-2 text-base leading-7 text-slate-100">
                {formatPercentage(detail.concept_analysis.kpis.relative_diff_pct)}
              </p>
            </div>
          </div>
        </article>

        <article className="rounded-[24px] border border-border-subtle bg-white/72 p-5 md:p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            Review summary
          </p>
          <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-foreground">
            {detail.concept_analysis.summary_statement ??
              "A summary statement is not available for this concept yet."}
          </h2>
          <p className="mt-4 text-sm leading-6 text-text-secondary">
            {detail.concept_analysis.recommended_action ??
              "Review the concept-level evidence and confirm the supporting records before closing the period."}
          </p>
        </article>
      </section>

      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          label="Records Analyzed"
          value={formatCompactNumber(detail.concept_analysis.kpis.record_count)}
        />
        <MetricCard
          label="Employees Affected"
          value={formatCompactNumber(
            detail.concept_analysis.kpis.impacted_employees_count ?? impactedEmployees,
          )}
        />
        <MetricCard
          label="Rows With Evidence"
          value={formatCompactNumber(
            detail.concept_analysis.evidence_summary.records_with_exception,
          )}
        />
        <MetricCard
          label="Highest impact anomaly"
          value={topCause?.exception_type ?? "No anomaly detected"}
        />
      </section>

      <section className="grid gap-4 xl:grid-cols-[1.05fr_0.95fr]">
        <article className="rounded-[24px] border border-border-subtle bg-white/75 p-5 md:p-6">
          <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
                Top Causes
              </p>
              <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-foreground">
                Ranked probable causes behind the difference.
              </h2>
            </div>
            <p className="max-w-sm text-sm leading-6 text-text-secondary">
              Start here before scanning every row in the evidence table.
            </p>
          </div>

          <div className="mt-5 space-y-4">
            {detail.concept_analysis.top_causes.length ? (
              detail.concept_analysis.top_causes.map((cause, index) => (
                <article
                  className="rounded-[22px] border border-border-subtle bg-surface p-4"
                  key={cause.id}
                >
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-surface-ink text-sm font-semibold text-white">
                        {index + 1}
                      </span>
                      <div>
                        <p className="font-semibold text-foreground">
                          {cause.exception_type}
                        </p>
                        <p className="text-sm text-text-secondary">
                          Severity {cause.severity} | Scope {cause.scope_level}
                        </p>
                      </div>
                    </div>
                    <div className="text-right text-sm text-text-secondary">
                      <p className="font-mono text-foreground">
                        {cause.estimated_impact_amount
                          ? formatCurrency(cause.estimated_impact_amount)
                          : "Impact N/A"}
                      </p>
                      <p>
                        Confidence{" "}
                        {cause.confidence
                          ? formatPercentage(Number.parseFloat(cause.confidence) * 100, 0)
                          : "N/A"}
                      </p>
                    </div>
                  </div>
                  <p className="mt-4 text-sm leading-6 text-text-secondary">
                    {cause.observation ??
                      "No additional observation was stored for this exception."}
                  </p>
                </article>
              ))
            ) : (
              <NoticeBanner
                detail="This concept does not currently expose ranked exception causes, even though the summary result is available."
                message="No ranked causes were returned for this concept."
                tone="warning"
              />
            )}
          </div>
        </article>

        <article className="rounded-[24px] border border-border-subtle bg-white/75 p-5 md:p-6">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
            Evidence summary
          </p>
          <div className="mt-5 space-y-4">
            <div className="rounded-[20px] border border-border-subtle bg-surface p-4">
              <p className="text-sm font-semibold text-foreground">Exception footprint</p>
              <div className="mt-3 grid gap-3 md:grid-cols-2">
                <MetricCard
                  label="Total Exceptions"
                  value={formatCompactNumber(
                    detail.concept_analysis.evidence_summary.total_exceptions,
                  )}
                />
                <MetricCard
                  label="Employees With Exception"
                  value={formatCompactNumber(
                    detail.concept_analysis.evidence_summary.employees_with_exception,
                  )}
                />
                <MetricCard
                  label="Rows in Deep Dive"
                  value={formatCompactNumber(drilldown.total_rows)}
                />
                <MetricCard
                  label="Total Amount"
                  value={formatCurrency(drilldown.summary.total_amount)}
                />
              </div>
            </div>

            <div className="rounded-[20px] border border-border-subtle bg-surface p-4">
              <p className="text-sm font-semibold text-foreground">
                Top exception types
              </p>
              <div className="mt-3 flex flex-wrap gap-2">
                {detail.concept_analysis.evidence_summary.top_exception_types.length ? (
                  detail.concept_analysis.evidence_summary.top_exception_types.map(
                    (exceptionType) => (
                      <span
                        className="rounded-full border border-border-subtle bg-white px-3 py-1.5 text-xs font-medium text-text-secondary"
                        key={exceptionType}
                      >
                        {exceptionType}
                      </span>
                    ),
                  )
                ) : (
                  <span className="text-sm text-text-secondary">
                    No exception types were returned for this concept.
                  </span>
                )}
              </div>
            </div>
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
              Validate the evidence directly from the same screen.
            </h2>
          </div>
          <p className="max-w-xl text-sm leading-6 text-text-secondary">
            Use light filters to reduce noise, then export the detailed evidence if needed.
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
            This concept does not have detailed rows available yet.
          </h2>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-text-secondary">
            The concept summary is still available, but the backend did not return persisted line-level rows for this concept.
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
            Clear one or more filters to restore the persisted evidence set.
          </p>
        </section>
      )}

      <section className="rounded-[24px] border border-border-subtle bg-white/72 p-5 md:p-6">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-text-muted">
          Recent run events
        </p>
        <div className="mt-4 space-y-4">
          {detail.event_log.slice(-2).map((event) => (
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
      </section>
    </div>
  );
}
