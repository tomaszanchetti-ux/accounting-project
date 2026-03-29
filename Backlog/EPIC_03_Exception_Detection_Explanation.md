# EPIC 03 — Exception Detection & Explanation Layer

## Contexto y objetivo

Esta epic implementa la capa que convierte al MVP en algo más que un reconciler numérico. Hasta la epic anterior, el sistema puede responder si un concepto reconcilia o no, y en qué estado cae. Lo que todavía no puede hacer es responder la pregunta de negocio más valiosa:

> **¿Por qué no cierran los números y qué conviene revisar primero?**

Ese es exactamente el diferencial del producto.

La función de esta epic es tomar:

- resultados agregados por concepto
- base conciliable normalizada
- flags y condiciones de calidad

y transformarlos en:

- excepciones detectadas
- impacto estimado por anomalía
- causas probables priorizadas
- narrativa explicativa
- recomendaciones de revisión

La lógica no busca “inteligencia mágica” ni inferencias opacas. El diseño del MVP favorece una capa:

- rule-based
- auditable
- trazable
- comercialmente convincente

Al terminar esta epic, el sistema debe poder:

- detectar anomalías concretas del catálogo MVP
- vincularlas a registros y conceptos
- estimar su aporte a la diferencia cuando sea posible
- construir una explicación priorizada por concepto
- sugerir el siguiente paso razonable de revisión

## Dominio(s) involucrado(s)

**D3 — Exception Detection & Explanation Layer**

## Dependencias

- **EPIC 02** completada o suficientemente avanzada, con motor de conciliación operativo
- **EPIC 01** completada o suficientemente avanzada, con anomalías y casos wow diseñados

## Criterio de aceptación de la Epic completa

- [ ] El sistema detecta excepciones del catálogo MVP sobre la base conciliable
- [ ] Existe lógica explícita de prioridad entre tipos de excepción
- [ ] Cada concepto con diferencia puede asociarse a una o varias causas probables
- [ ] El sistema puede estimar impacto por causa al menos en los casos principales del demo
- [ ] Existe una narrativa explicativa template-based por concepto
- [ ] El sistema genera recomendaciones de revisión concretas y sobrias
- [ ] Los casos wow del dataset (`MEAL_VOUCHER`, `CHILDCARE`, `OVERTIME`) producen explicaciones coherentes con la intención narrativa
- [ ] La salida de explicación queda estructurada para API, persistencia y UI

## Estado: PENDIENTE

---

## Feature 3.1 — Catálogo operativo de excepciones del MVP

**Objetivo:** bajar a implementación el catálogo de anomalías definido conceptualmente y fijar exactamente cuáles entran en esta versión del producto.

---

### Card 3.1.1 — Definir catálogo definitivo de excepciones del MVP

**Descripción:** antes de escribir reglas, conviene cerrar formalmente el universo de excepciones que el sistema detectará en esta versión. Esto evita ambigüedad, scope creep y falsas expectativas sobre la capacidad explicativa del motor.

**Criterio de aceptación:**

- Existe un catálogo explícito y cerrado de excepciones del MVP
- Cada excepción tiene definición funcional clara
- Se distingue entre excepciones principales y opcionales

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Confirmar excepciones principales del MVP:
  - `Duplicate Record`
  - `Missing Record / Missing Population`
  - `Unmapped Concept`
  - `Out-of-Period Record`
  - `Outlier Amount`
  - `Missing Expected Total`
  - `Invalid Amount / Data Quality Issue`
- [ ] Confirmar excepciones opcionales del MVP:
  - `Sign Error`
  - `Misclassified Concept`
- [ ] Documentar definición funcional de cada excepción
- [ ] Documentar cuáles son centrales para el demo y cuáles quedan como capacidad secundaria
- [ ] Commit sugerido: `docs(exceptions): definir catalogo definitivo del MVP`

---

### Card 3.1.2 — Definir taxonomía y severidad de excepciones

**Descripción:** no todas las excepciones cumplen el mismo rol. Algunas invalidan, otras explican, otras solo enriquecen la revisión. Esta taxonomía ordena el comportamiento del sistema.

