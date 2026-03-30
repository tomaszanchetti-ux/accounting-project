# EPIC 02 — Reconciliation Engine Core

## Contexto y objetivo

Esta epic implementa el núcleo lógico del producto: transformar un archivo operativo de payroll en un juicio de conciliación consistente, auditable y entendible. Hasta este punto, el proyecto ya tiene una base técnica y un universo de datos definidos. Lo que todavía no existe es el mecanismo que toma ese input, lo vuelve comparable y responde la pregunta central del producto:

> **¿El total observado de este concepto en este período coincide con el total esperado, y en qué estado cae esa conciliación?**

El objetivo de esta epic no es todavía explicar en profundidad por qué hay diferencias. Eso viene en la siguiente capa. Aquí el foco es construir una base sólida y predecible para:

- validar archivos de entrada
- normalizar datos crudos
- preparar una base conciliable
- agregar importes
- comparar observed vs expected
- asignar estados de conciliación

Esta epic es el punto donde el producto deja de ser un diseño y empieza a comportarse como un sistema.

Al terminar esta epic, el motor debe poder:

- leer un payroll file y expected totals
- validar si el input es utilizable
- normalizar conceptos, períodos e importes
- construir una base reconciliable
- calcular `observed totals`
- comparar contra `expected totals`
- producir resultados agregados por concepto y período
- asignar `Reconciled`, `Minor Difference`, `Unreconciled` o `Invalid / Incomplete`

## Dominio(s) involucrado(s)

**D2 — Reconciliation Engine Core**

## Dependencias

- **EPIC 00** completada o suficientemente avanzada
- **EPIC 01** completada o suficientemente avanzada, con universo de datos y esquemas cerrados

## Criterio de aceptación de la Epic completa

- [ ] El motor puede leer `payroll.csv` y `expected_totals.csv`
- [ ] Existen validaciones explícitas de esquema y calidad mínima
- [ ] El sistema normaliza columnas, conceptos, períodos e importes de forma consistente
- [ ] Existe una base conciliable intermedia claramente definida
- [ ] El motor calcula `observed totals` por unidad de conciliación
- [ ] El motor compara `observed` vs `expected` y calcula diferencias absolutas y relativas
- [ ] El motor asigna estados de conciliación según reglas de tolerancia cerradas
- [ ] El resultado agregado por concepto es reproducible y consistente con la tabla maestra del dataset
- [ ] El motor expone outputs estructurados reutilizables por API, persistencia y UI

## Estado: EN PROGRESO

---

## Feature 2.1 — Contrato funcional del motor de conciliación

**Objetivo:** fijar explícitamente qué hace el motor, cuál es su input, cuál es su output y cuál es la unidad de análisis que gobierna toda la epic.

---

### Card 2.1.1 — Definir la unidad de conciliación del MVP

**Descripción:** esta card baja a implementación la decisión conceptual ya tomada en los documentos madre: la conciliación primaria del MVP no ocurre por empleado, sino por concepto y período. El detalle por empleado existe, pero como drill-down operativo, no como unidad de conciliación base.

**Criterio de aceptación:**

- La unidad de conciliación queda explícitamente documentada
- Se distingue el nivel de conciliación primaria del nivel de drill-down
- La definición sirve como criterio rector para agregación, comparación y outputs

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Documentar que la unidad principal es `periodo + concepto`
- [x] Documentar que `legal_entity` puede ser dimensión secundaria opcional
- [x] Documentar que `employee_id` y `record_id` quedan fuera de la conciliación primaria
- [x] Dejar explícito que el empleado vive en la capa analítica/drill-down
- [ ] Commit sugerido: `docs(engine): definir unidad de conciliación del MVP`

---

### Card 2.1.2 — Definir el contrato de input del motor

**Descripción:** el motor necesita un contrato claro de entrada para poder ser llamado desde API, tests, scripts o UI sin reabrir interpretaciones.

**Criterio de aceptación:**

- Existe definición explícita de inputs requeridos
- Se distingue entre inputs obligatorios y opcionales
- El contrato sirve para implementación y validación

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir inputs obligatorios:
  - `payroll dataframe` o archivo fuente
  - `expected totals`
  - `periodo objetivo`
- [x] Definir inputs opcionales:
  - `concept master`
  - `employee reference`
  - `legal entity filter`
  - `tolerance profile`
