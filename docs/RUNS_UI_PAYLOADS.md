# Runs UI Payloads

## Objetivo

Fijar los contratos de respuesta de `EPIC 04` que el frontend puede consumir
casi directo para summary, concept analysis y drill-down.

Estos contratos viven implementados en `backend/app/schemas/runs.py`.

## 1. Summary UI

El payload de `GET /runs/{run_id}/summary` debe incluir:

- `run`
- `metrics`
- `preview_results`
- `event_log`

### KPIs minimos

- `concepts_reconciled`
- `concepts_minor_difference`
- `concepts_unreconciled`
- `concepts_invalid_incomplete`
- `observed_amount_total`
- `expected_amount_total`
- `overall_run_status`

### Uso esperado en UI

- header de corrida
- KPIs ejecutivos
- tabla preview
- timeline minima de trazabilidad

## 2. Concept Analysis UI

El payload de `GET /runs/{run_id}/results/{result_id}` debe incluir:

- `run`
- `result`
- `exceptions`
- `concept_analysis`
- `event_log`

### Estructura de `concept_analysis`

- `header`
- `kpis`
- `summary_statement`
- `top_causes`
- `recommended_action`
- `evidence_summary`

### Header minimo

- `concept_code_normalized`
- `concept_name_normalized`
- `period`
- `status`

### KPIs minimos

- `observed_amount`
- `expected_amount`
- `absolute_diff`
- `relative_diff_pct`
- `record_count`
- `employee_count`
- `impacted_records_count`
- `impacted_employees_count`
- `explained_amount_estimate`

### Evidence summary

- `total_exceptions`
- `top_exception_types`
- `records_with_exception`
- `employees_with_exception`

## 3. Drill-down UI

El payload de `GET /runs/{run_id}/results/{result_id}/drilldown` debe incluir:

- `run`
- `result`
- `total_rows`
- `summary`
- `filter_context`
- `rows`
- `event_log`

### Summary superior

- `concept_code_normalized`
- `total_rows`
- `total_amount`
- `rows_with_exception`
- `exception_types_present`

### Filter context

- `available_exception_types`
- `legal_entities`
- `countries`

### Columnas base de filas

- `record_id`
- `employee_id`
- `employee_name`
- `legal_entity`
- `concept_code_normalized`
- `concept_name_normalized`
- `amount`
- `payroll_period`
- `exception_flags`
- `invalid_reasons`

## 4. Regla de diseño

El backend debe entregar payloads listos para renderizar, no solo tablas
crudas. El frontend puede formatear visualmente, pero no deberia reconstruir:

- la jerarquia conceptual de detail
- los KPIs principales
- el resumen superior del drill-down
- la bitacora minima de trazabilidad
