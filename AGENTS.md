# AGENTS.md

> Documento madre del proyecto **Accounting Reconciliation MVP**.
> Debe leerse al inicio de cada sesión de trabajo y actualizarse al cierre de cada sesión.

---

## 1. Qué es este proyecto

Este proyecto construye un **MVP vendible** de conciliación entre payroll/RRHH y Contabilidad, con foco en:

- agregación automática
- conciliación contra expected totals
- detección de diferencias
- explicación rule-based de causas probables
- drill-down a registros concretos
- narrativa comercial clara para demo

No se está construyendo una plataforma enterprise final.  
Se está construyendo un **proto-producto creíble, reusable y demostrable**.

---

## 2. Norte del proyecto

Si en algún momento hay dudas sobre una decisión, usar esta pregunta:

> **¿Esto ayuda a que un controller o usuario de Contabilidad entienda por qué no le cierran los números en segundos?**

Si la respuesta es sí, probablemente vamos bien.  
Si la respuesta es no, probablemente nos estamos desviando.

---

## 3. Stack tecnológico del MVP

El stack base del proyecto está cerrado:

- **Frontend:** Next.js
- **Backend:** FastAPI
- **Motor:** Python + pandas + reglas explícitas
- **DB:** Supabase Postgres
- **Storage:** Supabase Storage
- **Deploy:** Vercel + Supabase
- **Explicación:** rule-based + template-based

### Regla importante

No reabrir estas decisiones en cada sesión salvo que exista un motivo fuerte y explícito.

La lógica del stack es:

- costo-eficiente
- rápida de construir
- suficiente para una demo vendible

---

## 4. Documentos que SIEMPRE hay que leer al empezar

Toda sesión debe empezar leyendo, como mínimo:

1. `AGENTS.md`
2. `Backlog/INDICE.md`
3. `Backlog/WORKFLOW_EJECUCION.md`
4. `Backlog/RESUMEN_MAESTRO.md`
5. la última `ARD_WS[N]_DDMMAAAA.md` disponible

Si la sesión toca una epic concreta, además hay que leer el documento de esa epic completo antes de ejecutar trabajo.

## 4.1 Rutina obligatoria al arrancar una WS

Cada vez que se retoma el proyecto, antes de implementar nada, se debe:

1. ubicar el repo local oficial en `/Users/tzanchetti/Documents/Proyectos Claudio/accounting-project`
2. entrar al repo correcto
3. revisar branch actual
4. ejecutar `git pull` para traer cambios remotos
5. leer los documentos obligatorios de contexto
6. hacer un reporte de status inicial:
   - que se hizo
   - que falta
   - proxima epic/card recomendada
   - riesgos o bloqueos
7. recien despues empezar la ejecucion tecnica

La referencia operativa ampliada para esto vive en `docs/WS_WORKFLOW.md`.

---

## 5. Regla de ejecución del proyecto

Este proyecto se ejecuta:

- **épica por épica**
- **card por card**
- **task por task**

La unidad real de trabajo es la **Card**.

### Regla operativa

No se trabaja “por arriba” de una épica.

La secuencia correcta es:

1. leer la epic
2. elegir la próxima card no resuelta
3. ejecutar sus tasks
4. validar en local
5. hacer commit
6. seguir con la próxima card

---

## 6. Branching y git

### Regla principal

Siempre trabajar en **branch por épica**.

Ejemplos:

- `codex/epic-00-setup`
- `codex/epic-01-data-foundation`
- `codex/epic-02-reconciliation-engine`

### Reglas obligatorias

- no trabajar directamente sobre `main`
- ejecutar primero siempre en local
- validar antes de push
- mergear a `main` solo cuando la épica completa pasó QA final en su branch

### Granularidad de commits

Idealmente:

- **1 commit por Card cerrada**

---

## 7. Validación mínima por card

Ninguna card debería considerarse terminada si no existe alguna validación real.

Validaciones válidas:

- prueba manual local
- test automatizado
- validación visual
- validación de endpoint/payload
- validación de dataset o export

Si no pudo validarse, debe dejarse explícito.

---

## 8. Estructura del backlog

El backlog vigente está compuesto por:

- `10 épicas`
- `85 features`
- `245 cards`
- `1039 tasks operativas`

El detalle maestro y orden de ejecución están en:

- `Backlog/INDICE.md`
- `Backlog/RESUMEN_MAESTRO.md`

---

## 9. Regla de cierre de sesión

Cada vez que termina una sesión de trabajo, se deben hacer **dos cosas obligatorias**:

### A. Actualizar `AGENTS.md` si cambió alguna regla madre del proyecto

Por ejemplo:

- cambio de workflow
- cambio de stack
- cambio de orden del backlog
- cambio de criterio de ejecución

### B. Crear un documento de sesión con formato obligatorio

Formato:

`ARD_WS[N]_DDMMAAAA.md`

Ejemplo:

`ARD_WS1_28032026.md`

### Ese documento de sesión debe dejar claro:

- qué se hizo
- qué documentos se crearon o actualizaron
- en qué estado quedó el proyecto
- qué falta hacer
- cuál es la próxima epic/card recomendada

---

## 10. Qué debe contener cada `ARD_WS...`

Toda nota de cierre de sesión debería incluir como mínimo:

- contexto de la sesión
- objetivo trabajado
- documentos creados o actualizados
- decisiones tomadas
- estado actual del backlog o implementación
- próximo paso sugerido
- riesgos, bloqueos o notas para la siguiente sesión

La idea no es escribir un diario largo.  
La idea es dejar un **handoff útil para el yo futuro o para otro agente**.

---

## 11. Estado actual del proyecto

### Backlog

- backlog completo documentado
- workflow de ejecución definido
- resumen maestro creado

### Implementación

- aún no comenzó la implementación técnica del producto
- el siguiente paso lógico es empezar con `EPIC 00`

---

## 12. Prioridad actual

La prioridad actual del proyecto es:

> **pasar de documentación estructurada a implementación real, empezando por `EPIC 00` y siguiendo el workflow de ejecución definido.**

---

## 13. Regla final

Si hay poco tiempo o duda sobre cómo proceder:

1. leer este documento
2. leer la última `ARD_WS...`
3. elegir una card concreta
4. implementarla con cuidado
5. validar en local
6. dejar commit y cierre de sesión claro

Ese es el comportamiento esperado para trabajar bien este proyecto.