**Criterio de aceptación:**

- Cada excepción tiene categoría funcional
- Cada excepción tiene severidad base sugerida
- La taxonomía sirve para UI, explicación y priorización

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Clasificar excepciones en grupos:
  - calidad/invalidez
  - temporalidad
  - mapping
  - población
  - anomalía cuantitativa
- [ ] Definir severidad base por tipo
- [ ] Documentar relación entre tipo de excepción y tono de explicación
- [ ] Commit sugerido: `docs(exceptions): definir taxonomia y severidad base`

---

## Feature 3.2 — Reglas de detección base

**Objetivo:** implementar el núcleo de reglas que identifica anomalías sobre la base conciliable construida en la epic anterior.

---

### Card 3.2.1 — Implementar detección de `Invalid Amount / Data Quality Issue`

**Descripción:** esta excepción es la más estructural y debe detectarse primero. Reúne montos no interpretables, campos críticos faltantes y registros que comprometen la evaluación.

**Criterio de aceptación:**

- El sistema detecta registros estructuralmente inválidos
- Los registros inválidos quedan identificados a nivel línea
- El motor puede distinguir invalidación de corrida vs invalidación parcial

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir condiciones exactas de `Invalid Amount / Data Quality Issue`
- [ ] Implementar flags a nivel registro
- [ ] Asociar observaciones estructuradas por causa
- [ ] Diferenciar error bloqueante de calidad no bloqueante
- [ ] Commit sugerido: `feat(exceptions): detectar invalid amount y data quality issues`

---

### Card 3.2.2 — Implementar detección de `Out-of-Period Record`

**Descripción:** identifica líneas cuyo período o fecha no corresponde al período de conciliación objetivo. Es una de las anomalías más demostrables del demo.

**Criterio de aceptación:**

- El sistema detecta registros fuera de período
- La detección funciona con `payroll_period` y/o `posting_date`
- Se puede cuantificar cuántos registros y cuánto monto quedan afectados

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Comparar período del registro vs período objetivo
- [ ] Considerar `posting_date` inconsistente como refuerzo de la anomalía
- [ ] Marcar líneas fuera de período
- [ ] Calcular impacto agregado preliminar por concepto
- [ ] Commit sugerido: `feat(exceptions): detectar out-of-period records`

---

### Card 3.2.3 — Implementar detección de `Unmapped Concept`

**Descripción:** identifica líneas que no pudieron traducirse a un concepto normalizado y que, por lo tanto, comprometen la comparabilidad del observed total.

**Criterio de aceptación:**

- El sistema identifica registros sin mapping válido
- La excepción queda disponible a nivel línea y a nivel concepto
- El impacto de las líneas no mapeadas puede resumirse por concepto

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Detectar registros sin `concept_code_normalized`
- [ ] Agrupar no mapeados por concepto raw o patrón útil
- [ ] Calcular conteo e impacto por concepto conciliable afectado
- [ ] Preparar observaciones útiles para explicación posterior
- [ ] Commit sugerido: `feat(exceptions): detectar unmapped concept lines`

---

### Card 3.2.4 — Implementar detección de `Duplicate Record`

**Descripción:** identifica líneas potencialmente duplicadas según una combinación de atributos clave. Es importante remarcar que el sistema detecta duplicados probables, no “verdad absoluta”.

**Criterio de aceptación:**

- Existe una regla explícita de duplicado potencial
- Los duplicados se identifican a nivel línea y agrupación
- El impacto duplicado puede estimarse de forma consistente

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir combinación clave de duplicado potencial:
  - `employee_id`
  - `payroll_period`
  - `concept_code_normalized`
  - `amount`
  - `legal_entity` si aplica
- [ ] Implementar detección de repetición exacta o altamente similar
- [ ] Marcar grupos de duplicados y registros afectados
- [ ] Estimar monto duplicado explicable
- [ ] Commit sugerido: `feat(exceptions): detectar duplicate records`

---

### Card 3.2.5 — Implementar detección de `Missing Expected Total`

