# Demo Case Validation

## Objetivo

Este documento valida los cuatro conceptos clave del walkthrough demo usando:

- el dataset oficial en `data/demo_seed/`
- la run canonica `Demo March 2026 - Canonical Walkthrough`
- los tests del motor ya existentes
- la consulta real de summary, concept analysis y drill-down

Su funcion es cerrar el contrato operativo de `Feature 8.4`.

## Run validada

Run usada como referencia:

- `run_label`: `Demo March 2026 - Canonical Walkthrough`
- `period`: `2026-03`
- `status`: `RECONCILED_WITH_EXCEPTIONS`
- `overall_status`: `unreconciled`

Estado agregado confirmado:

- `6` conceptos `Reconciled`
- `1` concepto `Minor Difference`
- `3` conceptos `Unreconciled`

## Caso 1: `MEAL_VOUCHER`

### Resultado esperado

- status `Unreconciled`
- desvio material y visible desde Summary
- narrativa multi-causa defendible en Concept Analysis
- drill-down con evidencia concreta

### Resultado validado

- `expected`: `42000.00`
- `observed`: `38220.00`
- `diff`: `-3780.00`
- `status`: `Unreconciled`

### Causas confirmadas

El concepto expone estas excepciones dentro de la run:

- `Unmapped Concept`
- `Out-of-Period Record`
- `Duplicate Record`

### Lectura demo

Este sigue siendo el wow moment principal porque demuestra que el producto no
solo detecta un desvio, sino que separa causas distintas dentro del mismo
concepto.

### Drill-down confirmado

- `519` filas del concepto
- `14` filas con excepcion
- exception types visibles en drill-down:
  - `Out-of-Period Record`
  - `Duplicate Record`

## Caso 2: `CHILDCARE`

### Resultado esperado

- status `Unreconciled`
- explicacion centrada en elegibilidad y poblacion faltante
- tono serio y cercano a un caso real de cobertura incompleta

### Resultado validado

- `expected`: `18500.00`
- `observed`: `17050.00`
- `diff`: `-1450.00`
- `status`: `Unreconciled`

### Causa confirmada

- `Missing Record / Missing Population`

### Lectura demo

Este caso demuestra que el sistema no se limita a detectar outliers o
duplicados. Puede argumentar que faltan empleados elegibles dentro de una
poblacion esperada.

### Drill-down confirmado

- `24` filas observadas del concepto
- sin excepciones por fila visibles en la tabla del concepto
- la explicacion se apoya en la comparacion contra poblacion esperada, no en una
  anomalia individual mecanica

## Caso 3: `OVERTIME`

### Resultado esperado

- status `Unreconciled`
- outlier dominante facil de explicar
- defensa rapida del caso en drill-down

### Resultado validado

- `expected`: `14000.00`
- `observed`: `14950.00`
- `diff`: `950.00`
- `status`: `Unreconciled`

### Causa confirmada

- `Outlier Amount`

### Lectura demo

Es el mejor caso para mostrar capacidad analitica puntual: el usuario ve un
desvio, abre el concepto y puede ir directo a una linea dominante en segundos.

### Drill-down confirmado

- `70` filas del concepto
- `1` fila con excepcion
- exception type visible en drill-down:
  - `Outlier Amount`

## Caso 4: `TRANSPORT`

### Resultado esperado

- status `Minor Difference`
- narrativa sobria
- sin competir con los casos wow

### Resultado validado

- `expected`: `21000.00`
- `observed`: `20760.00`
- `diff`: `-240.00`
- `status`: `Minor Difference`

### Lectura demo

Este concepto sirve para mostrar criterio y tolerancia.
No todo desvio se dramatiza ni exige una remediacion especial.

### Drill-down confirmado

- `350` filas del concepto
- `0` filas con excepcion
- sin recommended action especifica

## Conclusiones de la validacion

La combinacion de los cuatro conceptos sigue siendo correcta para el
walkthrough:

- `MEAL_VOUCHER` concentra el wow principal
- `CHILDCARE` demuestra logica de poblacion
- `OVERTIME` demuestra foco analitico sobre outliers
- `TRANSPORT` demuestra criterio y tolerancia

## Riesgo residual

La validacion hecha en esta epic confirma el contrato de datos y la narrativa
operativa.
La revalidacion visual final del walkthrough completo sigue siendo un tema
natural de `EPIC 09`.
