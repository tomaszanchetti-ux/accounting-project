# EPIC 07 — Drill-down, Exports & Demo Traceability

## Contexto y objetivo

Esta epic construye la capa operativa que convierte al MVP en una herramienta de trabajo y no solo en una vista analítica atractiva.

Hasta este punto, el producto ya puede:

- preparar y ejecutar una run
- resumir el estado general de conciliación
- mostrar resultados por concepto
- explicar causas probables y recomendaciones

Pero todavía falta una capacidad crítica para que el usuario termine de confiar en el sistema:

> **poder bajar a los registros concretos que explican una diferencia, y llevarse esa evidencia fuera de la pantalla.**

Ese es el rol de esta epic.

Su objetivo es completar el recorrido natural del usuario:

1. ve una corrida con problemas
2. abre un concepto
3. entiende las causas probables
4. baja al detalle concreto
5. puede exportar la evidencia o resultado

Además, esta epic refuerza una idea clave para el valor del MVP:

> **cada resultado del sistema debe poder rastrearse hacia registros reales y generar una salida utilizable.**

Al terminar esta epic, el producto debe tener:

- una vista de drill-down por concepto
- tabla de registros/empleados afectados
- filtros ligeros y orden útil
- indicadores de anomalía por línea
- exportables básicos de summary y exceptions
- una capa más fuerte de trazabilidad visible para demo

## Dominio(s) involucrado(s)

**D7 — Drill-down, Exports & Demo Traceability**

## Dependencias

- **EPIC 04** completada o suficientemente avanzada, con endpoints de drill-down y staging lines
- **EPIC 06** completada o suficientemente avanzada, con navegación desde concept analysis
- **EPIC 03** completada o suficientemente avanzada, con excepciones y causas detectadas

## Criterio de aceptación de la Epic completa

- [x] Existe una vista de drill-down conectada al backend
- [x] La vista muestra registros concretos que explican un concepto
- [x] Los registros muestran excepción asociada, empleado, importe y observación
- [x] Existen filtros ligeros y ordenamientos útiles
- [x] La navegación desde concept analysis hacia drill-down funciona correctamente
- [x] El usuario puede exportar un summary básico de conciliación
- [x] El usuario puede exportar un detalle básico de excepciones o registros impactados
- [x] La experiencia completa refuerza trazabilidad y credibilidad del producto

## Estado: COMPLETADA

## Implementacion WS16

- `docs/DRILLDOWN_UI_BLUEPRINT.md` fija el objetivo funcional del drill-down y
  confirma su alcance MVP antes de implementar UI
- `docs/EXPORTS_MVP.md` fija el alcance final de exportables y naming de
  archivos del MVP
- el drill-down queda formalizado como la capa que aterriza la explanation
  layer en evidencia concreta, no como una pantalla transaccional
- se confirma que la vista mostrara detalle por linea y por empleado asociado,
  con foco analitico, filtros ligeros y exportabilidad basica
- el blueprint ya define anatomia visual, resumen superior y columnas base de
  la tabla para implementar la pantalla con continuidad respecto de summary y
  concept analysis
- se implemento la pantalla real de drill-down conectada a
  `GET /runs/{run_id}/results/{result_id}/drilldown`
- se implementaron exports CSV reales desde backend para summary de run y
  detalle por concepto
- se integraron acciones de export en Summary, Concept Analysis y Drill-down
- se reforzo la trazabilidad visible con metadata de run, `rules_version` y
  eventos recientes en las pantallas analiticas
- se agregaron tabla reusable, filtros por excepcion, empleado y
  `legal_entity`, ordenamientos utiles y estados de loading/error/empty
- la navegacion desde Concept Analysis ya aterriza en una vista operativa con
  retorno claro a concept y summary
- validacion ejecutada:
  - `cd backend && .venv/bin/python -m unittest tests.test_runs_api_flow`
  - `cd frontend && npm run lint`
  - `cd frontend && npm run build`

---

## Feature 7.1 — Definición funcional del drill-down

**Objetivo:** fijar qué es exactamente el drill-down del MVP y qué debe responder.

---

### Card 7.1.1 — Definir objetivo funcional del drill-down

**Descripción:** esta card baja a especificación qué debe lograr la vista de detalle operativo y qué pregunta del usuario resuelve.

**Criterio de aceptación:**

