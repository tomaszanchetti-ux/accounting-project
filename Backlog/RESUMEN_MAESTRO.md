# Resumen Maestro del Backlog

> Documento de control maestro del backlog del proyecto **Accounting Reconciliation MVP**.
> Sirve para medir avance entre sesiones, entender tamaño relativo de cada épica y decidir el orden de implementación real.

---

## 1. Propósito

Este documento existe para responder, en cualquier momento:

- dónde estamos parados
- cuánto backlog real tiene el proyecto
- qué épica conviene ejecutar después
- qué volumen de trabajo tiene cada bloque

No reemplaza a las épicas ni al workflow.  
Los sintetiza para seguimiento.

---

## 2. Conteo total del backlog

Estado actual del backlog documentado:

- `10 épicas`
- `85 features`
- `245 cards`
- `1039 tasks operativas`

### Nota sobre el conteo

Las `tasks operativas` contadas acá corresponden a los checklists dentro de cada `Card`, no a criterios de aceptación generales de las épicas.

---

## 3. Conteo por épica

| Epic | Archivo | Features | Cards | Tasks |
| --- | --- | ---: | ---: | ---: |
| EPIC 00 | `EPIC_00_Setup_Tecnico_MVP.md` | 7 | 17 | 77 |
| EPIC 01 | `EPIC_01_Data_Foundation_Dataset_Demo.md` | 8 | 21 | 91 |
| EPIC 02 | `EPIC_02_Reconciliation_Engine_Core.md` | 9 | 26 | 123 |
| EPIC 03 | `EPIC_03_Exception_Detection_Explanation.md` | 10 | 29 | 127 |
| EPIC 04 | `EPIC_04_Runs_API_Persistence_Traceability.md` | 10 | 34 | 144 |
| EPIC 05 | `EPIC_05_UI_Foundation_Setup_Flow.md` | 7 | 24 | 99 |
| EPIC 06 | `EPIC_06_Summary_Concept_Analysis_UI.md` | 10 | 31 | 125 |
| EPIC 07 | `EPIC_07_Drilldown_Exports_Traceability.md` | 10 | 29 | 112 |
| EPIC 08 | `EPIC_08_Demo_Seed_Narrative_Commercial_Flow.md` | 8 | 20 | 74 |
| EPIC 09 | `EPIC_09_Hardening_QA_Demo_Ready.md` | 6 | 14 | 67 |

---

## 4. Lectura del tamaño relativo

### Épicas más pesadas

Por volumen de `cards + tasks`, las más pesadas del proyecto son:

1. `EPIC 04 — Runs API, Persistence & Traceability`
2. `EPIC 03 — Exception Detection & Explanation Layer`
3. `EPIC 06 — Summary, Concept Analysis & Explanation UI`
4. `EPIC 02 — Reconciliation Engine Core`
5. `EPIC 07 — Drill-down, Exports & Demo Traceability`

### Qué significa esto

Estas épicas son las que más probablemente:

- requieran varias sesiones
- acumulen más riesgo técnico
- necesiten más QA interno
- merezcan más atención a la granularidad card por card

---

## 5. Orden recomendado de implementación real

El orden base de implementación sigue el backlog:

1. `EPIC 00 — Setup Técnico del MVP`
2. `EPIC 01 — Data Foundation & Dataset Demo`
3. `EPIC 02 — Reconciliation Engine Core`
4. `EPIC 03 — Exception Detection & Explanation Layer`
5. `EPIC 04 — Runs API, Persistence & Traceability`
6. `EPIC 05 — UI Foundation & Setup Flow`
7. `EPIC 06 — Summary, Concept Analysis & Explanation UI`
8. `EPIC 07 — Drill-down, Exports & Demo Traceability`
9. `EPIC 08 — Demo Seed, Narrative & Commercial Flow`
10. `EPIC 09 — Hardening, QA & Demo-Ready Closure`

### Regla práctica

No empezar UI fuerte antes de tener:

- datos demo razonablemente cerrados
- motor funcionando
- capa de runs persistida

Eso protege muchísimo la velocidad real del proyecto.

---

## 6. Fases naturales del build

Aunque el backlog esté numerado por épica, en la práctica el proyecto puede entenderse en estas 5 fases:

### Fase 1 — Base técnica y datos

- `EPIC 00`
- `EPIC 01`

Objetivo:

- dejar stack listo
- definir y materializar el dataset demo

### Fase 2 — Núcleo lógico del producto

- `EPIC 02`
- `EPIC 03`

Objetivo:

- construir el motor de conciliación
- construir la explicación rule-based

### Fase 3 — Producto operativo

- `EPIC 04`

Objetivo:

- convertir cálculo + explicación en runs persistidas y APIs reales

### Fase 4 — Producto visible

- `EPIC 05`
- `EPIC 06`
- `EPIC 07`

Objetivo:

- construir setup
- construir summary
- construir concept analysis
- construir drill-down y exports

### Fase 5 — Demo y cierre

- `EPIC 08`
- `EPIC 09`

Objetivo:

- dejar demo sembrada y narrativamente fuerte
- cerrar QA, hardening y demo-ready

---

## 7. Cómo usar este documento en cada sesión

Al comenzar una sesión:

1. leer `AGENTS.md`
2. leer `Backlog/INDICE.md`
3. leer `Backlog/WORKFLOW_EJECUCION.md`
4. leer este `RESUMEN_MAESTRO.md`
5. leer la última `ARD_WS...` disponible
6. elegir la próxima `Card` a ejecutar

Al cerrar una sesión:

1. actualizar si hace falta este resumen maestro
2. actualizar `AGENTS.md`
3. crear un documento `ARD_WS[N]_DDMMAAAA.md`
4. dejar explícito qué quedó hecho y cuál es la próxima card recomendada

---

## 8. Estado de avance

### Estado actual

- `Backlog documentado: 100%`
- `Implementación real: iniciada`

| Epic | Estado Docs | Estado Implementación | Cards completadas | Observaciones |
| --- | --- | --- | --- | --- |
| EPIC 00 | ✅ | COMPLETADA | 17 / 17 | Setup tecnico, deploy frontend y estrategia de backend definidos |
| EPIC 01 | ✅ | COMPLETADA | 21 / 21 | Dataset demo definido y seed inicial materializado en `data/demo_seed/`; siguiente paso recomendado: `EPIC 02 / Card 2.1.1` |
| EPIC 02 | ✅ | COMPLETADA | 26 / 26 | Motor validado end-to-end con dataset demo; siguiente paso recomendado: `EPIC 03 / Card 3.1.1` |
| EPIC 03 | ✅ | COMPLETADA | 29 / 29 | Capa explicativa completa con deteccion, impacto, ranking, narrativa y validacion wow cerrada; siguiente paso recomendado: `EPIC 04 / Card 4.1.1` |
| EPIC 04 | ✅ | COMPLETADA | 34 / 34 | Vertical slice operativo implementado con schema SQL, repositorios, `execute_run`, endpoints principales, upload multipart, payloads UI, timeline minima y tests de trazabilidad; siguiente paso recomendado: preparar `EPIC 05` |
| EPIC 05 | ✅ | COMPLETADA | 24 / 24 | Base visual, setup flow, lifecycle de run, uploads, validación previa, smoke visual/manual y merge a `main` completados; siguiente paso recomendado: `EPIC 06 / Card 6.1.1` |
| EPIC 06 | ✅ | COMPLETADA | 31 / 31 | Summary Screen real, Concept Analysis dedicada, loading/error/empty states, CTA a drill-down y blueprint funcional implementados; siguiente paso recomendado: `EPIC 07 / Card 7.1.1` |

### Cómo registrar avance

Se recomienda que en futuras sesiones este documento incorpore una tabla de avance como:

| Epic | Estado Docs | Estado Implementación | Cards completadas | Observaciones |
| --- | --- | --- | --- | --- |
| EPIC 00 | ✅ | PENDIENTE | 0 / 17 | — |

Cuando empiece la implementación real, conviene mantener este cuadro actualizado.

---

## 9. Criterio de salud del proyecto

El proyecto va sano si, sesión a sesión:

- se avanza card por card
- no se mezclan muchas épicas a la vez
- cada card cierra con validación local
- cada épica llega a QA antes de mergear
- la demo final se fortalece, no se dispersa

El proyecto empieza a degradarse si:

- se saltean dependencias
- se construye mucha UI sobre backend inestable
- se acumulan cards “casi terminadas”
- se pierde trazabilidad entre sesiones

---

## 10. Próximo uso recomendado

Con el estado actual del proyecto, el siguiente paso lógico es:

1. abrir branch y contexto de `EPIC 07`
2. construir Drill-down UI, exports y continuidad de trazabilidad sobre la navegación ya preparada en `EPIC 06`
3. avanzar card por card hasta cerrar la capa operativa del demo

Este documento queda como tablero maestro para medir si ese avance está ocurriendo de forma ordenada.
