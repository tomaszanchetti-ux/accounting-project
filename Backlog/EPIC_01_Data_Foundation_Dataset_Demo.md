# EPIC 01 — Data Foundation & Dataset Demo

## Contexto y objetivo

Esta epic construye la base de datos funcional del MVP desde el punto de vista del negocio y de la narrativa del demo. No se trata solo de “tener CSVs”: se trata de diseñar un universo de datos deliberado, coherente y explicable, que haga posible una conciliación creíble y una historia comercial fuerte.

El dataset demo es una pieza central del producto. Si está mal diseñado:

- la conciliación parece artificial
- las diferencias se sienten forzadas
- la explicación pierde credibilidad
- el wow moment se debilita

Si está bien diseñado:

- el sistema se siente real
- los conceptos se entienden rápido
- los desvíos son plausibles
- la narrativa comercial fluye de forma natural

Al terminar esta epic, el proyecto debe tener:

- el diseño completo del universo de archivos del MVP
- esquemas y convenciones de datos cerradas
- dataset demo listo para ser generado o persistido
- una tabla de verdad interna por concepto para controlar expected, observed, diff y estado target

## Dominio(s) involucrado(s)

**D1 — Data Foundation & Dataset Demo**

## Dependencias

- **EPIC 00** completada o suficientemente avanzada para soportar trabajo con archivos, backend y persistencia mínima

## Criterio de aceptación de la Epic completa

- [ ] Existe definición cerrada del `payroll.csv` del demo
- [ ] Existe definición cerrada del `expected_totals.csv`
- [ ] Existe definición cerrada del `concept_master.csv`
- [ ] Existe definición cerrada del `employee_reference.csv` o se documenta explícitamente su exclusión
- [ ] El período principal del demo queda fijado y consistente
- [ ] Los conceptos del MVP quedan cerrados y categorizados
- [ ] Existe una estrategia explícita de construcción del dataset observado y los expected totals
- [ ] Están definidos los casos normales, menores y wow del demo
- [ ] Existe una tabla de diseño objetivo por concepto con `expected`, `observed`, `diff`, `estado` y explicación principal
- [ ] El dataset puede ser generado o cargado de manera reproducible

## Estado: PENDIENTE

---

## Feature 1.1 — Universo de archivos del demo

**Objetivo:** cerrar qué archivos existen en el MVP, qué rol cumple cada uno y cuál es su nivel de obligatoriedad.

---

### Card 1.1.1 — Definir el archivo principal `payroll.csv`

**Descripción:** `payroll.csv` es la fuente observada a conciliar. Debe parecer un export real de payroll/SAP, con múltiples líneas por empleado y por concepto, y suficiente riqueza para sostener agregación, excepciones y drill-down.

**Criterio de aceptación:**

- Queda definido el rol funcional de `payroll.csv`
- Se documenta su estructura mínima esperada
- Se fijan convenciones de formato y supuestos de calidad

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Confirmar que `payroll.csv` será el archivo principal del demo
- [x] Documentar que representa el export mensual de nómina / beneficios
- [x] Definir que contendrá múltiples líneas por empleado y concepto
- [x] Dejar explícito que es la fuente observada a conciliar
- [ ] Commit sugerido: `docs(data): definir payroll.csv como fuente principal del demo`

---

### Card 1.1.2 — Definir `expected_totals.csv`

**Descripción:** `expected_totals.csv` contiene la referencia contra la cual se compara el total observado. Es la “verdad de control” del demo y debe diseñarse con coherencia interna respecto al payroll.

**Criterio de aceptación:**

- Queda definido el rol funcional de `expected_totals.csv`
- Se fija su grano mínimo
- Se documenta cómo se relaciona con la unidad de conciliación

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir que `expected_totals.csv` tiene una fila por concepto y período
- [x] Evaluar si incluye `legal_entity` en MVP o queda nullable/fuera de alcance inicial
- [x] Documentar que actúa como referencia esperada del período
- [x] Documentar cómo se visualizará o cargará en el producto
- [ ] Commit sugerido: `docs(data): definir expected_totals.csv del MVP`

---

