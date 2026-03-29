# EPIC 08 — Demo Seed, Narrative & Commercial Flow

## Contexto y objetivo

Esta epic convierte al MVP en un **asset comercial demostrable**. A diferencia de las épicas anteriores, que construyen capacidad de producto, esta epic se enfoca en dejar la demo lista para ser mostrada de forma controlada, convincente y repetible.

Hasta este punto, el sistema ya debería poder:

- cargar archivos
- ejecutar una corrida
- mostrar summary, concept analysis y drill-down
- explicar diferencias
- exportar evidencia básica

Eso es necesario, pero no suficiente para una demo vendible.

Para que el producto realmente pueda usarse en una reunión comercial o de validación, hace falta además:

- un dataset demo consistente y fácilmente recuperable
- runs predecibles y narrativamente sólidas
- conceptos estrella que sostengan el wow moment
- una secuencia de navegación pensada para contar una historia
- un entorno que pueda resetearse y volver a mostrarse sin sorpresas

La tesis de esta epic es:

> **Una buena demo no es solo un sistema que funciona; es un sistema que cuenta bien su historia, con control narrativo y cero fricción operativa.**

Al terminar esta epic, el proyecto debe tener:

- seed de demo reproducible
- archivos del demo y runs alineados con la narrativa
- una corrida “ideal” o fácilmente regenerable
- conceptos wow validados visual y operativamente
- guión de demo de 5–8 minutos
- checklist de preparación para mostrar el MVP

## Dominio(s) involucrado(s)

No es un dominio funcional nuevo. Es una epic transversal de producto/demo.

## Dependencias

- **EPIC 01** completada o suficientemente avanzada, con dataset demo definido
- **EPIC 02** completada o suficientemente avanzada, con motor funcionando
- **EPIC 03** completada o suficientemente avanzada, con explanation layer operativa
- **EPIC 06** completada o suficientemente avanzada, con summary y concept analysis listos
- **EPIC 07** completada o suficientemente avanzada, con drill-down y exportables básicos

## Criterio de aceptación de la Epic completa

- [ ] Existe un seed o mecanismo reproducible para dejar la demo en estado listo
- [ ] El dataset demo cargado produce los estados y wow cases esperados
- [ ] Existe al menos una run demo lista para mostrar o fácilmente regenerable
- [ ] Los conceptos `MEAL_VOUCHER`, `CHILDCARE`, `OVERTIME` y `TRANSPORT` se comportan como fue diseñado
- [ ] La navegación de demo soporta un recorrido comercial de 5–8 minutos
- [ ] Existe un guión de demo con apertura, wow moment y cierre
- [ ] Existe un checklist de preparación y validación pre-demo

## Estado: PENDIENTE

---

## Feature 8.1 — Estrategia de seed del demo

**Objetivo:** definir cómo se materializa y recupera el estado demo del producto.

---

### Card 8.1.1 — Definir estrategia de seed del MVP

**Descripción:** antes de sembrar datos, conviene decidir si la demo se sostiene con una corrida precargada, una corrida regenerable en un click, o un enfoque mixto.

**Criterio de aceptación:**

- Existe estrategia clara de seed
- La estrategia elegida prioriza control narrativo y repetibilidad
- El equipo puede volver a un estado demo sin fricción

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Evaluar alternativas:
  - corrida precargada persistida
  - regeneración programática de run demo
  - enfoque híbrido
- [ ] Elegir estrategia recomendada para MVP
- [ ] Documentar ventajas y trade-offs
- [ ] Commit sugerido: `docs(demo): definir estrategia de seed del MVP`

---

### Card 8.1.2 — Definir alcance de lo que el seed debe dejar listo

**Descripción:** especificar qué parte exacta del producto quedará sembrada para la demo.

**Criterio de aceptación:**

- Existe lista clara de artefactos demo a crear
- El alcance del seed está alineado con el guión comercial
- Se evita tanto quedarse corto como sobresembrar innecesariamente

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir si el seed crea:
  - archivos demo
  - run demo
  - resultados persistidos
  - excepciones persistidas
  - exportables sample opcionales
- [ ] Documentar qué debe quedar listo al finalizar el seed
- [ ] Commit sugerido: `docs(demo): definir alcance del seed demo`

---

## Feature 8.2 — Materialización del dataset demo

**Objetivo:** asegurar que los datos sembrados o cargados reflejan exactamente la narrativa diseñada.

---

### Card 8.2.1 — Consolidar archivos demo finales

**Descripción:** tomar la definición de EPIC 01 y convertirla en el set final de archivos que se usará para la demo.

**Criterio de aceptación:**

