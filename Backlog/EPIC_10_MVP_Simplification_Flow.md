# EPIC 10 — MVP Simplification & Single-Flow UX

## Contexto y objetivo

El producto actual ya demuestra potencia funcional, pero quedó más cerca de una
demo narrativa multicapa que de un MVP obvio, simple e intuitivo para un primer
usuario.

Hoy el flujo visible quedó estructurado como:

- setup
- summary
- concept analysis
- drill-down
- exports

Ese recorrido funciona, pero exige demasiadas decisiones, demasiado framing y
demasiados clicks para llegar al valor principal.

La hipótesis de esta epic es:

> **Para vender mejor el MVP, el usuario debe poder cargar archivos, correr la conciliación, leer un summary claro y bajar a evidencia exportable sin atravesar capas intermedias innecesarias.**

Esta epic no cambia la base lógica del motor ni la persistencia principal.
Reordena y simplifica la experiencia del producto para que el flujo visible
quede más cerca de:

1. `Upload + Run`
2. `Results Summary`
3. `Deep Dive + Export`

Y agrega un artefacto de salida más ejecutivo:

4. `PDF report`

Al terminar esta epic, el producto debe tener:

- una pantalla inicial más simple y enfocada
- menos decisiones visibles antes de correr una run
- una navegación más corta hacia el detalle útil
- fusión o absorción del `Concept Analysis` dentro de un `Deep Dive`
- exportables orientados a revisión y demo
- un flujo más fácil de entender en pocos minutos

## Dominio(s) involucrado(s)

Epic transversal con foco principal en UX, IA, frontend y exportables del MVP.

## Dependencias

- **EPIC 04** completada o suficientemente avanzada
- **EPIC 05** completada
- **EPIC 06** completada
- **EPIC 07** completada
- **EPIC 09** completada o suficientemente avanzada como baseline del estado actual

## Criterio de aceptación de la Epic completa

- [ ] El flujo principal visible del MVP se reduce a `Setup -> Summary -> Deep Dive`
- [ ] El setup expone solo los inputs imprescindibles por defecto
- [ ] Las opciones avanzadas quedan ocultas o absorbidas por defaults razonables
- [ ] `Concept Analysis` deja de ser una parada obligatoria separada
- [ ] El deep dive combina explicación y evidencia en un solo lugar
- [ ] El summary sigue siendo ejecutivo pero con menos fricción de navegación
- [ ] El producto ofrece un exportable PDF sobrio y presentable
- [ ] El flujo simplificado se valida end-to-end en local

## Estado: PENDIENTE

---

## Feature 10.1 — Redefinición del flujo visible del MVP

**Objetivo:** dejar explícita la nueva forma del producto antes de editar pantallas.

---

### Card 10.1.1 — Definir el flujo simplificado objetivo

**Descripción:** documentar el journey objetivo para alinear producto, UX y ejecución técnica.

**Criterio de aceptación:**

- Existe un flujo objetivo explícito y breve
- Queda claro qué pantallas sobreviven, cuáles se fusionan y cuáles dejan de ser obligatorias
- El equipo puede implementar la simplificación sin reinterpretaciones ambiguas

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir journey objetivo `Upload + Run -> Summary -> Deep Dive + Export`
- [x] Dejar explícito que `Concept Analysis` deja de ser pantalla intermedia obligatoria
- [x] Acordar objetivo de navegación: menos clicks y menos contexto accesorio
- [x] Documentar criterio de éxito de UX para esta epic
- [ ] Commit sugerido: `docs(product): definir flujo simplificado del MVP`

**Resultado de ejecucion:**

- flujo simplificado objetivo documentado en `docs/MVP_SIMPLIFIED_FLOW_BLUEPRINT.md`
- decision de producto cerrada:
  - `Upload + Run`
  - `Results Summary`
  - `Deep Dive + Export`
- `Concept Analysis` deja de ser parada intermedia obligatoria y pasa a absorberse dentro del `Deep Dive`
- criterio de éxito UX definido para medir la simplificación en la implementación

---

### Card 10.1.2 — Definir qué capas visibles salen del MVP principal

**Descripción:** decidir qué elementos actuales quedan fuera del flujo principal para reducir ruido.

**Criterio de aceptación:**