### Card 1.1.3 — Definir `concept_master.csv`

**Descripción:** `concept_master.csv` normaliza conceptos, habilita mapping y sostiene varias de las excepciones del MVP.

**Criterio de aceptación:**

- Existe definición funcional de `concept_master.csv`
- Se documentan sus columnas mínimas
- Queda claro su rol en normalización y explicación

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir columnas mínimas de mapping y normalización
- [ ] Incluir categoría, signo esperado y grupo de conciliación
- [ ] Documentar que habilita excepciones como `unmapped concept` y `sign error`
- [ ] Commit sugerido: `docs(data): definir concept_master.csv`

---

### Card 1.1.4 — Definir `employee_reference.csv` opcional

**Descripción:** este archivo auxiliar permite modelar elegibilidad, población esperada y casos de faltantes, especialmente para `CHILDCARE` y beneficios selectivos.

**Criterio de aceptación:**

- Queda decidido si el archivo entra al MVP
- Si entra, se documenta su estructura mínima
- Si no entra, se documenta cómo se resolverá el caso de `missing population`

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Decidir si `employee_reference.csv` entra en el MVP base
- [ ] Si entra, definir columnas mínimas
- [ ] Documentar su uso para elegibilidad por concepto
- [ ] Commit sugerido: `docs(data): definir employee_reference.csv opcional`

---

## Feature 1.2 — Esquema del payroll demo

**Objetivo:** fijar el esquema de columnas, tipos y convenciones del archivo principal.

---

### Card 1.2.1 — Definir columnas del `payroll.csv`

**Descripción:** dejar cerrada la estructura tabular del payroll para que luego pueda generarse, validarse y persistirse sin ambigüedad.

**Criterio de aceptación:**

- Existe lista cerrada de columnas del payroll
- Cada columna tiene propósito funcional claro
- El esquema sostiene conciliación, explicación y drill-down

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir columnas recomendadas:
  - `record_id`
  - `employee_id`
  - `employee_name`
  - `legal_entity`
  - `country`
  - `cost_center`
  - `payroll_period`
  - `posting_date`
  - `concept_code`
  - `concept_name`
  - `amount`
  - `currency`
- [ ] Validar que el esquema cubre los casos wow definidos
- [ ] Commit sugerido: `docs(data): cerrar columnas de payroll.csv`

---

### Card 1.2.2 — Definir tipos y convenciones de formato

**Descripción:** documentar tipos, formatos y estandarización esperada para que el motor luego pueda validar y normalizar con criterios claros.

**Criterio de aceptación:**

- Cada columna crítica tiene tipo sugerido
- Existen convenciones explícitas de período, moneda y montos
- Se documentan supuestos de calidad de datos

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir tipos de dato por columna
- [ ] Fijar `payroll_period` como `YYYY-MM`
- [ ] Fijar moneda principal como `EUR`
- [ ] Fijar importes con 2 decimales
- [ ] Fijar `concept_code` normalizado en mayúsculas
- [ ] Commit sugerido: `docs(data): definir tipos y convenciones del payroll`

---

### Card 1.2.3 — Definir supuestos de calidad e input válido

**Descripción:** el MVP no busca tolerar caos total. Esta card fija qué asumimos como input razonable y qué clase de errores queremos modelar deliberadamente.

**Criterio de aceptación:**

- Se documenta el baseline de input válido
- Se distinguen errores plausibles de errores destructivos
- Queda claro qué condiciones invalidan una corrida y cuáles generan excepciones explicables

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir columnas obligatorias
- [ ] Definir qué errores se toleran como anomalías modelables
- [ ] Definir qué errores rompen la corrida
- [ ] Documentar el nivel de “realismo controlado” esperado
- [ ] Commit sugerido: `docs(data): definir supuestos de calidad del input`

---

## Feature 1.3 — Universo de empleados y organización

**Objetivo:** definir la población del demo y su distribución organizativa.

---

### Card 1.3.1 — Cerrar tamaño y composición del universo de empleados

**Descripción:** definir cuántos empleados existirán en el demo y qué variabilidad mínima deben mostrar para sentirse reales.

**Criterio de aceptación:**

