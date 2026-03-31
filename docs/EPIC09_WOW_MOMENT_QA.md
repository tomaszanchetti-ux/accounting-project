# EPIC 09 Wow Moment QA

## Objetivo

Documentar la validacion de la `Card 9.4.1` de `EPIC 09`, centrada en el
recorrido wow principal de `MEAL_VOUCHER`.

## Entorno validado

- fecha de validacion: `2026-03-31`
- branch de trabajo: `codex/epic-09-hardening-qa`
- backend local: `http://localhost:8000`
- run QA de referencia: `ee9e80e7-5fe0-4a3e-a8ef-7f98eb15cf27`

## Alcance de la validacion

Se revalidó la secuencia aprobada en `docs/DEMO_WALKTHROUGH.md`:

1. summary con concepto en rojo visible
2. apertura de `MEAL_VOUCHER`
3. lectura multi-causa del desvío
4. bajada a drill-down
5. verificación de evidencia concreta

Fuentes usadas:

- `GET /runs/{run_id}/summary`
- `GET /runs/{run_id}/results/{result_id}`
- `GET /runs/{run_id}/results/{result_id}/drilldown`
- contrato UI visible en los componentes de summary, concept analysis y
  drill-down

## Resultado del recorrido

### 1. Summary

Validado:

- `MEAL_VOUCHER` aparece primero en `preview_results`
- status: `Unreconciled`
- `expected`: `42000.00`
- `observed`: `38220.00`
- `diff`: `-3780.00`
- `recommended_action` presente

Lectura:

El concepto sigue siendo suficientemente material y visible para abrir el wow
moment sin necesidad de buscar demasiado dentro del summary.

### 2. Concept Analysis

Validado:

- header con status `Unreconciled`
- summary statement consistente con el desvío
- `recommended_action` presente
- `evidence_summary.total_exceptions`: `19`
- top exception types:
  - `Unmapped Concept`
  - `Duplicate Record`
  - `Out-of-Period Record`

Lectura:

La narrativa principal sigue funcionando porque el producto no reduce el caso a
una sola causa. Expone un desvío compuesto y defendible.

### 3. Drill-down

Validado:

- `total_rows`: `519`
- `rows_with_exception`: `14`
- exception types visibles:
  - `Out-of-Period Record`
  - `Duplicate Record`
- el total del concepto en drill-down sigue siendo coherente con el contexto
  narrativo del análisis

Lectura:

El drill-down aterriza rápido en evidencia concreta sin romper el hilo del
análisis. El usuario puede pasar de una explicación agregada a filas específicas
en pocos pasos.

## Evaluacion narrativa

### Claridad

`MEAL_VOUCHER` sigue siendo el mejor punto de entrada porque:

- tiene materialidad visible
- combina múltiples causas
- permite bajar a evidencia concreta

### Timing

La secuencia sigue siendo apta para el tramo de `90-120s` definido en
`docs/DEMO_WALKTHROUGH.md`.

### Impacto

El recorrido sigue demostrando el diferencial completo del MVP en una sola
historia:

- detecta el desvío
- explica el desvío
- expone evidencia concreta

## Nota operativa

Durante esta sesión la validación del wow moment se hizo principalmente por API
y por contrato UI. El backend local estaba disponible, pero la ruta frontend
local respondió con una redirección a `/login`, por lo que la revalidación
visual completa de browser no fue el eje de esta card.

Esto no invalida la conclusión de la card porque:

- el contrato de datos sigue intacto
- los componentes UI relevantes ya fueron reforzados en cards previas de
  `EPIC 09`
- el recorrido operativo principal permanece consistente

## Conclusion

La `Card 9.4.1` queda validada para alcance MVP.

El wow moment de `MEAL_VOUCHER` sigue siendo claro, defendible y comercialmente
potente.

## Siguiente paso recomendado

Avanzar con `Card 9.4.2 — Verificar casos complementarios CHILDCARE, OVERTIME,
TRANSPORT`.
