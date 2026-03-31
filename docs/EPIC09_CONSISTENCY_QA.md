# EPIC 09 Consistency QA

## Objetivo

Documentar la validacion de la `Card 9.1.2` de `EPIC 09`, centrada en
consistencia entre:

- capa logica
- persistencia
- payloads de API
- UI visible

## Entorno validado

- fecha de validacion: `2026-03-31`
- branch de trabajo: `codex/epic-09-hardening-qa`
- backend local: `http://localhost:8000`
- frontend local: `http://localhost:3000`

## Run usada como referencia

- `run_id`: `ee9e80e7-5fe0-4a3e-a8ef-7f98eb15cf27`
- `run_label`: `EPIC09 QA 2026-03-30T18:14:37`
- `period`: `2026-03`

## Alcance de la validacion

Se comparo:

- `GET /runs/{run_id}/summary`
- `GET /runs/{run_id}/results`
- `GET /runs/{run_id}/results/{result_id}`
- `GET /runs/{run_id}/results/{result_id}/drilldown`
- datos persistidos en:
  - `reconciliation_results`
  - `reconciliation_exceptions`
  - `run_payroll_lines`
- HTML renderizado de:
  - `/runs/{run_id}`
  - `/runs/{run_id}/concepts/{result_id}`
  - `/runs/{run_id}/concepts/{result_id}/drilldown`

El concepto auditado en profundidad fue `MEAL_VOUCHER`, por ser el wow case
principal del MVP.

## Chequeos ejecutados

### Summary vs results

Se verifico que:

- `total_concepts` coincide con la cantidad real de resultados persistidos
- `concepts_unreconciled` coincide con los resultados en estado `Unreconciled`
- `concepts_minor_difference` coincide con los resultados en estado
  `Minor Difference`
- `concepts_reconciled` coincide con los resultados en estado `Reconciled`
- `expected_amount_total` coincide con la suma de resultados
- `observed_amount_total` coincide con la suma de resultados

### Concept analysis vs resultado persistido

Se verifico que:

- el `status` del detalle coincide con `list_results`
- el `absolute_diff` del detalle coincide con `list_results`
- el `header.status` de `concept_analysis` coincide con `result.status`
- el KPI `observed_amount` coincide con `result.observed_amount`
- `evidence_summary.total_exceptions` coincide con la cantidad real de
  excepciones persistidas para el concepto

### Drill-down vs payroll lines persistidas

Se verifico que:

- `total_rows` coincide con la cantidad real de filas persistidas
- `summary.rows_with_exception` coincide con las filas que tienen
  `exception_flags` o `invalid_reasons`
- `summary.exception_types_present` coincide con los tipos efectivamente
  presentes en las filas
- `summary.total_amount` coincide con la suma de `amount` sobre el concepto

### Persistencia vs API

Se verifico que:

- `reconciliation_results` coincide con la longitud de `GET /results`
- `reconciliation_exceptions` coincide con `detail.exceptions`
- `run_payroll_lines` coincide con el drill-down expuesto por API

### API vs UI visible

Se verifico que las rutas renderizadas mantienen visibles los mismos estados y
valores narrativos principales:

- summary con `946,170.00` observado y `950,700.00` expected
- presencia de `MEAL_VOUCHER`, `CHILDCARE`, `OVERTIME`, `TRANSPORT`
- `MEAL_VOUCHER` visible como `Unreconciled`
- drill-down visible con `519` filas y `14` filas con excepcion

## Resultado

Se ejecutaron `21` chequeos de consistencia.

Resultado final:

- `21 / 21` checks OK
- `0` desviaciones detectadas

## Observaciones

### 1. Diferencia valida entre detalle y drill-down

`concept_analysis` para `MEAL_VOUCHER` expone `19` excepciones persistidas,
mientras que el drill-down muestra `14` filas con excepcion visible.

Esto no representa drift porque:

- `concept_analysis` cuenta registros de excepcion persistidos
- drill-down cuenta filas de payroll con al menos una bandera visible
- varias excepciones pueden vivir sobre menos filas unicas
- los `Unmapped Concept` siguen concentrados en concept analysis y en el export
  detail, no en la tabla principal del drill-down

### 2. Matiz de schema relevante para futuras consultas

`exception_flags` e `invalid_reasons` viven en persistencia como `jsonb`, por lo
que consultas SQL de QA deben usar `jsonb_array_length(...)` en vez de
`cardinality(...)`.

No es un bug del producto, pero conviene recordarlo para futuras cards de QA.

## Conclusion

La `Card 9.1.2` queda validada para el alcance MVP.

No se detecto drift visible entre motor, persistencia, API y UI en la run QA de
referencia.

## Siguiente paso recomendado

Avanzar con `Card 9.2.1 — Revisar errores de carga y ejecución de runs`.