- Existe una lista explícita de elementos visibles a recortar
- Lo removido o escondido no compromete el valor core del MVP
- Se preserva la potencia del producto con menos fricción

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Identificar controles no esenciales del setup visible
- [x] Identificar bloques de copy o trazabilidad que agregan ruido
- [x] Identificar CTAs redundantes o vueltas de navegación evitables
- [x] Definir qué queda como avanzado, secundario o fuera de pantalla
- [ ] Commit sugerido: `docs(product): recortar capas visibles del MVP`

**Resultado de ejecucion:**

- recorte visible del MVP documentado en `docs/MVP_VISIBLE_LAYER_CUTS.md`
- decision explícita:
  - `Concept Analysis` sale como pantalla separada
  - su contenido se fusiona con `Drill-down` en el nuevo `Deep Dive`
- setup:
  - se mantienen uploads + CTA principal
  - opciones secundarias y bloques de readiness pasan a segundo plano
- summary:
  - se mantiene como hub principal
  - se reduce `Run Context`, `Traceability` y copy metodológico
- labels, CTAs y copy global quedan encaminados hacia un lenguaje más corto y operativo

---

## Feature 10.2 — Simplificación del setup

**Objetivo:** convertir la home en un punto de entrada simple y accionable.

---

### Card 10.2.1 — Reducir el setup a inputs mínimos por defecto

**Descripción:** el setup debe mostrar solo lo imprescindible para correr una conciliación en un MVP.

**Criterio de aceptación:**

- El usuario ve solo inputs esenciales al entrar
- El foco queda en cargar archivos y correr la run
- La pantalla deja de sentirse como workspace de demo

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir inputs mínimos visibles por defecto
- [x] Mantener `payroll.csv` y `expected_totals.csv` como foco principal
- [x] Revisar si `period` se infiere o queda como campo simple
- [x] Simplificar el bloque superior de contexto y estado
- [x] Reducir copy de preparación y framing narrativo
- [ ] Commit sugerido: `feat(ui): simplificar setup al flujo minimo del MVP`

**Resultado de ejecucion:**

- home simplificada en `frontend/app/page.tsx`
- setup visible recortado en `frontend/components/setup/run-setup-form.tsx`
- primera vista ahora enfocada en:
  - período
  - `payroll.csv`
  - `expected_totals.csv`
  - CTA `Run Reconciliation`
- se removieron de la lectura principal:
  - métricas iniciales de run
  - framing de workspace/demo
  - bloque dominante de archivos de referencia
- feedback de setup y ejecución reescrito en `frontend/components/setup/setup-workspace.tsx` con lenguaje más corto y operativo
- validación ejecutada:
  - `cd frontend && npm run lint`

---

### Card 10.2.2 — Mover opciones secundarias a advanced settings

**Descripción:** las decisiones no esenciales deben existir sin competir con la acción principal.

**Criterio de aceptación:**

- Opciones secundarias no distraen del flujo principal
- El setup mantiene potencia sin sobrecargar la primera vista
- Los defaults elegidos sostienen el caso demo normal

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Mover `legal entity scope` a sección avanzada o resolverlo por default
- [x] Mover `tolerance profile` a sección avanzada o resolverlo por default
- [x] Mover `exceptions analysis` a sección avanzada o dejarlo siempre activo
- [x] Revisar si previews laterales deben simplificarse o colapsarse
- [x] Validar que el CTA principal siga claro después del recorte
- [ ] Commit sugerido: `feat(ui): ocultar opciones avanzadas del setup`

**Resultado de ejecucion:**

- opciones secundarias movidas a `Advanced settings`
- preview de expected totals y validaciones movidos a sección colapsable `Reference preview and validation`
- `legal entity scope`, `tolerance profile` y `exceptions analysis` ya no compiten con la acción principal
- el CTA principal queda visible como cierre natural del flujo simplificado
- validación ejecutada:
  - `cd frontend && npm run lint`

---

### Card 10.2.3 — Simplificar feedback de ejecución y salida al summary

**Descripción:** una vez corrida la run, el sistema debe llevar al usuario directo al valor, sin pasos intermedios ni estados ambiguos.

**Criterio de aceptación:**

