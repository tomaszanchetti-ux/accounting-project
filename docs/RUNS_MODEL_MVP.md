# Modelo de Runs del MVP

## Objetivo

Definir la entidad operativa que convierte una ejecucion del motor de
conciliacion en una corrida real, identificable y trazable dentro del producto.

La `reconciliation_run` es la unidad madre de la capa operativa del MVP:

- agrupa el contexto de una corrida
- referencia los insumos utilizados
- registra el estado tecnico de procesamiento
- conserva el estado de negocio del resultado
- habilita persistencia, API, UI y drill-down

## Entidad logica `reconciliation_run`

### Semantica

Una `reconciliation_run` representa una ejecucion concreta del proceso de
conciliacion para un periodo determinado, con un set identificable de inputs y
un resultado reproducible.

No representa:

- una configuracion permanente del sistema
- un job asincronico enterprise
- una auditoria completa de bajo nivel

Si representa:

- una corrida visible para usuario
- una unidad consultable desde frontend
- un contenedor de resultados, excepciones y staging
- una referencia estable para reproducir el demo

### Campos minimos

| Campo | Tipo sugerido | Obligatorio | Semantica MVP |
| --- | --- | --- | --- |
| `id` | `uuid` | si | identificador unico e inmutable de la corrida |
| `run_label` | `text` | si | nombre visible corto para UI y demo |
| `period` | `text` | si | periodo procesado en formato canonico del MVP |
| `status` | `text` | si | estado tecnico de la corrida |
| `overall_status` | `text` | no al crear, si al completar | estado de negocio resultante de la conciliacion |
| `source_file_name` | `text` | no al crear, si al subir input | nombre del archivo principal de payroll asociado |
| `record_count` | `integer` | no al crear, si al procesar | cantidad total de registros leidos del payroll |
| `concept_count` | `integer` | no al crear, si al procesar | cantidad de conceptos agregados en resultados |
| `legal_entity_scope` | `text` | no | filtro opcional por entidad legal cuando aplique |
| `created_at` | `timestamp with time zone` | si | momento de creacion de la run |
| `completed_at` | `timestamp with time zone` | no | momento de cierre exitoso o fallido de la run |

### Decision sobre scope

Para el MVP se adopta `legal_entity_scope` opcional.

Motivo:

- el motor actual ya contempla `legal_entity` como segmentacion opcional
- el lenguaje de negocio del proyecto usa `legal_entity`
- evita introducir una abstraccion extra como `entity_scope` sin necesidad real

Regla operativa:

- si la run procesa el universo completo del periodo, `legal_entity_scope` queda
  `null`
- si la run procesa una sola entidad legal, se persiste el valor aplicado

## Estados de la corrida

La run usa dos ejes complementarios:

- `status`: estado tecnico del ciclo de vida
- `overall_status`: estado de negocio de la conciliacion

### Estados tecnicos (`status`)

| Estado | Significado |
| --- | --- |
| `DRAFT` | la run fue creada pero todavia no tiene insumos suficientes para ejecutarse |
| `INPUT_VALIDATED` | los inputs minimos ya existen y pasaron validacion inicial |
| `PROCESSING` | el motor esta ejecutandose o la persistencia de outputs esta en curso |
| `RECONCILED` | la ejecucion termino correctamente y no quedaron diferencias materiales |
| `RECONCILED_WITH_EXCEPTIONS` | la ejecucion termino correctamente pero surgieron diferencias, excepciones o hallazgos relevantes |
| `INVALID_INPUT` | la corrida no pudo avanzar porque los inputs son invalidos o incompletos |
| `FAILED` | la corrida fallo por error tecnico o inconsistencia no atribuible al input esperado |

### Estado de negocio (`overall_status`)

`overall_status` queda separado de `status` para no mezclar salud tecnica con
resultado funcional.

Valores iniciales del MVP:

- `reconciled`
- `minor_difference`
- `unreconciled`
- `invalid_incomplete`

Regla de uso:

- mientras la run no haya terminado, `overall_status` puede quedar `null`
- al completar la corrida, `overall_status` se deriva del
  `overall_run_status` entregado por el engine
- `status` sigue diciendo si la corrida fue procesada con exito o no

### Transiciones validas

Flujo nominal:

`DRAFT` -> `INPUT_VALIDATED` -> `PROCESSING` -> `RECONCILED`

Flujo nominal con hallazgos:

`DRAFT` -> `INPUT_VALIDATED` -> `PROCESSING` -> `RECONCILED_WITH_EXCEPTIONS`

Flujo con input invalido:

`DRAFT` -> `INVALID_INPUT`

`INPUT_VALIDATED` -> `INVALID_INPUT`

Flujo con error tecnico:

`PROCESSING` -> `FAILED`

### Reglas de transicion

- una run no debe volver a `DRAFT` una vez validada
- una run en `PROCESSING` debe cerrar siempre en un estado terminal
- `RECONCILED`, `RECONCILED_WITH_EXCEPTIONS`, `INVALID_INPUT` y `FAILED` son
  terminales en el MVP
- si se necesita reintento, el camino recomendado del MVP es crear una nueva
  run, no reescribir la existente

## Metadata minima de trazabilidad

La corrida debe permitir responder de forma simple:

- que archivo se proceso
- cuando se proceso
- que periodo cubrio
- cuanto volumen tuvo
- con que reglas se evaluo
- que version funcional del motor produjo el resultado

### Metadata obligatoria

| Metadata | Campo sugerido | Semantica |
| --- | --- | --- |
| archivo utilizado | `source_file_name` | nombre del payroll principal usado en la corrida |
| timestamp de creacion | `created_at` | inicio de vida de la run |
| timestamp de cierre | `completed_at` | cierre de procesamiento |
| periodo procesado | `period` | periodo objetivo de la corrida |
| cantidad de registros | `record_count` | volumen de payroll procesado |
| cantidad de conceptos | `concept_count` | volumen agregado de salida |
| tolerancias aplicadas | `tolerance_profile_label` | perfil de tolerancia usado por el motor |
| version de reglas | `rules_version` | version funcional del engine y reglas explicativas |
| entidad legal aplicada | `legal_entity_scope` | scope opcional si hubo segmentacion |

### Metadata derivada util para persistencia

Aunque no es el nucleo de esta card, conviene asumir desde ahora que la run
tambien tendra relacion con:

- ubicacion del archivo crudo en storage
- snapshot de expected totals usados
- resultados agregados persistidos
- excepciones persistidas
- staging del payroll normalizado

Eso no obliga a meter todo en la tabla `reconciliation_runs`, pero si obliga a
que `id` sea la clave madre del dominio.

## Que queda fuera del MVP

Para evitar sobrediseño, no entran en esta capa base:

- versionado complejo de configuraciones por usuario
- reintentos automaticos de jobs
- colas asincronicas y worker orchestration
- auditoria fila por fila de cada transformacion interna
- historial de cambios manuales sobre una misma run
- auth enterprise y ownership multi-tenant avanzada

## Decisiones operativas resultantes

- la tabla fisica recomendada se llamara `reconciliation_runs`
- `legal_entity_scope` queda como campo opcional del modelo
- `status` y `overall_status` se persisten por separado
- la run es inmutable como unidad historica una vez cerrada
- el frontend deberia consumir la run como entidad central para setup,
  summary, concept analysis y drill-down
