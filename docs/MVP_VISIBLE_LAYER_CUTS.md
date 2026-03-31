# MVP Visible Layer Cuts

## Objetivo

Definir qué capas visibles del producto actual salen del flujo principal del
MVP simplificado, qué se fusiona y qué debe quedar subordinado.

Este documento ejecuta la decisión de `EPIC 10 / Card 10.1.2`.

## Principio de recorte

Si un bloque visible:

- no ayuda a cargar archivos
- no ayuda a correr la run
- no ayuda a priorizar un concepto
- no ayuda a validar evidencia
- o no ayuda a exportar

entonces no debe dominar la primera lectura del MVP.

## Regla operativa

Cada elemento evaluado queda en una de estas categorías:

- `KEEP`: se mantiene visible en primera lectura
- `HIDE`: pasa a avanzado, colapsado o secundaria
- `MERGE`: se absorbe dentro de otro bloque o pantalla
- `REMOVE`: sale del flujo principal del MVP

## 1. Home / Setup

### Elementos que se mantienen visibles

- `KEEP` upload de `payroll.csv`
- `KEEP` upload de `expected_totals.csv`
- `KEEP` campo `period` si sigue siendo necesario para ejecutar la run
- `KEEP` feedback corto de validación o error
- `KEEP` CTA principal `Run reconciliation`

### Elementos que pasan a segundo plano

- `HIDE` métricas iniciales:
  - `Run ID`
  - `Current status`
  - `Period` como métrica repetida
  - `API connectivity` como tarjeta visible permanente
- `HIDE` `Legal entity scope`
- `HIDE` `Tolerance profile`
- `HIDE` `Exceptions analysis`
- `HIDE` `ExpectedTotalsPreview` como panel lateral dominante
- `HIDE` `RunValidationSummary` si ocupa demasiado espacio antes de ejecutar
- `HIDE` detalle de archivos de referencia auto-cargados como bloque completo

### Elementos a recortar o reescribir

- `REMOVE` framing de `Demo workspace ready`
- `REMOVE` copy de preparación orientado a “canonical walkthrough”
- `REMOVE` lenguaje de “workspace status” como parte principal de la home
- `REMOVE` toda sensación de que la pantalla es una consola de preparación demo

### Decisión de implementación

La home debe leerse así:

1. qué archivos subir
2. qué período correr
3. cómo ejecutar

Todo lo demás queda:

- en advanced settings
- en texto auxiliar mínimo
- o fuera de la primera vista

## 2. Summary

### Elementos que se mantienen visibles

- `KEEP` estado general de la run
- `KEEP` KPIs principales
- `KEEP` tabla principal por concepto
- `KEEP` export summary
- `KEEP` CTA claro al detalle del concepto

### Elementos que pasan a segundo plano

- `HIDE` panel grande `Run Context`
- `HIDE` metadata técnica visible por defecto:
  - `run id`
  - `rules version`
  - `source file name` si ya aparece en resumen compacto
- `HIDE` bloque lateral completo de `Traceability`
- `HIDE` banner explicativo sobre filosofía data-first si no cambia la acción

### Elementos a recortar o reescribir

- `REMOVE` copy larga sobre “four executive questions”
- `REMOVE` CTA de continuidad que habla de “Concept Analysis and Drill-down”
- `REMOVE` cualquier texto que prepare una pantalla intermedia que ya no existirá

### Decisión de implementación

El summary debe responder:

1. la run salió bien o no
2. qué conceptos requieren atención
3. en cuál conviene entrar ahora

Si un bloque no ayuda a eso, se reduce o se saca de la lectura principal.

## 3. Concept Analysis

### Decisión principal

- `REMOVE` como pantalla intermedia separada del flujo principal

### Elementos que sobreviven por contenido

- `MERGE` `Summary statement`
- `MERGE` `Recommended next step`
- `MERGE` `Top Causes`
- `MERGE` KPIs principales del concepto
- `MERGE` export detail CSV

### Elementos que no deben sobrevivir como capa propia

- `REMOVE` header completo de `Concept Context`
- `REMOVE` botonera de ida y vuelta entre summary y drill-down
- `REMOVE` `Evidence framing` como bloque separado
- `REMOVE` metadata repetida de run ya mostrada antes
- `REMOVE` la lógica de “explicación primero, evidencia después” como paso obligatorio

### Decisión de implementación

El valor de esta pantalla no se elimina.
Se absorbe arriba del nuevo `Deep Dive`.

## 4. Drill-down / Deep Dive

### Elementos que se mantienen visibles

- `KEEP` tabla de registros
- `KEEP` filtros mínimos realmente útiles
- `KEEP` export detail CSV
- `KEEP` navegación simple de vuelta al summary

### Elementos que se incorporan desde Concept Analysis

- `MERGE` statement principal
- `MERGE` top causes
- `MERGE` recommended action
- `MERGE` KPIs de concepto

### Elementos que pasan a segundo plano

- `HIDE` panel completo de `Drill-down Context`
- `HIDE` metadata repetida de run
- `HIDE` paneles de `Traceability` y `Run Events`
- `HIDE` copy extensa de “Evidence summary” si puede resolverse en una línea

### Elementos a recortar

- `REMOVE` botón `Back to concept`
- `REMOVE` la necesidad de una ruta intermedia para ver detalle
- `REMOVE` paneles repetidos que explican la misma lógica ya vista en summary

### Decisión de implementación

El nuevo `Deep Dive` debe leerse en dos actos:

1. arriba: explicación ejecutiva corta
2. abajo: evidencia tabular exportable

## 5. Copy y labels globales

### Labels a cambiar

- `Concept Analysis` -> `Deep Dive` o `Details`
- `Open detailed records` -> `Open deep dive` o `View details`
- `Back to concept` -> `Back to summary`

### Lenguaje a reducir

- `demo workspace`
- `canonical walkthrough`
- `traceability framing`
- `evidence framing`
- explicaciones largas sobre la filosofía del producto

### Lenguaje a privilegiar

- upload
- run
- results
- details
- export
- report

## 6. Decisiones concretas para advanced / secundaria

Los siguientes elementos no desaparecen funcionalmente, pero dejan de estar en
la primera lectura:

- `legal entity scope`
- `tolerance profile`
- `exceptions analysis`
- validaciones demasiado detalladas antes de ejecutar
- metadata extensa de runs
- timelines de eventos
- notas metodológicas largas

## 7. Resultado esperado del recorte

Después de aplicar este recorte, el MVP debería verse así:

- una home simple con foco en archivos + run
- un summary con foco en KPIs + tabla
- un deep dive unificado con explicación + evidencia + export

## Próximo paso recomendado

Con este recorte ya definido, el siguiente paso correcto es arrancar la
implementación visible por:

1. `EPIC 10 / Card 10.2.1`
2. `EPIC 10 / Card 10.2.2`
3. luego `EPIC 10 / Card 10.3.1` y `10.3.2`