**Descripción:** identifica unidades conciliables observadas que no tienen referencia esperada correspondiente. Aunque esta condición afecta el estado, también debe existir como excepción explícita.

**Criterio de aceptación:**

- El sistema marca conceptos observados sin expected total
- La excepción queda disponible en el output explicativo
- Se alinea con estado `Invalid / Incomplete`

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Detectar unidades con observed pero sin expected
- [ ] Generar excepción a nivel concepto
- [ ] Vincularla con el estado de conciliación correspondiente
- [ ] Commit sugerido: `feat(exceptions): detectar missing expected total`

---

## Feature 3.3 — Reglas analíticas de excepción

**Objetivo:** detectar anomalías que requieren una capa un poco más interpretativa, pero todavía plenamente rule-based.

---

### Card 3.3.1 — Implementar detección de `Outlier Amount`

**Descripción:** identifica montos individuales atípicos respecto a la distribución del concepto. Es una de las anomalías más útiles para `OVERTIME`.

**Criterio de aceptación:**

- El sistema detecta outliers por concepto
- La regla es simple, consistente y explicable
- La detección produce impacto cuantificable y registros identificables

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Elegir método base del MVP:
  - mediana por concepto
  - umbral `3x` o `5x` mediana
- [ ] Implementar detección por registro
- [ ] Calcular impacto agregado por concepto
- [ ] Preparar observación específica del registro anómalo
- [ ] Commit sugerido: `feat(exceptions): detectar outlier amounts`

---

### Card 3.3.2 — Implementar detección de `Missing Record / Missing Population`

**Descripción:** esta excepción requiere comparar población observada con una referencia de elegibilidad o baseline esperado. Es clave para `CHILDCARE`.

**Criterio de aceptación:**

- El sistema puede detectar población faltante cuando existe referencia
- La lógica está acotada a casos controlados del MVP
- El output identifica empleados faltantes o cohortes ausentes

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir fuente de verdad para elegibilidad:
  - `employee_reference.csv`
  - baseline controlado del demo
- [ ] Comparar población esperada vs población observada por concepto elegible
- [ ] Identificar empleados ausentes
- [ ] Estimar impacto agregado de la población faltante
- [ ] Commit sugerido: `feat(exceptions): detectar missing population`

---

### Card 3.3.3 — Implementar detección opcional de `Sign Error`

**Descripción:** identifica registros cuyo signo contradice la polaridad esperada del concepto. Es una capacidad útil, aunque secundaria en el MVP.

**Criterio de aceptación:**

- Existe una regla explícita de detección de signo inesperado
- La excepción puede activarse en casos diseñados del demo
- No interfiere indebidamente con la agregación principal

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Leer signo esperado desde `concept_master`
- [ ] Comparar signo observado vs esperado
- [ ] Marcar registros sospechosos
- [ ] Estimar impacto cuando corresponda
- [ ] Commit sugerido: `feat(exceptions): detectar sign errors opcionales`

---

### Card 3.3.4 — Implementar detección opcional de `Misclassified Concept`

**Descripción:** identifica líneas que, por patrón o nombre, parecen pertenecer a otro concepto o categoría. En MVP debe usarse solo de forma controlada.

**Criterio de aceptación:**

- Existe una regla simple y acotada para misclassification
- La detección se limita a casos explícitos del demo
- No introduce complejidad excesiva ni falsos positivos generalizados

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar heurística mínima de misclassification
- [ ] Aplicarla solo en casos configurados del demo
- [ ] Documentar límites y no generalizar la capacidad
- [ ] Commit sugerido: `feat(exceptions): detectar misclassified concepts opcionales`

---

## Feature 3.4 — Priorización y gobernanza de excepciones

**Objetivo:** ordenar el universo de anomalías detectadas para evitar explicaciones caóticas o contradictorias.

---

### Card 3.4.1 — Definir prioridad entre excepciones

**Descripción:** cuando un mismo registro o concepto presenta múltiples anomalías, el sistema necesita una lógica estable de prioridad para decidir qué mostrar primero.

**Criterio de aceptación:**