- [x] Documentar formato esperado de entrada para uso programático
- [ ] Commit sugerido: `docs(engine): definir contrato de input del motor`

---

### Card 2.1.3 — Definir el contrato de output del motor

**Descripción:** esta card fija qué devuelve el motor al terminar una corrida lógica, antes de entrar en persistencia o visualización.

**Criterio de aceptación:**

- Existe output agregado por concepto claramente definido
- Existen métricas mínimas para trazabilidad interna
- El output es lo bastante estructurado para alimentar API, DB y UI

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir output agregado con campos mínimos:
  - `period`
  - `concept_code_normalized`
  - `concept_name_normalized`
  - `observed_amount`
  - `expected_amount`
  - `absolute_diff`
  - `relative_diff_pct`
  - `status`
- [x] Definir métricas auxiliares:
  - `record_count`
  - `employee_count`
  - `invalid_record_count`
- [x] Definir output técnico intermedio para debugging
- [ ] Commit sugerido: `docs(engine): definir contrato de output del motor`

---

## Feature 2.2 — Validación inicial del input

**Objetivo:** garantizar que el motor solo procese archivos utilizables y responda de forma controlada cuando el input no cumple el mínimo requerido.

---

### Card 2.2.1 — Implementar validación de esquema del payroll

**Descripción:** antes de hacer cualquier cálculo, el motor debe poder determinar si el archivo principal tiene las columnas mínimas necesarias para operar.

**Criterio de aceptación:**

- El motor detecta columnas obligatorias faltantes
- El resultado de validación es estructurado y legible
- Se distingue entre error bloqueante y observación no bloqueante

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Implementar lista de columnas obligatorias del payroll
- [x] Validar presencia de todas las columnas críticas
- [x] Devolver estructura de errores/advertencias
- [x] Definir respuesta bloqueante si falta una columna esencial
- [ ] Commit sugerido: `feat(engine): validar esquema base del payroll`

---

### Card 2.2.2 — Implementar validación de tipos y consistencia mínima

**Descripción:** más allá del esquema, el motor debe detectar si los datos se pueden interpretar razonablemente.

**Criterio de aceptación:**

- El motor valida campos críticos interpretables
- Se detectan montos inválidos, período faltante y registros no utilizables
- La validación alimenta el pipeline posterior sin duplicar lógica

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Validar `amount` interpretable como numérico
- [x] Validar `payroll_period` presente o derivable
- [x] Validar `concept_code` o `concept_name` presente
- [x] Validar `employee_id` presente en registros trazables
- [x] Generar flags de invalidez por registro si aplica
- [ ] Commit sugerido: `feat(engine): validar tipos y consistencia mínima del input`

---

### Card 2.2.3 — Implementar validación de `expected_totals`

**Descripción:** la conciliación requiere que la referencia esperada exista y sea coherente con la unidad conciliable.

**Criterio de aceptación:**

- El motor valida estructura de `expected_totals`
- Puede detectar faltantes de referencia por concepto/período
- Queda diferenciada la invalidación de input del missing expected por unidad conciliable

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Validar columnas mínimas de `expected_totals`
- [ ] Validar que el período objetivo exista en expected totals
- [ ] Detectar conceptos sin expected total correspondiente
- [ ] Definir cuándo esto invalida la corrida y cuándo invalida solo una unidad conciliable
- [ ] Commit sugerido: `feat(engine): validar expected totals del MVP`

---

## Feature 2.3 — Normalización del dataset

**Objetivo:** convertir inputs heterogéneos o imperfectos en una base consistente y comparable.

---

### Card 2.3.1 — Normalizar nombres de columnas y tipos base

**Descripción:** el motor debe trabajar con un contrato interno homogéneo, independientemente de pequeñas variaciones del archivo observado.

**Criterio de aceptación:**

- Las columnas internas quedan estandarizadas
- Los tipos críticos quedan convertidos a una representación consistente
- La normalización es trazable y determinística

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Estandarizar nombres de columnas a la convención interna
- [ ] Convertir `amount` a decimal/float controlado
- [ ] Convertir `posting_date` a fecha interpretable
- [ ] Normalizar strings relevantes (`trim`, casing, espacios)
- [ ] Commit sugerido: `feat(engine): normalizar columnas y tipos base`

