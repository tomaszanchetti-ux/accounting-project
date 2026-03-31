# EPIC 09 — Hardening, QA & Demo-Ready Closure

## Contexto y objetivo

Esta epic cierra el backlog operativo del MVP. No está pensada para agregar capacidades nuevas de producto, sino para asegurar que todo lo construido hasta ahora:

- funciona de forma consistente
- se ve lo suficientemente sólido
- resiste una demo real
- no se cae por bordes previsibles

En otras palabras: esta epic no construye “más producto”. Construye **confianza final**.

Después de las épicas anteriores, el sistema ya debería tener:

- stack operativo
- dataset demo
- motor de conciliación
- explanation layer
- runs y persistencia
- setup flow
- summary, concept analysis y drill-down
- exportables
- narrativa comercial

Lo que falta ahora es certificar que todo eso realmente está en estado **demo-ready**, con la calidad mínima visual, funcional y operativa para mostrarse sin ansiedad y sin improvisación defensiva.

La tesis de esta epic es:

> **Un MVP vendible no necesita ser perfecto, pero sí necesita sentirse consistente, estable y bajo control.**

Al terminar esta epic, el proyecto debe tener:

- validación funcional integral
- resolución de bordes visibles
- polish visual mínimo en pantallas clave
- documentación clara de riesgos residuales
- checklist final de “ready to show”

## Dominio(s) involucrado(s)

Epic transversal de cierre. No introduce un dominio funcional nuevo.

## Dependencias

- **EPIC 08** completada o suficientemente avanzada
- Idealmente todas las épicas anteriores implementadas al menos en su núcleo

## Criterio de aceptación de la Epic completa

- [ ] El flujo principal del MVP funciona end-to-end sin bloqueos
- [ ] Las pantallas clave tienen calidad visual mínima consistente
- [ ] Los casos wow funcionan correctamente en demo
- [ ] Los errores y bordes previsibles están manejados razonablemente
- [ ] Los exportables mínimos funcionan
- [ ] Existe una lista explícita de riesgos residuales aceptados
- [ ] Existe una definición formal de `demo-ready`

## Estado: PENDIENTE

---

## Feature 9.1 — Validación funcional integral del MVP

**Objetivo:** comprobar que el producto funciona como un todo y no solo como piezas aisladas.

---

### Card 9.1.1 — Validar flujo completo `Setup -> Run -> Summary -> Concept -> Drill-down -> Export`

**Descripción:** esta es la prueba funcional principal del MVP. Verifica que el recorrido natural del usuario realmente existe y puede sostener una demo.

**Criterio de aceptación:**

- El flujo principal funciona completo
- No hay bloqueos funcionales graves
- El sistema mantiene consistencia entre pantallas y datos

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Crear o resetear entorno demo
- [x] Ejecutar setup de una run
- [x] Correr la conciliación
- [x] Revisar summary
- [x] Abrir concept analysis
- [x] Abrir drill-down
- [x] Descargar exportables
- [x] Registrar issues detectados
- [x] Commit sugerido: `test(qa): validar flujo funcional integral del MVP`

**Resultado de ejecucion:**

- validacion end-to-end documentada en `docs/EPIC09_FUNCTIONAL_FLOW_QA.md`
- run QA recreada y validada: `ee9e80e7-5fe0-4a3e-a8ef-7f98eb15cf27`
- sin bloqueos funcionales graves detectados en el flujo principal

---

### Card 9.1.2 — Validar consistencia entre capa lógica, persistencia y UI

**Descripción:** asegurar que no existan contradicciones entre lo que calcula el motor, lo que se persiste y lo que se muestra.

**Criterio de aceptación:**

- Los números coinciden entre capas
- No hay drift visible entre payloads y UI
- Las explicaciones se sostienen sobre la persistencia real

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Verificar consistency de summary vs results
- [x] Verificar consistency de concept analysis vs exceptions persistidas
- [x] Verificar consistency de drill-down vs staging lines
- [x] Documentar y corregir desviaciones
- [ ] Commit sugerido: `test(qa): validar consistencia entre motor persistencia y UI`

**Resultado de ejecucion:**

- validacion documentada en `docs/EPIC09_CONSISTENCY_QA.md`
- `21 / 21` checks de consistencia OK sobre la run `ee9e80e7-5fe0-4a3e-a8ef-7f98eb15cf27`
- sin drift detectado entre motor, persistencia, API y UI

---

## Feature 9.2 — Hardening de casos borde y errores previsibles

**Objetivo:** reforzar los bordes más probables de la demo para que el sistema falle con claridad y no de forma caótica.

---

### Card 9.2.1 — Revisar errores de carga y ejecución de runs

**Descripción:** comprobar que los errores de input, upload o ejecución se expresan de forma clara y consistente.

**Criterio de aceptación:**