- Existe una política explícita de prioridad entre excepciones
- La política está documentada y es consistente con la narrativa del producto
- La prioridad puede aplicarse a nivel registro y a nivel concepto

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir orden sugerido de prioridad:
  1. `Invalid Amount / Data Quality Issue`
  2. `Out-of-Period Record`
  3. `Unmapped Concept`
  4. `Duplicate Record`
  5. `Missing Expected Total`
  6. `Missing Population`
  7. `Sign Error`
  8. `Outlier Amount`
  9. `Misclassified Concept`
- [ ] Documentar criterio de negocio detrás del orden
- [ ] Preparar uso de la prioridad en ranking explicativo
- [ ] Commit sugerido: `docs(exceptions): definir prioridad entre excepciones`

---

### Card 3.4.2 — Diseñar modelo estructurado de excepción

**Descripción:** las excepciones no deben vivir como texto libre. Esta card define un objeto/estructura reutilizable para persistencia, API y UI.

**Criterio de aceptación:**

- Existe un contrato estructurado de excepción
- El contrato sirve para línea, concepto y corrida
- Incluye tipo, severidad, impacto y observación

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir campos mínimos del objeto excepción:
  - `exception_type`
  - `severity`
  - `scope_level`
  - `record_id` o `concept_scope`
  - `employee_id` opcional
  - `estimated_impact_amount`
  - `observation`
- [ ] Definir cómo agrupar excepciones por concepto
- [ ] Reservar campo para `confidence` si hiciera falta
- [ ] Commit sugerido: `feat(exceptions): definir contrato estructurado de excepcion`

---

## Feature 3.5 — Estimación de impacto por causa

**Objetivo:** cuantificar, cuando sea posible, cuánto explica cada anomalía de la diferencia observada.

---

### Card 3.5.1 — Definir método de estimación por tipo de excepción

**Descripción:** cada tipo de excepción necesita una lógica específica de cuantificación. No todas permiten la misma precisión, pero el sistema debe mantener consistencia interna.

**Criterio de aceptación:**

- Existe método de estimación por tipo principal de excepción
- La estimación es suficientemente consistente para demo
- Se documenta el nivel de precisión esperado

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir método para:
  - `Out-of-Period`
  - `Unmapped`
  - `Duplicate`
  - `Missing Population`
  - `Outlier`
- [ ] Distinguir entre impacto exacto y estimado
- [ ] Documentar límites de cada metodología
- [ ] Commit sugerido: `docs(exceptions): definir metodo de estimacion de impacto`

---

### Card 3.5.2 — Implementar cálculo de impacto agregado por concepto

**Descripción:** esta card traduce las excepciones detectadas en montos atribuibles por concepto para alimentar el ranking explicativo.

**Criterio de aceptación:**

- El sistema puede calcular impacto agregado por causa y concepto
- El resultado es utilizable en explicación y UI
- Los casos wow producen números plausibles y consistentes

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Implementar funciones de impacto por tipo principal
- [ ] Consolidar impacto por `concept_code_normalized`
- [ ] Preparar estructura ordenable por impacto
- [ ] Validar resultados en `MEAL_VOUCHER`, `CHILDCARE` y `OVERTIME`
- [ ] Commit sugerido: `feat(exceptions): calcular impacto agregado por causa`

---

## Feature 3.6 — Ranking de causas probables

**Objetivo:** pasar de “hay excepciones detectadas” a “estas son las causas más relevantes para explicar la diferencia”.

---

### Card 3.6.1 — Definir lógica de ranking de causas

**Descripción:** el sistema debe ordenar causas combinando impacto estimado, severidad y confianza funcional de la detección.

**Criterio de aceptación:**

- Existe una lógica explícita de ranking
- La lógica es simple de explicar y de depurar
- El ranking evita resultados arbitrarios

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir fórmula o criterio de ranking combinando:
  - impacto estimado
  - severidad funcional
  - prioridad del tipo de excepción
  - confianza implícita
- [ ] Limitar cantidad de causas top mostradas
- [ ] Documentar desempates y bordes
- [ ] Commit sugerido: `docs(explanations): definir ranking de causas probables`

