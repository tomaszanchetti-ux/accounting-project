# Contrato del Reconciliation Engine

## Objetivo

Este documento fija el contrato funcional base del motor de conciliacion del
MVP.

Su objetivo es dejar explicito:

- cual es la unidad primaria de conciliacion
- que inputs necesita el motor para correr
- que outputs debe producir para alimentar API, persistencia y UI

## 1. Unidad de conciliacion del MVP

La unidad primaria de conciliacion del MVP es:

- `payroll_period + concept_code_normalized`

Esto significa que el motor responde la pregunta principal del producto a nivel
agregado:

> para un concepto dado en un periodo dado, ¿el total observado coincide con el
> total esperado?

### Dimension secundaria opcional

El MVP puede soportar una dimension secundaria opcional:

- `legal_entity`

Esta dimension no cambia la definicion primaria del producto. Solo agrega un
slice adicional de analisis cuando el caso de uso lo necesite.

La jerarquia correcta queda asi:

1. unidad primaria: `period + concept`
2. unidad secundaria opcional: `period + concept + legal_entity`

### Campos fuera de la conciliacion primaria

Los siguientes campos no forman parte de la llave primaria de conciliacion:

- `employee_id`
- `record_id`

Estos campos siguen siendo importantes, pero viven en capas posteriores:

- trazabilidad
- drill-down
- analitica
- explicacion de excepciones

### Regla rectora de implementacion

Toda agregacion, comparacion y asignacion de estado de la `EPIC 02` debe
respetar esta definicion.

Si una decision de implementacion empuja al motor a conciliar por empleado,
esa decision rompe el alcance del MVP base y debe evitarse.

## 2. Contrato de input del motor

El motor debe poder ser invocado de forma programatica desde:

- scripts locales
- tests
- API backend
- procesos futuros de persistencia

### Inputs obligatorios

- `payroll`
  - origen observado principal
  - puede recibirse como `pandas.DataFrame`, path local o archivo CSV fuente
- `expected_totals`
  - referencia esperada contra la cual se compara el observado
  - puede recibirse como `pandas.DataFrame`, path local o archivo CSV fuente
- `target_period`
  - periodo objetivo de la corrida
  - formato esperado: `YYYY-MM`

### Inputs opcionales

- `concept_master`
  - mapping y metadata de conceptos
- `employee_reference`
  - referencia auxiliar para analitica y excepciones posteriores
- `legal_entity`
  - filtro o slice opcional para corridas segmentadas
- `tolerance_profile`
  - perfil de tolerancias para clasificacion de estados

### Formato esperado para uso programatico

El contrato programatico recomendado del MVP es:

- aceptar `DataFrame` ya cargados cuando el caller controla IO
- aceptar `str` o `Path` cuando el motor deba resolver archivos locales
- exigir siempre `target_period` explicito

### Regla de responsabilidad

El motor no debe asumir implicitamente el periodo objetivo a partir del dataset
si el caller no lo declara.

Puede usar el dataset para validar consistencia temporal, pero no para inventar
el scope principal de la corrida.

## 3. Contrato de output del motor

El output principal del motor es una coleccion agregada por unidad conciliable.

### Output agregado minimo por fila

Cada fila agregada debe incluir como minimo:

- `period`
- `concept_code_normalized`
- `concept_name_normalized`
- `observed_amount`
- `expected_amount`
- `absolute_diff`
- `relative_diff_pct`
- `status`

### Metricas auxiliares minimas por fila

Cada unidad agregada debe exponer ademas:

- `record_count`
- `employee_count`
- `invalid_record_count`

Si se usa segmentacion opcional, tambien puede incluir:

- `legal_entity`

### Output tecnico intermedio para debugging

Ademas del resumen agregado, el motor debe poder devolver artefactos tecnicos
intermedios para trazabilidad y depuracion:

- `normalized_payroll`
- `observed_totals`
- `expected_totals_filtered`
- `validation_errors`
- `validation_warnings`

Estos artefactos no son la salida principal del producto, pero si son clave
para:

- tests
- debugging
- persistencia futura
- explicabilidad operativa

## 4. Estructura general recomendada

El resultado de una corrida del motor debe poder pensarse como:

1. `summary_rows`
2. `run_metrics`
3. `debug_artifacts`

Donde:

- `summary_rows` alimenta UI, API y persistencia principal
- `run_metrics` resume volumen y salud minima de la corrida
- `debug_artifacts` guarda evidencia tecnica reutilizable

## 5. Relacion con el dataset demo

Este contrato es consistente con el diseño del dataset demo definido en
`docs/DATASET_DEMO_FOUNDATION.md`.

En particular:

- `expected_totals.csv` ya fue diseñado sobre la llave `period + concept`
- `payroll.csv` aporta el observado agregable sobre esa misma llave
- `employee_id` se conserva para drill-down y explicacion, no para conciliar

## 6. Fallback de mapping de conceptos

La estrategia base del MVP para resolver conceptos observados es:

1. intentar match exacto por `concept_code`
2. usar `concept_name` solo como fallback controlado
3. si no hay match, marcar el registro como `unmapped`

Un concepto no mapeado no debe inventarse ni autocorregirse agresivamente.

En el dataset demo, esto protege de forma deliberada el caso narrativo de
`unmapped concept`.

## 7. Convencion de signos del motor

El motor conserva el importe observado tal como viene en la fuente normalizada.

La estrategia del MVP es:

1. no reescribir automaticamente el signo del monto
2. usar `concept_master.expected_sign` para crear un flag preliminar de
   `unexpected sign`
3. mantener `amount_for_aggregation` igual al monto observado para no distorsionar
   el calculo

Esto permite detectar inconsistencias de polaridad sin alterar artificialmente
el total observado.

## 8. Base conciliable intermedia

La base conciliable del MVP conserva todos los registros procesados y agrega
flags para distinguir:

- registros validos
- registros invalidos
- registros validos pero con excepcion analitica
- registros elegibles para conciliacion

La regla base es:

1. no descartar filas temprano si todavia aportan trazabilidad
2. marcar explicitamente si una fila es elegible o no para conciliacion
3. usar esa base como insumo auditable para agregacion, explicacion y drill-down