- Los errores previsibles tienen feedback claro
- La UI no deja al usuario en estados ambiguos
- La run no queda inconsistente ante errores comunes

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Probar archivo faltante o incorrecto
- [x] Probar expected totals faltante o inconsistente
- [x] Probar fallo de ejecución controlado
- [x] Revisar mensajes y estados resultantes
- [ ] Commit sugerido: `test(qa): revisar errores previsibles de runs`

**Resultado de ejecucion:**

- hardening aplicado en setup para no tratar `INVALID_INPUT` ni `FAILED` como éxito
- feedback visible ahora usa `run.error_message` cuando corresponde
- tests agregados para:
  - missing required files
  - expected totals sin período objetivo
  - fallo técnico controlado del motor
- evidencia documentada en `docs/EPIC09_RUN_ERRORS_AND_EXPORTS_QA.md`

---

### Card 9.2.2 — Revisar empty states y not found states

**Descripción:** confirmar que los estados vacíos y casos borde de navegación se sostienen visual y funcionalmente.

**Criterio de aceptación:**

- Empty states útiles y sobrios
- Not found states comprensibles
- La app mantiene continuidad aun cuando faltan datos

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Revisar empty states de summary
- [x] Revisar not found de concept analysis
- [x] Revisar empty/filter empty de drill-down
- [x] Ajustar textos y jerarquía visual si hace falta
- [ ] Commit sugerido: `test(qa): revisar empty states y not found states`

**Resultado de ejecucion:**

- summary ahora distingue `run not found` de error general de carga
- concept analysis y drill-down ganaron recuperación explícita con CTA visibles
- se creó un patrón visual común de estado para mantener continuidad de navegación
- evidencia documentada en `docs/EPIC09_RUN_ERRORS_AND_EXPORTS_QA.md`

---

### Card 9.2.3 — Revisar resiliencia básica de exportables

**Descripción:** verificar que las descargas mínimas no fallen en escenarios razonables del demo.

**Criterio de aceptación:**

- Summary export funciona de forma consistente
- Detail export funciona de forma consistente
- Fallos de export se manejan claramente si ocurren

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Descargar summary export múltiples veces
- [x] Descargar detail export desde concepto wow
- [x] Revisar naming, contenido y consistencia
- [x] Revisar feedback de fallo si se fuerza error
- [ ] Commit sugerido: `test(qa): revisar resiliencia basica de exportables`

**Resultado de ejecucion:**

- exportables pasaron de links directos a descarga controlada con feedback inline
- el usuario ahora ve estado de export y error de descarga en el mismo contexto
- se preserva el filename real informado por `Content-Disposition`
- evidencia documentada en `docs/EPIC09_RUN_ERRORS_AND_EXPORTS_QA.md`

---

## Feature 9.3 — Polish visual mínimo del MVP

**Objetivo:** resolver inconsistencias visuales y detalles de terminación que afecten la percepción de producto.

---

### Card 9.3.1 — Revisar consistencia visual entre pantallas clave

**Descripción:** asegurar que setup, summary, concept analysis y drill-down se sientan parte del mismo producto.

**Criterio de aceptación:**

- Las pantallas comparten tono y gramática visual
- No hay inconsistencias fuertes de spacing, header o componentes
- El producto se siente cohesivo

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Revisar headers, spacing y jerarquías
- [x] Revisar uso de badges, cards y tablas
- [x] Unificar patrones donde haga falta
- [ ] Commit sugerido: `chore(ui): pulir consistencia visual entre pantallas clave`

**Resultado de ejecucion:**

- setup, summary, concept analysis y drill-down ahora comparten un panel contextual consistente en el header
- se unificaron densidad, borde, sombra y disposición de acciones en pantallas clave
- el bloque de contexto ahora mantiene una gramática visual estable entre estados de navegación principales
- durante la pasada se normalizaron además algunos microtextos visibles del flujo

---

### Card 9.3.2 — Pulir copy, labels y microtextos

**Descripción:** un MVP puede perder credibilidad por textos torpes o inconsistentes. Esta card limpia esa capa.

**Criterio de aceptación:**

- Los labels son claros y consistentes
- El tono del producto se mantiene uniforme
- No hay microcopys confusos o demasiado técnicos

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Revisar títulos de pantalla
- [x] Revisar labels de botones
- [x] Revisar helper texts, empty states y mensajes de error
- [x] Ajustar terminología para consistencia
- [ ] Commit sugerido: `chore(ui): pulir copy y microtextos del MVP`

**Resultado de ejecucion:**

- se normalizó la gramática entre `open`, `back`, `ready`, `review` y `next step`
- setup, summary, concept analysis y drill-down ahora usan labels más consistentes
- se ajustaron helper texts y fallbacks visibles para evitar mezcla entre `loaded`, `missing`, `pending` y `not available`
- el tono quedó más uniforme y orientado a revisión operativa, no a UI genérica

