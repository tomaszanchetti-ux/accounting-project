# Dataset Demo Foundation

## Objetivo

Este documento define la base funcional del dataset demo del proyecto
**Accounting Reconciliation MVP**.

Su proposito es cerrar, card por card, que archivos existen, que representa
cada uno y bajo que supuestos se construye el universo de datos del MVP.

## Estado actual

### Archivo principal del demo

El archivo principal del demo sera:

- `payroll.csv`
- `expected_totals.csv` como referencia de control del periodo

## Definicion de `payroll.csv`

### Rol funcional

`payroll.csv` es la fuente observada principal a conciliar en el MVP.

Representa un export mensual de nomina y beneficios proveniente de payroll,
SAP o una fuente equivalente del proceso contable real.

No es un archivo auxiliar ni de configuracion:

- es el input operativo central del demo
- es la base del calculo observado
- es la fuente usada para agregacion por concepto
- es la fuente usada para drill-down a registros concretos

### Que contiene

`payroll.csv` debe contener multiples lineas por empleado y por concepto.

Eso implica que:

- un mismo empleado puede tener varias lineas en un mismo periodo
- un mismo concepto puede aparecer repetido para muchos empleados
- un empleado puede combinar conceptos regulares y beneficios
- la suma de las lineas observadas es la base de conciliacion contra
  `expected_totals.csv`

### Nivel de realismo esperado

El archivo debe sentirse como un export realista de operacion mensual, no como
una tabla inventada solo para la demo.

El objetivo no es copiar un layout enterprise exacto, sino sostener:

- agregacion creible
- desvio plausible
- explicacion entendible
- trazabilidad desde resumen hacia registro individual

### Convenciones base ya fijadas

Para `payroll.csv`, desde esta card quedan fijados estos supuestos base:

- representa un unico periodo principal del demo
- funciona como fuente observada a conciliar
- incluye lineas de nomina y beneficios
- permite multiples registros por `employee_id` y `concept_code`
- debe poder consumirse de forma reproducible en local y en entorno demo

### Relacion con el producto

Dentro del flujo del MVP, `payroll.csv` sera el archivo que el usuario carga o
utiliza como insumo principal para iniciar una corrida.

La secuencia funcional esperada es:

1. cargar `payroll.csv`
2. leer los registros observados del periodo
3. agregar montos por concepto
4. comparar contra `expected_totals.csv`
5. detectar diferencias y habilitar explicacion y drill-down

### Notas para las siguientes cards

Esta card no cierra todavia:

- la lista final de columnas
- los tipos y formatos
- las reglas de calidad del input

Esos puntos se completan en:

- `Card 1.2.1`
- `Card 1.2.2`
- `Card 1.2.3`

## Definicion de `expected_totals.csv`

### Rol funcional

`expected_totals.csv` es la referencia esperada contra la cual se compara el
total observado consolidado desde `payroll.csv`.

Su funcion no es reemplazar el detalle transaccional, sino actuar como verdad
de control del periodo para la conciliacion por concepto.

En el MVP:

- define que total deberia cerrar por concepto
- permite calcular `diff = observed - expected`
- habilita clasificacion de estado como `reconciled`, `minor` o
  `unreconciled`
- sostiene la narrativa explicativa del resumen

### Grano minimo

Desde esta card queda definido que `expected_totals.csv` tendra, como base, una
fila por:

- `payroll_period`
- `concept_code`

Ese es el grano minimo de conciliacion del MVP.

La comparacion principal del producto no estara gobernada inicialmente por
empleado ni por cost center, sino por concepto consolidado del periodo.

### Decision sobre `legal_entity`

Para el MVP base, `legal_entity` no sera una dimension obligatoria del archivo.

La decision operativa es:

- dejar `legal_entity` fuera del alcance inicial del grano obligatorio
- permitir que pueda incorporarse mas adelante como columna opcional o nullable
- mantener la conciliacion core enfocada en `periodo + concepto`

Esto reduce complejidad temprana y protege la claridad del demo comercial.

### Que representa

`expected_totals.csv` representa el total esperado del periodo segun la
referencia de control del negocio.

Puede pensarse como una tabla preparada por:

- controlling
- contabilidad
- una referencia funcional acordada para el cierre

No es un calculo derivado de `payroll.csv`, sino el benchmark contra el cual se
mide lo observado.

### Relacion con la unidad de conciliacion

La unidad de conciliacion del MVP queda definida, en esta etapa, como:

- un concepto en un periodo determinado

Por lo tanto:

- `payroll.csv` aporta el total observado por concepto
- `expected_totals.csv` aporta el total esperado por concepto
- el motor compara ambos universos sobre esa misma llave logica

### Relacion con el producto

Dentro del producto, `expected_totals.csv` podra cargarse como archivo de
control complementario de la corrida.

La secuencia esperada es:

1. cargar `payroll.csv` como fuente observada
2. cargar `expected_totals.csv` como referencia esperada
3. ejecutar la conciliacion por concepto y periodo
4. mostrar resumen, diferencias y explicaciones

### Visualizacion y uso en la demo

En la experiencia del MVP, el usuario no necesita ver todas las filas crudas de
`expected_totals.csv` como tabla protagonista.

Su rol visible sera:

- alimentar el resumen de expected vs observed
- sostener el calculo de diferencias por concepto
- justificar por que un concepto aparece como reconciliado o no

### Notas para las siguientes cards

Esta card deja cerrado el rol funcional del archivo, pero todavia no cierra:

- columnas finales exactas
- tipos de dato
- valores concretos por concepto del demo

Esos puntos se completan mas adelante cuando se definan:

- conceptos del MVP
- tabla objetivo de `expected / observed / diff / estado`

## Definicion de `concept_master.csv`

### Rol funcional

`concept_master.csv` es el archivo de referencia que normaliza el universo de
conceptos del MVP.

Su funcion principal es servir como capa de mapping entre los conceptos que
aparecen en `payroll.csv` y la logica de conciliacion que el producto necesita
para agregar, comparar y explicar.

En el MVP:

- traduce conceptos observados a una taxonomia controlada
- define como se agrupa cada concepto para conciliar
- fija el signo esperado de cada concepto
- aporta metadata util para explicacion y analisis

### Columnas minimas

Desde esta card quedan definidas como columnas minimas recomendadas:

- `source_concept_code`
- `source_concept_name`
- `normalized_concept_code`
- `normalized_concept_name`
- `concept_category`
- `reconciliation_group`
- `expected_sign`
- `is_active`

### Sentido de cada columna

