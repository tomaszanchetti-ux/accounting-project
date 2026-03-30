# Persistencia y API de Runs

## Objetivo

Documentar el modelo persistente y el vertical slice operativo implementado para
la capa de runs del MVP.

Este documento complementa `docs/RUNS_MODEL_MVP.md` y baja la definicion
logica a:

- tablas fisicas
- repositorios backend
- orquestacion de ejecucion
- endpoints ya expuestos

## Entidades persistidas

### `reconciliation_runs`

Entidad madre de la corrida.

Campos principales:

- `id`
- `run_label`
- `period`
- `status`
- `overall_status`
- `source_file_name`
- `record_count`
- `concept_count`
- `legal_entity_scope`
- `tolerance_profile_label`
- `rules_version`
- `run_metrics`
- `error_message`
- `created_at`
- `completed_at`

Uso:

- lookup principal de una corrida
- metadata visible para UI
- trazabilidad minima de ejecucion

### `uploaded_files`

Metadata de archivos o referencias cargadas por run.

Campos principales:

- `id`
- `run_id`
- `file_name`
- `file_type`
- `source_kind`
- `storage_bucket`
- `storage_path`
- `uploaded_at`

Decisiones MVP:

- `file_type` soporta `payroll`, `expected_totals`, `concept_master` y
  `employee_reference`
- `source_kind` soporta:
  - `local_path`
  - `supabase_storage`
- la combinacion `run_id + file_type` se trata como unica para que cada run use
  una referencia activa por tipo

### `expected_totals_used`

Snapshot de expected totals efectivamente usados en la corrida.

Campos principales:

- `id`
- `run_id`
- `period`
- `concept_code_normalized`
- `expected_amount`
- `currency`
- `legal_entity`

Decision MVP:

- se persiste snapshot filtrado por `period`
- eso permite reproducibilidad sin depender solo del archivo fuente

### `reconciliation_results`

Resultado agregado por unidad conciliable.

Campos principales:

- `id`
- `run_id`
- `period`
- `concept_code_normalized`
- `concept_name_normalized`
- `observed_amount`
- `expected_amount`
- `absolute_diff`
- `relative_diff_pct`
- `status`
- `record_count`
- `employee_count`
- `invalid_record_count`
- `legal_entity`
- `summary_explanation`
- `recommended_action`
- `explained_amount_estimate`
- `impacted_records_count`
- `impacted_employees_count`

Uso:

- summary UI
- tabla principal por concepto
- detalle de concepto

### `reconciliation_exceptions`

Persistencia de excepciones explicativas del motor.

Campos principales:

- `id`
- `run_id`
- `result_id`
- `record_id`
- `employee_id`
- `concept_scope`
- `exception_type`
- `severity`
- `scope_level`
- `estimated_impact_amount`
- `observation`
- `confidence`
- `created_at`

Decision MVP:

- una excepcion puede vivir a nivel concepto o a nivel registro
- `result_id` se asocia por `concept_scope` cuando existe matching directo

### `run_payroll_lines`

Staging del payroll normalizado para drill-down operativo.

Campos principales:

- `id`
- `run_id`
- `record_id`
- `employee_id`
- `employee_name`
- `legal_entity`
- `country`
- `cost_center`
- `payroll_period`
- `posting_date`
- `concept_code_raw`
- `concept_code_normalized`
- `concept_name_raw`
- `concept_name_normalized`
- `amount`
- `currency`
- `is_valid`
- `exception_flags`
- `invalid_reasons`

Decision MVP:

- `exception_flags` e `invalid_reasons` se persisten como listas JSON
- esto evita recalcular drill-down a partir del CSV bruto

## Integridad minima del schema

El schema implementado en `backend/app/models/runs_schema.sql` ya incluye:

- foreign keys por `run_id`
- foreign key opcional de `reconciliation_exceptions.result_id`
- indice por `run_id` en tablas hijas
- indice por `run_id + concept_code_normalized` en resultados y staging
- indice por `run_id + status` en resultados

## Orquestacion implementada

El servicio `backend/app/services/runs.py` ya resuelve este flujo:

1. crear run
2. registrar referencias de archivos por tipo
3. validar precondiciones minimas
4. cambiar la run a `PROCESSING`
5. ejecutar el engine existente
6. persistir snapshot de expected totals
7. persistir resultados
8. persistir excepciones
9. persistir staging lines
10. cerrar la run en `RECONCILED` o `RECONCILED_WITH_EXCEPTIONS`
11. si falla input, cerrar en `INVALID_INPUT`
12. si falla tecnicamente, cerrar en `FAILED`

## Endpoints implementados

El backend expone:

- `POST /runs`
- `POST /runs/{run_id}/upload`
- `POST /runs/{run_id}/execute`
- `GET /runs/{run_id}/summary`
- `GET /runs/{run_id}/results`
- `GET /runs/{run_id}/results/{result_id}`
- `GET /runs/{run_id}/results/{result_id}/drilldown`
- `GET /health`

## Alcance real del endpoint de upload hoy

El endpoint `POST /runs/{run_id}/upload` hoy soporta dos modos:

- `application/json` para registrar referencias existentes
- `multipart/form-data` para subir archivo real al bucket de inputs

### Modo referencia

Sirve para:

- desarrollo local
- testing
- corridas que ya tienen archivos disponibles en disco o storage

Formatos soportados:

- `local_path`
- `supabase_storage`

### Modo multipart

Sirve para:

- setup real desde frontend
- upload directo del payroll y archivos auxiliares

Comportamiento:

- guarda el archivo en `accounting-mvp-raw-inputs`
- usa path `runs/<run_id>/inputs/<filename>`
- persiste metadata en `uploaded_files`
- deja la run lista para ejecucion posterior