- Existen archivos demo finales consistentes
- Los archivos responden al diseño maestro del proyecto
- El set está listo para ser cargado o sembrado

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Consolidar versión final de:
  - `payroll.csv`
  - `expected_totals.csv`
  - `concept_master.csv`
  - `employee_reference.csv` si aplica
- [ ] Verificar naming y estructura definitivos
- [ ] Validar que sean fácilmente reutilizables en local/demo
- [ ] Commit sugerido: `feat(demo): consolidar archivos demo finales`

---

### Card 8.2.2 — Validar tabla maestra final del demo

**Descripción:** antes de cargar o sembrar nada, hay que validar por última vez que la tabla maestra por concepto sigue alineada con el comportamiento real esperado.

**Criterio de aceptación:**

- La tabla maestra final existe y está revisada
- Cada concepto tiene estado y explicación target consistentes
- La tabla puede usarse como contrato narrativo del demo

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Revisar expected, observed, diff y status por concepto
- [ ] Confirmar conceptos verdes, amarillos y rojos
- [ ] Confirmar explicación principal esperada por concepto
- [ ] Commit sugerido: `docs(demo): validar tabla maestra final del demo`

---

## Feature 8.3 — Creación de la run demo

**Objetivo:** dejar una corrida demo lista o fácilmente generable que soporte el recorrido comercial.

---

### Card 8.3.1 — Definir la run demo canónica del MVP

**Descripción:** esta card fija cuál será la corrida principal sobre la que se apoyará la demo comercial.

**Criterio de aceptación:**

- Existe una run demo canónica claramente definida
- La run tiene período, archivos y propósito establecidos
- La demo no depende de improvisación en tiempo real

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir nombre/label de la run demo
- [ ] Confirmar período `2026-03`
- [ ] Definir si habrá una única run principal o una pequeña familia de runs demo
- [ ] Commit sugerido: `docs(demo): definir run demo canonica`

---

### Card 8.3.2 — Implementar script o flujo para crear la run demo

**Descripción:** formalizar la forma en que esa run queda disponible en el entorno.

**Criterio de aceptación:**

- Existe script o flujo claro para crear la run demo
- El proceso puede repetirse
- La corrida queda operativa y consistente

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Crear script/comando para seed de run demo
- [ ] Asociar archivos a la run
- [ ] Ejecutar pipeline completo o cargar resultados persistidos
- [ ] Commit sugerido: `feat(demo): implementar script de creacion de run demo`

---

### Card 8.3.3 — Implementar reset del entorno demo

**Descripción:** toda demo vendible necesita la capacidad de volver a un estado limpio y controlado.

**Criterio de aceptación:**

- Existe una forma clara de resetear el entorno demo
- El reset evita datos residuales que afecten la narrativa
- El proceso es simple y repetible

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir qué limpia el reset:
  - runs demo
  - uploaded files demo
  - resultados y excepciones demo
- [ ] Implementar script/comando de reset
- [ ] Validar que el entorno pueda sembrarse de nuevo sin conflictos
- [ ] Commit sugerido: `feat(demo): implementar reset del entorno demo`

---

## Feature 8.4 — Validación narrativa de los conceptos estrella

**Objetivo:** asegurarse de que los conceptos clave del demo se comporten exactamente como deben en una presentación real.

---

### Card 8.4.1 — Validar caso wow principal `MEAL_VOUCHER`

**Descripción:** este concepto debe ser el núcleo dramático del demo. Debe abrirse bien, explicarse bien y defenderse bien en drill-down.

**Criterio de aceptación:**

- `MEAL_VOUCHER` aparece claramente como concepto problemático
- La explanation layer y el drill-down refuerzan la narrativa multi-causa
- El caso se siente fuerte y creíble en demo

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Validar status esperado
- [ ] Validar causas principales visibles
- [ ] Validar drill-down consistente
- [ ] Ajustar si el caso no produce suficiente wow
- [ ] Commit sugerido: `test(demo): validar wow case meal voucher`

---

### Card 8.4.2 — Validar caso `CHILDCARE`

**Descripción:** este concepto debe mostrar que el sistema entiende lógica de población elegible, no solo anomalías mecánicas.

**Criterio de aceptación:**

- `CHILDCARE` comunica claramente faltantes de población
- La explicación se siente cercana al caso real
- La recomendación final es convincente

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Validar empleados faltantes o elegibilidad esperada
- [ ] Validar copy explicativo y recomendación
- [ ] Confirmar legibilidad del caso en demo
- [ ] Commit sugerido: `test(demo): validar caso childcare`

---

### Card 8.4.3 — Validar caso `OVERTIME`