---

### Card 3.6.2 — Implementar agrupación multi-causa por concepto

**Descripción:** un concepto puede tener más de una causa relevante. Esta card implementa la capacidad de combinar varias anomalías sin reducir la explicación a una sola hipótesis simplista.

**Criterio de aceptación:**

- Un concepto puede devolver múltiples causas relevantes
- La agrupación evita duplicaciones o causas redundantes
- El resultado es usable por la narrativa template-based

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Agrupar excepciones por concepto
- [ ] Consolidar causas homogéneas
- [ ] Seleccionar top causas por ranking
- [ ] Preparar payload resumido por causa
- [ ] Commit sugerido: `feat(explanations): agrupar causas multiples por concepto`

---

## Feature 3.7 — Narrativa explicativa template-based

**Objetivo:** transformar causas detectadas en una explicación legible, profesional y útil para el usuario contable.

---

### Card 3.7.1 — Diseñar estructura narrativa de la explicación

**Descripción:** la explicación del MVP debe tener una forma estable y reconocible. No debe ser texto improvisado ni log técnico.

**Criterio de aceptación:**

- Existe una estructura estándar de explicación
- La estructura separa statement principal, causas y recomendación
- El formato es apto para UI y exportables

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir estructura en tres capas:
  - statement principal
  - top causes
  - recomendación
- [ ] Definir longitud y tono esperado
- [ ] Documentar que la explicación es útil, no “literaria”
- [ ] Commit sugerido: `docs(explanations): definir estructura narrativa base`

---

### Card 3.7.2 — Implementar statement principal por concepto

**Descripción:** construir la frase inicial que resume la situación del concepto de forma clara e inmediata.

**Criterio de aceptación:**

- Cada concepto con diferencia genera un statement principal
- El statement incluye monto y dirección de la diferencia
- El tono es claro, profesional y sobrio

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Crear template para `Unreconciled`
- [ ] Crear template para `Minor Difference`
- [ ] Crear template para `Invalid / Incomplete`
- [ ] Incluir concepto, período y diff relevante
- [ ] Commit sugerido: `feat(explanations): generar statement principal por concepto`

---

### Card 3.7.3 — Implementar bloque de causas probables

**Descripción:** generar una lista priorizada y legible de causas detectadas, con conteos e impacto cuando corresponda.

**Criterio de aceptación:**

- El bloque lista causas relevantes de forma clara
- Cada causa puede incluir evidencia resumida e impacto
- La salida es consistente con el ranking previo

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Construir templates por tipo de causa
- [ ] Incorporar conteo de registros o empleados cuando aplique
- [ ] Incorporar impacto estimado cuando exista
- [ ] Limitar salida a un número razonable de causas
- [ ] Commit sugerido: `feat(explanations): generar bloque de causas probables`

---

### Card 3.7.4 — Implementar framing de certeza y lenguaje prudente

**Descripción:** la explicación debe ser útil sin sonar omnisciente. El sistema necesita un framing que preserve credibilidad cuando la lógica es inferencial.

**Criterio de aceptación:**

- La narrativa usa lenguaje prudente cuando corresponde
- Se diferencia entre detección fuerte y causa probable
- El texto no promete más certeza de la que el motor puede sostener

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir expresiones estándar:
  - “se detectaron indicios de…”
  - “la diferencia se explica principalmente por…”
  - “posibles causas identificadas…”
- [ ] Aplicar framing según tipo de excepción
- [ ] Evitar lenguaje absoluto en inferencias débiles
- [ ] Commit sugerido: `feat(explanations): aplicar framing prudente de certeza`

---

## Feature 3.8 — Recomendaciones de revisión

**Objetivo:** cerrar la explicación con una siguiente acción clara para el usuario.

---

### Card 3.8.1 — Definir catálogo de recomendaciones por excepción

**Descripción:** cada excepción principal debe poder mapearse a una recomendación breve, profesional y accionable.

**Criterio de aceptación:**

