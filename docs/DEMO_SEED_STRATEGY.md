# Demo Seed Strategy

## Objetivo

Este documento define como se deja el MVP en estado demo-ready para
presentaciones comerciales, validaciones internas y ensayos repetibles.

Su trabajo es cerrar cuatro decisiones de `EPIC 08`:

- estrategia de seed del MVP
- alcance exacto del seed
- contrato narrativo final del dataset demo
- definicion de la run demo canonica

## Punto de partida real del proyecto

Hoy el repo ya tiene una base demo util y verificable:

- `data/demo_seed/generate_dataset.py` regenera el dataset de forma determinista
- `data/demo_seed/*.csv` materializa el universo demo final
- la UI de setup usa referencias demo por defecto
- el backend ya puede crear runs, registrar archivos, ejecutar conciliacion y
  exponer summary, concept analysis, drill-down y exports
- los tests del motor ya verifican los estados narrativos principales

La estrategia de `EPIC 08` no parte de cero.
Parte de una base funcional que ya sostiene la historia del demo y la vuelve
reproducible.

## Alternativas evaluadas

### 1. Corrida precargada persistida

Ventajas:

- cero tiempo de preparacion antes de mostrar
- todas las pantallas ya aparecen listas

Trade-offs:

- depende de un estado persistido fragil
- cuesta resetear sin tooling adicional
- puede degradarse si se mezclan corridas manuales o residuos operativos

### 2. Regeneracion programatica completa de la run demo

Ventajas:

- maxima repetibilidad
- fuente de verdad clara y versionable
- evita depender de una base "magica" precargada

Trade-offs:

- agrega un paso operativo antes del demo
- exige que el entorno backend y DB esten sanos en el momento de la siembra

### 3. Enfoque hibrido

Combinacion propuesta:

- dataset fuente versionado y determinista en repo
- script reproducible para crear la run demo canonica
- opcion de dejar una run ya sembrada cuando convenga para ensayos o reuniones

## Estrategia recomendada para el MVP

La estrategia elegida para el MVP es un **enfoque hibrido**.

### Decision

El estado demo no se apoya en una unica corrida "sagrada" persistida.
Se apoya en:

1. un dataset demo final y versionado como fuente de verdad
2. un flujo reproducible para crear la run demo canonica
3. un flujo complementario para resetear runs demo anteriores cuando haga falta

### Razon

Este enfoque maximiza lo que importa para el proyecto:

- control narrativo
- repetibilidad
- baja friccion operativa
- coherencia entre repo, tests y producto visible

Tambien evita dos extremos inconvenientes:

- depender solo de una corrida persistida que puede ensuciarse
- obligar a "rearmar a mano" la demo en cada reunion

## Alcance exacto del seed

El seed demo del MVP debe dejar listo lo siguiente:

### Artefactos que si deben quedar listos

- archivos demo finales en `data/demo_seed/`
- una run demo canonica en periodo `2026-03`
- referencias de archivos asociadas a esa run
- resultados persistidos por concepto
- excepciones persistidas
- payroll lines persistidas para drill-down
- metadata de trazabilidad suficiente para summary y detail

### Artefactos que no hace falta pre-sembrar

- multiples runs tematicas
- exportables pre-generados en storage
- variantes por pais o por legal entity
- snapshots visuales o material comercial fuera del repo

### Decision sobre exports

Los exports CSV del MVP quedan **on-demand**.
No hace falta persistirlos antes del demo porque el producto ya puede
generarlos desde la run sembrada.

## Dataset demo final

El set final de archivos para la demo comercial queda confirmado como:

- `data/demo_seed/payroll.csv`
- `data/demo_seed/expected_totals.csv`
- `data/demo_seed/concept_master.csv`
- `data/demo_seed/employee_reference.csv`

### Regla operativa

Estos cuatro archivos son la fuente oficial del walkthrough demo.
Si se regeneran, debe hacerse solo mediante:

```bash
python3 data/demo_seed/generate_dataset.py
```

## Contrato narrativo final por concepto

La tabla siguiente fija el comportamiento que la demo debe sostener en producto,
scripts y validaciones.

| Concepto | Expected | Observed | Diff | Status esperado | Rol narrativo |
| --- | ---: | ---: | ---: | --- | --- |
| `MEAL_VOUCHER` | 42000.00 | 38220.00 | -3780.00 | `Unreconciled` | wow principal multi-causa |
| `CHILDCARE` | 18500.00 | 17050.00 | -1450.00 | `Unreconciled` | faltante de poblacion elegible |
| `OVERTIME` | 14000.00 | 14950.00 | 950.00 | `Unreconciled` | outlier dominante |
| `TRANSPORT` | 21000.00 | 20760.00 | -240.00 | `Minor Difference` | caso sobrio de tolerancia |

### Explicacion target por concepto

`MEAL_VOUCHER`

- debe mostrar combinacion de `Unmapped Concept`, `Out-of-Period Record` y
  `Duplicate Record`
- es el caso principal para vender capacidad de explicacion y drill-down

`CHILDCARE`

- debe priorizar `Missing Record / Missing Population`
- tiene que hacer evidente que el sistema entiende elegibilidad, no solo
  errores mecanicos

`OVERTIME`

- debe priorizar `Outlier Amount`
- tiene que poder defenderse rapido en concept analysis y drill-down

`TRANSPORT`

- debe mantenerse como `Minor Difference`
- no debe competir visualmente con los casos wow

### Estado agregado esperado de la run demo

La run canonica del demo debe cerrar con:

- `6` conceptos reconciled
- `1` concepto con minor difference
- `3` conceptos unreconciled
- overall status `unreconciled`
- status tecnico de run `RECONCILED_WITH_EXCEPTIONS`

## Run demo canonica del MVP

La run principal del walkthrough queda definida como:

- `run_label`: `Demo March 2026 - Canonical Walkthrough`
- `period`: `2026-03`
- `dataset`: `data/demo_seed/*`
- `scope`: todos los datos del seed demo
- `proposito`: soportar la secuencia comercial principal de 5 a 8 minutos

### Decision sobre cantidad de runs demo

Para el MVP se define **una unica run principal**.

Puede existir una run regenerada mas reciente del mismo tipo para ensayos, pero
el producto no necesita una familia de demos paralelas en esta etapa.

## Flujo recomendado de preparacion

Secuencia operativa aprobada:

1. regenerar dataset solo si hubo cambios narrativos o tecnicos
2. ejecutar reset del entorno demo si hace falta limpiar corridas previas
3. crear la run canonica con el script oficial
4. abrir summary y confirmar rapidamente los cuatro conceptos clave
5. usar esa run para walkthrough, ensayo o reunion

## Criterio de exito de la estrategia elegida

La estrategia se considera correcta si permite:

- volver a un estado demo confiable en minutos
- mantener alineados repo, tests y comportamiento visible
- evitar improvisacion durante una reunion comercial
- sostener una narrativa consistente entre summary, concept analysis y
  drill-down
