# EPIC 09 Demo-Ready Checklist

## Objetivo

Definir un checklist final, breve y accionable, para decidir si el MVP está en
condición real de mostrarse.

Este documento cierra la `Card 9.6.1 — Definir checklist final de demo-ready`.

## Cuándo usar este checklist

Usarlo:

- antes de una reunión demo
- idealmente `15-30` minutos antes de presentar
- sobre el entorno que efectivamente se va a mostrar

Responsable sugerido:

- quien vaya a presentar la demo

## Cómo usarlo

Regla simple:

- si todos los checks críticos están en `OK`, el MVP está listo para mostrarse
- si falla un check crítico del flujo principal, no conviene presentar sin
  resolverlo o sin plan alternativo explícito
- si falla un check no crítico, puede seguirse solo si el impacto está entendido
  y no rompe la historia principal

## Checklist final

### 1. Entorno demo

- [ ] Frontend accesible en la URL que se va a mostrar
- [ ] Backend accesible y `GET /health` responde `200`
- [ ] Run canónica presente o recreable sin fricción
- [ ] Entorno pre-calentado para evitar latencia fría en summary y drill-down

### 2. Flujo principal

- [ ] Setup carga correctamente y muestra referencias demo listas
- [ ] Summary carga correctamente y expone KPIs + tabla por concepto
- [ ] Concept analysis abre correctamente desde summary
- [ ] Drill-down abre correctamente desde concept analysis
- [ ] El flujo principal puede recorrerse sin bloqueos visibles

### 3. Wow cases

- [ ] `MEAL_VOUCHER` aparece como caso wow principal y visible
- [ ] `MEAL_VOUCHER` conserva narrativa multi-causa defendible
- [ ] `CHILDCARE` se entiende como caso de población faltante
- [ ] `OVERTIME` se entiende como caso de outlier puntual
- [ ] `TRANSPORT` se entiende como caso de tolerancia y no compite con el wow principal

### 4. Exportables

- [ ] Summary CSV se descarga correctamente
- [ ] Detail CSV del wow case se descarga correctamente
- [ ] Los nombres y contenidos son coherentes con la run mostrada

### 5. Calidad visual mínima

- [ ] Setup, summary, concept analysis y drill-down se sienten parte del mismo producto
- [ ] No hay estados vacíos o errores visibles que dejen al usuario sin salida clara
- [ ] Las tablas principales se leen con comodidad en desktop o pantalla compartida
- [ ] Los labels y microtextos visibles mantienen tono consistente

### 6. Narrativa preparada

- [ ] El walkthrough entra en `5-8` minutos
- [ ] El presentador sabe dónde abrir el wow moment
- [ ] El cierre comercial está practicado
- [ ] Las respuestas base a objeciones frecuentes están claras
- [ ] Los límites aceptados del MVP pueden explicarse sin improvisación

## Criterio práctico de decisión

### Mostrar

Se puede mostrar si:

- todos los checks de entorno y flujo principal están en `OK`
- el wow moment principal está íntegro
- exportables responden
- no hay fricción visible que rompa la historia comercial

### No mostrar todavía

No conviene mostrar si:

- el flujo principal no llega de setup a drill-down
- `MEAL_VOUCHER` perdió claridad o impacto
- exports fallan en el entorno real de demo
- la narrativa necesita demasiada explicación defensiva para sostenerse

## Siguiente paso recomendado

Aplicar este checklist formalmente sobre el producto real y emitir el veredicto
final de `demo-ready`.
