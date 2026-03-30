# Catalogo de Excepciones del MVP

## Objetivo

Este documento fija el catalogo definitivo de excepciones del
**Accounting Reconciliation MVP** para `EPIC 03`.

Su objetivo es dejar cerrado:

- que excepciones detecta formalmente el producto en esta version
- cuales son principales y cuales opcionales
- como se define funcionalmente cada una
- cuales son centrales para la demo y cuales cumplen un rol secundario

La regla de este documento es simple:

> si una excepcion no esta en este catalogo, no forma parte del MVP base.

## 1. Principios del catalogo

El catalogo debe favorecer una capa de explicacion:

- rule-based
- auditable
- trazable
- comercialmente clara

Por lo tanto, cada excepcion incluida en el MVP debe cumplir al menos una de
estas condiciones:

- explicar una diferencia real del dataset demo
- mejorar la calidad o confiabilidad de la corrida
- aportar un siguiente paso de revision entendible para Contabilidad

## 2. Excepciones principales del MVP

Estas excepciones forman parte del alcance central del producto y deben estar
soportadas por la capa de deteccion y explicacion de `EPIC 03`.

| Exception Type | Scope natural | Definicion funcional | Rol en el MVP | Centralidad demo |
| --- | --- | --- | --- | --- |
| `Invalid Amount / Data Quality Issue` | registro, concepto, corrida | El registro tiene monto no interpretable, campo critico faltante o inconsistencia estructural que compromete la evaluacion. | protege confiabilidad del resultado y permite invalidacion parcial o bloqueante | secundaria pero estructural |
| `Out-of-Period Record` | registro y concepto | La linea pertenece a un periodo distinto del `target_period` o presenta una fecha de posting inconsistente que refuerza esa desviacion. | explica diferencias temporales y montos excluidos del observado | central |
| `Unmapped Concept` | registro, patron raw, concepto afectado | La linea no puede traducirse a un `concept_code_normalized` valido segun el mapping del MVP. | explica por que parte del payroll no entra al observado conciliable | central |
| `Duplicate Record` | registro y grupo de registros | Existen lineas potencialmente duplicadas segun una combinacion estable de atributos clave; el sistema las trata como duplicados probables, no como verdad absoluta. | explica sobreconteos o distorsiones por repeticion | central |
| `Missing Record / Missing Population` | empleado, cohorte y concepto | Faltan empleados o registros esperables para un concepto cuya poblacion elegible esta definida en una referencia controlada. | explica diferencias por subcobertura o poblacion ausente | central |
| `Outlier Amount` | registro y concepto | Un monto individual es atipico frente al comportamiento habitual del concepto y merece revision puntual. | explica diferencias concentradas en pocos registros anormalmente grandes o chicos | central |
| `Missing Expected Total` | concepto | Existe observado conciliable pero no una referencia correspondiente en `expected_totals` para la unidad conciliable. | explicita incompletitud del baseline esperado y alinea con estados invalidos/incompletos | principal de soporte |

## 3. Excepciones opcionales del MVP

Estas excepciones se consideran capacidad secundaria. Pueden implementarse en
el MVP si ayudan a enriquecer la demo, pero no deben bloquear el cierre del
producto base.

| Exception Type | Scope natural | Definicion funcional | Rol en el MVP | Centralidad demo |
| --- | --- | --- | --- | --- |
| `Sign Error` | registro y concepto | El signo observado contradice la polaridad esperada definida en `concept_master`. | enriquece revision de calidad y consistencia contable | secundaria |
| `Misclassified Concept` | registro o patron de registros | El registro parece pertenecer a otro concepto por patron controlado, nombre o heuristica minima configurada para el demo. | agrega capacidad analitica puntual sin generalizar reclasificacion automatica | secundaria |

## 4. Definicion operativa por excepcion

### `Invalid Amount / Data Quality Issue`

Se activa cuando una linea no puede evaluarse con normalidad por problemas de
calidad de datos. En el MVP incluye, como minimo:

- `amount` ausente o no interpretable
- campos criticos faltantes para trazabilidad o clasificacion
- inconsistencias estructurales que impiden evaluar inclusion o exclusion