---

### Card 9.3.3 — Pulir densidad visual y legibilidad de tablas

**Descripción:** confirmar que las tablas principales se pueden leer cómodamente en una demo real proyectada o compartida en pantalla.

**Criterio de aceptación:**

- Las tablas se leen bien en desktop
- No hay densidad excesiva ni columnas mal alineadas
- El foco visual sigue funcionando bajo uso real

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Revisar tabla de conceptos
- [x] Revisar tabla de drill-down
- [x] Ajustar widths, alignment y truncation si hace falta
- [ ] Commit sugerido: `chore(ui): pulir legibilidad de tablas clave`

**Resultado de ejecucion:**

- la tabla de summary ahora usa una distribución de anchos más estable y jerarquía más clara entre concepto, números, explicación y CTA
- la tabla de drill-down redistribuyó ancho hacia columnas de mayor carga semántica como concepto y observación
- se redujo fricción visual con padding, tamaños tipográficos y alineaciones más consistentes para lectura en demo

---

## Feature 9.4 — Validación específica del wow moment

**Objetivo:** certificar que el momento más importante del demo se sostiene con fuerza suficiente.

---

### Card 9.4.1 — Ensayar recorrido wow completo de `MEAL_VOUCHER`

**Descripción:** esta card prueba el clímax narrativo del producto en su secuencia exacta.

**Criterio de aceptación:**

- El wow moment se siente claro y potente
- La secuencia summary -> concept -> drill-down fluye naturalmente
- La evidencia refuerza la explicación

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Abrir summary con rojo visible
- [x] Entrar a `MEAL_VOUCHER`
- [x] Mostrar causas probables
- [x] Abrir drill-down
- [x] Evaluar claridad, timing e impacto
- [ ] Commit sugerido: `test(demo): ensayar wow moment completo de meal voucher`

**Resultado de ejecucion:**

- `MEAL_VOUCHER` sigue apareciendo como caso principal en summary con diff material y status `Unreconciled`
- concept analysis sigue separando claramente `Unmapped Concept`, `Duplicate Record` y `Out-of-Period Record`
- drill-down sigue aterrizando la historia en `519` filas con `14` filas marcadas por excepción visible
- la secuencia mantiene claridad narrativa, timing razonable e impacto comercial
- evidencia documentada en `docs/EPIC09_WOW_MOMENT_QA.md`

---

### Card 9.4.2 — Verificar casos complementarios `CHILDCARE`, `OVERTIME`, `TRANSPORT`

**Descripción:** además del wow principal, conviene asegurar que los demás conceptos soporte de la narrativa también se sostienen.

**Criterio de aceptación:**

- Los casos complementarios se entienden rápido
- Cada uno cumple su rol narrativo específico
- No compiten innecesariamente con el wow principal

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Validar `CHILDCARE` como caso de población faltante
- [x] Validar `OVERTIME` como caso de outlier
- [x] Validar `TRANSPORT` como caso amarillo
- [x] Ajustar si alguno pierde claridad o protagonismo correcto
- [ ] Commit sugerido: `test(demo): verificar casos complementarios del walkthrough`

**Resultado de ejecucion:**

- `CHILDCARE` sigue defendiendo la narrativa de población faltante
- `OVERTIME` sigue funcionando como caso rápido de outlier dominante
- `TRANSPORT` sigue actuando como caso sobrio de tolerancia sin competir con el wow principal
- no se detectó que alguno de los tres casos compita o confunda respecto a `MEAL_VOUCHER`
- evidencia documentada en `docs/EPIC09_SUPPORTING_CASES_QA.md`

---

## Feature 9.5 — Riesgos residuales y límites conscientes del MVP

**Objetivo:** dejar explicitado qué riesgos o limitaciones se aceptan para esta versión.

---

### Card 9.5.1 — Documentar riesgos funcionales residuales

**Descripción:** no todo edge case va a quedar cubierto en MVP. Esta card documenta lo que conscientemente se acepta.

**Criterio de aceptación:**

- Existe lista explícita de riesgos residuales
- Los riesgos están descritos con honestidad y foco
- El equipo sabe qué no prometer todavía

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Documentar riesgos como:
  - explicación limitada a reglas explícitas
  - dataset controlado
  - ejecución sincrónica
  - exportables básicos
- [x] Separar claramente límites del MVP de bugs reales
- [ ] Commit sugerido: `docs(qa): documentar riesgos funcionales residuales`

**Resultado de ejecucion:**

- se documentaron riesgos funcionales residuales con foco en expectativa correcta de demo
- quedaron separados de bugs reales y de bloqueos críticos
- evidencia documentada en `docs/EPIC09_RESIDUAL_RISKS_AND_LIMITS.md`

---

### Card 9.5.2 — Documentar límites UX y operativos aceptados