- Se fija el tamaño objetivo del universo
- Se documentan tipos de empleados y casos especiales
- El volumen es coherente con el nivel de demo deseado

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Fijar universo target de `360 empleados`
- [ ] Documentar que el rango aceptable es `300–500`
- [ ] Definir perfiles estándar y casos especiales
- [ ] Commit sugerido: `docs(data): cerrar universo de empleados del demo`

---

### Card 1.3.2 — Definir entidades, países y cost centers

**Descripción:** dar textura organizativa al demo sin complejizar en exceso la conciliación principal.

**Criterio de aceptación:**

- Existen `legal_entities` definidas
- Existe distribución simple por país
- Existen cost centers suficientes para drill-down y realismo

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir `legal_entities` del MVP
- [ ] Fijar foco principal en España
- [ ] Definir lista acotada de `cost_centers`
- [ ] Documentar que estas dimensiones enriquecen, pero no gobiernan la conciliación base
- [ ] Commit sugerido: `docs(data): definir estructura organizativa del dataset`

---

## Feature 1.4 — Universo de conceptos del MVP

**Objetivo:** cerrar la lista de conceptos a conciliar, su rol funcional y los conceptos protagonistas del demo.

---

### Card 1.4.1 — Definir conceptos del MVP

**Descripción:** elegir un set de conceptos suficientemente realista, entendible y útil para narrativa comercial.

**Criterio de aceptación:**

- Existe una lista cerrada de conceptos del MVP
- Cada concepto tiene racional funcional
- La lista es manejable para demo y suficientemente rica para análisis

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir lista objetivo de `8–10 conceptos`
- [ ] Incluir al menos:
  - `BASE_SALARY`
  - `BONUS`
  - `MEAL_VOUCHER`
  - `CHILDCARE`
  - `TRANSPORT`
  - `HEALTH_INSURANCE`
  - `SOCIAL_SECURITY`
  - `INCOME_TAX`
  - `OVERTIME`
  - `OTHER_ADJUSTMENT`
- [ ] Confirmar conceptos limpios vs protagonistas del wow
- [ ] Commit sugerido: `docs(data): definir universo de conceptos del MVP`

---

### Card 1.4.2 — Categorizar conceptos y signos esperados

**Descripción:** documentar categorías y polaridad esperada para habilitar normalización, explicación y futuras reglas.

**Criterio de aceptación:**

- Cada concepto tiene categoría funcional
- Cada concepto tiene signo esperado
- La información puede volcarse luego a `concept_master.csv`

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Asignar categoría por concepto
- [ ] Definir signo esperado por concepto
- [ ] Documentar qué conceptos son candidatos a `sign error`
- [ ] Commit sugerido: `docs(data): categorizar conceptos y signos esperados`

---

### Card 1.4.3 — Definir conceptos estrella del demo

**Descripción:** dejar cerrados los conceptos que van a sostener la narrativa principal del MVP.

**Criterio de aceptación:**

- Se identifican conceptos wow principales y secundarios
- Se documenta por qué fueron elegidos
- Queda clara su relación con la narrativa comercial

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Fijar `MEAL_VOUCHER` como caso wow principal
- [ ] Fijar `CHILDCARE` como caso de población faltante
- [ ] Fijar `OVERTIME` como caso analítico/outlier
- [ ] Documentar rol de `TRANSPORT` como caso amarillo
- [ ] Commit sugerido: `docs(data): definir conceptos estrella del demo`

---

## Feature 1.5 — Período del demo y lógica temporal

**Objetivo:** fijar el contexto temporal y su uso narrativo en la conciliación.

---

### Card 1.5.1 — Definir período principal del MVP

**Descripción:** el demo debe girar en torno a un único período central, con algunos registros de borde para sostener excepciones temporales.

**Criterio de aceptación:**

- Existe un período objetivo definido
- El período está alineado con el plan maestro
- Todo el dataset se diseña alrededor de ese corte temporal

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Fijar `2026-03` como período principal del demo
- [ ] Documentar que expected totals y mayoría de registros responden a ese período
- [ ] Commit sugerido: `docs(data): definir periodo principal del MVP`

