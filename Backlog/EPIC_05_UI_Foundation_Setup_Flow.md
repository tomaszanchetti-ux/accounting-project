# EPIC 05 — UI Foundation & Setup Flow

## Contexto y objetivo

Esta epic construye la base visible del producto y la primera experiencia completa que el usuario tendrá frente al sistema: preparar una corrida de conciliación.

Hasta ahora el proyecto ya cuenta con:

- arquitectura técnica definida
- dataset demo estructurado
- motor de conciliación y explicación
- capa operativa de runs, persistencia y API

Lo que todavía no existe es la primera traducción real de todo eso a una interfaz usable, creíble y alineada con el tipo de usuario objetivo: alguien de Contabilidad, Administración & Finanzas o control operativo, que necesita entender rápido qué está haciendo el sistema y disparar una corrida sin fricción.

La tesis de esta epic es:

> **La primera pantalla del producto no vende sofisticación. Vende orden, claridad y confianza.**

El flujo de setup debe comunicar que:

- el sistema recibe pocos insumos
- valida que son utilizables
- deja visible el contexto de la corrida
- está listo para ejecutar

Al terminar esta epic, el producto debe tener:

- una base visual consistente para el MVP
- layout inicial y componentes fundacionales
- una pantalla de setup funcional
- flujo de creación de run, carga de archivos y preview mínimo de configuración
- CTA principal de ejecución claramente definido

## Dominio(s) involucrado(s)

**D5 — UI Foundation & Setup Flow**

## Dependencias

- **EPIC 00** completada o suficientemente avanzada
- **EPIC 01** completada o suficientemente avanzada
- **EPIC 04** completada o suficientemente avanzada, con endpoints de runs y upload disponibles

## Criterio de aceptación de la Epic completa

- [x] Existe una base visual consistente y reusable para el MVP
- [x] La app presenta una landing interna o pantalla inicial del producto con framing claro
- [x] Existe un flujo funcional para crear una run desde UI
- [x] El usuario puede cargar payroll y expected totals desde la pantalla de setup
- [x] La UI muestra validación/preparación de inputs de forma clara
- [x] Existe una preview mínima de expected totals o configuración de corrida
- [x] El botón principal `Run Reconciliation` está disponible y conectado al backend
- [x] La experiencia de setup se siente enterprise, sobria y orientada a negocio

## Estado: EN PROGRESO

## Estado de implementación WS13

Implementación materializada sobre branch:

- `codex/epic-05-ui-foundation`

Entregables principales:

- documento `docs/UI_FOUNDATION_SETUP_FLOW.md`
- nueva gramática visual del frontend
- `AppShell`, `AppHeader`, badges, métricas y feedback reusable
- estado vacío/landing interna del producto
- `RunSetupForm`, `UploadBox`, `ExpectedTotalsPreview`,
  `RunValidationSummary`
- lifecycle de setup con `POST /runs`
- registro automático de `concept_master.csv`,
  `employee_reference.csv` y `expected_totals.csv` demo
- upload real de `payroll.csv` y reemplazo opcional de expected totals
- `Run Reconciliation` conectado a `POST /runs/{run_id}/execute`
- snapshot post-ejecución y ruta `/runs/[runId]`

Validación ejecutada en esta WS:

- `cd frontend && npm run lint`
- `cd frontend && npm run build`

Nota operativa:

- la implementación queda lista para continuar con `EPIC 06`
- antes de mergear a `main` sigue siendo recomendable un smoke visual/manual en navegador

---

## Feature 5.1 — Sistema visual base del MVP

**Objetivo:** fijar la gramática visual del producto antes de construir pantallas más complejas.

---

### Card 5.1.1 — Definir principios visuales del MVP

**Descripción:** antes de implementar componentes, conviene dejar cerrados los principios que van a ordenar toda la UI. Esta card traduce la visión UX del plan maestro a reglas operativas de implementación.

**Criterio de aceptación:**

- Existe una base explícita de principios visuales
- Los principios son coherentes con el usuario contable del MVP
- Sirven como guardrail para todas las pantallas futuras

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Documentar principios visuales:
  - enterprise clean
  - data-first
  - claridad antes que ornamento
  - color con propósito
  - jerarquía visual simple
- [ ] Definir que el tono debe ser serio, sobrio y ejecutivo-operativo
- [ ] Evitar charts decorativos y densidad innecesaria
- [ ] Commit sugerido: `docs(ui): definir principios visuales del MVP`

---

### Card 5.1.2 — Definir paleta base y semántica del producto