No busca capturar cualquier warning menor. Su foco es separar ruido tolerable
de problemas que comprometen la lectura de la corrida.

### `Out-of-Period Record`

Se activa cuando el registro no pertenece al periodo objetivo del run. La
fuente principal es `payroll_period`; `posting_date` funciona como evidencia
complementaria cuando refuerza la anomalia temporal.

En el MVP, estos registros quedan fuera del observado conciliable, pero siguen
vivos en la base para explicacion y drill-down.

### `Unmapped Concept`

Se activa cuando el payroll trae un codigo o nombre que no puede resolverse a
un concepto normalizado del `concept_master` bajo las reglas controladas del
motor.

No se permite autocorregir agresivamente estos casos. Si no hay mapping
confiable, el registro queda marcado como `unmapped`.

### `Duplicate Record`

Se activa cuando dos o mas lineas muestran una coincidencia exacta o casi
exacta en la clave de duplicado definida por el MVP, con foco esperado en:

- `employee_id`
- `payroll_period`
- `concept_code_normalized`
- `amount`
- `legal_entity` si aplica

La deteccion es de duplicado potencial. El lenguaje del producto debe reflejar
siempre esa cautela.

### `Missing Record / Missing Population`

Se activa cuando un concepto con elegibilidad conocida presenta empleados o
cohortes ausentes respecto de la referencia controlada del demo, por ejemplo
`employee_reference.csv`.

No implica que falte cualquier linea observada. Implica que falta cobertura
esperable de una poblacion elegible.

### `Outlier Amount`

Se activa cuando una linea individual se desvía claramente del comportamiento
tipico del concepto. La logica del MVP debe ser simple y explicable, por
ejemplo un umbral sobre mediana por concepto.

No busca hacer analitica estadistica compleja. Busca señalar montos que merecen
revision inmediata.

### `Missing Expected Total`

Se activa cuando existe monto observado conciliable para una unidad
`period + concept`, pero no existe fila correspondiente en `expected_totals`.

Esta excepcion no explica una anomalia del payroll sino una ausencia del
baseline esperado. Por eso cumple un rol de soporte dentro de la capa
explicativa.

### `Sign Error`

Se activa cuando el signo del monto observado contradice el signo esperado del
concepto. En el MVP debe operar como capacidad opcional y controlada, sin
reescribir automaticamente el importe original.

### `Misclassified Concept`

Se activa cuando una heuristica minima y explicitamente configurada sugiere que
el registro pertenece a otro concepto o categoria.

En el MVP no debe convertirse en un motor general de reclasificacion. Solo debe
usarse en casos muy acotados donde la narrativa del demo lo justifique.

## 5. Centralidad para la demo comercial

Las excepciones mas importantes para la narrativa del MVP son:

- `Out-of-Period Record`
- `Unmapped Concept`
- `Duplicate Record`
- `Missing Record / Missing Population`
- `Outlier Amount`

Estas son las que sostienen los casos wow principales del dataset:

- `MEAL_VOUCHER`: mezcla de `Out-of-Period Record`, `Unmapped Concept` y
  `Duplicate Record`
- `CHILDCARE`: caso principal de `Missing Record / Missing Population`
- `OVERTIME`: caso principal de `Outlier Amount`

Las excepciones importantes pero no protagonistas del demo son:

- `Invalid Amount / Data Quality Issue`
- `Missing Expected Total`

Las excepciones secundarias u opcionales del MVP son:

- `Sign Error`
- `Misclassified Concept`

## 6. Taxonomia funcional y severidad base

La taxonomia del MVP ordena las excepciones segun el rol que cumplen dentro de
la lectura de una corrida. No todas tienen el mismo peso ni deben narrarse con
el mismo tono.

