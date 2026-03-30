# Exports MVP

## Alcance confirmado

Los exportables minimos de `EPIC 07` son:

- `Reconciliation Summary Export`
- `Exception Detail Export`

Formato principal aprobado:

- `CSV`

Decision de alcance:

- `Excel` no entra en esta fase
- no se construyen archivos multi-sheet
- no se agregan layouts de presentacion ni decoracion visual

## Reconciliation Summary Export

Objetivo:

- llevar fuera de la UI la tabla principal por concepto
- permitir seguimiento o sharing rapido sin depender de la pantalla

Columnas confirmadas:

- `run_label`
- `period`
- `concept_code`
- `concept_name`
- `expected_amount`
- `observed_amount`
- `absolute_diff`
- `relative_diff_pct`
- `status`
- `explanation_preview`

Convencion de nombre:

- `reconciliation-summary-<run-label>-<period>.csv`

## Exception Detail Export

Objetivo:

- llevar fuera de la UI la evidencia operativa del drill-down
- permitir revision offline de registros concretos y anomalias

Columnas confirmadas:

- `run_label`
- `period`
- `record_id`
- `employee_id`
- `employee_name`
- `legal_entity`
- `concept_code`
- `concept_name`
- `amount`
- `currency`
- `exception_type`
- `observation`

Convencion de nombre:

- `exception-detail-<run-label>-<period>-<concept-code>.csv`

## Que no entra todavia

- `Excel`
- exports agregados multi-run
- archivos zip
- formatos listos para presentacion ejecutiva
- configuracion avanzada de columnas
- plantillas custom por cliente