- Existe un catálogo de recomendaciones por tipo de excepción
- Las recomendaciones son concretas y no alarmistas
- El catálogo es reusable por varios conceptos

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir recomendaciones para:
  - `Unmapped Concept`
  - `Out-of-Period`
  - `Duplicate`
  - `Outlier`
  - `Missing Expected Total`
  - `Missing Population`
- [ ] Mantener tono profesional y orientado a revisión
- [ ] Commit sugerido: `docs(explanations): definir catalogo de recomendaciones`

---

### Card 3.8.2 — Implementar recomendación final por concepto

**Descripción:** tomar las causas más relevantes y traducirlas a una recomendación final corta para el usuario.

**Criterio de aceptación:**

- Cada concepto explicable puede producir una recomendación final
- La recomendación está alineada con la causa principal o combinación dominante
- El output es apto para summary y concept analysis

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir lógica de selección de recomendación principal
- [ ] Manejar casos multi-causa
- [ ] Generar texto final breve por concepto
- [ ] Commit sugerido: `feat(explanations): generar recomendacion final por concepto`

---

## Feature 3.9 — Empaquetado estructurado de la explicación

**Objetivo:** producir una salida estable que pueda ser persistida, servida por API y mostrada en UI.

---

### Card 3.9.1 — Definir contrato estructurado de explicación por concepto

**Descripción:** la explicación no debe quedar solo como texto. Debe existir un contrato compuesto con texto, causas, métricas e indicadores útiles.

**Criterio de aceptación:**

- Existe schema/DTO de explicación por concepto
- Incluye statement, causas, recomendaciones y metadata
- Puede persistirse y serializarse fácilmente

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir campos mínimos:
  - `summary_statement`
  - `probable_causes`
  - `recommended_action`
  - `explained_amount_estimate`
  - `impacted_records_count`
  - `impacted_employees_count`
- [ ] Definir formato de `probable_causes`
- [ ] Preparar compatibilidad con API/UI
- [ ] Commit sugerido: `feat(explanations): definir contrato estructurado de explicacion`

---

### Card 3.9.2 — Crear orquestador de detección + explicación

**Descripción:** esta card unifica la detección de excepciones, el cálculo de impacto y la generación narrativa en un flujo estable por concepto o corrida.

**Criterio de aceptación:**

- Existe una función principal para la capa explicativa
- La función procesa resultados del motor y base conciliable
- El pipeline es reutilizable desde API y pruebas

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar secuencia:
  - detectar excepciones
  - agrupar por concepto
  - estimar impacto
  - rankear causas
  - generar narrativa
  - devolver payload estructurado
- [ ] Integrar inputs provenientes de EPIC 02
- [ ] Manejar salidas vacías o conceptos sin explicación relevante
- [ ] Commit sugerido: `feat(explanations): crear orquestador de excepciones y narrativa`

---

## Feature 3.10 — Validación funcional de los casos wow

**Objetivo:** asegurar que la capa explicativa reproduce la intención comercial y narrativa definida en los documentos madre.

---

### Card 3.10.1 — Validar caso wow principal `MEAL_VOUCHER`

**Descripción:** este concepto debe convertirse en la prueba más fuerte de valor del producto. La explicación debe combinar múltiples causas y mostrarlas con claridad.

**Criterio de aceptación:**

- `MEAL_VOUCHER` produce una explicación multi-causa coherente
- Aparecen `out-of-period`, `unmapped` y `duplicates` según diseño
- La narrativa es comercialmente fuerte y técnicamente creíble

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Ejecutar capa explicativa sobre `MEAL_VOUCHER`
- [ ] Validar orden e impacto de causas
- [ ] Ajustar templates o ranking si la narrativa no queda sólida
- [ ] Commit sugerido: `test(explanations): validar caso wow meal voucher`

---

### Card 3.10.2 — Validar caso `CHILDCARE`

**Descripción:** este concepto debe demostrar que el sistema puede detectar una lógica de población faltante y no solo errores de archivo.

**Criterio de aceptación:**