- La ejecución se comunica de forma breve y clara
- El usuario entiende qué pasó y hacia dónde sigue
- El redirect al summary es natural y sin ruido

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [ ] Revisar feedback de creación, upload y ejecución de run
- [ ] Reducir mensajes redundantes o demasiado técnicos
- [ ] Alinear CTA final a `View results` o equivalente simple
- [ ] Confirmar redirect limpio al summary al completar ejecución
- [ ] Commit sugerido: `feat(ui): simplificar feedback post-run`

---

## Feature 10.3 — Simplificación de navegación y arquitectura de resultados

**Objetivo:** reducir la cantidad de capas entre summary y evidencia.

---

### Card 10.3.1 — Redefinir el summary como hub principal de resultados

**Descripción:** el summary debe ser la pantalla principal de lectura y decisión, sin pedir pasos extra para entender qué hacer después.

**Criterio de aceptación:**

- El summary comunica estado, materialidad y próximos pasos con claridad
- Desde la tabla se puede abrir el detalle útil en un click
- La pantalla evita bloques accesorios que no mejoran la decisión

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Revisar bloques del summary y eliminar ruido no esencial
- [x] Mantener KPIs y tabla como centro de lectura
- [x] Simplificar traceability visible si no ayuda a decisión inmediata
- [x] Alinear CTA por concepto hacia el nuevo deep dive
- [x] Revisar jerarquía de export summary dentro del flujo
- [ ] Commit sugerido: `feat(ui): simplificar summary como hub principal`

**Resultado de ejecucion:**

- summary simplificado en `frontend/components/summary/run-summary-screen.tsx`
- tabla principal alineada al nuevo lenguaje en `frontend/components/summary/concept-results-table.tsx`
- cambios principales:
  - header más corto y menos narrativo
  - `Run Context` reducido a `Results`
  - metadata técnica removida de la primera lectura
  - traceability reducida a eventos recientes en bloque secundario
  - CTA por concepto simplificado a `View details`
- validación ejecutada:
  - `cd frontend && npm run lint`

---

### Card 10.3.2 — Fusionar explicación y evidencia en un solo deep dive

**Descripción:** el usuario no debería pasar por una pantalla entera separada solo para leer una explicación antes de ver la evidencia.

**Criterio de aceptación:**

- Existe una única pantalla de detalle por concepto
- Esa pantalla combina explicación ejecutiva y tabla de evidencia
- El flujo desde summary al detalle se resuelve en un solo salto

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Diseñar estructura objetivo del `Deep Dive`
- [x] Reubicar statement principal y top causes dentro del deep dive
- [x] Mantener la tabla de registros como segunda mitad de la misma pantalla
- [x] Reducir navegación de ida y vuelta entre pantallas intermedias
- [x] Revisar componentes existentes para reutilización y fusión
- [ ] Commit sugerido: `feat(ui): fusionar concept analysis y drilldown`

**Resultado de ejecucion:**

- nuevo componente unificado en `frontend/components/deep-dive/deep-dive-screen.tsx`
- la ruta `frontend/app/runs/[runId]/concepts/[resultId]/page.tsx` ahora carga:
  - payload de concept detail
  - payload de drilldown
  - ambos en una sola vista `Deep Dive`
- el nuevo `Deep Dive` combina:
  - summary statement
  - recommended action
  - top causes
  - KPIs de concepto
  - filtros
  - tabla de evidencia
- la ruta vieja `.../drilldown` ahora redirige a la ruta de concepto para evitar duplicación de flujo
- validación ejecutada:
  - `cd frontend && npm run lint`

---

### Card 10.3.3 — Simplificar rutas, labels y CTAs del flujo

**Descripción:** el producto debe sentirse más corto también en su lenguaje y navegación.

**Criterio de aceptación:**

- Las rutas y labels expresan mejor el flujo real
- Los CTAs principales son consistentes entre pantallas
- La app se percibe menos fragmentada

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Revisar naming visible de `Concept Analysis` vs `Deep Dive`
- [x] Unificar labels de navegación y botones de retorno
- [x] Confirmar que la profundidad del flujo no obliga clicks de más
- [x] Ajustar breadcrumbs o links secundarios si hacen falta
- [ ] Commit sugerido: `refactor(ui): simplificar rutas y CTAs del MVP`

**Resultado de ejecucion:**

- labels visibles alineados a:
  - `Results`
  - `View details`
  - `Deep Dive`
