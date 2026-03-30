# EPIC 06 — Summary, Concept Analysis & Explanation UI

## Contexto y objetivo

Esta epic construye el corazón visible del MVP. Si la `EPIC_05` resuelve cómo iniciar una corrida, esta epic resuelve cómo mostrar el valor del sistema una vez que la corrida terminó.

Es, probablemente, la parte más importante del producto desde el punto de vista comercial y de adopción inmediata.

La razón es simple:

- el usuario no compra una pantalla de upload
- no compra un backend ordenado
- no compra una arquitectura prolija

Lo que sí compra es la experiencia de ver, en segundos:

- qué conceptos conciliaron
- cuáles no
- qué tan grande es el problema
- por qué ocurre

La tesis de esta epic es:

> **El producto demuestra valor cuando transforma una corrida técnica en una lectura ejecutiva inmediata y en una explicación navegable por concepto.**

Esta epic debe construir una experiencia que haga visibles tres niveles de lectura:

1. **Nivel ejecutivo:** estado general de la corrida
2. **Nivel analítico:** resultados por concepto
3. **Nivel explicativo:** causas probables y recomendación

Al terminar esta epic, el producto debe tener:

- una pantalla de summary ejecutiva
- KPI cards claras y sobrias
- tabla de resultados por concepto con semaforización
- navegación hacia un concepto individual
- panel o vista de análisis por concepto
- bloque de explicación narrativa y causas probables

## Dominio(s) involucrado(s)

**D6 — Summary, Concept Analysis & Explanation UI**

## Dependencias

- **EPIC 03** completada o suficientemente avanzada, con payload estructurado de explicación
- **EPIC 04** completada o suficientemente avanzada, con endpoints y payloads de summary/result/detail
- **EPIC 05** completada o suficientemente avanzada, con layout, componentes base y setup flow

## Criterio de aceptación de la Epic completa

- [x] Existe una pantalla de summary de corrida conectada al backend
- [x] La summary muestra KPIs ejecutivos claros
- [x] Existe tabla por concepto con expected, observed, diff, diff % y status
- [x] La tabla prioriza visualmente conceptos con problemas
- [x] Existe navegación o expansión hacia análisis por concepto
- [x] La vista por concepto muestra KPIs, statement principal, causas probables y recomendación
- [x] La experiencia es clara, sobria, data-first y consistente con el usuario objetivo
- [x] Los conceptos wow del demo lucen convincentes en esta capa

## Estado: COMPLETADA

## Implementación WS15

- `docs/SUMMARY_CONCEPT_UI_BLUEPRINT.md` cierra objetivo funcional, anatomía, KPIs, tabla, patrón de navegación y CTA hacia drill-down
- la ruta `frontend/app/runs/[runId]/page.tsx` pasó de snapshot operativo a Summary Screen completa conectada a backend real
- se implementó navegación dedicada a Concept Analysis en `frontend/app/runs/[runId]/concepts/[resultId]/page.tsx`
- se dejaron loading, error y empty states consistentes para summary y concept analysis
- se preparó el handoff narrativo a drill-down en `frontend/app/runs/[runId]/concepts/[resultId]/drilldown/page.tsx`
- validación ejecutada: `cd frontend && npm run lint` y `cd frontend && npm run build`

---

## Feature 6.1 — Modelo visual del summary ejecutivo

**Objetivo:** fijar la estructura y función de la pantalla de summary antes de construir componentes concretos.

---

### Card 6.1.1 — Definir objetivo funcional de la Summary Screen

**Descripción:** esta card baja a una especificación concreta qué debe responder la pantalla principal post-run.

**Criterio de aceptación:**

- Existe una definición clara del propósito de la pantalla
- La pantalla responde preguntas ejecutivas concretas
- El objetivo sirve como guardrail para el resto de la epic

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Documentar que la Summary Screen debe responder:
  - ¿La corrida salió bien?
  - ¿Cuántos conceptos conciliaron?
  - ¿Dónde están los principales desvíos?
  - ¿Qué tan material es el problema?