- `source_concept_code`: codigo tal como puede venir en la fuente observada
- `source_concept_name`: descripcion original del concepto observado
- `normalized_concept_code`: codigo canonico usado por el MVP
- `normalized_concept_name`: nombre legible del concepto canonico
- `concept_category`: categoria funcional, por ejemplo salary, benefit o bonus
- `reconciliation_group`: grupo sobre el cual el motor agrega y compara
- `expected_sign`: signo esperado del concepto, por ejemplo positive o negative
- `is_active`: indica si el mapping sigue vigente para el periodo demo

### Rol en normalizacion y conciliacion

`concept_master.csv` evita que el motor dependa directamente de nombres o
codigos crudos del export.

Eso permite:

- estabilizar la agregacion por concepto
- manejar variantes de nombres o codigos de origen
- controlar de forma centralizada la logica de agrupacion
- sostener explicaciones mas consistentes en UI y backend

### Relacion con excepciones y explicacion

Este archivo tambien habilita varias excepciones del MVP.

En particular:

- si un concepto observado no encuentra mapping valido, puede disparar
  `unmapped concept`
- si el signo observado contradice el `expected_sign`, puede disparar
  `sign error`

Ademas, `concept_category` y `reconciliation_group` ayudan a construir
explicaciones mas claras sobre por que una diferencia pertenece a cierto bloque
funcional del payroll.

### Relacion con el producto

Dentro de una corrida, `concept_master.csv` funcionara como archivo de apoyo o
tabla de referencia previa al calculo.

La secuencia esperada es:

1. leer los conceptos observados desde `payroll.csv`
2. resolver su mapping con `concept_master.csv`
3. normalizar los conceptos a la taxonomia del MVP
4. consolidar resultados para conciliacion y excepciones

### Notas para las siguientes cards

Esta card deja cerrado el rol del archivo y sus columnas minimas, pero todavia
no cierra:

- la lista final de conceptos canonicos del MVP
- categorias definitivas por concepto
- valores concretos del mapping demo

Esos puntos se completan cuando se cierre el universo de conceptos de la epic.

## Definicion de `employee_reference.csv`

### Decision de alcance

`employee_reference.csv` si entra en el MVP base.

La razon es simple:

- el caso `CHILDCARE` fue definido como uno de los casos wow del demo
- ese caso necesita una referencia de elegibilidad o poblacion esperada
- resolverlo sin archivo auxiliar haria la explicacion menos creible

Por lo tanto, el MVP incorpora `employee_reference.csv` como archivo auxiliar
acotado y orientado a elegibilidad.

### Rol funcional

`employee_reference.csv` no es una fuente contable ni transaccional.

Su funcion es aportar contexto de poblacion esperada para conceptos selectivos,
especialmente beneficios donde no toda la nomina es elegible.

En el MVP:

- define que empleados son elegibles para ciertos conceptos
- permite comparar poblacion esperada vs poblacion observada
- sostiene la excepcion `missing population`
- agrega contexto explicativo para conceptos como `CHILDCARE`

### Columnas minimas

Desde esta card quedan definidas como columnas minimas recomendadas:

- `employee_id`
- `employee_name`
- `legal_entity`
- `country`
- `cost_center`
- `payroll_period`
- `is_childcare_eligible`

### Sentido de cada columna

- `employee_id`: identificador estable para cruzar con `payroll.csv`
- `employee_name`: apoyo visual y validacion manual del demo
- `legal_entity`: contexto organizativo minimo
- `country`: contexto geografico para lectura del caso
- `cost_center`: ayuda para drill-down y filtros futuros
- `payroll_period`: periodo sobre el cual aplica la elegibilidad
- `is_childcare_eligible`: marca booleana de elegibilidad para `CHILDCARE`

### Uso en elegibilidad por concepto

En esta primera version, `employee_reference.csv` se usara sobre todo para
`CHILDCARE`.

La logica base sera:

- existe una poblacion elegible esperada para el periodo
- parte de esa poblacion puede no aparecer en `payroll.csv` con el concepto
- esa brecha ayuda a explicar una diferencia de tipo `missing population`

Mas adelante el archivo podria ampliarse para otros beneficios selectivos, pero
eso no es obligatorio para el MVP inicial.

### Relacion con el producto

Dentro de una corrida, `employee_reference.csv` funcionara como referencia
auxiliar opcional pero prevista dentro del flujo base del demo.

La secuencia esperada es:

1. cargar `payroll.csv`
2. cargar `expected_totals.csv`
3. cargar `employee_reference.csv` cuando la corrida requiera validar
   elegibilidad
4. cruzar elegibilidad esperada contra poblacion observada
5. explicar faltantes de cobertura en conceptos selectivos

### Decision de simplificacion

Para proteger el tiempo de build del MVP:

- el archivo no modelara reglas HR complejas
- no se versionaran decenas de flags por beneficio
- no se intentara convertirlo en maestro global de empleados

## Universo de empleados del demo

### Tamaño objetivo

Desde `Card 1.3.1` queda fijado que el universo target del demo sera de:

- `360 empleados`

Ese valor se considera el punto de diseno recomendado para el MVP porque:

- permite suficiente volumen para que la conciliacion se sienta real
- sostiene varios conceptos repetidos sobre una base poblacional creible
- habilita casos wow sin que el dataset se vuelva pesado de operar
- mantiene el drill-down legible para demo comercial

### Rango aceptable

Aunque el target de trabajo queda fijado en `360`, el rango aceptable del MVP
sera:

- `300-500 empleados`

Ese rango protege flexibilidad operativa en la generacion del dataset sin
romper la narrativa del producto.

Por debajo de `300` empleados el demo empieza a sentirse demasiado pequeno y
artificial.

Por encima de `500` empleados el volumen deja de agregar valor claro al MVP y
puede introducir complejidad innecesaria en construccion, QA y demo.

### Composicion esperada del universo

El universo del demo no buscara representar una estructura HR exhaustiva. Su
objetivo es sostener una nomina plausible, diversa y util para conciliacion.

La composicion esperada sera:

- una mayoria de empleados regulares con conceptos recurrentes de nomina
- un subconjunto menor con beneficios selectivos
- un subconjunto menor con conceptos variables o extraordinarios
- unos pocos casos especiales diseniados para sostener diferencias explicables

### Perfiles estandar

Como base del dataset, se asumen estos perfiles estandar:

- empleados administrativos con conceptos estables y baja variabilidad
- empleados operativos con presencia ocasional de `OVERTIME`
- empleados con beneficios comunes como `MEAL_VOUCHER` o `TRANSPORT`
- empleados con deducciones regulares como `SOCIAL_SECURITY` e `INCOME_TAX`

