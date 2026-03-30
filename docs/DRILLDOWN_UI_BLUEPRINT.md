# Drill-down UI Blueprint

## Objetivo funcional del drill-down

El drill-down debe responder en segundos estas tres preguntas:

- que registros explican esta diferencia
- que empleados estan involucrados
- que anomalias concretas fueron detectadas

La vista no existe para volver a explicar el concepto desde cero.
Existe para aterrizar la explanation layer en evidencia concreta y auditable.

## Rol del drill-down dentro del producto

El drill-down representa el ultimo paso del recorrido analitico del MVP:

1. summary para detectar donde esta el problema
2. concept analysis para entender causas probables
3. drill-down para ver la evidencia concreta

Decision de producto:

- el drill-down no reemplaza la explanation layer
- el drill-down aterriza la explicacion en registros reales
- el drill-down refuerza confianza, trazabilidad y credibilidad demo

## Alcance del drill-down del MVP

El alcance confirmado para MVP es:

- detalle por linea de payroll persistida
- contexto del empleado asociado cuando exista
- resumen superior minimo para contextualizar volumen e impacto
- filtros ligeros para reducir ruido operativo
- tabla reusable orientada a analisis
- exportabilidad basica de la evidencia

## Que entra en la pantalla

La experiencia de drill-down del MVP debe incluir:

- header con contexto de run y concepto
- resumen superior del detalle
- filtros simples y opcionales
- tabla de registros afectados
- indicadores visibles de anomalia por fila
- acciones de export basicas

## Anatomia de la Drill-down Screen

Orden de lectura definido:

1. header del concepto
2. resumen superior del drill-down
3. filtros ligeros
4. tabla de registros
5. acciones de export

Bloques visuales obligatorios:

- header con nombre del concepto, run, periodo y acciones de retorno
- resumen superior con volumen, impacto y cobertura de anomalias
- franja de filtros opcionales y livianos
- tabla principal de evidencia por linea
- acciones visibles para exportar evidencia util

La jerarquia visual debe priorizar primero el contexto y el volumen del caso, y
despues la lectura detallada de registros.

## Resumen superior del drill-down

Antes de la tabla, la pantalla debe responder rapidamente que tan grande y de
que tipo es el problema que el usuario esta abriendo.

El resumen superior debe mostrar como minimo:

- registros impactados
- empleados afectados
- tipos de anomalia detectados

Tono aprobado:

- breve
- operativo
- orientado a revision

El resumen no debe duplicar la narrativa completa de Concept Analysis.
Debe contextualizar la tabla y ayudar a decidir por donde empezar a revisar.

## Tabla operativa de registros afectados

La tabla principal del drill-down debe ser legible, auditable y suficientemente
densa para analisis real, sin convertirse en una grilla pesada.

Columnas base confirmadas:

- `Record ID`
- `Employee ID`
- `Employee Name`
- `Legal Entity`
- `Concept`
- `Amount`
- `Period`
- `Exception Type`
- `Observation`

Decision sobre `cost_center`:

- no entra como columna visible por defecto
- puede mostrarse mas adelante si el espacio y el caso lo justifican
- por ahora se preserva como dato disponible para filtros o export futuros

## Nivel de detalle confirmado

El drill-down muestra:

- detalle por linea
- detalle por empleado asociado
- excepciones observables por registro

Esto permite que el usuario conecte el desvio agregado con evidencia puntual sin
salir del flujo del producto.

## Que no entra en el MVP

Para proteger foco y velocidad, esta capa no incluye:

- edicion inline de registros
- comentarios colaborativos
- workflow de aprobacion
- correcciones transaccionales
- automatizaciones de remediacion

## Regla operativa de la vista

El drill-down del MVP es:

- analitico
- exportable
- auditable

No es una pantalla transaccional.
Su trabajo es ayudar a entender, priorizar y llevar evidencia fuera de la app.