**Descripción:** la UI necesita una paleta coherente que transmita claridad y profesionalismo, con una semaforización clara para estados de conciliación.

**Criterio de aceptación:**

- Existe paleta base definida
- Existen colores semánticos para estados del sistema
- Las decisiones de color son consistentes con el uso de semáforos del producto

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir fondo de página, superficie, texto principal y secundario
- [ ] Definir semántica para:
  - `Reconciled`
  - `Minor Difference`
  - `Unreconciled`
  - `Invalid / Incomplete`
- [ ] Definir que el color solo comunica estados, no decoración
- [ ] Commit sugerido: `docs(ui): definir paleta base y semantica del MVP`

---

### Card 5.1.3 — Definir tipografía y escala de jerarquía

**Descripción:** el producto necesita una estructura tipográfica estable que favorezca lectura rápida de datos y headers claros.

**Criterio de aceptación:**

- Existe una tipografía base definida
- Existe escala jerárquica para título, subtítulo, label, body y caption
- La jerarquía puede reutilizarse en todas las pantallas del MVP

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir fuente base del producto
- [ ] Definir escala para:
  - page title
  - section heading
  - card title
  - body
  - metadata
- [ ] Documentar reglas de legibilidad en tablas y formularios
- [ ] Commit sugerido: `docs(ui): definir tipografia y jerarquia base`

---

## Feature 5.2 — Shell inicial de la aplicación

**Objetivo:** construir la estructura base sobre la cual vivirán las pantallas del MVP.

---

### Card 5.2.1 — Definir layout general del producto

**Descripción:** el MVP no necesita una navegación compleja, pero sí una estructura clara con header, content area y suficiente framing para parecer producto.

**Criterio de aceptación:**

- Existe un layout base del producto
- El layout soporta header y contenido principal
- La estructura es lo bastante simple para extenderse a pantallas futuras

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir layout principal con:
  - page wrapper
  - header
  - main content
- [ ] Decidir si MVP usa topbar simple o sidebar mínima
- [ ] Preparar layout reusable para pantallas futuras
- [ ] Commit sugerido: `feat(ui): crear layout base del producto`

---

### Card 5.2.2 — Implementar header de producto

**Descripción:** el header debe dar contexto inmediato al usuario: qué sistema está usando, qué pantalla está viendo y cuál es la acción primaria.

**Criterio de aceptación:**

- Existe header consistente
- El header contiene título, subtítulo contextual y espacio para acción primaria
- La solución es reusable en pantallas futuras

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar header con:
  - nombre del producto o módulo
  - título de página
  - subtítulo descriptivo
  - slot para acción primaria
- [ ] Definir spacing y jerarquía visual
- [ ] Implementar componente reusable
- [ ] Commit sugerido: `feat(ui): implementar header base del MVP`

---

### Card 5.2.3 — Crear estado inicial vacío o landing interna

**Descripción:** cuando el usuario entra a la app sin una corrida activa, debe ver una pantalla inicial que explique rápidamente qué hace el sistema y qué acción puede tomar.

**Criterio de aceptación:**

- Existe estado inicial claro y útil
- La pantalla comunica propósito del producto
- Dirige naturalmente hacia crear una nueva run

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar pantalla inicial con:
  - framing del producto
  - breve explicación del flujo
  - CTA para nueva corrida
- [ ] Evitar exceso de texto o marketing
- [ ] Implementar empty state reusable
- [ ] Commit sugerido: `feat(ui): crear estado inicial del producto`

---

## Feature 5.3 — Componentes fundacionales del flujo de setup

**Objetivo:** construir los componentes UI básicos que estructurarán la pantalla de configuración de corrida.

---

### Card 5.3.1 — Crear `RunSetupForm`

**Descripción:** componente contenedor del formulario de configuración de corrida. Debe centralizar inputs clave sin convertirse en wizard innecesario.

**Criterio de aceptación:**

- Existe componente principal del setup
- El formulario organiza inputs de manera clara
- Está preparado para integrarse con la API de runs

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Crear estructura base de `RunSetupForm`
- [ ] Definir secciones internas del formulario
- [ ] Integrar estado local base del setup
- [ ] Commit sugerido: `feat(ui): crear componente RunSetupForm`

---

### Card 5.3.2 — Crear componente `UploadBox`

**Descripción:** componente reusable para cargar archivos del MVP. Debe verse serio, claro y mostrar feedback de estado sin complejidad innecesaria.

**Criterio de aceptación:**