Estos perfiles ayudan a que la mayor parte del universo se comporte de forma
esperable y sostenga una distribucion sana de conceptos reconciliados.

### Casos especiales del demo

Ademas del universo base, el dataset debera incluir algunos casos especiales
deliberados.

Los casos especiales esperados son:

- empleados elegibles para `CHILDCARE` que no aparezcan observados en el
  payroll del periodo
- pocos empleados con importes extraordinarios de `OVERTIME` para sostener
  outliers claros
- algunos registros con variaciones o errores controlados en conceptos
  protagonistas del demo
- empleados con combinacion de beneficios y conceptos variables para enriquecer
  el drill-down

### Criterio narrativo

El universo de `360 empleados` no existe para impresionar por volumen. Existe
para que el usuario perciba que:

- hay una base poblacional suficientemente real
- los conceptos wow no estan fabricados sobre una muestra diminuta
- las diferencias pueden explicarse sobre patrones plausibles de operacion

### Relacion con las siguientes cards

Esta decision deja cerrado el tamano y la composicion minima del universo, pero
todavia no cierra:

- la distribucion exacta por `legal_entity`
- la distribucion exacta por `country`
- la lista final de `cost_centers`
- la asignacion concreta de empleados a conceptos y anomalias

Eso se completa en:

- `Card 1.3.2`
- `Feature 1.4`
- `Feature 1.6`

## Estructura organizativa del dataset

### Principio de diseno

Desde `Card 1.3.2` queda definido que el dataset demo incluira textura
organizativa suficiente para sentirse real, pero sin convertir esa dimension en
el eje de conciliacion del MVP.

La regla de diseno es simple:

- `legal_entity`, `country` y `cost_center` enriquecen el analisis
- no gobiernan la unidad base de conciliacion
- la comparacion principal sigue ocurriendo sobre `payroll_period + concept_code`

### `legal_entities` del MVP

Para el demo base se define un set acotado de entidades legales:

- `ARD Spain SL`
- `ARD Iberia Services SL`
- `ARD Portugal Unipessoal Lda`

La intencion de esta lista no es modelar una estructura corporativa compleja,
sino aportar realismo suficiente para:

- mostrar que el payroll puede venir de mas de una entidad
- habilitar filtros y drill-down mas creibles
- sostener una narrativa regional iberica con foco comercial claro

### Foco principal en Espana

El pais principal del demo sera:

- `Spain`

La mayor parte del universo de empleados y de los registros de `payroll.csv`
debera concentrarse en Espana.

Esto ayuda a:

- mantener coherencia con el contexto funcional ya definido
- simplificar la narrativa del demo comercial
- evitar dispersion geografica innecesaria en la explicacion

### Distribucion simple por pais

La distribucion geografica recomendada para el MVP sera deliberadamente simple:

- mayoria clara de registros en `Spain`
- minoria acotada en `Portugal`

No hace falta que ambos paises tengan el mismo peso ni la misma riqueza de
casos.

El objetivo es que `Portugal` aporte variacion organizativa visible, sin
competir con el escenario principal del demo.

### Lista acotada de `cost_centers`

Para el MVP se define una lista pequena y legible de `cost_centers`:

- `FIN-ADM`
- `HR-OPS`
- `SALES`
- `TECH`
- `CUSTOMER_SUCCESS`
- `SHARED_SERVICES`

Esta lista esta pensada para:

- dar textura realista a los registros individuales
- habilitar filtros simples en drill-down futuro
- sostener explicaciones mas creibles cuando se revisen poblaciones o outliers

### Rol funcional de estas dimensiones

En el MVP base:

- `legal_entity` agrega contexto organizativo de alto nivel
- `country` aporta lectura geografica del caso
- `cost_center` agrega granularidad util para exploracion posterior

Sin embargo, estas dimensiones no cambian la definicion del core del producto.

La conciliacion principal:

- no se cerrara por entidad legal
- no se cerrara por pais
- no se cerrara por cost center
- seguira centrada en el total por concepto dentro del periodo

### Relacion con el demo

Estas dimensiones se incluyen porque mejoran la credibilidad del producto
cuando el usuario baja desde el resumen hacia registros concretos.

Permiten que el drill-down muestre un universo mas plausible y que algunas
explicaciones suenen menos abstractas, especialmente en:

- `missing population`
- `outlier`
- revisiones manuales de conceptos con diferencia

### Limites del alcance

Para proteger el tiempo de build del MVP:

- no se modelaran jerarquias organizativas complejas
- no habra consolidacion por multiples niveles contables
- no se intentara reconciliar por subpoblaciones organizativas en esta epic

### Relacion con las siguientes cards

Esta card deja cerrada la textura organizativa minima del dataset, pero todavia
no cierra:

- la lista final de conceptos del MVP
- la asignacion exacta de conceptos por perfil de empleado
- la tabla objetivo final de expected vs observed por concepto

Eso se completa en:

- `Feature 1.4`
- `Feature 1.6`
- `Feature 1.7`

## Universo de conceptos del MVP

### Criterio de seleccion

Desde `Card 1.4.1` queda definida una lista cerrada de conceptos para el MVP.

La seleccion no busca cubrir toda la complejidad de una nomina real. Busca un
set que sea:

- entendible en pocos segundos por un usuario de Contabilidad
- suficientemente realista para una demo vendible
- util para construir conceptos reconciliados, menores y wow cases
- manejable para explicacion, UI y tabla de resumen

### Lista objetivo de conceptos

El universo canonico del MVP quedara compuesto por `10 conceptos`:

- `BASE_SALARY`
- `BONUS`
- `MEAL_VOUCHER`
- `CHILDCARE`
- `TRANSPORT`
- `HEALTH_INSURANCE`
- `SOCIAL_SECURITY`
- `INCOME_TAX`
- `OVERTIME`
- `OTHER_ADJUSTMENT`

Esta lista cumple el objetivo definido en la epic de trabajar con un set
acotado de `8-10 conceptos`, sin perder riqueza narrativa.

### Racional funcional por concepto

