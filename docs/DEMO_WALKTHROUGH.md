# Demo Walkthrough

## Objetivo

Este documento fija el recorrido comercial principal del MVP para una demo de
`5` a `8` minutos.

Su funcion es cerrar:

- estructura del demo
- wow moment principal
- cierre comercial
- guion operativo paso a paso
- FAQ sugerida
- checklist tecnico y narrativo pre-demo
- criterio practico de demo-ready

## Estructura del demo de 5 a 8 minutos

Secuencia recomendada:

1. contexto del problema
2. setup muy breve
3. summary ejecutivo
4. apertura del wow case `MEAL_VOUCHER`
5. bajada a drill-down
6. casos complementarios rapidos
7. cierre comercial

### Timing sugerido

- contexto: `45-60s`
- setup: `30-45s`
- summary: `60-90s`
- wow case `MEAL_VOUCHER`: `90-120s`
- drill-down: `60-90s`
- casos complementarios: `45-60s`
- cierre: `30-45s`

## Wow moment principal

La secuencia wow aprobada es:

1. mostrar en Summary que hay conceptos en rojo
2. abrir `MEAL_VOUCHER`
3. explicar que el sistema no da una causa unica simplista
4. mostrar que separa `Unmapped Concept`, `Out-of-Period Record` y
   `Duplicate Record`
5. bajar a drill-down para aterrizar la historia en registros concretos

### Por que esta secuencia vende valor

Porque muestra en menos de dos minutos el diferencial completo del producto:

- detecta que algo no cierra
- explica por que no cierra
- permite ir a la evidencia concreta

## Cierre comercial

Mensaje de cierre recomendado:

> En vez de revisar manualmente miles de lineas para entender por que el cierre
> no netea, el equipo puede ir del desvio agregado a la causa probable y a la
> evidencia puntual en minutos, con una trazabilidad que despues puede escalarse
> a otros periodos, entidades o clientes.

## Guion operativo paso a paso

### 1. Abrir el producto

Que mostrar:

- workspace principal del MVP
- que el producto ya parte de referencias demo controladas

Que decir:

- "Tomamos un export mensual de payroll y lo contrastamos contra los expected
  totals del periodo."

Que no mostrar:

- configuraciones accesorias
- detalles tecnicos de infraestructura

### 2. Mostrar setup solo como puente

Que mostrar:

- periodo `2026-03`
- referencia a archivos demo ya listos
- run canonica ya sembrada o flujo de siembra resuelto

Que decir:

- "La preparacion queda estandarizada para que la demo y el proceso sean
  repetibles."

Que no mostrar:

- pasos manuales innecesarios
- exploracion larga del formulario

### 3. Entrar en Summary

Que mostrar:

- overall status
- KPI cards
- tabla por concepto

Que decir:

- "En segundos vemos cuantos conceptos conciliaron, cuantos quedaron abiertos y
  donde esta la materialidad real."

Foco visual:

- conceptos `Unreconciled`
- `TRANSPORT` como caso menor

### 4. Abrir `MEAL_VOUCHER`

Que mostrar:

- diff visible
- statement principal
- top causes
- recommended action

Que decir:

- "Aca no vemos solo que falta dinero; vemos que el desvio mezcla mapping,
  registros fuera de periodo y duplicados."

Que no hacer:

- leer todas las filas
- quedarse demasiado tiempo en copy secundaria

### 5. Bajar a drill-down

Que mostrar:

- tabla concreta
- excepciones visibles
- volumen de filas impactadas

Que decir:

- "El usuario puede ir de un insight ejecutivo a evidencia accionable sin salir
  del flujo."

### 6. Mostrar casos complementarios

Orden recomendado:

1. `CHILDCARE`
2. `OVERTIME`
3. `TRANSPORT`

Mensajes clave:

- `CHILDCARE`: "No es solo una anomalía de archivo; faltan empleados elegibles."
- `OVERTIME`: "El sistema identifica rapido una linea atipica dominante."
- `TRANSPORT`: "No todo desvio se dramatiza; tambien hay criterio de tolerancia."

### 7. Cerrar

Que decir:

- "Esto reduce trabajo manual, mejora explicabilidad y deja una trazabilidad
  mucho mas util para cierre y seguimiento."

## FAQ sugerida

### ¿Esto se integra con SAP?

Respuesta sugerida:

En el MVP trabajamos con exports CSV para maximizar velocidad de demo y control
del flujo. La logica esta pensada para conectarse despues a fuentes reales como
SAP o payroll systems sin cambiar la narrativa principal del producto.

### ¿Que tan manual es el setup?

Respuesta sugerida:

Para demo queda casi resuelto por seed y run canonica. En un proyecto real, el
objetivo seria parametrizar fuentes y expected totals para que el proceso sea
cada vez mas repetible.

### ¿Como se adapta a otro cliente?

Respuesta sugerida:

La capa reusable es el modelo: expected totals, concept master, reglas y
excepciones. Cambia el dataset y el mapping, no el valor central del flujo.

### ¿Como explica diferencias complejas?

Respuesta sugerida:

Hoy el MVP usa reglas explicitas y templates controlados. Eso permite una
explicacion auditable y consistente. En fases futuras puede enriquecerse, pero
para demo y operaciones financieras esta trazabilidad es una fortaleza.

### ¿Esto reemplaza el analisis humano?

Respuesta sugerida:

No. Lo acelera y lo enfoca. El producto reduce el tiempo necesario para llegar
de un desvio agregado a una hipotesis fuerte y a la evidencia concreta.

## Checklist tecnico pre-demo

Antes de una reunion verificar:

- frontend levantado
- backend levantado
- base accesible
- run demo canonica presente o recreada con
  `cd backend && .venv/bin/python scripts/demo_seed.py create --reset-first`
- summary cargando sin error
- `MEAL_VOUCHER`, `CHILDCARE`, `OVERTIME` y `TRANSPORT` con estados correctos
- drill-down de `MEAL_VOUCHER` cargando
- export summary descargable
- export detail descargable

Responsable sugerido:

- quien vaya a presentar el demo

Momento recomendado:

- `15-30` minutos antes de la reunion

## Checklist narrativo pre-demo

Antes de presentar verificar:

- historia principal clara
- wow moment identificado
- cierre comercial practicado
- respuestas a objeciones revisadas
- demo dentro de `5-8` minutos
- orden de casos complementarios memorizado

## Criterio practico de demo-ready

El MVP puede considerarse demo-ready si cumple estas condiciones:

- la run canonica puede recrearse sin friccion
- el walkthrough principal entra en `5-8` minutos
- `MEAL_VOUCHER` sostiene el wow moment
- `CHILDCARE`, `OVERTIME` y `TRANSPORT` refuerzan el mensaje sin ruido
- summary, concept analysis, drill-down y exports funcionan
- no hay improvisacion necesaria para explicar el valor central

## Que evitar en la demo

- abrir demasiados conceptos
- discutir arquitectura en exceso antes de mostrar valor
- convertir el walkthrough en un tour de features
- improvisar sobre casos no sembrados
- perder tiempo en configuraciones que no aportan insight
