# EPIC 09 Supporting Cases QA

## Objetivo

Documentar la validacion de la `Card 9.4.2` de `EPIC 09`, centrada en los casos
complementarios del walkthrough:

- `CHILDCARE`
- `OVERTIME`
- `TRANSPORT`

## Entorno validado

- fecha de validacion: `2026-03-31`
- branch de trabajo: `codex/epic-09-hardening-qa`
- backend local: `http://localhost:8000`
- run QA de referencia: `ee9e80e7-5fe0-4a3e-a8ef-7f98eb15cf27`

## Alcance

Se contrastaron los tres casos contra:

- `docs/DEMO_WALKTHROUGH.md`
- `docs/DEMO_CASE_VALIDATION.md`
- `GET /runs/{run_id}/results/{result_id}`
- `GET /runs/{run_id}/results/{result_id}/drilldown`

## Resultado por caso

### 1. CHILDCARE

Validado:

- status: `Unreconciled`
- `expected`: `18500.00`
- `observed`: `17050.00`
- `diff`: `-1450.00`
- `recommended_action` presente
- top exception types:
  - `Missing Record / Missing Population`
- `total_exceptions`: `6`
- `drill_total_rows`: `24`
- `drill_rows_with_exception`: `0`

Lectura:

El caso sigue funcionando como historia de cobertura incompleta y población
faltante. La ausencia de filas marcadas en drill-down no debilita el caso; al
contrario, refuerza que la lógica está apoyada en población esperada y no en
una anomalía mecánica de archivo.

### 2. OVERTIME

Validado:

- status: `Unreconciled`
- `expected`: `14000.00`
- `observed`: `14950.00`
- `diff`: `950.00`
- `recommended_action` presente
- top exception types:
  - `Outlier Amount`
- `total_exceptions`: `1`
- `drill_total_rows`: `70`
- `drill_rows_with_exception`: `1`
- `drill_exception_types`:
  - `Outlier Amount`

Lectura:

El caso sigue siendo el mejor soporte para mostrar foco analítico inmediato: hay
un desvío concreto, una causa dominante y una sola fila crítica para defender la
historia en segundos.

### 3. TRANSPORT

Validado:

- status: `Minor Difference`
- `expected`: `21000.00`
- `observed`: `20760.00`
- `diff`: `-240.00`
- `recommended_action`: `None`
- top exception types: `[]`
- `total_exceptions`: `0`
- `drill_total_rows`: `350`
- `drill_rows_with_exception`: `0`

Lectura:

El caso sigue cumpliendo bien su rol de tolerancia y criterio. No compite con
los casos wow y demuestra que el sistema no dramatiza cada diferencia.

## Conclusion

La `Card 9.4.2` queda validada para alcance MVP.

Los tres casos complementarios siguen alineados con la narrativa comercial:

- `CHILDCARE` demuestra lógica de población
- `OVERTIME` demuestra capacidad de outlier puntual
- `TRANSPORT` demuestra criterio y tolerancia

## Siguiente paso recomendado

Avanzar con el bloque final de cierre demo-ready de `EPIC 09`.