- Existe definición clara del propósito del drill-down
- La vista responde una pregunta operativa concreta
- El objetivo sirve como guardrail para toda la epic

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Documentar que el drill-down debe responder:
  - ¿qué registros explican esta diferencia?
  - ¿qué empleados están involucrados?
  - ¿qué anomalías concretas fueron detectadas?
- [x] Documentar que el drill-down no reemplaza la explanation layer, la aterriza
- [ ] Commit sugerido: `docs(drilldown): definir objetivo funcional del drilldown`

---

### Card 7.1.2 — Definir alcance del drill-down del MVP

**Descripción:** esta card deja claro qué nivel de detalle entra en MVP y qué se deja fuera para evitar sobrecarga.

**Criterio de aceptación:**

- Existe una definición explícita del alcance del drill-down
- Se documenta qué columnas, filtros y acciones entran
- Se protegen foco y simplicidad

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Confirmar que el drill-down muestra detalle por línea y por empleado asociado
- [x] Confirmar que el MVP no incluye edición inline, comments ni workflow de aprobación
- [x] Definir que el drill-down es analítico y exportable, no transaccional
- [ ] Commit sugerido: `docs(drilldown): definir alcance del drilldown del MVP`

---

## Feature 7.2 — Anatomía visual de la pantalla de drill-down

**Objetivo:** definir la estructura visual de la vista detallada antes de construir componentes.

---

### Card 7.2.1 — Diseñar estructura general de la Drill-down Screen

**Descripción:** establecer la anatomía base de la pantalla para que la implementación sea consistente y orientada a trabajo real.

**Criterio de aceptación:**

- Existe anatomía clara de la pantalla
- La jerarquía visual prioriza resumen y tabla
- La estructura es consistente con las vistas anteriores

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir bloques:
  - header del concepto
  - resumen superior del drill-down
  - filtros ligeros
  - tabla de registros
  - acciones de export
- [x] Definir orden de lectura visual
- [ ] Commit sugerido: `docs(drilldown-ui): diseñar estructura general de drilldown screen`

---

### Card 7.2.2 — Definir resumen superior del drill-down

**Descripción:** antes de llegar a la tabla, el usuario debe recibir una síntesis mínima de lo que está viendo.

**Criterio de aceptación:**

- Existe un bloque resumen claro en la parte superior
- Resume volumen y tipos de anomalía
- Ayuda a contextualizar la tabla de detalle

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir resumen superior con:
  - registros impactados
  - empleados afectados
  - tipos de anomalía detectados
- [x] Definir tono y nivel de detalle adecuados
- [ ] Commit sugerido: `docs(drilldown-ui): definir resumen superior del drilldown`

---

## Feature 7.3 — Tabla operativa de registros afectados

**Objetivo:** construir la tabla principal del drill-down, que muestra evidencia concreta por línea.

---

### Card 7.3.1 — Definir columnas de la tabla de drill-down

**Descripción:** fijar la estructura funcional de la tabla de registros para que sirva tanto a análisis como a export.

**Criterio de aceptación:**

- Existe una lista cerrada de columnas de la tabla
- Las columnas soportan análisis operativo real
- La tabla no queda ni demasiado pobre ni innecesariamente densa

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Confirmar columnas base:
  - `Record ID`
  - `Employee ID`
  - `Employee Name`
  - `Legal Entity`
  - `Concept`
  - `Amount`
  - `Period`
  - `Exception Type`
  - `Observation`
- [x] Evaluar visibilidad de `cost_center` según espacio disponible
- [ ] Commit sugerido: `docs(drilldown-ui): definir columnas de la tabla de drilldown`

---

### Card 7.3.2 — Implementar componente `ExceptionDrilldownTable`

**Descripción:** construir la tabla reusable que mostrará el detalle operativo del concepto.

**Criterio de aceptación:**

- Existe tabla reusable de drill-down
- La tabla es legible, sobria y orientada a análisis
- El componente soporta estados de loading, empty y error

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Implementar tabla con columnas definidas
- [x] Diseñar celdas numéricas alineadas y texto legible
- [x] Diseñar badges o labels de excepción
- [x] Implementar estados base de carga y vacío
- [ ] Commit sugerido: `feat(drilldown-ui): implementar ExceptionDrilldownTable`

---

### Card 7.3.3 — Implementar resaltado visual de anomalías

**Descripción:** la tabla debe permitir identificar rápido qué registros son más relevantes sin caer en exceso visual.

**Criterio de aceptación:**

