# Demo Readiness Report

## Objetivo

Este documento registra el ensayo end-to-end del walkthrough principal del MVP
y deja una conclusion explicita sobre el estado `demo-ready` al cierre de
`EPIC 08`.

## Entorno usado

- frontend local en `http://localhost:3000`
- backend local en `http://localhost:8000`
- run canonica:
  - `53a31779-a1dd-481d-ab89-e2aeecee0706`
  - `Demo March 2026 - Canonical Walkthrough`

## Recorrido ensayado

Secuencia validada:

1. home / setup
2. summary de la run canonica
3. concept analysis de `MEAL_VOUCHER`
4. drill-down de `MEAL_VOUCHER`
5. export summary CSV
6. export detail CSV

## Evidencia tecnica del ensayo

### API

- `GET /health` -> `200`
- `GET /runs/{run_id}/summary` -> `200`
- `GET /runs/{run_id}/results/{result_id}` -> `200`
- `GET /runs/{run_id}/results/{result_id}/drilldown` -> `200`
- `GET /runs/{run_id}/exports/summary` -> `200`
- `GET /runs/{run_id}/results/{result_id}/exports/detail` -> `200`

### Frontend

- `/` -> `200`
- `/runs/{run_id}` -> `200`
- `/runs/{run_id}/concepts/{result_id}` -> `200`
- `/runs/{run_id}/concepts/{result_id}/drilldown` -> `200`

## Tiempos observados

### Frontend

- home: `0.05s`
- summary: `1.59s`
- concept analysis: `2.12s`
- drill-down: `2.43s`

### API

- summary payload: `1.61s`
- concept detail payload: `1.98s`
- drill-down payload: `2.27s`
- summary export: `1.02s`
- detail export: `1.67s`

## Validacion funcional del walkthrough

### Setup / home

Resultado:

- carga correctamente
- muestra referencias demo listas
- comunica mejor el estado actual del producto despues del ajuste de copy

### Summary

Resultado:

- KPIs visibles y consistentes
- orden narrativo correcto
- casos `MEAL_VOUCHER`, `CHILDCARE`, `OVERTIME` y `TRANSPORT` visibles
- CTA a concept analysis funcional

### Concept Analysis

Resultado:

- `MEAL_VOUCHER` muestra status `Unreconciled`
- statement principal correcto
- recommended action correcta
- top causes y evidence summary visibles
- CTA `View detailed records` funcional

### Drill-down

Resultado:

- la vista carga correctamente
- tabla operativa visible
- evidencia por registro presente
- export detail disponible

### Exports

Resultado:

- summary CSV descargable y consistente con la run
- detail CSV descargable y consistente con la evidencia del concepto

## Fricciones detectadas durante el ensayo

### 1. Copy viejo en la home

Estado:

- detectado durante el ensayo
- corregido en la misma sesion

Cambio aplicado:

- se reemplazo framing viejo de `EPIC 05` por copy orientado a demo canonica

### 2. Skeleton inicial en rutas con streaming

Estado:

- observado pero no bloqueante

Lectura:

- summary, concept analysis y drill-down muestran loading state inicial antes
  del contenido final
- esto es consistente con la implementacion actual y no rompe el walkthrough
  mientras el entorno este pre-calentado

## Conclusion sobre `demo-ready`

### Veredicto

El MVP puede considerarse **demo-ready para el alcance previsto**.

### Razones

- la run canonica puede recrearse con tooling reproducible
- el walkthrough principal existe de punta a punta
- el wow moment de `MEAL_VOUCHER` se sostiene
- los casos complementarios refuerzan la narrativa
- summary, concept analysis, drill-down y exports responden correctamente
- no quedaron fricciones criticas visibles en el recorrido principal

## Riesgos residuales no bloqueantes

- el drill-down sigue siendo la parte mas pesada del flujo
- conviene abrir el entorno unos minutos antes de una reunion para evitar
  latencia fria
- la validacion visual final proyectada o compartida en pantalla sigue siendo
  trabajo razonable de `EPIC 09`

## Recomendacion siguiente

Con este estado, el siguiente paso natural del proyecto es abrir
`EPIC 09 — Hardening, QA & Demo-Ready Closure`.