| Exception Type | Categoria funcional | Severidad base | Tono de explicacion esperado | Razon de negocio |
| --- | --- | --- | --- | --- |
| `Invalid Amount / Data Quality Issue` | calidad / invalidez | critica | sobrio, preventivo y de confiabilidad | puede comprometer la lectura del run o invalidar parte del resultado |
| `Out-of-Period Record` | temporalidad | alta | directo, causal y cuantificable | explica desalineacion entre el payroll procesado y el periodo conciliado |
| `Unmapped Concept` | mapping | alta | claro y operativo | explica exclusion del observado por falta de traduccion confiable |
| `Duplicate Record` | calidad analitica / duplicidad | alta | cauteloso pero accionable | sugiere sobreconteo probable y requiere revision puntual |
| `Missing Record / Missing Population` | poblacion / cobertura | alta | explicativo y orientado a cobertura | explica diferencias por ausencia de empleados o cohortes elegibles |
| `Outlier Amount` | anomalia cuantitativa | media | analitico y focalizado | señala registros atipicos con alto potencial explicativo |
| `Missing Expected Total` | baseline / completitud | alta | sobrio y estructural | indica que falta referencia esperada para evaluar correctamente la unidad |
| `Sign Error` | calidad / polaridad | media | cauteloso y de validacion | sugiere inconsistencia contable sin asumir correccion automatica |
| `Misclassified Concept` | mapping analitico | baja | hipotetico y muy prudente | solo apunta una posible reclasificacion bajo casos controlados |

## 7. Lectura de categorias funcionales

### Calidad / invalidez

Agrupa excepciones donde la prioridad es proteger la confiabilidad del run.

Incluye:

- `Invalid Amount / Data Quality Issue`
- `Sign Error`
- `Duplicate Record` como caso de calidad analitica

Estas excepciones no siempre explican por si solas toda la diferencia, pero
definen si el dato base merece confianza suficiente para interpretar el resto.

### Temporalidad

Agrupa excepciones donde el problema principal es que el registro no pertenece
al periodo correcto del analisis.

Incluye:

- `Out-of-Period Record`

Su tono debe ser causal y cuantificable: que quedo fuera, cuanto impacta y que
conviene revisar primero.

### Mapping

Agrupa excepciones donde la capa de traduccion entre payroll y concepto
normalizado no alcanza a clasificar el registro con confianza.

Incluye:

- `Unmapped Concept`
- `Misclassified Concept`

`Unmapped Concept` es estructural y accionable. `Misclassified Concept` debe
tratarse como capacidad secundaria e hipotetica.

### Poblacion / cobertura

Agrupa excepciones donde el problema no es el importe de una linea sino la
ausencia de registros esperables para una cohorte elegible.

Incluye:

- `Missing Record / Missing Population`

Su tono debe ayudar a Contabilidad a entender que la brecha puede venir de
personas faltantes, no de montos mal calculados.

### Anomalia cuantitativa

Agrupa excepciones donde la diferencia parece concentrarse en uno o pocos
montos atipicos.

Incluye:

- `Outlier Amount`

Su tono debe ser analitico y puntual, orientado a detectar una linea dominante.

### Baseline / completitud

Agrupa excepciones donde la referencia esperada esta ausente o incompleta.

Incluye:

- `Missing Expected Total`

Su tono debe ser estructural: el sistema no esta diciendo que el payroll este
mal, sino que falta una base esperada valida para evaluar esa unidad.

## 8. Regla de uso narrativo

La taxonomia no solo ordena deteccion. Tambien ordena como se cuenta la
historia:

- severidad `critica`: priorizar confiabilidad, invalidez o bloqueo
- severidad `alta`: priorizar como causa probable principal de diferencia
- severidad `media`: usar como explicacion complementaria o analitica
- severidad `baja`: mostrar solo cuando aporte contexto y sin sobredramatizar

La regla general del MVP es:

> primero proteger la confianza del dato, despues explicar la diferencia y por
> ultimo enriquecer la lectura con señales secundarias.

## 9. Prioridad entre excepciones

Cuando un mismo registro o concepto presenta multiples señales, el MVP debe
priorizar la explicacion en este orden:

1. `Invalid Amount / Data Quality Issue`
2. `Out-of-Period Record`
3. `Unmapped Concept`
4. `Duplicate Record`
5. `Missing Expected Total`
6. `Missing Record / Missing Population`
7. `Sign Error`
8. `Outlier Amount`
9. `Misclassified Concept`