---

### Card 2.3.2 — Normalizar período y lógica temporal

**Descripción:** la capa temporal debe quedar unificada para que el motor sepa con precisión qué registros pertenecen al período conciliado y cuáles no.

**Criterio de aceptación:**

- El período de cada línea queda normalizado
- El motor puede comparar período del registro vs período objetivo
- Quedan listos los flags base para `out-of-period`

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Normalizar `payroll_period` al formato interno `YYYY-MM`
- [ ] Derivar o validar período desde `posting_date` si hace falta
- [ ] Crear flag preliminar de alineación temporal
- [ ] Separar registros del período objetivo de registros externos
- [ ] Commit sugerido: `feat(engine): normalizar periodo y lógica temporal`

---

### Card 2.3.3 — Normalizar conceptos usando `concept_master`

**Descripción:** la conciliación solo es posible si los conceptos del payroll observado se traducen a una taxonomía normalizada.

**Criterio de aceptación:**

- Existe mapping de `concept_code` / `concept_name` a concepto normalizado
- Los no mapeados quedan identificados explícitamente
- El dataset resultante puede agregarse sobre conceptos consistentes

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Implementar lookup contra `concept_master`
- [ ] Resolver `concept_code_normalized` y `concept_name_normalized`
- [ ] Marcar registros no mapeados
- [ ] Documentar estrategia de fallback si falla el mapping
- [ ] Commit sugerido: `feat(engine): normalizar conceptos con concept master`

---

### Card 2.3.4 — Normalizar signos y montos interpretables

**Descripción:** aunque la explicación detallada venga después, el motor debe preparar montos consistentes y detectar inconsistencias evidentes de polaridad.

**Criterio de aceptación:**

- Los montos quedan listos para agregación
- Se documenta la convención de signo aplicada
- Existen flags preliminares para posibles errores de signo

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Confirmar convención de signo observada del dataset
- [ ] Alinear importes al contrato interno del motor
- [ ] Crear flag preliminar de signo inesperado según `concept_master`
- [ ] Evitar que la detección preliminar distorsione el cálculo observado
- [ ] Commit sugerido: `feat(engine): normalizar signos y montos`

---

## Feature 2.4 — Construcción de la base conciliable

**Objetivo:** preparar una capa intermedia clara y reutilizable sobre la cual el motor pueda agregar, comparar y posteriormente explicar.

---

### Card 2.4.1 — Definir y construir `reconcilable payroll base`

**Descripción:** esta es la tabla intermedia central del motor. No es todavía el resultado final, pero sí la representación operativa sobre la cual todo el resto se apoya.

**Criterio de aceptación:**

- Existe una tabla/base intermedia explícita
- La base contiene solo o principalmente registros elegibles para conciliación
- Los registros inválidos y flags de calidad quedan trazados

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar estructura interna de la base conciliable
- [ ] Incluir campos normalizados, flags de validez y metadata útil
- [ ] Separar registros válidos, inválidos y observables con excepciones
- [ ] Definir si la base contiene todos los registros o solo los elegibles
- [ ] Commit sugerido: `feat(engine): construir base conciliable intermedia`

---

### Card 2.4.2 — Definir reglas de inclusión/exclusión para observed totals

**Descripción:** no toda línea del payroll debe entrar necesariamente al total observado. Esta card fija esas reglas.

**Criterio de aceptación:**

- Existen reglas explícitas de inclusión/exclusión
- El observed total es consistente con esas reglas
- Las decisiones son auditables y no implícitas

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir si registros `out-of-period` quedan fuera del cálculo observado
- [ ] Definir tratamiento de registros `unmapped`
- [ ] Definir tratamiento de montos inválidos o conceptos indeterminados
- [ ] Documentar implicancias de negocio de cada exclusión
- [ ] Commit sugerido: `docs(engine): definir reglas de inclusion del observed total`

---

### Card 2.4.3 — Preparar base para drill-down futuro

**Descripción:** aunque la UI de detalle venga más adelante, desde esta epic conviene dejar la base lista para que cada resultado agregado pueda rastrearse hacia líneas y empleados.

**Criterio de aceptación:**