- [ ] Documentar que la pantalla prioriza lectura rápida antes que detalle exhaustivo
- [ ] Commit sugerido: `docs(summary-ui): definir objetivo funcional de summary screen`

---

### Card 6.1.2 — Diseñar anatomía de la Summary Screen

**Descripción:** definir la estructura visual de la pantalla para que la implementación posterior sea coherente y consistente.

**Criterio de aceptación:**

- Existe una anatomía clara de la pantalla
- La jerarquía visual es explícita
- La estructura separa metadata, KPIs y tabla principal

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir bloques de pantalla:
  - header de corrida
  - KPI cards
  - overall status
  - tabla resumida por concepto
  - accesos a detalle
- [ ] Definir orden de lectura visual
- [ ] Commit sugerido: `docs(summary-ui): diseñar anatomia de summary screen`

---

## Feature 6.2 — Header y framing de corrida

**Objetivo:** mostrar contexto claro de la corrida analizada antes de entrar en números y estado.

---

### Card 6.2.1 — Implementar header de corrida en Summary Screen

**Descripción:** el header debe ubicar al usuario inmediatamente: qué período está viendo, qué archivo se procesó y qué corrida está revisando.

**Criterio de aceptación:**

- Existe header de corrida visible y claro
- El header muestra metadata relevante sin recargar
- La solución es consistente con la base visual del MVP

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Mostrar:
  - `run_id` o label amigable
  - período analizado
  - timestamp
  - nombre del archivo procesado
- [ ] Mantener tono ejecutivo y sobrio
- [ ] Integrar el header en layout reusable
- [ ] Commit sugerido: `feat(summary-ui): implementar header de corrida`

---

### Card 6.2.2 — Mostrar estado general de corrida

**Descripción:** la corrida necesita una etiqueta visual que sintetice el resultado global antes de que el usuario entre a la tabla.

**Criterio de aceptación:**

- Existe un bloque de `overall run status`
- El estado general es comprensible y visualmente claro
- El bloque funciona como síntesis de la corrida

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Mostrar `overall_run_status`
- [ ] Definir copy adecuado:
  - `Reconciled`
  - `Reconciled with Exceptions`
  - `Attention Required`
  - `Invalid Input`
- [ ] Integrar semántica visual consistente con status
- [ ] Commit sugerido: `feat(summary-ui): mostrar estado general de corrida`

---

## Feature 6.3 — KPI cards del summary

**Objetivo:** construir el bloque de lectura rápida que convierte resultados técnicos en señales ejecutivas.

---

### Card 6.3.1 — Definir KPIs principales de la Summary Screen

**Descripción:** antes de construir cards, hay que fijar qué métricas merecen protagonismo ejecutivo.

**Criterio de aceptación:**

- Existe un set cerrado de KPIs principales
- Los KPIs están alineados con la lógica del producto
- El set es compacto y suficiente

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Confirmar KPIs principales:
  - `Concepts Reconciled`
  - `Concepts with Minor Differences`
  - `Unreconciled Concepts`
  - `Total Amount Reconciled`
  - `Amount Pending Explanation`
- [ ] Validar que no se sumen KPIs accesorios innecesarios
- [ ] Commit sugerido: `docs(summary-ui): definir kpis principales`

---

### Card 6.3.2 — Implementar componente `RunSummaryCards`

**Descripción:** crear el componente visual que renderiza los KPIs principales con jerarquía, espaciado y semántica clara.

**Criterio de aceptación:**

- Existe componente de KPI cards reusable
- El componente comunica KPIs de forma legible y sobria
- Se adapta al layout desktop-first del MVP

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar grid o layout de KPI cards
- [ ] Renderizar label, valor y metadata mínima
- [ ] Integrar colores semánticos solo donde aporten claridad
- [ ] Commit sugerido: `feat(summary-ui): implementar RunSummaryCards`