- `BASE_SALARY`: ancla principal del payroll y referencia de volumen estable
- `BONUS`: agrega variabilidad controlada sobre un concepto conocido
- `MEAL_VOUCHER`: beneficio recurrente ideal para el wow principal del demo
- `CHILDCARE`: beneficio selectivo ideal para explicar `missing population`
- `TRANSPORT`: beneficio simple apto para diferencias menores
- `HEALTH_INSURANCE`: beneficio recurrente y creible para completar cobertura
- `SOCIAL_SECURITY`: deduccion estructural esperable en cualquier payroll
- `INCOME_TAX`: deduccion estructural facil de reconocer por negocio
- `OVERTIME`: concepto variable apto para outliers y analisis puntual
- `OTHER_ADJUSTMENT`: concepto comodin controlado para ajustes plausibles

### Balance entre conceptos limpios y protagonistas

Para la narrativa del MVP, no todos los conceptos deben comportarse igual.

Se define esta separacion funcional:

- conceptos principalmente limpios o estables:
  `BASE_SALARY`, `HEALTH_INSURANCE`, `SOCIAL_SECURITY`, `INCOME_TAX`
- conceptos con variabilidad controlada:
  `BONUS`, `OTHER_ADJUSTMENT`
- conceptos protagonistas del demo:
  `MEAL_VOUCHER`, `CHILDCARE`, `OVERTIME`, `TRANSPORT`

### Por que esta mezcla funciona para el demo

Esta combinacion permite que el resumen final se sienta creible:

- hay conceptos grandes y previsibles que deberian cerrar bien
- hay conceptos con pequenas variaciones plausibles
- hay pocos conceptos especialmente utiles para contar la historia del producto

Eso protege el principio clave del MVP:

- la mayoria de los conceptos deben verse sanos
- algunos deben requerir revision
- muy pocos deben concentrar el momento wow

### Relacion con las siguientes cards

Esta card deja cerrada la lista canonica de conceptos, pero todavia no cierra:

- la categoria funcional de cada concepto
- el signo esperado por concepto
- cuales quedan como wow principal, wow secundario o caso amarillo
- la distribucion final de estados por concepto

Eso se completa en:

- `Card 1.4.2`
- `Card 1.4.3`
- `Feature 1.6`

## Categorias y signos esperados por concepto

### Objetivo de esta definicion

Desde `Card 1.4.2` queda documentada la metadata minima necesaria para poder
volcar el universo de conceptos a `concept_master.csv` sin ambiguedad.

Cada concepto del MVP queda asociado a:

- una categoria funcional
- un signo esperado
- su condicion de candidato o no a `sign error`

### Tabla funcional por concepto

| Concepto | Categoria | Signo esperado | Candidato a `sign error` | Racional breve |
| --- | --- | --- | --- | --- |
| `BASE_SALARY` | `salary` | `positive` | `no` | componente principal y estable del payroll |
| `BONUS` | `bonus` | `positive` | `no` | pago variable pero naturalmente positivo |
| `MEAL_VOUCHER` | `benefit` | `positive` | `si` | beneficio recurrente donde un signo incorrecto seria claramente anomalo |
| `CHILDCARE` | `benefit` | `positive` | `si` | beneficio selectivo donde una inversion de signo seria facil de detectar |
| `TRANSPORT` | `benefit` | `positive` | `si` | beneficio simple apto para validar consistencia de polaridad |
| `HEALTH_INSURANCE` | `benefit` | `positive` | `si` | beneficio esperable cuya inversion seria poco creible y visible |
| `SOCIAL_SECURITY` | `deduction` | `negative` | `si` | deduccion estructural donde el signo incorrecto rompe la lectura contable |
| `INCOME_TAX` | `deduction` | `negative` | `si` | deduccion estructural de alta visibilidad para negocio |
| `OVERTIME` | `variable_compensation` | `positive` | `no` | concepto variable donde el foco analitico principal sera outlier, no polaridad |
| `OTHER_ADJUSTMENT` | `adjustment` | `positive` | `si` | ajuste controlado donde un signo invertido puede servir como caso opcional |

### Criterio de categorias

Las categorias funcionales elegidas para el MVP son:

- `salary`
- `bonus`
- `benefit`
- `deduction`
- `variable_compensation`
- `adjustment`

No hace falta crear una taxonomia mas fina en esta etapa. Estas categorias ya
son suficientes para:

- ordenar el universo de conceptos
- enriquecer explicaciones
- apoyar filtros o agrupaciones futuras
- mantener `concept_master.csv` simple y legible

### Criterio de signos esperados

Para el MVP se adopta esta convencion:

- conceptos de pago o beneficio hacia el empleado: `positive`
- conceptos de deduccion o retencion: `negative`

Eso deja una lectura consistente para:

- conciliacion por concepto
- deteccion opcional de `sign error`
- explicaciones template-based

### Conceptos candidatos a `sign error`

Los candidatos mas claros a `sign error` en el MVP seran:

- `MEAL_VOUCHER`
- `CHILDCARE`
- `TRANSPORT`
- `HEALTH_INSURANCE`
- `SOCIAL_SECURITY`
- `INCOME_TAX`
- `OTHER_ADJUSTMENT`

La idea no es saturar el dataset con este tipo de anomalia, sino dejar
predefinidos los conceptos donde la contradiccion de signo seria interpretable
por el motor y por el usuario.

### Conceptos no priorizados para `sign error`

En esta etapa no se prioriza `sign error` para:

- `BASE_SALARY`
- `BONUS`
- `OVERTIME`

Motivo:

- `BASE_SALARY` debe comportarse como ancla sana del demo
- `BONUS` aporta variabilidad, pero no necesita complejidad extra todavia
- `OVERTIME` ya tiene un rol narrativo mas fuerte como caso de outlier

### Relacion con las siguientes cards

Esta card deja cerradas categorias y signos esperados, pero todavia no cierra:

- el rol exacto de cada concepto en la narrativa comercial
- cuales seran wow principal, wow secundario y caso amarillo
- la distribucion final de estados y anomalias por concepto

Eso se completa en:

- `Card 1.4.3`
- `Feature 1.6`

## Conceptos estrella del demo

### Objetivo narrativo

Desde `Card 1.4.3` quedan definidos los conceptos que sostendran la narrativa
principal del MVP.

La idea no es que todos los conceptos compitan por atencion. La demo debe guiar
al usuario hacia pocos casos memorables y faciles de explicar.

### Caso wow principal

El caso wow principal del demo sera:

- `MEAL_VOUCHER`

Se fija como caso principal porque combina muy bien los atributos que mas valor
le dan al producto:

- diferencia visible en el resumen
- explicacion multi-causa plausible
- posibilidad de bajar a registros concretos
- narrativa clara para mostrar por que los numeros no cierran

`MEAL_VOUCHER` es el mejor candidato para abrir en vivo durante la demo
comercial.