**Descripción:** dejar explícito qué no se pulió más allá del mínimo necesario para demo.

**Criterio de aceptación:**

- Existe lista de límites UX/operativos aceptados
- El equipo puede defender esos límites sin improvisar
- Se protege al MVP de expectativas incorrectas

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Documentar límites como:
  - desktop-first
  - sin auth enterprise
  - sin historial sofisticado
  - sin configuración avanzada por usuario
- [x] Confirmar que los límites no rompen el objetivo demo
- [ ] Commit sugerido: `docs(qa): documentar limites UX y operativos del MVP`

**Resultado de ejecucion:**

- se documentaron límites UX y operativos aceptados para no sobredimensionar el alcance del MVP
- los límites quedaron defendibles desde una lógica de demo vendible y control narrativo
- evidencia documentada en `docs/EPIC09_RESIDUAL_RISKS_AND_LIMITS.md`

---

## Feature 9.6 — Definición formal de `demo-ready`

**Objetivo:** cerrar con un criterio explícito de cuándo el MVP puede considerarse listo para mostrarse.

---

### Card 9.6.1 — Definir checklist final de `demo-ready`

**Descripción:** convertir la noción de “ya está listo” en una lista concreta y verificable.

**Criterio de aceptación:**

- Existe checklist final de demo-ready
- El checklist es breve, accionable y suficiente
- Permite decidir si mostrar o no el producto

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Incluir checks de:
  - flujo principal
  - wow cases
  - exportables
  - entorno demo
  - calidad visual mínima
  - narrativa preparada
- [x] Documentar cómo usar el checklist antes de una reunión
- [ ] Commit sugerido: `docs(qa): definir checklist final demo-ready`

**Resultado de ejecucion:**

- se definió un checklist final breve y accionable para decidir si mostrar o no el producto
- el checklist quedó organizado por entorno, flujo principal, wow cases, exportables, calidad visual y narrativa
- también quedó documentado cómo usarlo `15-30` minutos antes de una reunión
- evidencia documentada en `docs/EPIC09_DEMO_READY_CHECKLIST.md`

---

### Card 9.6.2 — Evaluar estado final del MVP contra checklist

**Descripción:** aplicar formalmente el checklist al producto real y dejar una conclusión explícita.

**Criterio de aceptación:**

- Existe evaluación final documentada
- Se concluye si el MVP está `demo-ready` o no
- Si no lo está, quedan claros los gaps

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Ejecutar checklist final
- [x] Marcar cumplido / no cumplido
- [x] Documentar gaps residuales si existen
- [x] Emitir veredicto final del estado del MVP
- [ ] Commit sugerido: `docs(qa): evaluar estado final del MVP contra checklist`

**Resultado de ejecucion:**

- se aplicó formalmente el checklist final al estado real del producto
- el MVP quedó evaluado como funcionalmente demo-ready para el alcance previsto
- se confirmó que la redirección previa a `/login` no pertenecía a este repo sino a otra app local ocupando `3000`
- el frontend real del proyecto quedó validado correctamente en un puerto libre y el cierre de `demo-ready` se sostuvo
- evidencia documentada en `docs/EPIC09_FINAL_DEMO_READY_EVALUATION.md`

---

## Resumen de commits esperados en EPIC 09

- `test(qa): validar flujo funcional integral del MVP`
- `test(qa): validar consistencia entre motor persistencia y UI`
- `test(qa): revisar errores previsibles de runs`
- `test(qa): revisar empty states y not found states`
- `test(qa): revisar resiliencia basica de exportables`
- `chore(ui): pulir consistencia visual entre pantallas clave`
- `chore(ui): pulir copy y microtextos del MVP`
- `chore(ui): pulir legibilidad de tablas clave`
- `test(demo): ensayar wow moment completo de meal voucher`
- `test(demo): verificar casos complementarios del walkthrough`
- `docs(qa): documentar riesgos funcionales residuales`
- `docs(qa): documentar limites UX y operativos del MVP`
- `docs(qa): definir checklist final demo-ready`
- `docs(qa): evaluar estado final del MVP contra checklist`

---

## Notas técnicas

### Regla central de esta epic

No usar esta epic para meter scope nuevo.

Su responsabilidad es:

- validar
- corregir bordes
- pulir
- decidir si el MVP está listo

No es una “epic comodín” para agregar ideas tardías.

### Criterio de calidad del MVP

El producto no necesita ser perfecto. Sí necesita:

- verse consistente
- sostener su narrativa
- no romperse en el flujo principal
- permitir una demo sin fricción grave

### Qué no entra en esta epic

- nuevas features de negocio
- rediseños grandes de UX
- re-arquitectura técnica
- capacidades enterprise adicionales
- una segunda demo paralela

Esta epic existe para cerrar, no para reabrir.
