# EPIC 09 Functional Flow QA

## Objetivo

Documentar la validacion integral de la `Card 9.1.1` de `EPIC 09` sobre el
flujo principal del MVP:

- setup
- run
- summary
- concept analysis
- drill-down
- exports

## Entorno validado

- fecha de validacion: `2026-03-30`
- frontend local: `http://localhost:3000`
- backend local: `http://localhost:8000`
- branch de trabajo: `codex/epic-09-hardening-qa`

## Runs verificadas

### Run canonica ya existente

- `53a31779-a1dd-481d-ab89-e2aeecee0706`
- label: `Demo March 2026 - Canonical Walkthrough`

### Run QA recreada para esta validacion

- `ee9e80e7-5fe0-4a3e-a8ef-7f98eb15cf27`
- label: `EPIC09 QA 2026-03-30T18:14:37`

La run QA se creo con el tooling oficial:

```bash
cd backend
.venv/bin/python scripts/demo_seed.py create --run-label "EPIC09 QA 2026-03-30T18:14:37" --allow-duplicates
```

## Flujo ejecutado

### 1. Entorno demo

Validado:

- backend con `GET /health` en `200`
- frontend respondiendo en `/`
- run canonica existente
- creacion exitosa de una run QA nueva usando el seed oficial

### 2. Setup de run

Validado:

- la home sigue exponiendo el setup demo y las referencias seed
- la run QA pudo crearse y asociar correctamente:
  - `payroll.csv`
  - `expected_totals.csv`
  - `concept_master.csv`
  - `employee_reference.csv`

### 3. Ejecucion de conciliacion

Validado:

- la run QA finalizo con status tecnico `RECONCILED_WITH_EXCEPTIONS`
- el business status resultante fue `unreconciled`

### 4. Summary

Validado sobre `GET /runs/{run_id}/summary` y la ruta frontend
`/runs/{run_id}`.

Resultado:

- `MEAL_VOUCHER` visible como `Unreconciled`
- `CHILDCARE` visible como `Unreconciled`
- `OVERTIME` visible como `Unreconciled`
- `TRANSPORT` visible como `Minor Difference`

### 5. Concept analysis

Validado sobre `GET /runs/{run_id}/results/{result_id}` y la ruta frontend
`/runs/{run_id}/concepts/{result_id}` para `MEAL_VOUCHER`.

Resultado:

- status `Unreconciled`
- summary explanation consistente
- recommended action presente
- excepciones visibles:
  - `Unmapped Concept`
  - `Duplicate Record`
  - `Out-of-Period Record`

### 6. Drill-down

Validado sobre `GET /runs/{run_id}/results/{result_id}/drilldown` y la ruta
frontend `/runs/{run_id}/concepts/{result_id}/drilldown`.

Resultado:

- `519` filas totales del concepto
- `14` filas con excepcion visible en tabla
- exception types visibles:
  - `Duplicate Record`
  - `Out-of-Period Record`

### 7. Exportables

Validado:

- `GET /runs/{run_id}/exports/summary` en `200`
- `GET /runs/{run_id}/results/{result_id}/exports/detail` en `200`

Archivos descargados:

- `reconciliation-summary-epic09-qa-2026-03-30t18-14-37-2026-03.csv`
- `exception-detail-epic09-qa-2026-03-30t18-14-37-2026-03-meal-voucher.csv`

## Hallazgos

### Bloqueos funcionales graves

- no se detectaron

### Observaciones no bloqueantes

- el contrato real de `result detail` usa `result` y `exceptions` en el payload,
  mientras que `drilldown` usa `summary`, `rows` y `exception_flags`; no es un
  bug, pero conviene tenerlo presente para la validacion de consistencia de la
  `Card 9.1.2`
- el drill-down de `MEAL_VOUCHER` sigue mostrando evidencia visible de
  `Duplicate Record` y `Out-of-Period Record`, mientras que los `Unmapped
  Concept` viven principalmente en concept analysis y en el detail export; esto
  sigue alineado con la narrativa documentada del demo

## Conclusion

La `Card 9.1.1` queda validada para el alcance MVP.

El flujo principal `Setup -> Run -> Summary -> Concept -> Drill-down -> Export`
funciona end-to-end sin bloqueos funcionales graves y sostiene la historia
comercial principal del producto.

## Siguiente paso recomendado

Avanzar con `Card 9.1.2 — Validar consistencia entre capa lógica, persistencia y UI`.