- Las filas con anomalías relevantes se distinguen con claridad
- El resaltado es sobrio y consistente
- El diseño no compite con la legibilidad de la tabla

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir badge visual por `exception_type`
- [x] Aplicar color sutil o indicador por severidad
- [x] Evitar decoraciones ruidosas o excesivas
- [ ] Commit sugerido: `feat(drilldown-ui): implementar resaltado visual de anomalias`

---

## Feature 7.4 — Filtros y orden operativo

**Objetivo:** permitir que el usuario reduzca ruido y priorice revisión sin convertir la vista en una herramienta compleja.

---

### Card 7.4.1 — Implementar filtro por tipo de excepción

**Descripción:** este es el filtro más útil del MVP porque permite aislar rápidamente la causa que el usuario quiere revisar.

**Criterio de aceptación:**

- El usuario puede filtrar por `exception_type`
- El filtro se integra naturalmente con la tabla
- La interacción es simple y rápida

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir control UI para filtro por excepción
- [x] Integrarlo con el dataset de drill-down
- [x] Soportar reset de filtro fácilmente
- [ ] Commit sugerido: `feat(drilldown-ui): implementar filtro por tipo de excepcion`

---

### Card 7.4.2 — Implementar filtro por empleado

**Descripción:** permite revisar rápidamente si una diferencia está concentrada en pocos empleados o investigar un caso puntual.

**Criterio de aceptación:**

- El usuario puede filtrar por empleado
- El filtro resulta útil en casos wow y revisión puntual
- La UI no se vuelve compleja por este agregado

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir control simple para empleado
- [x] Integrar con tabla existente
- [x] Manejar no-match y reset
- [ ] Commit sugerido: `feat(drilldown-ui): implementar filtro por empleado`

---

### Card 7.4.3 — Implementar filtro por `legal_entity`

**Descripción:** esta dimensión puede enriquecer el análisis cuando el concepto tenga distribución organizativa relevante.

**Criterio de aceptación:**

- Existe filtro por `legal_entity` si hay datos suficientes
- El filtro aporta sin recargar la pantalla
- La interacción se mantiene opcional y liviana

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Implementar filtro por `legal_entity`
- [x] Mostrarlo solo cuando aporte valor
- [x] Validar compatibilidad con otros filtros
- [ ] Commit sugerido: `feat(drilldown-ui): implementar filtro por legal entity`

---

### Card 7.4.4 — Implementar ordenamientos útiles del drill-down

**Descripción:** más allá de los filtros, el usuario necesita poder priorizar por monto o severidad visualmente.

**Criterio de aceptación:**

- Existen ordenamientos relevantes y simples
- La tabla puede priorizar registros más impactantes
- El ordenamiento no introduce complejidad innecesaria

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Soportar orden por:
  - mayor monto
  - severidad/anomalía
  - employee id si hace falta
- [x] Definir orden por defecto más útil
- [ ] Commit sugerido: `feat(drilldown-ui): implementar ordenamientos utiles`

---

## Feature 7.5 — Conexión del drill-down con backend real

**Objetivo:** enlazar la pantalla de detalle con los endpoints existentes para que opere sobre datos reales.

---

### Card 7.5.1 — Conectar vista con `GET /runs/{run_id}/results/{result_id}/drilldown`

**Descripción:** integrar la tabla y el resumen superior con el endpoint real del backend.

**Criterio de aceptación:**

- La vista consume datos reales del endpoint
- La tabla refleja registros persistidos de la run
- La conexión no depende de mocks

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Consumir endpoint de drill-down
- [x] Mapear payload a tabla y resumen superior
- [x] Integrar estado de loading y error
- [ ] Commit sugerido: `feat(drilldown-ui): conectar vista de detalle con backend`

---

### Card 7.5.2 — Validar consistencia entre summary, concept analysis y drill-down

**Descripción:** el usuario no debe sentir saltos o contradicciones entre capas del producto.

**Criterio de aceptación:**

- Los números y conceptos son consistentes entre vistas
- El contexto se mantiene a lo largo de la navegación
- La experiencia se siente continua y confiable

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Verificar consistencia entre:
  - tabla de conceptos
  - detalle por concepto
  - drill-down de registros
- [x] Validar continuidad de `run_id`, `result_id` y concepto visible
- [x] Corregir cualquier drift entre payloads
- [ ] Commit sugerido: `test(drilldown-ui): validar consistencia entre capas de analisis`

---

## Feature 7.6 — Navegación completa de análisis a detalle

**Objetivo:** cerrar el flujo analítico completo desde el summary hasta la evidencia concreta.

