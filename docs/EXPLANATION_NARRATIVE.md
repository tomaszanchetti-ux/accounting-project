# Narrative Structure for Explanations

## Objetivo

Este documento fija la estructura narrativa base de la capa explicativa del
MVP construida en `EPIC 03`.

La explicacion debe ser:

- util
- profesional
- sobria
- facil de serializar para API y UI

No debe sonar como log tecnico ni como texto literario.

## 1. Estructura estandar

Cada explicacion por concepto se organiza en tres capas:

1. `summary_statement`
2. `probable_causes`
3. `recommended_action`

## 2. Summary statement

El statement principal resume:

- concepto
- periodo
- estado general
- direccion de la diferencia cuando aplica

El tono esperado es:

- claro
- directo
- contable
- no alarmista

## 3. Probable causes

El bloque de causas:

- usa el ranking previo del motor
- muestra hasta `3` causas por concepto
- incluye evidencia resumida e impacto cuando existe
- preserva framing prudente para causas inferenciales

## 4. Framing de certeza

La narrativa distingue entre:

- deteccion fuerte
- causa probable
- señal analitica

Reglas base:

- `Duplicate Record` debe expresarse como probable
- `Missing Population` debe expresarse como explicacion operativa, no como
  certeza absoluta
- `Outlier Amount` debe expresarse como indicio dominante, no como veredicto
  final
- `Invalid Amount / Data Quality Issue` puede dominar el mensaje aunque no haya
  monto atribuible

## 5. Recomendacion final

La recomendacion final:

- toma la causa dominante
- propone un siguiente paso de revision
- mantiene tono profesional
- sirve tanto para summary como para concept analysis

## 6. Contrato estructurado

La salida estructurada por concepto debe incluir como minimo:

- `summary_statement`
- `probable_causes`
- `recommended_action`
- `explained_amount_estimate`
- `impacted_records_count`
- `impacted_employees_count`

Este contrato ya esta alineado con la implementacion del backend y preparado
para persistencia, API y UI.