- `CHILDCARE` refleja faltantes de población elegible
- La explicación se siente operativa y cercana al caso real
- La recomendación final es coherente con ese patrón

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Ejecutar capa explicativa sobre `CHILDCARE`
- [ ] Verificar empleados faltantes y monto asociado
- [ ] Validar recomendación final
- [ ] Commit sugerido: `test(explanations): validar caso childcare`

---

### Card 3.10.3 — Validar caso `OVERTIME`

**Descripción:** este concepto debe demostrar capacidad analítica mediante detección de outliers y explicación focalizada.

**Criterio de aceptación:**

- `OVERTIME` identifica uno o pocos registros atípicos relevantes
- La explicación prioriza el outlier principal
- La narrativa es clara y demostrable en drill-down

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Ejecutar capa explicativa sobre `OVERTIME`
- [ ] Verificar identificación del outlier dominante
- [ ] Validar statement y recomendación asociados
- [ ] Commit sugerido: `test(explanations): validar caso overtime`

---

### Card 3.10.4 — Validar caso amarillo `TRANSPORT`

**Descripción:** este caso confirma que la capa explicativa también sabe comportarse con diferencias menores y no sobreactúa todo como incidente crítico.

**Criterio de aceptación:**

- `TRANSPORT` produce una explicación sobria de diferencia menor
- El tono es proporcional a la severidad
- No se sobredimensiona una anomalía marginal

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Ejecutar capa explicativa sobre `TRANSPORT`
- [ ] Verificar tono y brevedad
- [ ] Validar que la recomendación no escale innecesariamente
- [ ] Commit sugerido: `test(explanations): validar caso transport minor difference`

---

## Resumen de commits esperados en EPIC 03

- `docs(exceptions): definir catalogo definitivo del MVP`
- `docs(exceptions): definir taxonomia y severidad base`
- `feat(exceptions): detectar invalid amount y data quality issues`
- `feat(exceptions): detectar out-of-period records`
- `feat(exceptions): detectar unmapped concept lines`
- `feat(exceptions): detectar duplicate records`
- `feat(exceptions): detectar missing expected total`
- `feat(exceptions): detectar outlier amounts`
- `feat(exceptions): detectar missing population`
- `feat(exceptions): detectar sign errors opcionales`
- `feat(exceptions): detectar misclassified concepts opcionales`
- `docs(exceptions): definir prioridad entre excepciones`
- `feat(exceptions): definir contrato estructurado de excepcion`
- `docs(exceptions): definir metodo de estimacion de impacto`
- `feat(exceptions): calcular impacto agregado por causa`
- `docs(explanations): definir ranking de causas probables`
- `feat(explanations): agrupar causas multiples por concepto`
- `docs(explanations): definir estructura narrativa base`
- `feat(explanations): generar statement principal por concepto`
- `feat(explanations): generar bloque de causas probables`
- `feat(explanations): aplicar framing prudente de certeza`
- `docs(explanations): definir catalogo de recomendaciones`
- `feat(explanations): generar recomendacion final por concepto`
- `feat(explanations): definir contrato estructurado de explicacion`
- `feat(explanations): crear orquestador de excepciones y narrativa`
- `test(explanations): validar caso wow meal voucher`
- `test(explanations): validar caso childcare`
- `test(explanations): validar caso overtime`
- `test(explanations): validar caso transport minor difference`

---

## Notas técnicas

### Tesis central de esta epic

El valor del MVP no está solo en detectar una diferencia, sino en reducir drásticamente el trabajo manual necesario para entenderla.

La explicación del sistema debe sentirse:

- útil
- profesional
- controlada
- inmediata

No debe sentirse:

- arbitraria
- “demasiado AI”
- opaca
- grandilocuente

### Regla de implementación

Si una regla mejora la capacidad de explicar un caso wow pero vuelve el sistema mucho más difícil de entender o mantener, no entra al MVP.

### Qué no entra en esta epic

- LLMs para generar explicación libre
- aprendizaje automático para clasificar anomalías
- configuración libre de reglas por usuario
- explicaciones largas tipo reporte narrativo completo
- scoring de riesgo enterprise

La meta acá es una capa explicativa **rule-based + template-based** que ya sea suficientemente fuerte para vender el producto.