### Caso de poblacion faltante

El caso principal de `missing population` sera:

- `CHILDCARE`

Se elige porque:

- necesita cruce con `employee_reference.csv`
- permite mostrar elegibilidad esperada vs poblacion observada
- produce una explicacion muy intuitiva para negocio

Su rol en la narrativa es mostrar que el producto no solo compara montos, sino
que tambien puede explicar brechas de cobertura o poblacion.

### Caso analitico de outlier

El caso analitico principal de outlier sera:

- `OVERTIME`

Se elige porque:

- permite mostrar uno o pocos registros con impacto desproporcionado
- hace muy natural el drill-down a nivel fila
- refuerza la idea de analisis puntual y accionable

Su funcion dentro del demo es complementar al wow principal con una historia
mas analitica y menos poblacional.

### Caso amarillo de diferencia menor

El caso amarillo del demo sera:

- `TRANSPORT`

Su rol no es competir con `MEAL_VOUCHER`, sino aportar realismo.

Se incluye como caso amarillo porque:

- sostiene una diferencia menor creible
- permite mostrar que no todo desvio es dramatico
- ayuda a balancear el resumen entre verdes, amarillos y rojos

### Jerarquia narrativa resultante

Con esta definicion, la jerarquia narrativa del MVP queda asi:

- wow principal: `MEAL_VOUCHER`
- wow secundario de poblacion: `CHILDCARE`
- wow secundario analitico: `OVERTIME`
- caso amarillo de soporte: `TRANSPORT`

### Relacion con la demo comercial

Esta seleccion sostiene una demo de 5 a 8 minutos con una progresion clara:

1. mostrar resumen ejecutivo
2. abrir `MEAL_VOUCHER` como caso principal
3. reforzar profundidad con `CHILDCARE` o `OVERTIME`
4. mostrar `TRANSPORT` como ejemplo de diferencia menor y controlada

Asi el producto se percibe:

- explicativo
- creible
- accionable
- no dependiente de un unico truco visual

### Relacion con las siguientes cards

Esta card deja cerrados los conceptos estrella, pero todavia no cierra:

- el periodo principal del demo
- los casos `out-of-period`
- la distribucion final de estados por concepto
- las anomalias concretas a inyectar en cada concepto protagonista

Eso se completa en:

- `Feature 1.5`
- `Feature 1.6`

## Periodo principal del MVP

### Periodo objetivo

Desde `Card 1.5.1` queda fijado que el periodo principal del demo sera:

- `2026-03`

Este sera el corte temporal central sobre el cual se diseniara la corrida del
MVP.

### Por que se elige `2026-03`

Se toma `2026-03` porque ya aparece alineado con el plan maestro y funciona
bien como referencia unica para:

- `payroll.csv`
- `expected_totals.csv`
- `employee_reference.csv`
- resumen ejecutivo
- demo comercial y narrativa de explicacion

Al fijar un solo periodo central, el producto gana claridad y reduce
ambiguedad operativa.

### Regla para los datos esperados y observados

Desde esta card queda definido que:

- `expected_totals.csv` representara los totales esperados de `2026-03`
- la gran mayoria de las lineas de `payroll.csv` pertenecera a `2026-03`
- la elegibilidad principal de `employee_reference.csv` tambien se modelara
  para `2026-03`

Esto significa que el dataset del MVP se construira alrededor de un unico mes
principal y no como una serie historica completa.

### Impacto en la experiencia del producto

Al ejecutar una corrida del demo, el usuario deberia percibir con claridad que:

- el periodo analizado es `2026-03`
- los expected totals fueron preparados para ese mismo mes
- las diferencias se explican contra ese corte temporal

Eso ayuda a que la lectura del summary sea inmediata y que los casos wow se
entiendan sin contexto adicional.

### Alcance temporal del MVP

El MVP no necesita modelar comparativas mensuales, tendencias ni multiples
cierres simultaneos.

En esta etapa alcanza con:

- un periodo principal fuerte
- pocos registros de borde para excepciones temporales

La complejidad temporal adicional se deja fuera del alcance inicial para
proteger time-to-demo.

### Relacion con las siguientes cards

Esta card deja cerrado el periodo principal del demo, pero todavia no cierra:

- la definicion exacta de `out-of-period`
- el uso de `2026-02` como periodo incorrecto inyectado
- el rol de `posting_date` como refuerzo narrativo de anomalias temporales

Eso se completa en:

- `Card 1.5.2`

## Reglas temporales y casos out-of-period

### Definicion de `out-of-period`

Desde `Card 1.5.2` queda definido que un registro estara `out-of-period` cuando:

- la corrida se ejecute para `2026-03`
- y el valor de `payroll_period` del registro sea distinto de `2026-03`

Para el MVP, la senal principal de esta anomalia sera `payroll_period`.

`posting_date` podra reforzar la lectura del caso, pero no reemplaza la regla
base.

### Regla temporal del demo

La corrida principal del MVP se entiende asi:

- periodo objetivo de analisis: `2026-03`
- expected totals preparados para `2026-03`
- mayoria de registros observados correspondientes a `2026-03`

Sobre esa base, el dataset podra incluir pocos registros deliberadamente fuera
de periodo para sostener explicaciones creibles.

### Uso de `2026-02` como periodo incorrecto inyectado

El periodo incorrecto recomendado para inyectar en el demo sera:

- `2026-02`

La razon es simple:

- es el mes inmediatamente anterior
- resulta intuitivo para negocio
- hace que la explicacion temporal se entienda en segundos

No hace falta introducir varios meses erroneos. Con `2026-02` alcanza para
crear una anomalia temporal clara sin ensuciar el dataset.

### Uso de `posting_date` inconsistente

Ademas del `payroll_period`, el campo `posting_date` podra utilizarse como
refuerzo narrativo.

Su uso recomendado en el MVP es:

- acompañar registros cuyo `payroll_period` sea `2026-02`
- o mostrar fechas de imputacion que no calzan naturalmente con la corrida de
  marzo 2026

Esto ayuda a construir explicaciones mas convincentes, por ejemplo:

- lineas etiquetadas como febrero dentro de un archivo del periodo marzo
- fechas de posting que hacen visible el arrastre temporal

### Jerarquia de evidencia temporal

Para evitar ambiguedad en el futuro motor, la jerarquia queda asi:

1. la regla principal se evalua con `payroll_period`
2. `posting_date` funciona como evidencia adicional
3. la explicacion final puede mencionar ambas senales cuando convenga

### Uso narrativo recomendado