---

### Card 7.6.1 — Implementar navegación desde Concept Analysis a Drill-down

**Descripción:** esta card convierte el CTA de la epic anterior en navegación funcional real.

**Criterio de aceptación:**

- El usuario puede llegar al drill-down desde la vista por concepto
- La navegación mantiene contexto
- El flujo es simple y predecible

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Implementar navegación real
- [x] Preservar `run_id` y `result_id`
- [x] Mostrar contexto del concepto en destino
- [ ] Commit sugerido: `feat(drilldown-ui): conectar concept analysis con drilldown`

---

### Card 7.6.2 — Implementar navegación de regreso hacia Concept Analysis / Summary

**Descripción:** el usuario debe poder volver atrás sin perder orientación.

**Criterio de aceptación:**

- Existe navegación clara de retorno
- El usuario no queda atrapado en el detalle
- El flujo completo mantiene continuidad mental

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Agregar breadcrumb, back action o navegación visible
- [x] Mantener contexto del concepto y la corrida
- [ ] Commit sugerido: `feat(drilldown-ui): implementar navegacion de retorno desde detalle`

---

## Feature 7.7 — Exportables básicos del MVP

**Objetivo:** permitir que el usuario se lleve evidencia útil fuera de la app y reforzar percepción de producto real.

---

### Card 7.7.1 — Definir alcance de exportables del MVP

**Descripción:** fijar qué archivos exportables entran en esta fase del producto y con qué nivel de sofisticación.

**Criterio de aceptación:**

- Existe definición explícita del alcance de exportables
- Los exportables elegidos son suficientes para demo
- Se evita sobreingeniería innecesaria

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Confirmar exportables mínimos:
  - `Reconciliation Summary Export`
  - `Exception Detail Export`
- [x] Confirmar formato principal:
  - `CSV`
  - `Excel` si el costo de implementación es razonable
- [x] Documentar qué no entra todavía
- [ ] Commit sugerido: `docs(exports): definir alcance de exportables del MVP`

---

### Card 7.7.2 — Diseñar export `Reconciliation Summary`

**Descripción:** el summary export debe reflejar la tabla principal de conceptos de forma útil para seguimiento o presentación.

**Criterio de aceptación:**

- Existe definición clara del export de summary
- El archivo incluye campos esenciales del resultado
- Es útil sin depender de la UI

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir columnas del export summary:
  - concepto
  - expected
  - observed
  - diff
  - diff %
  - status
  - explanation preview opcional
- [x] Definir nombre y convención del archivo
- [ ] Commit sugerido: `docs(exports): diseñar export de reconciliation summary`

---

### Card 7.7.3 — Diseñar export `Exception Detail`

**Descripción:** este export debe capturar el detalle de registros impactados y sus anomalías principales.

**Criterio de aceptación:**

- Existe definición clara del export de exceptions
- El archivo refleja drill-down y evidencia operativa
- Es útil para revisión offline

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir columnas del export detail:
  - record id
  - employee id
  - employee name
  - legal entity
  - concept
  - amount
  - period
  - exception type
  - observation
- [x] Definir naming del archivo
- [ ] Commit sugerido: `docs(exports): diseñar export de exception detail`

---

### Card 7.7.4 — Implementar export de summary desde backend

**Descripción:** construir el backend necesario para descargar el resultado resumido de la corrida.

**Criterio de aceptación:**

- Existe endpoint o servicio para exportar summary
- El archivo contiene datos reales persistidos
- La descarga funciona de forma consistente

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Implementar generación de CSV/archivo summary
- [x] Exponer endpoint de descarga
- [x] Integrar naming y metadata de la run
- [ ] Commit sugerido: `feat(exports): implementar export de summary desde backend`

---

### Card 7.7.5 — Implementar export de exception detail desde backend

**Descripción:** construir el backend necesario para descargar el detalle operativo de un concepto o corrida.

**Criterio de aceptación:**

- Existe endpoint o servicio para exportar detalle
- El archivo refleja registros y excepciones reales
- La descarga funciona de forma consistente

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Implementar generación de CSV/archivo detail
- [x] Exponer endpoint de descarga
- [x] Validar consistencia con drill-down UI
- [ ] Commit sugerido: `feat(exports): implementar export de exception detail desde backend`

---

### Card 7.7.6 — Implementar acciones de export en UI

**Descripción:** exponer la capacidad de descarga desde summary, concept analysis o drill-down según corresponda.