**Descripción:** este concepto debe reforzar la capacidad analítica del sistema con un caso claro de outlier.

**Criterio de aceptación:**

- `OVERTIME` muestra correctamente el outlier dominante
- La vista por concepto y drill-down refuerzan la detección
- El caso se entiende rápido en demo

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Validar outlier y métricas asociadas
- [ ] Confirmar que el caso no se diluye entre otras anomalías
- [ ] Revisar claridad de recomendación
- [ ] Commit sugerido: `test(demo): validar caso overtime`

---

### Card 8.4.4 — Validar caso `TRANSPORT`

**Descripción:** este caso confirma que el sistema también maneja diferencias menores con criterio y sin dramatización.

**Criterio de aceptación:**

- `TRANSPORT` aparece como minor difference
- La UI no sobredimensiona el caso
- El concepto sirve para mostrar criterio y tolerancia

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Validar `Minor Difference`
- [ ] Confirmar tono sobrio de explicación
- [ ] Ajustar visual si compite demasiado con casos wow
- [ ] Commit sugerido: `test(demo): validar caso transport`

---

## Feature 8.5 — Orden narrativo del demo

**Objetivo:** convertir la demo en una secuencia comercial clara y fácil de ejecutar.

---

### Card 8.5.1 — Definir estructura del demo de 5–8 minutos

**Descripción:** fijar la narrativa principal para mostrar el MVP en un entorno comercial o de validación.

**Criterio de aceptación:**

- Existe una secuencia narrativa cerrada
- La secuencia está alineada con la UX del producto
- El recorrido es corto, claro y orientado a insight

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir secuencia:
  - contexto
  - setup breve
  - summary
  - caso wow principal
  - drill-down
  - cierre de valor
- [ ] Estimar tiempos por tramo
- [ ] Commit sugerido: `docs(demo): definir estructura del demo comercial`

---

### Card 8.5.2 — Definir momento wow del demo

**Descripción:** el demo necesita un clímax claro, reconocible y repetible.

**Criterio de aceptación:**

- Existe una definición explícita del wow moment
- El wow está anclado en una navegación concreta del producto
- El momento es coherente con la propuesta de valor

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir wow moment como secuencia:
  - summary con rojo visible
  - apertura de `MEAL_VOUCHER`
  - top causes
  - bajada a drill-down
- [ ] Documentar por qué esa secuencia vende valor
- [ ] Commit sugerido: `docs(demo): definir wow moment principal`

---

### Card 8.5.3 — Definir cierre comercial del walkthrough

**Descripción:** el demo no termina en el detalle técnico. Debe cerrar con una lectura de negocio clara.

**Criterio de aceptación:**

- Existe cierre comercial explícito
- El cierre conecta la demo con dolor, ahorro de tiempo y trazabilidad
- El mensaje final es breve y accionable

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Redactar mensaje de cierre
- [ ] Vincular con:
  - reducción de trabajo manual
  - explicación inmediata
  - trazabilidad
  - escalabilidad futura
- [ ] Commit sugerido: `docs(demo): definir cierre comercial del walkthrough`

---

## Feature 8.6 — Script operativo del demo

**Objetivo:** documentar el recorrido exacto del presentador para que la demo sea consistente entre sesiones y personas.

---

### Card 8.6.1 — Crear guión paso a paso de la demo

**Descripción:** esta card transforma la narrativa general en una secuencia operativa concreta frente al producto.

**Criterio de aceptación:**

- Existe un script paso a paso
- El script sigue el orden real de navegación del producto
- El script es utilizable por otra persona sin contexto oral adicional

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Documentar pantalla por pantalla qué mostrar
- [ ] Documentar qué decir en cada tramo
- [ ] Documentar qué evitar mostrar para no dispersar el foco
- [ ] Commit sugerido: `docs(demo): crear guion operativo paso a paso`

---

### Card 8.6.2 — Documentar preguntas frecuentes esperables y respuestas sugeridas

**Descripción:** anticipar objeciones o preguntas típicas de clientes o stakeholders durante el demo.

**Criterio de aceptación:**

- Existe listado de preguntas frecuentes
- Las respuestas están alineadas con el estado real del MVP
- El guión gana robustez comercial

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Identificar preguntas típicas:
  - ¿esto se integra con SAP?
  - ¿cómo se configura para otro cliente?
  - ¿qué tan manual es el setup?
  - ¿cómo se explican diferencias complejas?
- [ ] Redactar respuestas honestas y comercialmente útiles
- [ ] Commit sugerido: `docs(demo): documentar faq del walkthrough`

---

## Feature 8.7 — Checklist pre-demo

**Objetivo:** reducir riesgo operativo antes de una reunión real.