La anomalia temporal debe ayudar a contar una historia concreta, no a agregar
ruido.

Ejemplo de narrativa esperada:

"Se detectaron lineas de `MEAL_VOUCHER` correspondientes a `2026-02` dentro de
la corrida objetivo de `2026-03`, reforzadas por fechas de posting
inconsistentes."

Este tipo de explicacion es:

- facil de entender
- plausible para negocio
- fuerte para demo comercial

### Limites del alcance

Para proteger simplicidad y time-to-demo:

- no se modelaran calendarios complejos
- no se definiran reglas avanzadas de cierre contable
- no se hara reconciliacion multi-periodo en esta epic

### Relacion con las siguientes cards

Esta card deja cerrada la logica temporal del demo, pero todavia no cierra:

- cuantas anomalias temporales habra por concepto
- en que conceptos exactos se inyectaran
- como se combinan con duplicates, unmapped o outliers

Eso se completa en:

- `Feature 1.6`

## Distribucion objetivo de estados

### Objetivo de balance

Desde `Card 1.6.1` queda definida una distribucion objetivo de estados para el
demo.

El objetivo no es maximizar errores. El objetivo es que el dataset se sienta
real:

- la mayoria de los conceptos debe cerrar bien
- algunos deben mostrar diferencias menores
- pocos deben concentrar los casos mas interesantes

### Distribucion target del MVP

Con un universo de `10 conceptos`, la distribucion objetivo queda asi:

- `6 / 10` conceptos `reconciled` -> `60%`
- `2 / 10` conceptos `minor difference` -> `20%`
- `2 / 10` conceptos `unreconciled` -> `20%`

Esta distribucion cae dentro del rango narrativo esperado para el MVP:

- `60%-70%` reconciled
- `20%-25%` minor difference
- `10%-20%` unreconciled

### Conceptos por banda de estado

La asignacion target por concepto sera:

- `reconciled`:
  `BASE_SALARY`, `BONUS`, `HEALTH_INSURANCE`, `SOCIAL_SECURITY`,
  `INCOME_TAX`, `OTHER_ADJUSTMENT`
- `minor difference`:
  `TRANSPORT`, `OVERTIME`
- `unreconciled`:
  `MEAL_VOUCHER`, `CHILDCARE`

### Racional narrativo

Esta distribucion funciona bien para el demo porque:

- deja una base amplia de conceptos sanos y creibles
- reserva pocos conceptos para revision real
- hace que los casos wow destaquen sin que todo el summary se vea rojo

Ademas:

- `MEAL_VOUCHER` y `CHILDCARE` sostienen los rojos mas demostrables
- `TRANSPORT` y `OVERTIME` permiten mostrar criterio y matiz analitico
- los conceptos estructurales del payroll se mantienen mayormente estables

## Catalogo de anomalias del demo

### Principio general

Desde `Card 1.6.2` queda definido que el dataset usara un catalogo acotado de
anomalias deliberadas.

La regla es:

- pocas anomalias
- claras
- cuantificables
- distribuidas

### Anomalias objetivo del MVP

El catalogo base del MVP quedara compuesto por:

- `duplicates`
- `unmapped concept`
- `out-of-period`
- `missing population`
- `outlier`
- `sign error` opcional

### Volumen esperado por tipo

Para no saturar el dataset con ruido, el volumen objetivo sera:

- `duplicates`: `3` lineas
- `unmapped concept`: `5` lineas
- `out-of-period`: `8` lineas
- `missing population`: `6` empleados elegibles ausentes
- `outlier`: `1-2` registros fuertes
- `sign error`: `0` en el seed inicial, reservado como anomalia opcional

### Rol funcional de cada anomalia

- `duplicates`: sostener explicaciones de sobreconteo o ruido operacional
- `unmapped concept`: demostrar valor de `concept_master.csv`
- `out-of-period`: reforzar lectura temporal del motor
- `missing population`: mostrar explicacion basada en elegibilidad
- `outlier`: sostener drill-down analitico claro
- `sign error`: dejar abierta una expansion futura sin cargar el seed inicial

### Regla de higiene narrativa

El seed inicial no debe usar todas las anomalias en todos los conceptos.

El objetivo es que cada anomalia:

- tenga un lugar claro
- pueda explicarse rapido
- no opaque el resto del dataset

## Anomalias concretas por concepto

### `MEAL_VOUCHER`

Desde `Card 1.6.3`, `MEAL_VOUCHER` queda diseñado como el caso multi-causa del
demo.

Anomalias concretas:

- `8` lineas con `payroll_period = 2026-02`
- `3` posibles duplicados
- `5` lineas con codigo no mapeado `MEAL_VCHR`

Resultado narrativo esperado:

- diferencia material
- mezcla de temporalidad, mapping y calidad de carga
- explicacion rica para summary y concept analysis

### `CHILDCARE`

`CHILDCARE` queda diseñado como el caso principal de `missing population`.

Anomalias concretas:

- `6` empleados elegibles ausentes respecto a `employee_reference.csv`
- `2` registros observados con importe inferior al esperado

Resultado narrativo esperado:

- diferencia negativa clara
- explicacion centrada en poblacion faltante
- lectura muy entendible para negocio

### `OVERTIME`

`OVERTIME` queda diseñado como caso analitico de outlier con estado amarillo.

Anomalias concretas:

- `1` registro principal con importe mayor a `5x` la mediana del concepto
- `1` segundo registro alto, pero no dominante, como apoyo analitico opcional

Resultado narrativo esperado:

- diferencia menor o moderada
- explicacion dominada por outlier
- drill-down fuerte sin convertir el concepto en rojo principal

### `TRANSPORT`

`TRANSPORT` queda diseñado como caso amarillo de diferencia menor.

Anomalias concretas:

- `4` importes parciales o microdesvios
- sin outliers extremos
- sin ruido adicional innecesario

Resultado narrativo esperado:

- diferencia acotada
- caso util para mostrar bandas de tolerancia
- resumen mas creible y menos binario

## Tabla maestra de control por concepto

### Objetivo

Desde `Card 1.7.1` queda definida la tabla cuantitativa maestra del demo.

Esta tabla sera la referencia de control para:

- dataset
- expected totals
- validacion de consistencia
- narrativa comercial

### Tabla maestra

