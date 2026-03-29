# Fase G — Backlog Operativo del MVP

> Índice maestro de épicas para el proyecto **Accounting Reconciliation MVP**.
> Este backlog traduce la definición conceptual del producto a una estructura ejecutable por agente, con dependencia explícita entre épicas y foco en time-to-demo.

---

## Principios operativos del backlog

- La prioridad del proyecto es llegar a una **demo vendible, creíble y navegable** antes que construir una arquitectura enterprise final.
- Cada épica debe poder ejecutarse de forma **granular**, bajando a `Feature -> Card -> Tasks`.
- Cada Card debe ser lo bastante concreta como para que un agente pueda implementarla sin ambigüedad.
- Toda decisión técnica debe favorecer un stack **costo-eficiente**, simple de operar y consistente con el enfoque tomado en Obsydian.

---

## Stack objetivo del MVP

La arquitectura base del proyecto se considera cerrada salvo que una épica posterior justifique un ajuste puntual.

| Capa | Decisión MVP | Criterio |
| --- | --- | --- |
| Frontend | Next.js | App web real, demo creíble, deploy simple |
| Backend | FastAPI | Python natural para CSV, pandas y reglas |
| Motor | Python + pandas + reglas explícitas | Explicación controlada, auditable y rápida |
| Base de datos | Supabase Postgres | Persistencia real con bajo overhead |
| Storage | Supabase Storage | Archivos persistentes sin infra extra |
| Deploy | Vercel + Supabase | Stack costo-eficiente, rápido y familiar |
| Explicación | Rule-based + template-based | Sin LLM en MVP base |

---

## Mapa de épicas

| # | Epic | Dominio | Depende de | Doc | Implementación |
| --- | --- | --- | --- | --- | --- |
| 0 | [Setup Técnico del MVP](./EPIC_00_Setup_Tecnico_MVP.md) | Transversal | — | ⏳ WS1 | PENDIENTE |
| 1 | [Data Foundation & Dataset Demo](./EPIC_01_Data_Foundation_Dataset_Demo.md) | D1 | 0 | ⏳ WS1 | PENDIENTE |
| 2 | [Reconciliation Engine Core](./EPIC_02_Reconciliation_Engine_Core.md) | D2 | 0, 1 | ⏳ WS2 | PENDIENTE |
| 3 | [Exception Detection & Explanation Layer](./EPIC_03_Exception_Detection_Explanation.md) | D3 | 2 | ⏳ WS2 | PENDIENTE |
| 4 | [Runs API, Persistence & Traceability](./EPIC_04_Runs_API_Persistence_Traceability.md) | D4 | 1, 2, 3 | ⏳ WS3 | PENDIENTE |
| 5 | [UI Foundation & Setup Flow](./EPIC_05_UI_Foundation_Setup_Flow.md) | D5 | 0, 1, 4 | ⏳ WS3 | PENDIENTE |
| 6 | [Summary, Concept Analysis & Explanation UI](./EPIC_06_Summary_Concept_Analysis_UI.md) | D6 | 3, 4, 5 | ⏳ WS4 | PENDIENTE |
| 7 | [Drill-down, Exports & Demo Traceability](./EPIC_07_Drilldown_Exports_Traceability.md) | D7 | 4, 6 | ⏳ WS4 | PENDIENTE |
| 8 | [Demo Seed, Narrative & Commercial Flow](./EPIC_08_Demo_Seed_Narrative_Commercial_Flow.md) | — | 1, 2, 3, 6, 7 | ⏳ WS5 | PENDIENTE |
| 9 | [Hardening, QA & Demo-Ready Closure](./EPIC_09_Hardening_QA_Demo_Ready.md) | Transversal | 8 | ⏳ WS5 | PENDIENTE |

---

## Cadena de dependencias

```text
EPIC 0 (Setup Técnico)
  └── EPIC 1 (Data Foundation & Dataset Demo)
        └── EPIC 2 (Reconciliation Engine Core)
              └── EPIC 3 (Exception Detection & Explanation)
                    └── EPIC 4 (Runs API, Persistence & Traceability)
                          ├── EPIC 5 (UI Foundation & Setup Flow)
                          │     └── EPIC 6 (Summary, Concept Analysis & Explanation UI)
                          │           └── EPIC 7 (Drill-down, Exports & Demo Traceability)
                          │                 └── EPIC 8 (Demo Seed, Narrative & Commercial Flow)
                          │                       └── EPIC 9 (Hardening, QA & Demo-Ready Closure)
                          └── EPIC 8 (Demo Seed, Narrative & Commercial Flow)
```