**Criterio de aceptación:**

- El usuario puede iniciar export desde UI
- Las acciones están bien ubicadas visualmente
- La UX de export es clara y no intrusiva

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir ubicación de acciones de export
- [x] Conectar summary export
- [x] Conectar detail export
- [x] Implementar feedback mínimo de descarga
- [ ] Commit sugerido: `feat(exports-ui): implementar acciones de export en UI`

---

## Feature 7.8 — Trazabilidad visible del producto

**Objetivo:** reforzar visualmente que cada resultado tiene soporte en datos reales, archivos procesados y registros concretos.

---

### Card 7.8.1 — Mostrar metadata útil de origen en drill-down o concept view

**Descripción:** sin construir un panel de auditoría completo, el producto puede mostrar pequeños elementos de trazabilidad visibles que aumentan confianza.

**Criterio de aceptación:**

- Existen referencias visibles a origen de datos y contexto de corrida
- La metadata visible aporta confianza sin recargar
- El usuario entiende que el sistema está apoyado en inputs concretos

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Mostrar metadata útil como:
  - período procesado
  - fuente de archivo
  - cantidad de registros
  - run label o timestamp
- [x] Ubicar metadata en summary/concept/drilldown donde aporte
- [ ] Commit sugerido: `feat(traceability-ui): mostrar metadata visible de origen`

---

### Card 7.8.2 — Integrar `rules_version` o metadata de ejecución visible cuando sume valor

**Descripción:** el MVP puede beneficiarse de mostrar que la corrida está basada en reglas explícitas, siempre que eso no se vuelva técnico de más.

**Criterio de aceptación:**

- La metadata técnica visible está cuidadosamente dosificada
- Aporta credibilidad sin confundir al usuario
- El producto se siente trazable y serio

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Evaluar si mostrar `rules_version` o similar
- [x] Mostrarlo solo si aporta valor en la narrativa demo
- [x] Evitar exponer detalles innecesariamente técnicos
- [ ] Commit sugerido: `feat(traceability-ui): integrar metadata tecnica visible`

---

## Feature 7.9 — Estados de loading, error y casos borde del detalle

**Objetivo:** asegurar que la capa operativa se sienta robusta y usable en condiciones reales de demo.

---

### Card 7.9.1 — Implementar loading states del drill-down

**Descripción:** mientras se cargan registros reales, la UI debe mantener estructura y claridad.

**Criterio de aceptación:**

- Existen loading states coherentes en la vista de detalle
- La experiencia no se siente rota o improvisada
- El usuario entiende que se están cargando datos reales

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Diseñar skeleton o loading state para tabla
- [x] Diseñar loading state para resumen superior
- [x] Mantener consistencia visual con pantallas anteriores
- [ ] Commit sugerido: `feat(drilldown-ui): implementar loading states del detalle`

---

### Card 7.9.2 — Implementar error states del drill-down

**Descripción:** la capa operativa debe fallar con claridad si algo sale mal.

**Criterio de aceptación:**

- Existen error states claros en la vista de detalle
- Los errores no rompen navegación ni contexto
- La UX sigue siendo profesional y comprensible

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Diseñar error state de carga de detalle
- [x] Agregar acción de retry si corresponde
- [x] Mantener contexto visible del concepto/run
- [ ] Commit sugerido: `feat(drilldown-ui): implementar error states del detalle`

---

### Card 7.9.3 — Implementar empty states del drill-down

**Descripción:** contemplar casos donde no haya registros impactados visibles o el filtro elimine todas las filas.

**Criterio de aceptación:**

- Existen empty states útiles
- El usuario entiende por qué no ve registros
- Los filtros no dejan la experiencia en silencio ambiguo

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Diseñar empty state por ausencia de registros
- [x] Diseñar empty state por filtros sin match
- [x] Ajustar copy al tono del producto
- [ ] Commit sugerido: `feat(drilldown-ui): implementar empty states del detalle`

---

## Feature 7.10 — Validación integral del flujo analítico-operativo

**Objetivo:** verificar que el recorrido completo desde summary hasta export produce una experiencia sólida y convincente.

---

### Card 7.10.1 — Validar flujo completo `Summary -> Concept -> Drill-down`

**Descripción:** prueba integral del recorrido más importante del producto.

**Criterio de aceptación:**