| concepto | expected | observed | diff | estado target | explicacion_principal |
| --- | ---: | ---: | ---: | --- | --- |
| `BASE_SALARY` | `1200000.00` | `1200010.00` | `10.00` | `reconciled` | redondeo insignificante |
| `BONUS` | `48000.00` | `48000.00` | `0.00` | `reconciled` | pagos variables dentro de lo esperado |
| `MEAL_VOUCHER` | `42000.00` | `38820.00` | `-3180.00` | `unreconciled` | out-of-period + unmapped + duplicates |
| `CHILDCARE` | `18500.00` | `17050.00` | `-1450.00` | `unreconciled` | missing eligible population |
| `TRANSPORT` | `21000.00` | `20760.00` | `-240.00` | `minor_difference` | diferencias menores en importes parciales |
| `HEALTH_INSURANCE` | `18000.00` | `18000.00` | `0.00` | `reconciled` | beneficio estable sin desvio material |
| `SOCIAL_SECURITY` | `-216000.00` | `-216000.00` | `0.00` | `reconciled` | deduccion estructural estable |
| `INCOME_TAX` | `-198000.00` | `-198000.00` | `0.00` | `reconciled` | retencion estable y coherente |
| `OVERTIME` | `14000.00` | `14950.00` | `950.00` | `minor_difference` | un registro atipico eleva el total |
| `OTHER_ADJUSTMENT` | `3200.00` | `3180.00` | `-20.00` | `reconciled` | ajuste menor dentro de tolerancia |

### Coherencia matematica y narrativa

Esta tabla fue elegida para que:

- los conceptos grandes den sensacion de estabilidad
- los casos wow tengan diferencias visibles pero plausibles
- el resumen final no quede dominado por errores artificiales

### Coherencia de estados

La tabla maestra respeta la distribucion objetivo definida antes:

- `6` reconciled
- `2` minor difference
- `2` unreconciled

## Metodo de construccion del dataset

### Regla recomendada

Desde `Card 1.7.2` queda definido que el metodo recomendado sera:

1. construir un payroll observado base creible
2. fijar la tabla maestra por concepto
3. derivar `expected_totals.csv` coherentes con esa tabla
4. inyectar anomalias controladas en conceptos concretos
5. verificar que el resultado final preserve estados y narrativa target

### Enfoque conceptual

El dataset no se construira ni completamente manual ni completamente aleatorio.

La logica sera:

- base observada generada de forma deterministica
- expected totals curados para sostener estados target
- anomalias inyectadas deliberadamente

### Que se genera y que se cura manualmente

Elementos principalmente generados:

- `employee_reference.csv`
- gran parte de `payroll.csv`

Elementos principalmente curados:

- tabla maestra de control
- `expected_totals.csv`
- definicion de anomalias por concepto
- `concept_master.csv`

### Criterio de reproducibilidad

El dataset debe poder regenerarse sin reinterpretar la logica del demo.

Por eso:

- la verdad narrativa vive en esta documentacion
- la materializacion se resuelve con una generacion deterministica
- el resultado final debe ser inspeccionable dentro del repo

## Estrategia de generacion del dataset

### Decision de estrategia

Desde `Card 1.8.1` queda definida una estrategia `hibrida`.

La estrategia elegida combina:

- generacion programatica deterministica
- curacion manual de objetivos narrativos

### Por que se elige un enfoque hibrido

Este enfoque protege simultaneamente:

- control narrativo
- reproducibilidad
- velocidad de mantenimiento

Una generacion totalmente manual haria mas lento ajustar el dataset.

Una generacion totalmente automatica pondria en riesgo la historia comercial.

### Carpeta destino

Los archivos demo iniciales del MVP viviran en:

- `data/demo_seed/`

Dentro de esa carpeta el repo debera contener:

- archivos CSV resultantes
- un script simple de regeneracion deterministica

### Regla operativa para el seed

El seed inicial debe:

- poder inspeccionarse directamente en el repo
- poder regenerarse sin tocar logica del producto
- mantenerse alineado con la tabla maestra de control

## Archivos demo iniciales materializados

### Estado del seed inicial

Desde `Card 1.8.2` el repo ya contiene un seed inicial materializado en:

- `data/demo_seed/payroll.csv`
- `data/demo_seed/expected_totals.csv`
- `data/demo_seed/concept_master.csv`
- `data/demo_seed/employee_reference.csv`
- `data/demo_seed/generate_dataset.py`

### Consistencia basica validada

El seed inicial queda validado a nivel estructural con estas referencias:

- `360` empleados en `employee_reference.csv`
- `3268` lineas en `payroll.csv`
- `10` filas en `expected_totals.csv`
- `10` filas en `concept_master.csv`

### Coherencia con la tabla maestra

El seed generado queda alineado con la tabla maestra documentada para los
conceptos canonicos del MVP.

Tambien incorpora las anomalias clave previstas:

- `8` lineas `out-of-period`
- `5` lineas `unmapped concept`
- `3` duplicados intencionales
- `6` empleados elegibles ausentes en `CHILDCARE`

### Criterio de reutilizacion

Estos archivos pasan a ser la base versionada de trabajo para:

- desarrollo del motor
- pruebas locales del backend
- validacion temprana de flujos y payloads
- futuras corridas de demo controlada

Su objetivo en esta etapa es resolver, de manera creible, el caso de
`missing population` sin inflar el sistema.

### Notas para las siguientes cards

Esta card deja decidido que el archivo entra al MVP y define su estructura
minima, pero todavia no cierra:

- el volumen final de empleados elegibles
- los valores concretos del caso `CHILDCARE`
- si luego se agregan flags para otros beneficios

Eso se completara cuando se diseñe el universo de empleados y los casos wow del
dataset.

## Esquema base de `payroll.csv`

### Columnas cerradas del archivo

Desde esta card queda definida la siguiente estructura base para `payroll.csv`:

- `record_id`
- `employee_id`
- `employee_name`
- `legal_entity`
- `country`
- `cost_center`
- `payroll_period`
- `posting_date`
- `concept_code`
- `concept_name`
- `amount`
- `currency`

### Proposito funcional de cada columna

- `record_id`: identificador unico por fila para trazabilidad y drill-down
- `employee_id`: llave principal para agrupar registros por empleado
- `employee_name`: apoyo visual para lectura humana y demo comercial
- `legal_entity`: contexto organizativo de la linea de payroll
- `country`: contexto geografico del empleado o registro
- `cost_center`: dimension organizativa util para filtros y explicacion
- `payroll_period`: periodo contable o de nomina al que pertenece la linea
- `posting_date`: fecha de imputacion o contabilizacion del registro
- `concept_code`: codigo del concepto observado en la fuente
- `concept_name`: descripcion legible del concepto observado
- `amount`: importe monetario de la linea
- `currency`: moneda en que viene expresado el importe