---

## Lectura funcional de las épicas

### EPIC 00 — Setup Técnico del MVP

Define la base del proyecto con un stack costo-eficiente y vendible: frontend en Next.js, backend en FastAPI, Supabase como DB y storage, despliegue simple y estructura inicial de repositorio.

### EPIC 01 — Data Foundation & Dataset Demo

Construye el universo de datos del MVP: `payroll.csv`, `expected_totals.csv`, `concept_master.csv`, `employee_reference.csv` opcional, schema lógico y dataset demo controlado con los casos wow ya definidos.

### EPIC 02 — Reconciliation Engine Core

Implementa el núcleo matemático y funcional: validación, normalización, agregación, observed totals, comparación contra expected totals y asignación de estados de conciliación.

### EPIC 03 — Exception Detection & Explanation Layer

Construye la capa diferencial del producto: detección de duplicados, out-of-period, unmapped, missing population, outliers y generación de explicación narrativa con recomendaciones.

### EPIC 04 — Runs API, Persistence & Traceability

Formaliza runs, endpoints, persistencia de resultados, staging de payroll normalizado y trazabilidad mínima de ejecución para reproducibilidad y credibilidad de producto.

### EPIC 05 — UI Foundation & Setup Flow

Construye la base UX del producto: app shell, layout, design rules, pantalla de setup, carga de archivos, preview de expected totals y trigger de ejecución.

### EPIC 06 — Summary, Concept Analysis & Explanation UI

Entrega el corazón visible del demo: summary ejecutivo, tabla por concepto, semaforización, KPIs, análisis por concepto y panel de explicación.

### EPIC 07 — Drill-down, Exports & Demo Traceability

Agrega la capacidad operativa: bajar a registros concretos, filtrar anomalías, revisar evidencia y exportar salidas útiles para demo y seguimiento.

### EPIC 08 — Demo Seed, Narrative & Commercial Flow

Deja la demo lista para ser mostrada: carga de seed consistente, corridas prearmadas o reproducibles, datos narrativos controlados y guión comercial.

### EPIC 09 — Hardening, QA & Demo-Ready Closure

Cierra el MVP con validación funcional, chequeos manuales, polish visual, corrección de bordes y checklist de “demo-ready”.

---

## Criterio general de “completada”

Una Epic se considera completada cuando:

1. Todas sus Cards están en estado `COMPLETADA`
2. El flujo funcional cubierto por la épica funciona end-to-end en local
3. La implementación quedó documentada y verificable
4. Existe validación manual suficiente para el alcance del MVP
5. No deja bloqueos no explicitados para la siguiente épica

---

## Estados posibles

### Estados de implementación

- `PENDIENTE` — no iniciada
- `EN PROGRESO` — hay sesión activa trabajando en ella
- `COMPLETADA` — implementada y validada para el alcance MVP
- `BLOQUEADA` — no puede avanzar por dependencia o decisión abierta

### Estados de documentación

- `✅ WSn` — épica documentada en sesión n
- `⏳ WSn` — épica prevista para documentarse en sesión n

---

## Lectura obligatoria al iniciar una sesión

Antes de seguir trabajo sobre este proyecto, siempre leer:

1. `AGENTS.md`
2. `Backlog/WORKFLOW_EJECUCION.md`
3. `Backlog/RESUMEN_MAESTRO.md`
4. la última `ARD_WS[N]_DDMMAAAA.md`
5. la epic específica a ejecutar

---

## Orden recomendado de documentación

Para este proyecto conviene documentar en este orden:

1. `EPIC_00_Setup_Tecnico_MVP.md`
2. `EPIC_01_Data_Foundation_Dataset_Demo.md`
3. `EPIC_02_Reconciliation_Engine_Core.md`
4. `EPIC_03_Exception_Detection_Explanation.md`
5. `EPIC_04_Runs_API_Persistence_Traceability.md`
6. `EPIC_05_UI_Foundation_Setup_Flow.md`
7. `EPIC_06_Summary_Concept_Analysis_UI.md`
8. `EPIC_07_Drilldown_Exports_Traceability.md`
9. `EPIC_08_Demo_Seed_Narrative_Commercial_Flow.md`
10. `EPIC_09_Hardening_QA_Demo_Ready.md`

---

## Nota de diseño

Aunque este backlog hereda la lógica operativa de Obsydian, este producto no necesita arrastrar complejidad innecesaria. La regla es simple:

> si una decisión no mejora la demo, la explicabilidad o la velocidad de construcción, no entra al MVP.
