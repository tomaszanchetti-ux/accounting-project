# UI Foundation & Setup Flow

## Objetivo

Dejar una base visual y operativa consistente para `EPIC 05`, centrada en una
sola pantalla de setup capaz de crear una run, preparar inputs y disparar la
conciliacion sin friccion innecesaria.

## 1. Principios visuales del MVP

- `enterprise clean`: superficies sobrias, ritmo espacioso y eliminacion de
  ruido visual.
- `data-first`: el contenido principal son estados, inputs, KPIs y tablas, no
  ilustraciones ni charts decorativos.
- `claridad antes que ornamento`: cada bloque debe ayudar a entender si la run
  esta lista, corriendo o terminada.
- `color con proposito`: el color queda reservado para estados, alertas,
  readiness y reconciliacion.
- `jerarquia simple`: una sola accion primaria por pantalla, headings claros y
  metadata secundaria silenciosa.

## 2. Tono del producto

La interfaz debe sentirse:

- seria
- sobria
- ejecutiva-operativa
- orientada a control y trazabilidad

La pantalla no debe sonar tecnica ni experimental. El framing correcto es:

> preparar una corrida, confirmar insumos y ejecutar con confianza.

## 3. Paleta base y semantica

### Base

- `background`: `#f3f1ea`
- `background-accent`: `#e3dccd`
- `surface`: `#fcfbf7`
- `surface-strong`: `#f1ecdf`
- `surface-ink`: `#132033`
- `border-subtle`: `#d8d1c3`
- `text-primary`: `#1c2738`
- `text-secondary`: `#586579`
- `text-muted`: `#7b8697`

### Semantica de estados

- `Reconciled`: `#2d6a4f`
- `Minor Difference`: `#b7791f`
- `Unreconciled`: `#b23a48`
- `Invalid / Incomplete`: `#5a6472`
- `Info / Processing`: `#295c8a`

### Regla de uso

El color no entra como decoracion. Solo entra para:

- readiness
- loading
- alertas
- estado de conciliacion
- confirmacion de exito

## 4. Tipografia y jerarquia

### Tipografia base

- Sans principal: `IBM Plex Sans`
- Mono de soporte: `IBM Plex Mono`

### Escala

- `page title`: 44 / 52, semibold
- `section heading`: 24 / 32, semibold
- `card title`: 18 / 26, semibold
- `body`: 15 / 24, regular
- `metadata`: 13 / 18, medium

### Reglas de legibilidad

- Las tablas deben priorizar scan horizontal rapido y numeros alineados a la
  derecha.
- Los formularios deben mostrar labels cortos, helper text util y una sola idea
  por bloque.
- Los estados tecnicos van en texto pequeno y de bajo contraste; el usuario no
  deberia leer IDs ni jerga como paso principal.

## 5. Estructura de la pantalla `New Reconciliation Run`

La anatomia base queda asi:

1. Header de producto
2. Resumen de contexto de la run
3. Bloque principal de setup
4. Preview de expected totals
5. Resumen de validacion previa
6. CTA principal `Run Reconciliation`
7. Snapshot post-ejecucion

## 6. Exclusiones explicitas del MVP

No entra en la pantalla de setup:

- wizard largo
- multiples tabs
- configuracion avanzada de reglas
- edicion compleja de expected totals
- parametros tecnicos visibles
- charts decorativos
- navegacion densa estilo dashboard

## 7. Rational de exclusiones

- Wizard largo: agrega friccion y oculta el readiness global.
- Tabs: rompe el modelo de una sola pantalla clara.
- Configuracion avanzada: desplaza el foco desde la operacion al tuning.
- Edicion compleja: pertenece a una fase posterior, no al setup del MVP.
- Parametros tecnicos: erosionan el tono ejecutivo-operativo.
- Charts decorativos: no agregan comprension en el primer contacto.

## 8. Base reusable para epicas siguientes

La base de `EPIC 05` debe dejar preparados:

- layout reutilizable para Summary y Drill-down
- header de producto con slot de accion
- componentes de estado, badges y feedback
- contratos de `run`, `summary` y uploads reutilizables
- tabla compacta de preview que luego pueda crecer a Summary UI