### Por que este esquema es suficiente para el MVP

Este esquema sostiene las tres necesidades clave del producto:

- conciliacion:
  permite agregar por `concept_code`, periodo y otras dimensiones si hiciera
  falta
- explicacion:
  preserva suficiente contexto para entender de donde viene una diferencia
- drill-down:
  permite bajar desde resumen a fila individual con identidad clara

### Cobertura de los casos wow

La estructura definida cubre los casos wow ya planteados para el demo:

- `MEAL_VOUCHER`:
  puede observarse como concepto con multiples lineas por empleado
- `CHILDCARE`:
  puede cruzarse con `employee_reference.csv` para analizar poblacion faltante
- `OVERTIME`:
  puede analizarse por concepto y monto para detectar outliers plausibles

Ademas, `posting_date`, `concept_code` y `amount` ayudan a sostener
excepciones futuras como:

- `out-of-period`
- `unmapped concept`
- `sign error`
- `outlier`

### Notas para las siguientes cards

Esta card cierra la lista de columnas, pero todavia no cierra:

- tipos concretos por columna
- formatos esperados
- reglas de calidad del input

Esos puntos se completan en:

- `Card 1.2.2`
- `Card 1.2.3`

## Tipos y convenciones de `payroll.csv`

### Tipos sugeridos por columna

Para el MVP, estas son las convenciones de tipo recomendadas:

- `record_id`: string
- `employee_id`: string
- `employee_name`: string
- `legal_entity`: string
- `country`: string
- `cost_center`: string
- `payroll_period`: string con formato controlado
- `posting_date`: date
- `concept_code`: string
- `concept_name`: string
- `amount`: decimal
- `currency`: string

### Convenciones de formato

Desde esta card quedan fijadas estas convenciones base:

- `payroll_period` se expresa como `YYYY-MM`
- `posting_date` se expresa como fecha ISO `YYYY-MM-DD`
- la moneda principal del demo es `EUR`
- `amount` se expresa con 2 decimales
- `concept_code` se normaliza en mayusculas

### Notas practicas por campo

- `record_id` debe poder serializarse sin transformaciones especiales
- `employee_id` no debe tratarse como entero, para evitar perdida de formato
- `employee_name` mantiene capitalizacion legible para UI y drill-down
- `legal_entity`, `country` y `cost_center` se almacenan como texto estable
- `concept_name` preserva legibilidad humana aunque exista mapping canonico
- `currency` admite texto corto ISO, aunque en el demo el valor dominante sera
  `EUR`

### Convencion para montos

El campo `amount` debe representar el valor monetario de la linea con precision
de 2 decimales.

La expectativa del MVP es:

- usar punto decimal
- no incluir separadores de miles en el CSV
- conservar signo explicito cuando aplique

### Convencion para periodos y codigos

El periodo principal del demo se modela a nivel mensual, por eso
`payroll_period` queda estandarizado como `YYYY-MM`.

`concept_code` debe venir ya normalizado en mayusculas para reducir ambiguedad
en:

- joins con `concept_master.csv`
- agregacion por concepto
- validaciones del motor

### Objetivo de estas convenciones

Estas decisiones buscan que el archivo sea:

- facil de generar
- facil de validar
- facil de leer manualmente
- consistente con el motor y la UI

### Notas para la siguiente card

Esta card cierra tipos y formatos base, pero todavia no define:

- que columnas son estrictamente obligatorias
- que errores se toleran como anomalias modelables
- que errores deben invalidar una corrida

Eso se cierra en `Card 1.2.3`.

## Supuestos de calidad e input valido de `payroll.csv`

### Baseline de input valido

El MVP no asume un archivo perfecto, pero si asume un baseline minimo de orden
y consistencia para poder ejecutar una corrida util.

El principio rector es:

- errores de negocio plausibles se modelan como excepciones explicables
- errores estructurales graves invalidan la corrida

### Columnas obligatorias

Para considerar que un `payroll.csv` es procesable en el MVP, estas columnas
son obligatorias:

- `record_id`
- `employee_id`
- `payroll_period`
- `posting_date`
- `concept_code`
- `amount`
- `currency`

Las siguientes columnas son esperadas y muy recomendables para una buena demo,
pero no necesariamente deben invalidar una corrida si el producto luego decide
soportar defaults o degradacion controlada:

- `employee_name`
- `legal_entity`
- `country`
- `cost_center`
- `concept_name`

### Errores tolerados como anomalias modelables

Estos casos no deben romper automaticamente la corrida, porque forman parte del
valor analitico del MVP:

- registros fuera del periodo esperado (`out-of-period`)
- conceptos sin mapping valido (`unmapped concept`)
- duplicados plausibles (`duplicates`)
- importes atipicos dentro de un concepto (`outlier`)
- signos inconsistentes respecto a lo esperado (`sign error`)
- faltantes de poblacion elegible (`missing population`)

La idea es que estos casos entren al motor, se detecten y luego se expliquen.

### Errores que deben romper la corrida

Estos casos deben invalidar la corrida porque impiden una lectura confiable del
dataset:

- falta de columnas obligatorias
- archivo vacio o sin filas procesables
- `amount` no parseable como valor numerico
- `posting_date` invalida o no parseable
- `payroll_period` ausente o fuera del formato esperado
- `currency` vacia de forma masiva o inconsistente al punto de impedir lectura
- archivos corruptos o delimitacion incompatible con el parser esperado

### Regla de realismo controlado

El dataset demo debe sentirse realista, pero no caotico.

Eso significa:

- se aceptan desvíos plausibles diseñados a propósito
- no se acepta suciedad estructural masiva que opaque la narrativa
- la corrida debe fallar solo cuando el input deja de ser interpretable

En otras palabras, queremos un universo donde los numeros no cierran por
motivos analizables, no por un CSV roto.

### Criterio operativo para futuras implementaciones

Cuando el backend procese `payroll.csv`, deberia seguir esta logica:

1. validar estructura minima del archivo
2. rechazar errores destructivos
3. procesar filas validas bajo convenciones conocidas
4. detectar anomalias modelables como parte del analisis

### Objetivo de esta separacion

Esta separacion protege dos cosas al mismo tiempo:

- la credibilidad tecnica del MVP
- la claridad comercial de la demo

Si todo error rompe la corrida, el producto pierde valor analitico.
Si nada rompe la corrida, el sistema pierde confiabilidad.

El balance correcto para el MVP es:

- tolerar anomalias explicables
- frenar inputs estructuralmente invalidos