- la ruta vieja de `drilldown` redirige a la ruta unificada de concepto
- snapshots y loaders fueron alineados al nuevo lenguaje del flujo
- validación ejecutada:
  - `cd frontend && npm run lint`

---

## Feature 10.4 — Exportables ejecutivos del flujo simplificado

**Objetivo:** reforzar la salida del MVP con exportes más presentables y más cercanos al uso real.

---

### Card 10.4.1 — Definir el modelo de reporte exportable del MVP

**Descripción:** antes de implementar el PDF conviene cerrar qué historia cuenta y qué nivel de detalle incluye.

**Criterio de aceptación:**

- Existe una estructura explícita del reporte PDF
- El reporte es sobrio, ejecutivo y útil
- El alcance del PDF está controlado para no sobrediseñar el MVP

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir si el PDF es por run, por concepto o ambos en MVP
- [x] Definir secciones mínimas del reporte
- [x] Definir si el PDF usa summary + concepto wow como baseline
- [x] Definir criterio visual sobrio para PDF MVP
- [ ] Commit sugerido: `docs(exports): definir reporte PDF del MVP`

**Resultado de ejecucion:**

- spec del PDF MVP documentada en `docs/MVP_PDF_REPORT_SPEC.md`
- decisión cerrada:
  - PDF inicial por concepto
  - exportado desde el `Deep Dive`
  - foco en resumen ejecutivo + evidencia breve

---

### Card 10.4.2 — Implementar export PDF del deep dive o reporte resumido

**Descripción:** construir la primera versión funcional del exportable en PDF para uso demo y revisión ejecutiva.

**Criterio de aceptación:**

- El producto puede exportar al menos un PDF útil y presentable
- El contenido es consistente con los datos mostrados en UI
- El flujo de descarga es claro

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Elegir estrategia técnica de generación de PDF para MVP
- [x] Implementar endpoint o pipeline de export PDF
- [x] Construir template inicial del reporte
- [x] Conectar CTA visible desde summary o deep dive
- [x] Validar naming, contenido y descarga
- [ ] Commit sugerido: `feat(exports): agregar reporte PDF del MVP`

**Resultado de ejecucion:**

- dependencia `reportlab` agregada en `backend/requirements.txt`
- endpoint PDF agregado en `backend/app/api/routes/runs.py`
- generación del reporte implementada en `backend/app/services/runs.py`
- CTA `Export PDF report` agregado al `Deep Dive`
- validación ejecutada:
  - `cd backend && .venv/bin/ruff check app`
  - `cd backend && .venv/bin/python -m unittest tests.test_runs_api_flow`
  - `cd frontend && npm run lint`

---

### Card 10.4.3 — Alinear exportables con el flujo simplificado

**Descripción:** CSV y PDF deben sentirse parte del mismo producto, no salidas dispersas.

**Criterio de aceptación:**

- Los exportables tienen naming y entry points consistentes
- Se entiende qué export sirve para qué caso
- La UI no multiplica acciones sin explicar su valor

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [x] Revisar naming de summary CSV y detail CSV
- [x] Ubicar PDF y CSV en puntos de decisión claros
- [x] Reducir redundancia de CTAs de export
- [x] Validar consistencia entre contenido exportado y pantalla origen
- [ ] Commit sugerido: `chore(exports): alinear exportables al flujo simplificado`

**Resultado de ejecucion:**

- exportables alineados por pantalla:
  - summary -> `Export summary`
  - deep dive -> `Export evidence CSV` + `Export PDF report`
- `ExportCsvButton` quedó unificado sobre el mismo patrón reusable de descarga
- naming y entry points ahora acompañan la acción principal de cada pantalla
- validación ejecutada:
  - `cd frontend && npm run lint`
  - `cd backend && .venv/bin/python -m unittest tests.test_runs_api_flow`

---

## Feature 10.5 — Simplificación de copy y framing visual

**Objetivo:** hacer que el producto suene y se sienta más simple.

---

### Card 10.5.1 — Reescribir el copy del producto hacia lenguaje operativo simple

**Descripción:** hoy parte del copy está demasiado orientado a narrativa de demo y demasiada explicación de contexto.

**Criterio de aceptación:**