---

### Card 6.3.3 — Conectar KPI cards con payload real del backend

**Descripción:** conectar el componente visual al endpoint de summary para que deje de ser estático.

**Criterio de aceptación:**

- Las KPI cards reflejan datos reales de una run
- Loading, error y empty state están contemplados
- El componente no depende de mocks para funcionar

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Consumir `GET /runs/{run_id}/summary`
- [ ] Mapear payload a cards reales
- [ ] Implementar loading state sobrio
- [ ] Implementar error state útil
- [ ] Commit sugerido: `feat(summary-ui): conectar KPI cards con backend`

---

## Feature 6.4 — Tabla de resultados por concepto

**Objetivo:** construir la tabla principal del MVP, que conecta la lectura ejecutiva con el análisis detallado.

---

### Card 6.4.1 — Definir columnas y comportamiento de la tabla principal

**Descripción:** esta card fija la estructura funcional de la tabla que el usuario usará para navegar los resultados.

**Criterio de aceptación:**

- Existe lista cerrada de columnas
- La tabla refleja la unidad de conciliación del producto
- El comportamiento de orden y foco está documentado

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Confirmar columnas:
  - `Concept`
  - `Expected`
  - `Observed`
  - `Diff`
  - `Diff %`
  - `Status`
  - `Explanation Preview` opcional
- [ ] Definir comportamiento de orden inicial
- [ ] Definir nivel de densidad visual aceptable
- [ ] Commit sugerido: `docs(summary-ui): definir tabla principal por concepto`

---

### Card 6.4.2 — Implementar componente `ConceptResultsTable`

**Descripción:** construir la tabla reusable que mostrará resultados agregados por concepto.

**Criterio de aceptación:**

- Existe componente de tabla reusable
- El componente muestra datos con jerarquía clara
- La tabla se ve limpia y entendible en desktop

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Implementar tabla base con columnas definidas
- [ ] Diseñar celdas numéricas alineadas correctamente
- [ ] Diseñar columna de estado con badge o semáforo
- [ ] Diseñar comportamiento hover y focus simple
- [ ] Commit sugerido: `feat(summary-ui): implementar ConceptResultsTable`

---

### Card 6.4.3 — Implementar semaforización y badges de estado

**Descripción:** los estados deben poder leerse en segundos sin convertir la pantalla en un tablero ruidoso.

**Criterio de aceptación:**

- Existen badges o indicadores visuales de estado
- La semaforización es consistente con el resto de la UI
- El color refuerza el texto, no lo reemplaza

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Crear badges para:
  - `Reconciled`
  - `Minor Difference`
  - `Unreconciled`
  - `Invalid / Incomplete`
- [ ] Aplicar estilo visual sobrio y consistente
- [ ] Validar legibilidad en tabla densa
- [ ] Commit sugerido: `feat(summary-ui): implementar semaforizacion de estados`

---

### Card 6.4.4 — Priorizar visualmente conceptos problemáticos

**Descripción:** la tabla debe llevar el ojo hacia los conceptos más relevantes para revisión y demo.

**Criterio de aceptación:**

- Los conceptos más críticos aparecen primero
- La tabla guía el recorrido narrativo del usuario
- La priorización es consistente con el valor del producto

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Ordenar por:
  - rojos primero
  - luego amarillos
  - luego verdes
- [ ] Definir desempate por materialidad o diff
- [ ] Confirmar comportamiento de orden por defecto
- [ ] Commit sugerido: `feat(summary-ui): priorizar conceptos problematicos en tabla`

---

### Card 6.4.5 — Conectar tabla con endpoint real de resultados

**Descripción:** conectar la tabla principal al backend para que opere sobre runs reales.

**Criterio de aceptación:**