- La base intermedia conserva referencias a línea y empleado
- Los resultados agregados podrán enlazarse luego con detalle
- No se pierde trazabilidad al agregar

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Conservar `record_id`, `employee_id` y `employee_name` en la base intermedia
- [ ] Mantener `legal_entity`, `cost_center` y período por registro
- [ ] Diseñar claves o joins que faciliten drill-down futuro
- [ ] Commit sugerido: `chore(engine): preparar base conciliable para drilldown`

---

## Feature 2.5 — Agregación y cálculo de observed totals

**Objetivo:** consolidar la base conciliable en totales observados según la unidad de conciliación definida.

---

### Card 2.5.1 — Implementar agregación principal por concepto y período

**Descripción:** el observed total del MVP surge de sumar importes válidos por concepto y período.

**Criterio de aceptación:**

- El motor produce un total observado por unidad conciliable
- La agregación respeta reglas de inclusión definidas
- Se puede contrastar con la tabla maestra del dataset

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Agrupar por `payroll_period + concept_code_normalized`
- [ ] Sumar `amount` de registros elegibles
- [ ] Calcular `record_count` por grupo
- [ ] Calcular `employee_count` por grupo
- [ ] Commit sugerido: `feat(engine): implementar observed totals por concepto y periodo`

---

### Card 2.5.2 — Implementar dimensión secundaria opcional por `legal_entity`

**Descripción:** esta card deja preparado el motor para segmentar resultados si la narrativa o la UI del demo lo requieren, sin hacer esa dimensión obligatoria desde el día uno.

**Criterio de aceptación:**

- La agregación soporta `legal_entity` como dimensión opcional
- La lógica principal no se rompe si no se usa
- El comportamiento está documentado y testeado

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar agregación extensible con `legal_entity`
- [ ] Permitir modo simple y modo segmentado
- [ ] Documentar cuándo usar cada modo
- [ ] Commit sugerido: `feat(engine): soportar agregacion opcional por legal entity`

---

## Feature 2.6 — Comparación contra expected totals

**Objetivo:** convertir observed totals en un juicio comparativo contra la referencia esperada.

---

### Card 2.6.1 — Enlazar observed totals con expected totals

**Descripción:** una vez agregados los observados, el motor debe poder cruzarlos correctamente con la referencia esperada.

**Criterio de aceptación:**

- Cada unidad conciliable se cruza con su expected correspondiente
- Se detectan unidades sin referencia esperada
- La comparación es consistente con el grano elegido

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Implementar join entre observed y expected
- [ ] Resolver casos faltantes de expected
- [ ] Definir placeholders o estado intermedio si falta expected
- [ ] Commit sugerido: `feat(engine): enlazar observed totals con expected totals`

---

### Card 2.6.2 — Calcular diferencias absolutas y relativas

**Descripción:** esta card implementa las métricas base que gobiernan todo el estado de conciliación.

**Criterio de aceptación:**

- Se calcula `absolute_diff`
- Se calcula `relative_diff_pct`
- Existen resguardos para expected igual a cero o faltante

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Calcular `absolute_diff = observed - expected`
- [ ] Calcular `relative_diff_pct`
- [ ] Definir comportamiento con `expected = 0`
- [ ] Redondear o formatear con criterio consistente
- [ ] Commit sugerido: `feat(engine): calcular diferencias absolutas y relativas`

---

## Feature 2.7 — Estados de conciliación y tolerancias

**Objetivo:** traducir la comparación numérica a estados claros, accionables y consistentes con la narrativa del producto.

---

### Card 2.7.1 — Implementar política de tolerancia del MVP

**Descripción:** el motor necesita una política simple y explicable que combine umbral absoluto y relativo.

**Criterio de aceptación:**

- Existe una política híbrida documentada e implementada
- La lógica es simple de explicar a negocio
- La política se aplica de forma consistente a todos los conceptos del MVP

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Implementar banda `Reconciled`
  - `abs(diff) <= 50` o `abs(diff_pct) <= 0.5%`
- [ ] Implementar banda `Minor Difference`
  - `abs(diff) <= 500` o `abs(diff_pct) <= 2%`
- [ ] Definir `Unreconciled` por encima de esas bandas
- [ ] Documentar racional de usar umbral absoluto y relativo
- [ ] Commit sugerido: `feat(engine): implementar politica de tolerancia del MVP`

---

