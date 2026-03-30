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