- Existe componente reusable de upload
- El componente soporta al menos payroll y expected totals
- Muestra nombre de archivo y estado de carga

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar zona de upload clara y sobria
- [ ] Mostrar nombre de archivo cargado
- [ ] Mostrar estado: pendiente, cargado, error
- [ ] Preparar integración con backend
- [ ] Commit sugerido: `feat(ui): crear componente UploadBox`

---

### Card 5.3.3 — Crear componente `ExpectedTotalsPreview`

**Descripción:** el usuario debe poder ver rápidamente qué expected totals se van a usar. No hace falta edición avanzada todavía, pero sí visibilidad.

**Criterio de aceptación:**

- Existe componente para preview de expected totals
- El preview es simple, legible y orientado a negocio
- Puede mostrar datos precargados o cargados desde archivo

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar preview tabular simple
- [ ] Mostrar concepto y expected amount
- [ ] Preparar modo vacío, loading y data present
- [ ] Commit sugerido: `feat(ui): crear preview de expected totals`

---

### Card 5.3.4 — Crear componente `RunValidationSummary`

**Descripción:** antes de ejecutar la conciliación, el sistema debe mostrar si el input parece listo. Esta es una pequeña pieza de confianza muy valiosa.

**Criterio de aceptación:**

- Existe un bloque visual de prevalidación
- Resume estado de archivo, período y conceptos detectados
- Sirve para evitar la sensación de caja negra

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar resumen de validación previa
- [ ] Incluir:
  - archivo cargado
  - registros detectados
  - conceptos detectados
  - período objetivo
- [ ] Preparar estado vacío y validado
- [ ] Commit sugerido: `feat(ui): crear resumen de validacion previa`

---

## Feature 5.4 — Pantalla de setup de corrida

**Objetivo:** implementar la primera pantalla funcional del MVP: configurar y lanzar una reconciliación.

---

### Card 5.4.1 — Diseñar estructura de la pantalla `New Reconciliation Run`

**Descripción:** esta card define la anatomía general de la pantalla principal de setup.

**Criterio de aceptación:**

- La pantalla tiene estructura clara y jerarquía legible
- El flujo visual conduce naturalmente hacia la acción principal
- La página comunica rápidamente qué hacer

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar secciones principales:
  - header de pantalla
  - selector de período
  - upload payroll
  - expected totals
  - validación previa
  - CTA principal
- [ ] Definir layout desktop-first
- [ ] Evitar wizard largo o navegación fragmentada
- [ ] Commit sugerido: `docs(ui): diseñar estructura de pantalla New Reconciliation Run`

---

### Card 5.4.2 — Implementar selector de período

**Descripción:** el período es uno de los parámetros mínimos de la corrida y debe ser visible desde el inicio.

**Criterio de aceptación:**

- Existe control de período visible
- El valor por defecto del MVP está precompletado
- El componente es simple y consistente con el producto

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Implementar selector o input controlado para período
- [ ] Precompletar con `2026-03`
- [ ] Validar formato esperado
- [ ] Commit sugerido: `feat(ui): implementar selector de periodo del setup`

---

### Card 5.4.3 — Implementar bloque de carga de `payroll.csv`

**Descripción:** conectar visual y funcionalmente la carga del archivo principal de la corrida.

**Criterio de aceptación:**

- El usuario puede cargar `payroll.csv`
- La UI muestra feedback del upload
- El archivo queda asociado a la run en backend

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Integrar `UploadBox` con `POST /runs/{run_id}/upload`
- [ ] Manejar loading, éxito y error
- [ ] Mostrar metadata mínima del archivo cargado
- [ ] Commit sugerido: `feat(ui): conectar carga de payroll en pantalla setup`

---

### Card 5.4.4 — Implementar bloque de carga o preview de expected totals

**Descripción:** el usuario debe poder ver o cargar la referencia esperada sin fricción excesiva.

**Criterio de aceptación:**

- Se pueden mostrar expected totals precargados o cargados
- El bloque es coherente con el resto del setup
- La experiencia no obliga al usuario a navegar fuera del flujo principal

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Integrar preview de expected totals con datos del backend o archivos locales
- [ ] Permitir carga si el diseño final lo requiere
- [ ] Mostrar estados vacío, loading y cargado
- [ ] Commit sugerido: `feat(ui): implementar bloque de expected totals en setup`

---

### Card 5.4.5 — Implementar bloque de parámetros mínimos de corrida

**Descripción:** el MVP no necesita settings complejos, pero sí puede exponer algunos parámetros simples sin generar fricción.

**Criterio de aceptación:**