### Card 2.7.2 — Implementar asignación de estados de conciliación

**Descripción:** esta card traduce resultados numéricos y condiciones de calidad a los cuatro estados funcionales del MVP.

**Criterio de aceptación:**

- El motor asigna `Reconciled`
- El motor asigna `Minor Difference`
- El motor asigna `Unreconciled`
- El motor asigna `Invalid / Incomplete` cuando corresponde

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Implementar estado `Reconciled`
- [ ] Implementar estado `Minor Difference`
- [ ] Implementar estado `Unreconciled`
- [ ] Implementar estado `Invalid / Incomplete`
- [ ] Priorizar problemas de calidad por encima de semáforos numéricos cuando aplique
- [ ] Commit sugerido: `feat(engine): asignar estados de conciliacion`

---

### Card 2.7.3 — Validar resultados contra la tabla maestra del demo

**Descripción:** esta card conecta el motor con el diseño narrativo del dataset. Es donde se comprueba que el comportamiento implementado coincide con la historia esperada.

**Criterio de aceptación:**

- Los resultados del motor se contrastan contra la tabla maestra del demo
- Se documentan desvíos relevantes
- Queda claro si el motor reproduce la intención narrativa del dataset

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Comparar output por concepto con la tabla maestra de EPIC 01
- [ ] Revisar conceptos verdes, amarillos y rojos
- [ ] Ajustar reglas si el motor contradice el diseño del demo sin justificación
- [ ] Commit sugerido: `test(engine): validar estados del motor contra tabla maestra`

---

## Feature 2.8 — Empaquetado de resultados del motor

**Objetivo:** dejar una salida estructurada y reutilizable para las capas posteriores del sistema.

---

### Card 2.8.1 — Diseñar el objeto de resultado agregado

**Descripción:** el motor no debe devolver solo un dataframe suelto. Debe producir un contrato estable para resultados por concepto.

**Criterio de aceptación:**

- Existe un esquema claro de resultado agregado
- El esquema incluye métricas, estado y metadata mínima
- El contrato puede usarse en persistencia y UI sin reinterpretaciones

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir schema/DTO para resultado por concepto
- [ ] Incluir campos agregados y métricas de soporte
- [ ] Incluir placeholders o campos reservados para explicación posterior
- [ ] Commit sugerido: `feat(engine): definir contrato de resultado agregado`

---

### Card 2.8.2 — Diseñar el objeto de resumen general de corrida lógica

**Descripción:** además del resultado por concepto, el motor debe poder sintetizar el estado general de la corrida.

**Criterio de aceptación:**

- Existe un resumen general reutilizable
- Resume conteos y montos relevantes
- Puede alimentar la Summary UI futura

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Calcular:
  - conceptos reconciled
  - conceptos minor difference
  - conceptos unreconciled
  - conceptos invalid/incomplete
- [ ] Calcular montos observados y esperados agregados si aplica
- [ ] Definir `overall run status` lógico
- [ ] Commit sugerido: `feat(engine): definir resumen general de corrida`

---

### Card 2.8.3 — Crear función orquestadora del motor

**Descripción:** esta card unifica el flujo completo de validación, normalización, agregación y comparación en una sola función o servicio principal del dominio.

**Criterio de aceptación:**

- Existe una función principal del motor
- La función ejecuta el pipeline completo en orden claro
- El motor puede invocarse desde tests, API o scripts

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Implementar secuencia:
  - parse
  - validate
  - normalize
  - build reconcilable base
  - aggregate
  - compare
  - assign status
  - package outputs
- [ ] Diseñar firma estable para la función principal
- [ ] Manejar errores de forma estructurada
- [ ] Commit sugerido: `feat(engine): crear orquestador principal del motor de conciliacion`

---

## Feature 2.9 — Testing funcional del motor

**Objetivo:** validar que el núcleo lógico del MVP se comporte como se espera antes de agregar explicación y UI.

---

### Card 2.9.1 — Crear casos de prueba unitarios de validación y normalización

**Descripción:** cubrir los bloques más determinísticos del motor con tests rápidos y específicos.

**Criterio de aceptación:**