- La tabla consume datos reales del endpoint
- Los conceptos se renderizan correctamente
- La tabla contempla loading, error y empty state

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Consumir `GET /runs/{run_id}/results`
- [ ] Mapear payload a estructura de tabla
- [ ] Implementar loading state
- [ ] Implementar empty state útil
- [ ] Implementar error state claro
- [ ] Commit sugerido: `feat(summary-ui): conectar tabla de conceptos con backend`

---

## Feature 6.5 — Navegación hacia análisis por concepto

**Objetivo:** permitir pasar de la visión general al concepto específico sin perder contexto.

---

### Card 6.5.1 — Definir patrón de navegación a Concept Analysis

**Descripción:** decidir cómo baja el usuario desde la tabla principal a la vista detallada de un concepto.

**Criterio de aceptación:**

- Existe patrón claro de navegación
- El patrón es simple y coherente con el MVP
- La navegación mantiene continuidad visual y mental

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Decidir entre:
  - página dedicada
  - panel lateral
  - expansión inline
- [ ] Priorizar claridad y simplicidad sobre sofisticación visual
- [ ] Documentar decisión final
- [ ] Commit sugerido: `docs(concept-ui): definir patron de navegacion a concept analysis`

---

### Card 6.5.2 — Implementar interacción de apertura desde la tabla

**Descripción:** conectar la tabla principal con la vista de análisis elegida.

**Criterio de aceptación:**

- El usuario puede abrir un concepto desde la tabla
- La interacción es evidente y consistente
- El flujo mantiene contexto de la corrida

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Agregar acción o interacción por fila
- [ ] Pasar `run_id` y `result_id`
- [ ] Mantener contexto visible de la corrida
- [ ] Commit sugerido: `feat(concept-ui): implementar apertura de concept analysis desde tabla`

---

## Feature 6.6 — Vista de análisis por concepto

**Objetivo:** construir la capa de lectura analítica donde el producto deja de mostrar solo números y empieza a mostrar estructura de explicación.

---

### Card 6.6.1 — Definir anatomía de la Concept Analysis Screen

**Descripción:** fijar la estructura base de la vista por concepto antes de implementarla.

**Criterio de aceptación:**

- Existe anatomía clara de la vista
- Se distinguen KPIs, explicación y evidencia resumida
- La estructura es coherente con la narrativa del producto

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir bloques:
  - header del concepto
  - KPIs del concepto
  - statement principal
  - causas probables
  - recomendación
  - evidencia resumida
- [ ] Definir orden de lectura
- [ ] Commit sugerido: `docs(concept-ui): definir anatomia de concept analysis`

---

### Card 6.6.2 — Implementar header del concepto

**Descripción:** el usuario debe ver inmediatamente qué concepto está analizando, para qué período y en qué estado se encuentra.

**Criterio de aceptación:**

- Existe header claro del concepto
- El header incluye estado y período
- La vista se siente enfocada y no ambigua

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Mostrar nombre del concepto
- [ ] Mostrar período
- [ ] Mostrar status del concepto
- [ ] Mostrar navegación de vuelta al summary si corresponde
- [ ] Commit sugerido: `feat(concept-ui): implementar header del concepto`

---

### Card 6.6.3 — Implementar KPIs del concepto

**Descripción:** construir el bloque numérico principal del concepto individual.

**Criterio de aceptación:**

- Existen KPIs del concepto visibles y ordenados
- Las métricas son legibles y útiles
- El bloque conecta números con lectura analítica

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Mostrar:
  - `Expected Total`
  - `Observed Total`
  - `Absolute Difference`
  - `Difference %`
  - `Records Analyzed`
  - `Employees Affected`
- [ ] Diseñar layout claro para estos KPIs
- [ ] Commit sugerido: `feat(concept-ui): implementar KPIs del concepto`

---

### Card 6.6.4 — Conectar vista de concepto con endpoint real

**Descripción:** enlazar la vista con el payload detallado del backend.

**Criterio de aceptación:**