---

### Card 1.5.2 — Definir reglas temporales y casos out-of-period

**Descripción:** dejar explícito cómo se modelan registros de otro período y cómo se usarán para explicación.

**Criterio de aceptación:**

- Se documenta la lógica temporal del demo
- Quedan definidos los casos `out-of-period`
- La anomalía temporal es usable por el motor y por la narrativa

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir qué significa estar fuera de período
- [ ] Documentar uso de `2026-02` como período incorrecto inyectado
- [ ] Documentar uso de `posting_date` inconsistente como refuerzo narrativo
- [ ] Commit sugerido: `docs(data): definir casos temporales y out-of-period`

---

## Feature 1.6 — Distribución de estados y anomalías del demo

**Objetivo:** diseñar deliberadamente cuántos conceptos deben reconciliar, cuántos quedan en amarillo y cuántos deben convertirse en wow cases.

---

### Card 1.6.1 — Definir distribución objetivo de estados

**Descripción:** el dataset debe parecer real. La mayoría de los conceptos deben estar bien, algunos con diferencias menores y pocos con errores interesantes.

**Criterio de aceptación:**

- Existe una distribución objetivo de estados del demo
- La distribución es coherente con una historia creíble
- Se sabe de antemano qué conceptos serán verde, amarillo y rojo

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir distribución target:
  - `60%–70%` reconciled
  - `20%–25%` minor difference
  - `10%–20%` unreconciled
- [ ] Asociar conceptos a cada banda
- [ ] Documentar racional narrativo de esa distribución
- [ ] Commit sugerido: `docs(data): definir distribución objetivo de estados`

---

### Card 1.6.2 — Definir catálogo de anomalías inyectadas

**Descripción:** listar las anomalías deliberadas que el dataset contendrá y su función dentro del demo.

**Criterio de aceptación:**

- Existe un catálogo explícito de anomalías del MVP
- Cada anomalía tiene propósito funcional
- El volumen de anomalías es deliberado y controlado

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Incluir anomalías objetivo:
  - `duplicates`
  - `unmapped concept`
  - `out-of-period`
  - `missing population`
  - `outlier`
  - `sign error` opcional
- [ ] Documentar volúmenes esperados por tipo
- [ ] Validar que no se sature el dataset con ruido
- [ ] Commit sugerido: `docs(data): definir catálogo de anomalías del demo`

---

### Card 1.6.3 — Diseñar anomalías concretas por concepto

**Descripción:** traducir el catálogo general a casos concretos por concepto protagonista.

**Criterio de aceptación:**

- Cada concepto protagonista tiene anomalías concretas asignadas
- Existe coherencia entre anomalías, diff target y explicación target
- El diseño permite al motor explicar el desvío de forma convincente

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar `MEAL_VOUCHER` con:
  - líneas fuera de período
  - posibles duplicados
  - códigos no mapeados
- [ ] Diseñar `CHILDCARE` con:
  - empleados elegibles ausentes
  - importes incorrectos
- [ ] Diseñar `OVERTIME` con:
  - 1 o 2 outliers claros
- [ ] Diseñar `TRANSPORT` como minor difference
- [ ] Commit sugerido: `docs(data): diseñar anomalías concretas por concepto`

---

## Feature 1.7 — Tabla de verdad del demo

**Objetivo:** crear el diseño cuantitativo maestro por concepto, que servirá de control para dataset, motor y UI.

---

### Card 1.7.1 — Definir tabla maestra por concepto

**Descripción:** esta tabla es el corazón de control narrativo del dataset. Para cada concepto debe saberse de antemano qué esperamos que ocurra.

**Criterio de aceptación:**

- Existe una tabla maestra por concepto
- Cada fila tiene `expected`, `observed`, `diff`, `estado target` y explicación principal
- La tabla puede usarse como guía de implementación y validación

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Crear tabla de diseño interno con columnas:
  - `concepto`
  - `expected`
  - `observed`
  - `diff`
  - `estado`
  - `explicacion_principal`
- [ ] Incluir al menos los conceptos principales del MVP
- [ ] Revisar coherencia matemática y narrativa
- [ ] Commit sugerido: `docs(data): crear tabla maestra de control por concepto`