- Existen tests para validaciones base
- Existen tests para normalización de conceptos y períodos
- Los tests cubren casos esperados y bordes principales

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Testear columnas faltantes
- [ ] Testear `amount` inválido
- [ ] Testear normalización de `payroll_period`
- [ ] Testear mapping de conceptos con y sin match
- [ ] Commit sugerido: `test(engine): cubrir validacion y normalizacion base`

---

### Card 2.9.2 — Crear pruebas de agregación y estados de conciliación

**Descripción:** validar el comportamiento central del motor sobre datos controlados.

**Criterio de aceptación:**

- Existen tests de observed totals
- Existen tests de cálculo de diff
- Existen tests de asignación de estado por tolerancia

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Testear agregación por concepto/período
- [ ] Testear `absolute_diff` y `relative_diff_pct`
- [ ] Testear bandas verde/amarillo/rojo
- [ ] Testear `Invalid / Incomplete`
- [ ] Commit sugerido: `test(engine): cubrir agregacion y estados de conciliacion`

---

### Card 2.9.3 — Crear prueba end-to-end del motor con dataset demo

**Descripción:** esta prueba verifica que el motor se comporte correctamente con el dataset diseñado para el MVP, no solo con fixtures pequeños.

**Criterio de aceptación:**

- Existe una prueba integrada del motor
- Usa el dataset del demo o un subconjunto representativo
- Permite detectar desviaciones contra la intención narrativa del proyecto

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Cargar dataset demo o fixture equivalente
- [ ] Ejecutar motor end-to-end
- [ ] Validar outputs por concepto clave
- [ ] Validar resumen general de corrida
- [ ] Commit sugerido: `test(engine): agregar prueba end-to-end del motor`

---

## Resumen de commits esperados en EPIC 02

- `docs(engine): definir unidad de conciliación del MVP`
- `docs(engine): definir contrato de input del motor`
- `docs(engine): definir contrato de output del motor`
- `feat(engine): validar esquema base del payroll`
- `feat(engine): validar tipos y consistencia mínima del input`
- `feat(engine): validar expected totals del MVP`
- `feat(engine): normalizar columnas y tipos base`
- `feat(engine): normalizar periodo y lógica temporal`
- `feat(engine): normalizar conceptos con concept master`
- `feat(engine): normalizar signos y montos`
- `feat(engine): construir base conciliable intermedia`
- `docs(engine): definir reglas de inclusion del observed total`
- `chore(engine): preparar base conciliable para drilldown`
- `feat(engine): implementar observed totals por concepto y periodo`
- `feat(engine): soportar agregacion opcional por legal entity`
- `feat(engine): enlazar observed totals con expected totals`
- `feat(engine): calcular diferencias absolutas y relativas`
- `feat(engine): implementar politica de tolerancia del MVP`
- `feat(engine): asignar estados de conciliacion`
- `test(engine): validar estados del motor contra tabla maestra`
- `feat(engine): definir contrato de resultado agregado`
- `feat(engine): definir resumen general de corrida`
- `feat(engine): crear orquestador principal del motor de conciliacion`
- `test(engine): cubrir validacion y normalizacion base`
- `test(engine): cubrir agregacion y estados de conciliacion`
- `test(engine): agregar prueba end-to-end del motor`

---

## Notas técnicas

### Límite deliberado de esta epic

Esta epic no resuelve todavía la explicación rica de diferencias. Puede dejar flags preliminares y metadata útil, pero su responsabilidad principal es:

- producir observed totals confiables
- compararlos bien
- clasificar su estado

La capa de explicación profunda pertenece a la siguiente epic.

### Decisión de diseño importante

El motor debe ser:

- **determinístico**
- **auditable**
- **rápido**
- **fácil de depurar**

Eso favorece una implementación modular en Python con `pandas`, reglas explícitas y outputs estructurados. No hace falta introducir LLMs ni heurísticas complejas en este punto.

### Pregunta rectora de implementación

En cada card de esta epic conviene chequear:

> “¿Esto hace más confiable el cálculo y más claro el estado de conciliación?”

Si la respuesta es no, probablemente no pertenece a esta epic.

### Qué no entra en esta epic

- ranking de causas probables
- narrativa explicativa final
- recomendaciones automáticas de revisión
- UI de summary o concept analysis
- persistencia completa de runs en DB
- exports

Todo eso vendrá después. Esta epic construye el núcleo lógico sobre el que esas capas se van a apoyar.
