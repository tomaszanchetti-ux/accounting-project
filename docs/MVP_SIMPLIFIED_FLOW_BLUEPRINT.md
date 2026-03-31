# MVP Simplified Flow Blueprint

## Objetivo

Definir el flujo objetivo simplificado del producto para guiar la implementación
de `EPIC 10` sin ambigüedad.

La decisión de producto es explícita:

> el MVP debe pasar de una demo narrativa multicapa a un flujo operativo simple
> y rápido de entender.

## Problema del flujo actual

El flujo visible actual pide demasiado contexto y demasiadas paradas:

1. setup con varios controles visibles
2. summary
3. concept analysis
4. drill-down
5. exportables

Eso genera fricción en tres niveles:

- demasiadas decisiones antes de correr una run
- demasiados clicks hasta llegar a evidencia útil
- demasiado framing textual para entender qué hacer

## Flujo objetivo aprobado

El flujo visible del MVP queda redefinido como:

1. `Upload + Run`
2. `Results Summary`
3. `Deep Dive + Export`

## Principio rector de UX

Cada pantalla debe responder primero a una acción concreta:

- cargar
- correr
- revisar
- exportar

Todo elemento que no ayude directamente a una de esas acciones debe:

- esconderse
- comprimirse
- o salir del flujo principal

## Mapa de pantallas objetivo

### 1. Pantalla inicial: `New Reconciliation`

Rol:

- punto único de entrada
- carga de archivos
- disparo de la run

Debe mostrar por defecto:

- upload de `payroll.csv`
- upload de `expected_totals.csv`
- campo simple de período si realmente hace falta
- CTA principal `Run reconciliation`

Debe dejar fuera de la primera vista:

- metadata extensa de workspace
- bloques de readiness demasiado verbosos
- controles secundarios no esenciales
- framing de “demo workspace”

### 2. Pantalla de resultados: `Results Summary`

Rol:

- lectura ejecutiva de la run
- priorización de conceptos con diferencia
- puente directo al detalle útil

Debe mostrar:

- estado general de la run
- KPIs principales
- tabla de conceptos
- export summary

Debe resolver en un click:

- abrir el deep dive de un concepto

Debe evitar:

- paneles grandes de trazabilidad si no cambian la decisión
- copy excesivo explicando el método
- navegación redundante

### 3. Pantalla de detalle: `Deep Dive`

Rol:

- unir explicación y evidencia en una sola vista

Debe combinar:

- statement principal del concepto
- top causes
- recomendación de revisión
- tabla de registros
- export detail CSV
- export PDF

Decisión clave:

- `Concept Analysis` deja de existir como parada obligatoria separada
- su contenido se absorbe arriba del `Deep Dive`

## Qué sobrevive y qué cambia

### Sobrevive

- setup como punto de arranque
- summary como vista ejecutiva principal
- drill-down como evidencia tabular
- export CSV
- explicación rule-based

### Se fusiona

- `Concept Analysis` + `Drill-down` -> `Deep Dive`

### Se reduce o se subordina

- traceability visible
- metadata repetida entre pantallas
- copy narrativo de demo
- controles secundarios del setup

## Objetivo de navegación

El producto debe reducir fricción visible de manera medible.

Objetivos concretos:

- menos profundidad de navegación
- menos contexto accesorio en headers y paneles
- menos clicks hasta evidencia útil
- menos texto para entender la acción principal

## Criterio de éxito UX para `EPIC 10`

La simplificación se considera bien encaminada si:

1. desde home se entiende en segundos qué hay que cargar y qué botón acciona el flujo
2. desde summary se puede abrir el detalle útil en un solo click
3. el usuario no necesita pasar por una pantalla intermedia solo para llegar a la evidencia
4. el producto puede explicarse en lenguaje simple:
   - subís archivos
   - corrés la conciliación
   - ves el resumen
   - abrís el detalle
   - exportás el reporte

## Criterio explícito para decisiones futuras

Si una decisión:

- agrega pasos
- agrega copy
- agrega chrome visual
- o agrega paneles que no cambian la acción inmediata

entonces esa decisión debe considerarse sospechosa para el MVP simplificado.

## Próximo paso recomendado

Ejecutar `EPIC 10 / Card 10.1.2` para listar qué capas visibles salen del flujo
principal y dejar el recorte definido antes de tocar la implementación UI.
