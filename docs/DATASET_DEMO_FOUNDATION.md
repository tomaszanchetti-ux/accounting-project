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