- Existen parámetros mínimos visibles
- Los parámetros no abruman al usuario
- El formulario mantiene foco en la ejecución

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Evaluar inclusión de:
  - `legal_entity_scope` opcional
  - `tolerance_profile` opcional
  - `include_exceptions_analysis` activado por default
- [ ] Implementar solo los parámetros que sumen realmente al MVP
- [ ] Evitar settings avanzados o ruido visual
- [ ] Commit sugerido: `feat(ui): implementar parametros minimos de corrida`

---

### Card 5.4.6 — Implementar bloque de validación previa

**Descripción:** la pantalla debe dejar visible si el sistema está listo para correr la conciliación o si todavía falta algo.

**Criterio de aceptación:**

- El usuario ve el estado de preparación de la corrida
- El sistema comunica qué está listo y qué falta
- El bloque mejora confianza sin generar complejidad

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Integrar `RunValidationSummary` con estado real de la run
- [ ] Mostrar checklist o resumen de readiness
- [ ] Deshabilitar ejecución si faltan condiciones críticas
- [ ] Commit sugerido: `feat(ui): implementar bloque de validacion previa real`

---

### Card 5.4.7 — Implementar CTA principal `Run Reconciliation`

**Descripción:** el botón principal de la pantalla debe ser el foco natural y disparar la ejecución real de la run.

**Criterio de aceptación:**

- Existe CTA principal claro y visible
- El botón ejecuta la corrida real
- La UI maneja loading y errores de forma clara

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Implementar botón principal destacado
- [ ] Integrarlo con `POST /runs/{run_id}/execute`
- [ ] Mostrar estado de ejecución
- [ ] Manejar éxito, error y bloqueo por precondiciones
- [ ] Commit sugerido: `feat(ui): conectar CTA Run Reconciliation`

---

## Feature 5.5 — Estado local, integración API y lifecycle del setup

**Objetivo:** organizar el comportamiento del setup como una experiencia real y no como una pantalla estática.

---

### Card 5.5.1 — Implementar creación automática o guiada de run desde UI

**Descripción:** la pantalla necesita un mecanismo claro para asegurarse de que existe una run antes de empezar a cargar archivos y parámetros.

**Criterio de aceptación:**

- La UI crea o recupera una run activa de setup
- El usuario no tiene que lidiar con IDs ni estados técnicos
- El flujo es natural desde el primer render

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Decidir si la run se crea al entrar o al primer input
- [ ] Integrar `POST /runs`
- [ ] Persistir `run_id` en estado local del flujo
- [ ] Commit sugerido: `feat(ui): implementar lifecycle de creacion de run`

---

### Card 5.5.2 — Implementar capa de fetch/state para setup

**Descripción:** el flujo necesita una estrategia de state y fetch consistente para conectar formulario, uploads y prevalidación.

**Criterio de aceptación:**

- Existe patrón claro de manejo de estado y requests
- Los componentes del setup comparten estado sin fragilidad
- La solución es reusable para épicas UI siguientes

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir estrategia de fetch:
  - hooks propios
  - librería ligera
  - server/client components según convenga
- [ ] Centralizar estado de la run actual
- [ ] Manejar loading y errores de manera consistente
- [ ] Commit sugerido: `feat(ui): implementar estado y fetch del flujo setup`

---

### Card 5.5.3 — Implementar feedback de éxito, error y loading

**Descripción:** la pantalla debe responder visualmente a acciones del usuario sin dejar dudas sobre qué está pasando.

**Criterio de aceptación:**

- Existe feedback claro para uploads, creación de run y ejecución
- Loading, éxito y error se expresan de forma sobria y útil
- El usuario nunca queda en un estado ambiguo

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Diseñar patrón de feedback global o local
- [ ] Implementar mensajes de error útiles
- [ ] Implementar estados de loading sobrios
- [ ] Commit sugerido: `feat(ui): implementar feedback de loading y errores`

---

## Feature 5.6 — Guardrails de experiencia del setup

**Objetivo:** asegurar que la primera pantalla mantenga foco, simpleza y tono consistente con el producto.

---

### Card 5.6.1 — Definir qué NO entra en la pantalla de setup

**Descripción:** para que la pantalla funcione bien, conviene dejar explícito qué se excluye del MVP.

**Criterio de aceptación:**

- Existe una lista explícita de exclusiones del setup
- La pantalla evita scope creep visual y funcional
- Queda protegido el foco de la experiencia

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Dejar fuera:
  - wizard largo
  - configuración avanzada de reglas
  - edición compleja de expected totals
  - múltiples tabs
  - parámetros técnicos visibles
