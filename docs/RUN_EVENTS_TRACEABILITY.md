# Run Events and Traceability

## Objetivo

Definir la bitacora minima de eventos de una corrida del MVP.

La meta no es construir un audit trail enterprise, sino dejar una secuencia
clara para debugging, demo y narrativa interna.

## Decision MVP

Para esta etapa, la bitacora vive como una **timeline estructurada derivada**
desde metadata persistida y estado de la run.

No requiere tabla dedicada todavia.

Ventajas:

- cero complejidad extra de schema
- util para frontend desde ya
- suficiente para explicar retrospectivamente una corrida demo

Si en una etapa futura hace falta persistencia fina, esta timeline puede bajar a
tabla `run_events` o a logs estructurados.

## Eventos minimos

### `run_created`

Se emite cuando la run existe con:

- label
- period
- timestamp de creacion

### `file_uploaded`

Se emite por cada archivo asociado a la run.

Incluye:

- tipo de archivo
- nombre
- origen (`local_path` o `supabase_storage`)

### `processing_started`

Indica que la corrida paso a estado operativo.

Sirve para separar:

- setup de inputs
- ejecucion efectiva

### `results_persisted`

Indica que los resultados agregados ya quedaron guardados.

Incluye:

- cantidad de conceptos persistidos
- periodo procesado

### `run_completed`

Se emite cuando la run cierra en:

- `RECONCILED`
- `RECONCILED_WITH_EXCEPTIONS`

Incluye:

- estado tecnico final
- `overall_status` de negocio

### `run_invalid_input`

Se emite cuando la run cierra en `INVALID_INPUT`.

Incluye:

- motivo de invalidacion

### `run_failed`

Se emite cuando la run cierra en `FAILED`.

Incluye:

- error tecnico resumido

## Donde se expone

La timeline minima debe estar disponible al menos en:

- `GET /runs/{run_id}/summary`
- `GET /runs/{run_id}/results/{result_id}`
- `GET /runs/{run_id}/results/{result_id}/drilldown`

## Criterio de suficiencia para el MVP

La trazabilidad se considera suficiente si, viendo solo la API persistida, se
puede responder:

- que run se ejecuto
- con que periodo
- con que archivos
- cuando se cargo y ejecuto
- cuantos resultados produjo
- como termino