---

### Card 1.7.2 — Validar coherencia entre payroll observado y expected totals

**Descripción:** antes de generar archivos reales, hay que fijar el método de construcción para que el dataset no se rompa internamente.

**Criterio de aceptación:**

- Existe un método claro de construcción del dataset
- Se documenta si se parte del payroll observado o de expected totals
- El método permite reproducibilidad

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Documentar método recomendado:
  - construir payroll base
  - derivar o diseñar expected totals coherentes
  - inyectar anomalías controladas
- [ ] Definir qué elementos serán generados y cuáles curados manualmente
- [ ] Commit sugerido: `docs(data): definir método de construcción del dataset`

---

## Feature 1.8 — Generación y persistencia del dataset demo

**Objetivo:** dejar definida la forma en que los archivos demo serán materializados y reutilizados.

---

### Card 1.8.1 — Definir estrategia de generación del dataset

**Descripción:** decidir si el dataset se genera por script, se construye manualmente o se usa un enfoque híbrido.

**Criterio de aceptación:**

- Existe una estrategia explícita de generación
- La estrategia elegida es reproducible
- Queda alineada con velocidad de mantenimiento y control narrativo

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Evaluar enfoque:
  - generación programática
  - curación manual
  - enfoque híbrido
- [ ] Priorizar control narrativo y reproducibilidad
- [ ] Definir carpeta destino para archivos demo
- [ ] Commit sugerido: `docs(data): definir estrategia de generación del dataset`

---

### Card 1.8.2 — Crear archivos demo iniciales del MVP

**Descripción:** materializar por primera vez los archivos del dataset en el repo o en la ubicación operativa elegida.

**Criterio de aceptación:**

- Existen archivos demo iniciales
- Los archivos respetan el diseño definido en la epic
- Pueden ser inspeccionados y reutilizados en desarrollo

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Crear `payroll.csv`
- [ ] Crear `expected_totals.csv`
- [ ] Crear `concept_master.csv`
- [ ] Crear `employee_reference.csv` si aplica
- [ ] Verificar consistencia estructural básica
- [ ] Commit sugerido: `feat(data): crear dataset demo inicial del MVP`

---

## Resumen de commits esperados en EPIC 01

- `docs(data): definir payroll.csv como fuente principal del demo`
- `docs(data): definir expected_totals.csv del MVP`
- `docs(data): definir concept_master.csv`
- `docs(data): definir employee_reference.csv opcional`
- `docs(data): cerrar columnas de payroll.csv`
- `docs(data): definir tipos y convenciones del payroll`
- `docs(data): definir supuestos de calidad del input`
- `docs(data): cerrar universo de empleados del demo`
- `docs(data): definir estructura organizativa del dataset`
- `docs(data): definir universo de conceptos del MVP`
- `docs(data): categorizar conceptos y signos esperados`
- `docs(data): definir conceptos estrella del demo`
- `docs(data): definir periodo principal del MVP`
- `docs(data): definir casos temporales y out-of-period`
- `docs(data): definir distribución objetivo de estados`
- `docs(data): definir catálogo de anomalías del demo`
- `docs(data): diseñar anomalías concretas por concepto`
- `docs(data): crear tabla maestra de control por concepto`
- `docs(data): definir método de construcción del dataset`
- `docs(data): definir estrategia de generación del dataset`
- `feat(data): crear dataset demo inicial del MVP`

---

## Notas técnicas

### Regla principal de esta epic

El dataset no se diseña para “parecer complejo”; se diseña para:

- soportar explicación
- sostener narrativa
- permitir validación consistente

### Tensión a resolver

Debe existir equilibrio entre:

- realismo suficiente
- control narrativo
- velocidad de implementación

Si un detalle suma realismo pero complica mucho el build sin aportar al demo, queda fuera.

### Qué no entra en esta epic

- ingestión real desde SAP
- generación masiva de datasets multi-país
- variantes complejas por moneda
- aleatoriedad no controlada
- simulación exhaustiva de payroll enterprise

El alcance aquí es: **fake data, real problem, believable behavior**.