- La vista consume datos reales del backend
- La estructura del payload se representa correctamente
- Loading, error y not found están contemplados

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Consumir `GET /runs/{run_id}/results/{result_id}`
- [ ] Mapear payload a header, KPIs y bloques de explicación
- [ ] Implementar loading state
- [ ] Implementar error/not found state
- [ ] Commit sugerido: `feat(concept-ui): conectar vista de concepto con backend`

---

## Feature 6.7 — Bloque de explicación del concepto

**Objetivo:** mostrar el diferencial del producto con una narrativa clara, profesional y accionable.

---

### Card 6.7.1 — Implementar bloque `Statement Principal`

**Descripción:** el statement principal debe traducir el problema del concepto a una frase clara y de alto valor interpretativo.

**Criterio de aceptación:**

- Existe bloque visual destacado para el statement principal
- El statement es legible y se entiende sin esfuerzo
- El tono es coherente con el producto

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar bloque visual del statement
- [ ] Destacarlo sin sobreactuar visualmente
- [ ] Integrar texto desde payload estructurado
- [ ] Commit sugerido: `feat(concept-ui): implementar bloque de statement principal`

---

### Card 6.7.2 — Implementar bloque `Top Causes`

**Descripción:** esta es una de las piezas más importantes de la vista. Debe hacer evidente la composición de la diferencia.

**Criterio de aceptación:**

- Existe lista clara de causas probables
- Cada causa puede mostrar impacto y evidencia resumida
- El bloque se siente fuerte pero no recargado

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Renderizar causas ordenadas
- [ ] Mostrar:
  - nombre de la causa
  - impacto estimado
  - registros/empleados afectados cuando aplique
- [ ] Definir visual de ranking sobrio
- [ ] Commit sugerido: `feat(concept-ui): implementar bloque de top causes`

---

### Card 6.7.3 — Implementar bloque `Recommended Review Action`

**Descripción:** la explicación debe cerrar con un siguiente paso concreto, no solo con diagnóstico.

**Criterio de aceptación:**

- Existe bloque de recomendación final
- La recomendación es breve, útil y profesional
- El bloque se integra naturalmente con la narrativa explicativa

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar visual del bloque de recomendación
- [ ] Integrar texto desde payload del backend
- [ ] Mantener tono sobrio y no alarmista
- [ ] Commit sugerido: `feat(concept-ui): implementar recommended review action`

---

### Card 6.7.4 — Implementar framing de certeza y evidencia resumida

**Descripción:** el usuario debe entender que el sistema está mostrando causas probables basadas en reglas y evidencia observada, no una sentencia absoluta.

**Criterio de aceptación:**

- Existe framing sutil de certeza
- La pantalla muestra evidencia resumida sin volverse técnica de más
- El bloque refuerza credibilidad del sistema

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Mostrar subtítulo o nota breve sobre análisis basado en reglas/records
- [ ] Mostrar evidencia resumida como:
  - `highest impact anomaly`
  - `top impacted employee`
  - `top impacted legal entity`
- [ ] Evitar texto excesivo o defensivo
- [ ] Commit sugerido: `feat(concept-ui): implementar framing de certeza y evidencia resumida`

---

## Feature 6.8 — CTA hacia drill-down

**Objetivo:** preparar la transición desde la explicación por concepto al detalle operativo que vendrá en la siguiente epic.

---

### Card 6.8.1 — Diseñar CTA `View Detailed Records`

**Descripción:** la vista por concepto debe invitar claramente al usuario a bajar al detalle cuando lo necesite.

**Criterio de aceptación:**

- Existe CTA visible hacia drill-down
- El CTA está bien posicionado en la vista
- El lenguaje es claro y profesional

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir copy del CTA
- [ ] Definir ubicación visual adecuada
- [ ] Preparar navegación futura a detalle
- [ ] Commit sugerido: `docs(concept-ui): diseñar CTA hacia drilldown`

---

### Card 6.8.2 — Implementar navegación placeholder o real hacia detalle