### Criterio de negocio detras del orden

- primero se protege la confiabilidad del dato y la validez del scope
- despues se priorizan causas estructurales que excluyen o distorsionan el
  observado
- luego se elevan causas poblacionales o de baseline
- por ultimo se muestran señales analiticas o heuristicas secundarias

La regla no implica ocultar otras excepciones. Implica decidir cual aparece
primero cuando la historia necesita un driver principal.

## 10. Metodo de estimacion de impacto por tipo

El MVP distingue entre impacto `exacto`, `estimado` y `no cuantificable`.

La meta no es prometer precision contable absoluta para todos los casos. La
meta es mantener una metodologia consistente, entendible y util para demo.

| Exception Type | Metodo base | Nivel esperado |
| --- | --- | --- |
| `Out-of-Period Record` | sumar importes de lineas fuera de scope excluidas del observado | exacto dentro del criterio del motor |
| `Unmapped Concept` | sumar importes de lineas no mapeadas excluidas del observado | exacto dentro del criterio del motor |
| `Duplicate Record` | estimar sobreconteo como importe repetido por copias extra del grupo | exacto segun la regla de duplicado probable, pero no verdad absoluta de negocio |
| `Missing Expected Total` | usar monto observado de la unidad sin baseline esperado | exacto respecto del observado, estructural respecto de la causa |
| `Missing Record / Missing Population` | estimar faltante desde elegibilidad esperada y acotar por la brecha real del concepto | estimado y controlado |
| `Outlier Amount` | medir exceso del registro atipico por encima de la mediana del concepto | estimado, explicable y util para ranking |
| `Invalid Amount / Data Quality Issue` | no forzar monto atribuible salvo que la causa sea cuantificable de forma segura | normalmente no cuantificable |

### Regla de precision

- `exacto` significa consistente con las reglas del motor y el scope del run
- `estimado` significa util para priorizar, pero no para prometer trazabilidad
  contable perfecta
- `no cuantificable` significa que la señal sirve para gobernanza o confianza
  del dato, aunque no explique un monto preciso

### Limites del MVP

- no se debe sumar ciegamente impacto de causas superpuestas como si fueran
  independientes
- `Duplicate Record` sigue siendo una deteccion probable, por eso su impacto es
  cuantitativo pero no absoluto
- `Missing Population` debe evitar sobreatribuir y por eso puede acotarse por
  la diferencia real del concepto
- `Invalid Amount / Data Quality Issue` puede dominar la narrativa sin aportar
  monto exacto

## 11. Logica de ranking de causas probables

El ranking del MVP combina cuatro dimensiones:

1. `estimated_impact_amount`
2. severidad funcional
3. `confidence`
4. prioridad del tipo de excepcion

### Criterio operativo

La ordenacion sugerida por concepto es:

1. mayor impacto estimado
2. mayor severidad
3. mayor confianza
4. mejor prioridad del tipo
5. mayor cantidad de ocurrencias cuando siga habiendo empate

### Limite de causas mostradas

Por defecto el MVP debe mostrar hasta `3` causas por concepto.

Eso permite:

- una causa principal clara
- una o dos causas secundarias relevantes
- evitar explicaciones largas y caoticas

### Desempates y bordes

- si dos causas tienen impacto parecido, gana la de mayor severidad
- si la severidad empata, gana la de mayor confianza funcional
- si ambas empatan, gana la de prioridad mas alta en el catalogo
- causas con impacto `0` o no cuantificable pueden aparecer, pero no deben
  desplazar una causa material mejor sustentada

## 12. Regla de alcance

Este catalogo y su taxonomia definen el alcance funcional de `EPIC 03` para el
MVP base.

Por lo tanto:

- las excepciones principales deben quedar detectables y explicables
- las opcionales pueden implementarse de forma controlada y no bloqueante
- no deben agregarse nuevos tipos sin actualizar este documento, la epic y la
  nota de sesion correspondiente