- El lenguaje visible es más directo
- La UI habla de tareas, no de performance narrativa
- El usuario entiende qué hacer sin leer demasiado

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Revisar copy de home, summary y detalle
- [x] Reemplazar framing de `demo workspace` por framing operativo simple
- [x] Reducir texto de apoyo donde no aporta acción
- [x] Confirmar tono sobrio y ejecutivo
- [ ] Commit sugerido: `copy(ui): simplificar lenguaje del MVP`

**Resultado de ejecucion:**

- copy principal reescrito en:
  - `frontend/app/page.tsx`
  - `frontend/components/ui/empty-state.tsx`
  - `frontend/components/setup/run-setup-form.tsx`
  - `frontend/components/summary/run-summary-screen.tsx`
  - `frontend/components/deep-dive/deep-dive-screen.tsx`
- el lenguaje visible ahora prioriza:
  - upload
  - run
  - results
  - details
  - export
- validación ejecutada:
  - `cd frontend && npm run lint`

---

### Card 10.5.2 — Reducir chrome y bloques accesorios de trazabilidad visible

**Descripción:** la trazabilidad sigue siendo valiosa, pero no todo debe estar siempre al frente.

**Criterio de aceptación:**

- La interfaz tiene menos bloques contextuales secundarios
- Lo importante aparece primero y lo accesorio queda subordinado
- El producto se siente más limpio y menos cargado

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Revisar `Run Context`, `Traceability`, `Evidence framing` y bloques similares
- [x] Mover metadata secundaria a zonas menos dominantes
- [x] Reducir paneles repetidos entre summary y detalle
- [x] Validar continuidad visual tras el recorte
- [ ] Commit sugerido: `chore(ui): reducir chrome accesorio del MVP`

**Resultado de ejecucion:**

- `Run Context` quedó reducido a `Results`
- `Traceability` pasó a eventos recientes y bloques secundarios
- `Evidence framing` como capa separada salió del flujo principal
- metadata técnica repetida dejó de dominar setup, summary y detalle
- validación ejecutada:
  - `cd frontend && npm run lint`

---

## Feature 10.6 — Validación del MVP simplificado

**Objetivo:** comprobar que la simplificación mejora el producto y no solo lo hace “más corto”.

---

### Card 10.6.1 — Validar el flujo simplificado end-to-end

**Descripción:** verificar que el nuevo recorrido principal funciona como producto coherente.

**Criterio de aceptación:**

- El nuevo flujo corre de punta a punta
- No aparecen regresiones funcionales graves
- El valor principal se entiende más rápido que antes

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Ejecutar setup simplificado
- [x] Correr una run completa
- [x] Revisar summary simplificado
- [x] Abrir deep dive unificado
- [x] Descargar exportes disponibles
- [x] Documentar issues o fricciones residuales
- [ ] Commit sugerido: `test(ux): validar flujo simplificado end-to-end`

**Resultado de ejecucion:**

- flujo simplificado validado localmente con:
  - setup simplificado
  - summary simplificado
  - deep dive unificado
  - exportes CSV y PDF
- evidencia resumida en `docs/MVP_SIMPLIFICATION_VALIDATION.md`
- validación ejecutada:
  - `cd frontend && npm run lint`
  - `cd backend && .venv/bin/ruff check app`
  - `cd backend && .venv/bin/python -m unittest tests.test_runs_api_flow`

---

### Card 10.6.2 — Medir claridad de demo y tiempo hasta insight

**Descripción:** la simplificación debe traducirse en menos fricción perceptible.

**Criterio de aceptación:**

- Existe validación breve del before/after
- Se puede explicar el producto más rápido
- El flujo principal reduce clicks y tiempo hasta insight

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Medir clicks desde home hasta detalle útil
- [x] Medir tiempo aproximado hasta primer insight relevante
- [x] Comparar flujo previo vs flujo simplificado
- [x] Registrar criterio final de éxito o ajustes pendientes
- [ ] Commit sugerido: `docs(ux): medir claridad del MVP simplificado`

**Resultado de ejecucion:**

- before/after documentado en `docs/MVP_SIMPLIFICATION_VALIDATION.md`
- mejora principal registrada:
  - de `2 clicks` a `1 click` desde summary hasta evidencia útil
- veredicto documentado:
  - menos fricción visible
  - menos carga cognitiva
  - narrativa operativa más simple
