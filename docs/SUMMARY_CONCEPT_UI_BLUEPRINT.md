# Summary & Concept Analysis UI Blueprint

## Objetivo funcional de la Summary Screen

La Summary Screen debe responder en segundos estas cuatro preguntas:

- la corrida salio bien o requiere atencion
- cuantos conceptos conciliaron y cuantos quedaron abiertos
- donde estan los desvios principales
- que tan material sigue siendo el problema

La pantalla prioriza lectura ejecutiva rapida antes que detalle exhaustivo.

## Anatomia de la Summary Screen

Orden de lectura definido:

1. header de corrida
2. overall status de la run
3. KPI cards
4. tabla principal por concepto
5. trazabilidad resumida

Bloques visuales obligatorios:

- header con run label, periodo, timestamp y archivo procesado
- bloque de overall status con copy ejecutivo
- KPI cards compactas
- tabla de resultados por concepto
- accesos claros a Concept Analysis

## KPIs principales

Set confirmado para el MVP:

- `Concepts Reconciled`
- `Concepts with Minor Differences`
- `Unreconciled Concepts`
- `Total Amount Reconciled`
- `Amount Pending Explanation`

No se agregan KPIs accesorios mientras no mejoren la comprension ejecutiva.

## Tabla principal por concepto

Columnas cerradas:

- `Concept`
- `Expected`
- `Observed`
- `Diff`
- `Diff %`
- `Status`
- `Explanation Preview`

Orden por defecto:

1. invalid / incomplete
2. unreconciled
3. minor difference
4. reconciled

Desempate:

- mayor materialidad por `absolute_diff`
- luego `concept_code_normalized`

## Patron de navegacion a Concept Analysis

Decision final: `pagina dedicada`

Razon:

- mantiene claridad y foco
- evita competir con la tabla principal
- encaja mejor con la narrativa summary -> concept -> drill-down

## Anatomia de la Concept Analysis Screen

Orden de lectura:

1. header del concepto
2. KPIs del concepto
3. statement principal
4. top causes
5. recommended review action
6. evidence summary
7. CTA a drill-down

## CTA hacia drill-down

Copy aprobado:

- `View detailed records`

La navegacion queda preparada desde `EPIC 06` con contexto de `run_id` y
`result_id`, aunque la experiencia completa de detalle vive en `EPIC 07`.