---

### Card 8.7.1 — Definir checklist técnico pre-demo

**Descripción:** verificar que la demo y el entorno estén en estado correcto antes de mostrar el producto.

**Criterio de aceptación:**

- Existe checklist técnico claro
- El checklist cubre dataset, run y navegación principal
- Su ejecución reduce riesgo de fallo visible

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Verificar:
  - app levantada
  - backend operativo
  - run demo presente
  - conceptos wow correctos
  - drill-down funcionando
  - exports descargables
- [ ] Documentar responsable y momento de ejecución
- [ ] Commit sugerido: `docs(demo): definir checklist tecnico pre-demo`

---

### Card 8.7.2 — Definir checklist narrativo pre-demo

**Descripción:** además del estado técnico, conviene chequear que la secuencia comercial esté clara antes de la reunión.

**Criterio de aceptación:**

- Existe checklist narrativo breve
- El checklist ayuda a mantener foco y timing
- La demo reduce improvisación innecesaria

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Verificar:
  - historia principal clara
  - wow moment identificado
  - cierre comercial preparado
  - respuestas a objeciones revisadas
- [ ] Documentar tiempos recomendados
- [ ] Commit sugerido: `docs(demo): definir checklist narrativo pre-demo`

---

## Feature 8.8 — Validación integral del demo-ready state

**Objetivo:** certificar que el producto está realmente listo para mostrarse sin depender de buena suerte.

---

### Card 8.8.1 — Ejecutar ensayo completo de demo end-to-end

**Descripción:** realizar una corrida completa del guión con el producto real para detectar fricciones, huecos narrativos o problemas operativos.

**Criterio de aceptación:**

- El walkthrough completo puede ejecutarse en el tiempo esperado
- No aparecen bloqueos técnicos o narrativos relevantes
- La demo se sostiene de principio a fin

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Correr demo completa como ensayo
- [ ] Medir duración real
- [ ] Registrar puntos de fricción
- [ ] Ajustar si el flujo se cae o pierde fuerza
- [ ] Commit sugerido: `test(demo): ejecutar ensayo completo de demo`

---

### Card 8.8.2 — Validar demo-ready criteria del MVP

**Descripción:** cerrar formalmente si el producto está o no en estado “listo para demo”.

**Criterio de aceptación:**

- Existe evaluación explícita del estado demo-ready
- Se documentan riesgos residuales si los hubiera
- El equipo tiene criterio claro para pasar a la siguiente fase

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Evaluar:
  - estabilidad funcional
  - consistencia narrativa
  - wow moment
  - calidad visual mínima
  - exportables mínimos
- [ ] Documentar gaps restantes si existen
- [ ] Commit sugerido: `docs(demo): validar demo-ready criteria del MVP`

---

## Resumen de commits esperados en EPIC 08

- `docs(demo): definir estrategia de seed del MVP`
- `docs(demo): definir alcance del seed demo`
- `feat(demo): consolidar archivos demo finales`
- `docs(demo): validar tabla maestra final del demo`
- `docs(demo): definir run demo canonica`
- `feat(demo): implementar script de creacion de run demo`
- `feat(demo): implementar reset del entorno demo`
- `test(demo): validar wow case meal voucher`
- `test(demo): validar caso childcare`
- `test(demo): validar caso overtime`
- `test(demo): validar caso transport`
- `docs(demo): definir estructura del demo comercial`
- `docs(demo): definir wow moment principal`
- `docs(demo): definir cierre comercial del walkthrough`
- `docs(demo): crear guion operativo paso a paso`
- `docs(demo): documentar faq del walkthrough`
- `docs(demo): definir checklist tecnico pre-demo`
- `docs(demo): definir checklist narrativo pre-demo`
- `test(demo): ejecutar ensayo completo de demo`
- `docs(demo): validar demo-ready criteria del MVP`

---

## Notas técnicas

### Regla principal de esta epic

La demo debe sentirse:

- controlada
- clara
- profesional
- repetible

No debe depender de:

- improvisación narrativa
- datos inconsistentes
- runs manuales difíciles de reconstruir
- recorrido UI no ensayado

### Decisión importante del MVP

Si hay tensión entre:

- “mostrar más cosas”
- o “mostrar mejor el núcleo de valor”

siempre gana lo segundo.

Esta epic no busca agrandar la demo; busca **afilarla**.

### Qué no entra en esta epic

- múltiples demos temáticas
- branching narrativo complejo
- benchmarking con datasets alternativos
- automatización avanzada de preparación
- assets comerciales externos complejos

La meta es dejar **una demo principal muy fuerte**, no muchas demos mediocres.
