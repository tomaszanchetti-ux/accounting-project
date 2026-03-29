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