**Descripción:** si la siguiente epic aún no existe, al menos debe quedar preparada la navegación sin romper la experiencia.

**Criterio de aceptación:**

- Existe interacción hacia drill-down
- La navegación mantiene contexto de run y concepto
- El sistema no deja al usuario en un dead end

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Pasar `run_id` y `result_id` hacia detalle
- [ ] Implementar navegación real o placeholder estructurado
- [ ] Confirmar continuidad del flujo
- [ ] Commit sugerido: `feat(concept-ui): implementar paso hacia drilldown`

---

## Feature 6.9 — Estado de carga, error y empty states de la capa analítica

**Objetivo:** hacer que summary y concept analysis se sientan robustos y no frágiles frente a latencia o errores del backend.

---

### Card 6.9.1 — Implementar loading states del summary

**Descripción:** mientras la UI consulta datos, debe mostrar un estado transitorio sobrio y consistente.

**Criterio de aceptación:**

- La pantalla tiene loading state claro
- El loading respeta la estructura final de la vista
- El usuario entiende que el sistema está cargando datos reales

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar skeletons o placeholders para KPI cards
- [ ] Diseñar loading state para tabla
- [ ] Mantener consistencia con layout final
- [ ] Commit sugerido: `feat(summary-ui): implementar loading states`

---

### Card 6.9.2 — Implementar error states del summary y concept analysis

**Descripción:** las pantallas deben poder comunicar fallos de lectura sin romper tono ni claridad.

**Criterio de aceptación:**

- Existen error states claros y útiles
- El usuario recibe feedback accionable
- La experiencia sigue sintiéndose profesional

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar mensajes de error de carga
- [ ] Incluir CTA de retry cuando tenga sentido
- [ ] Implementar error states en summary y concept view
- [ ] Commit sugerido: `feat(ui): implementar error states de capa analitica`

---

### Card 6.9.3 — Implementar empty states y casos borde

**Descripción:** contemplar corridas sin resultados relevantes, conceptos no encontrados o runs vacías.

**Criterio de aceptación:**

- Existen empty states útiles
- Los casos borde no rompen la navegación
- La UI mantiene tono y claridad

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar empty state para corrida sin resultados
- [ ] Diseñar not found state para concepto inexistente
- [ ] Validar mensajes y tono
- [ ] Commit sugerido: `feat(ui): implementar empty states de summary y concepto`

---

## Feature 6.10 — Validación funcional y narrativa del wow moment

**Objetivo:** asegurar que las pantallas más importantes del MVP realmente sostengan la narrativa comercial definida.

---

### Card 6.10.1 — Validar Summary Screen con datos reales del demo

**Descripción:** verificar que la pantalla principal cuenta bien la historia general del período y guía naturalmente hacia los conceptos correctos.

**Criterio de aceptación:**

- La summary se entiende en segundos
- Los conceptos problemáticos aparecen donde deben
- La pantalla sirve para una demo de negocio real

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Probar summary con dataset demo real
- [ ] Revisar orden de conceptos y KPIs
- [ ] Ajustar visual o copy si el recorrido no es claro
- [ ] Commit sugerido: `test(summary-ui): validar summary screen con datos demo`

---

### Card 6.10.2 — Validar caso wow `MEAL_VOUCHER` en Concept Analysis

**Descripción:** este caso debe lucir especialmente fuerte en la vista por concepto.

**Criterio de aceptación:**

- `MEAL_VOUCHER` muestra una narrativa clara y convincente
- El usuario puede entender diferencia, causas y acción sin esfuerzo
- La vista soporta bien el momento wow del demo

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Abrir `MEAL_VOUCHER` desde la tabla
- [ ] Validar KPIs, statement, causes y recommendation
- [ ] Ajustar jerarquía visual si hace falta
- [ ] Commit sugerido: `test(concept-ui): validar wow case meal voucher`

---

### Card 6.10.3 — Validar caso `CHILDCARE`