- El flujo completo funciona sin fricciones
- El usuario mantiene contexto en cada paso
- La experiencia cuenta bien la historia del producto

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Abrir summary
- [x] Entrar a un concepto problemático
- [x] Abrir drill-down
- [x] Volver hacia arriba manteniendo contexto
- [x] Validar continuidad del flujo
- [ ] Commit sugerido: `test(flow): validar recorrido summary-concept-drilldown`

---

### Card 7.10.2 — Validar wow moment en `MEAL_VOUCHER`

**Descripción:** esta prueba verifica que el concepto estrella del demo tenga respaldo operativo real en la vista de detalle.

**Criterio de aceptación:**

- `MEAL_VOUCHER` muestra registros concretos alineados con la explicación
- El drill-down refuerza la narrativa multi-causa
- La combinación entre explicación y evidencia es convincente

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Abrir `MEAL_VOUCHER` desde summary
- [x] Verificar causas y luego drill-down
- [x] Confirmar presencia de líneas out-of-period, unmapped o duplicate según diseño
- [ ] Commit sugerido: `test(drilldown-ui): validar wow case meal voucher end-to-end`

---

### Card 7.10.3 — Validar utilidad real de los exportables

**Descripción:** asegurar que los archivos descargables no sean decorativos, sino útiles para un usuario real.

**Criterio de aceptación:**

- Los exportables son legibles y consistentes con UI
- Pueden usarse fuera del producto sin explicación oral adicional
- Refuerzan trazabilidad y utilidad del sistema

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Descargar summary export
- [x] Descargar exception detail export
- [x] Revisar columnas, naming y utilidad
- [x] Ajustar si el output no se sostiene por sí mismo
- [ ] Commit sugerido: `test(exports): validar utilidad de exportables del MVP`

---

## Resumen de commits esperados en EPIC 07

- `docs(drilldown): definir objetivo funcional del drilldown`
- `docs(drilldown): definir alcance del drilldown del MVP`
- `docs(drilldown-ui): diseñar estructura general de drilldown screen`
- `docs(drilldown-ui): definir resumen superior del drilldown`
- `docs(drilldown-ui): definir columnas de la tabla de drilldown`
- `feat(drilldown-ui): implementar ExceptionDrilldownTable`
- `feat(drilldown-ui): implementar resaltado visual de anomalias`
- `feat(drilldown-ui): implementar filtro por tipo de excepcion`
- `feat(drilldown-ui): implementar filtro por empleado`
- `feat(drilldown-ui): implementar filtro por legal entity`
- `feat(drilldown-ui): implementar ordenamientos utiles`
- `feat(drilldown-ui): conectar vista de detalle con backend`
- `test(drilldown-ui): validar consistencia entre capas de analisis`
- `feat(drilldown-ui): conectar concept analysis con drilldown`
- `feat(drilldown-ui): implementar navegacion de retorno desde detalle`
- `docs(exports): definir alcance de exportables del MVP`
- `docs(exports): diseñar export de reconciliation summary`
- `docs(exports): diseñar export de exception detail`
- `feat(exports): implementar export de summary desde backend`
- `feat(exports): implementar export de exception detail desde backend`
- `feat(exports-ui): implementar acciones de export en UI`
- `feat(traceability-ui): mostrar metadata visible de origen`
- `feat(traceability-ui): integrar metadata tecnica visible`
- `feat(drilldown-ui): implementar loading states del detalle`
- `feat(drilldown-ui): implementar error states del detalle`
- `feat(drilldown-ui): implementar empty states del detalle`
- `test(flow): validar recorrido summary-concept-drilldown`
- `test(drilldown-ui): validar wow case meal voucher end-to-end`
- `test(exports): validar utilidad de exportables del MVP`

---

## Notas técnicas

### Regla central de esta epic

El drill-down debe probar que el sistema puede responder:

> “Muéstrame exactamente qué registros explican esto.”

Si la vista no logra eso de manera clara, la explicación se debilita.

### Decisión UX del MVP

Esta epic prioriza:

- legibilidad de tabla
- filtros mínimos pero útiles
- continuidad del flujo
- exportables simples y valiosos

No prioriza:

- exploración compleja
- tablas gigantes con demasiadas opciones
- customización avanzada
- herramientas de trabajo colaborativo

### Qué no entra en esta epic

- comments
- workflow de aprobación
- anotaciones manuales sobre registros
- exports avanzados multi-sheet sofisticados
- filtros complejos tipo BI
- portfolio multi-run

Esta epic cierra la capa operativa del análisis del MVP: del insight a la evidencia concreta.