- [ ] Documentar racional de cada exclusión
- [ ] Commit sugerido: `docs(ui): definir exclusiones del setup flow`

---

### Card 5.6.2 — Validar tono y framing de la pantalla

**Descripción:** la pantalla debe sentirse como una herramienta seria de trabajo, no como una demo técnica improvisada.

**Criterio de aceptación:**

- El lenguaje de la pantalla es profesional y claro
- Los textos de ayuda son útiles y no verbosos
- El framing es consistente con usuario contable/financiero

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Revisar títulos, labels y helper text
- [ ] Evitar jerga técnica innecesaria
- [ ] Alinear tono con “seriedad enterprise sobria”
- [ ] Commit sugerido: `docs(ui): validar tono y framing del setup`

---

## Feature 5.7 — Validación integral del flujo de setup

**Objetivo:** verificar que la primera experiencia del producto funcione end-to-end y esté lista para soportar las pantallas siguientes.

---

### Card 5.7.1 — Validar flujo completo de setup en local

**Descripción:** prueba integral de la pantalla de setup conectada al backend real.

**Criterio de aceptación:**

- Se puede crear una run desde UI
- Se pueden cargar archivos
- Se puede ejecutar la corrida desde la pantalla
- El flujo no requiere intervención manual extra

**Complejidad:** Alta

**Estado:** PENDIENTE

**Tasks:**

- [ ] Entrar a la app y crear run
- [ ] Cargar payroll
- [ ] Cargar o visualizar expected totals
- [ ] Validar resumen previo
- [ ] Ejecutar run desde la UI
- [ ] Commit sugerido: `test(ui): validar flujo completo de setup en local`

---

### Card 5.7.2 — Validar base reusable para épicas UI siguientes

**Descripción:** esta prueba verifica que la base construida no sea solo suficiente para setup, sino también útil para Summary, Concept Analysis y Drill-down.

**Criterio de aceptación:**

- Layout y componentes base son reutilizables
- No hay acoplamientos innecesarios a la pantalla de setup
- La epic deja una base sólida para pantallas siguientes

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Revisar reusabilidad de layout, header y componentes base
- [ ] Revisar contratos de datos del setup
- [ ] Documentar puntos de extensión para próximas épicas
- [ ] Commit sugerido: `test(ui): validar base reusable de UI para siguientes epicas`

---

## Resumen de commits esperados en EPIC 05

- `docs(ui): definir principios visuales del MVP`
- `docs(ui): definir paleta base y semantica del MVP`
- `docs(ui): definir tipografia y jerarquia base`
- `feat(ui): crear layout base del producto`
- `feat(ui): implementar header base del MVP`
- `feat(ui): crear estado inicial del producto`
- `feat(ui): crear componente RunSetupForm`
- `feat(ui): crear componente UploadBox`
- `feat(ui): crear preview de expected totals`
- `feat(ui): crear resumen de validacion previa`
- `docs(ui): diseñar estructura de pantalla New Reconciliation Run`
- `feat(ui): implementar selector de periodo del setup`
- `feat(ui): conectar carga de payroll en pantalla setup`
- `feat(ui): implementar bloque de expected totals en setup`
- `feat(ui): implementar parametros minimos de corrida`
- `feat(ui): implementar bloque de validacion previa real`
- `feat(ui): conectar CTA Run Reconciliation`
- `feat(ui): implementar lifecycle de creacion de run`
- `feat(ui): implementar estado y fetch del flujo setup`
- `feat(ui): implementar feedback de loading y errores`
- `docs(ui): definir exclusiones del setup flow`
- `docs(ui): validar tono y framing del setup`
- `test(ui): validar flujo completo de setup en local`
- `test(ui): validar base reusable de UI para siguientes epicas`

---

## Notas técnicas

### Regla central de esta epic

La pantalla de setup debe hacer sentir que el sistema:

- entiende el problema
- necesita pocos insumos
- está listo para trabajar

No debe sentirse como:

- formulario legacy
- wizard largo
- dashboard genérico
- prototipo técnico

### Decisión UX del MVP

Esta epic prioriza:

- una sola pantalla clara
- pocos parámetros
- fuerte visibilidad del input
- CTA único y evidente

La complejidad de navegación vendrá, si hace falta, más adelante. No ahora.

### Qué no entra en esta epic

- Summary UI completa
- Concept Analysis UI
- Drill-down operativo
- exportables
- multi-run dashboard
- historial sofisticado
- auth compleja en frontend

Todo eso se apoya en esta base, pero no se construye todavía acá.