**Descripción:** verificar que la vista soporta una explicación más de negocio que de error técnico.

**Criterio de aceptación:**

- `CHILDCARE` se entiende como caso de población faltante
- La narrativa se siente operativa y creíble
- La recomendación resultante es útil

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Validar vista de `CHILDCARE`
- [ ] Confirmar claridad del caso de missing population
- [ ] Ajustar copy o visual si fuera necesario
- [ ] Commit sugerido: `test(concept-ui): validar caso childcare`

---

### Card 6.10.4 — Validar caso `OVERTIME`

**Descripción:** verificar que la vista puede mostrar bien una anomalía tipo outlier.

**Criterio de aceptación:**

- `OVERTIME` prioriza correctamente el outlier
- La evidencia resumida aporta al análisis
- La vista mantiene claridad sin saturación

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Validar vista de `OVERTIME`
- [ ] Revisar foco visual sobre el outlier principal
- [ ] Confirmar claridad de recomendación
- [ ] Commit sugerido: `test(concept-ui): validar caso overtime`

---

## Resumen de commits esperados en EPIC 06

- `docs(summary-ui): definir objetivo funcional de summary screen`
- `docs(summary-ui): diseñar anatomia de summary screen`
- `feat(summary-ui): implementar header de corrida`
- `feat(summary-ui): mostrar estado general de corrida`
- `docs(summary-ui): definir kpis principales`
- `feat(summary-ui): implementar RunSummaryCards`
- `feat(summary-ui): conectar KPI cards con backend`
- `docs(summary-ui): definir tabla principal por concepto`
- `feat(summary-ui): implementar ConceptResultsTable`
- `feat(summary-ui): implementar semaforizacion de estados`
- `feat(summary-ui): priorizar conceptos problematicos en tabla`
- `feat(summary-ui): conectar tabla de conceptos con backend`
- `docs(concept-ui): definir patron de navegacion a concept analysis`
- `feat(concept-ui): implementar apertura de concept analysis desde tabla`
- `docs(concept-ui): definir anatomia de concept analysis`
- `feat(concept-ui): implementar header del concepto`
- `feat(concept-ui): implementar KPIs del concepto`
- `feat(concept-ui): conectar vista de concepto con backend`
- `feat(concept-ui): implementar bloque de statement principal`
- `feat(concept-ui): implementar bloque de top causes`
- `feat(concept-ui): implementar recommended review action`
- `feat(concept-ui): implementar framing de certeza y evidencia resumida`
- `docs(concept-ui): diseñar CTA hacia drilldown`
- `feat(concept-ui): implementar paso hacia drilldown`
- `feat(summary-ui): implementar loading states`
- `feat(ui): implementar error states de capa analitica`
- `feat(ui): implementar empty states de summary y concepto`
- `test(summary-ui): validar summary screen con datos demo`
- `test(concept-ui): validar wow case meal voucher`
- `test(concept-ui): validar caso childcare`
- `test(concept-ui): validar caso overtime`

---

## Notas técnicas

### Regla central de esta epic

La pantalla de summary y la vista por concepto deben optimizar:

- comprensión inmediata
- priorización visual
- lectura ejecutiva rápida
- transición natural hacia análisis

No deben optimizar:

- densidad máxima de datos
- flexibilidad extrema
- visualizaciones llamativas pero poco útiles

### Tensión principal que debe resolver esta epic

La UI tiene que verse:

- suficientemente seria para una multinacional
- suficientemente simple para entenderse en una demo
- suficientemente rica para demostrar valor analítico

Si una decisión mejora el “look” pero complica la lectura, no entra.

### Qué no entra en esta epic

- tabla completa de drill-down
- exportables
- historial multi-run
- portfolio/dashboard general del producto
- filtros avanzados de tabla
- colaboración o comentarios

Esta epic construye el núcleo del wow visual del MVP. El detalle operativo vendrá en la siguiente capa.
