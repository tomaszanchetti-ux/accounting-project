# Workflow de Ejecución del MVP

> Documento operativo para ejecutar el backlog del proyecto **Accounting Reconciliation MVP**.
> Su objetivo es estandarizar cómo se implementa cada épica, card y task, especialmente cuando el trabajo lo ejecuta un agente.

---

## 1. Propósito del workflow

Este proyecto ya tiene:

- visión de producto
- arquitectura funcional
- backlog estructurado por épicas
- detalle de `Features -> Cards -> Tasks`

Lo que este documento agrega es la **lógica de ejecución**.

La intención es simple:

> **reducir improvisación, proteger calidad y permitir que el proyecto avance de manera consistente, granular y auditable.**

Este workflow existe para que cada sesión de trabajo:

- tenga foco claro
- evite saltos caóticos entre partes del sistema
- preserve trazabilidad de cambios
- minimice riesgo de romper lo ya hecho
- produzca avance real y verificable

---

## 2. Principio rector

La ejecución del proyecto debe hacerse:

- **épica por épica**
- **card por card**
- **task por task**

No se trabaja “por intuición general”.  
No se mezclan varias cards grandes a la vez salvo que sea estrictamente necesario.  
No se salta a una epic posterior solo porque “parece más entretenida” o porque una pantalla suena más vistosa.

La lógica correcta es:

1. leer la épica completa
2. elegir una card concreta
3. ejecutar sus tasks con atención al detalle
4. validar localmente
5. recién entonces pasar a la siguiente card

---

## 3. Unidad real de trabajo

La unidad real de ejecución del proyecto es la **Card**.

La jerarquía es:

- **Epic**: agrupa una capacidad completa
- **Feature**: ordena un bloque funcional dentro de la épica
- **Card**: unidad implementable y controlable
- **Task**: checklist operativo para completar la card

### Regla de trabajo

Una sesión ideal no debería arrancar diciendo:

> “vamos a hacer la épica completa”

Debería arrancar diciendo:

> “vamos a ejecutar la Card X.Y.Z, completar sus tasks, validarla y dejarla cerrada”

Esto mejora muchísimo:

- foco
- calidad
- trazabilidad
- facilidad de retomar trabajo
- facilidad de QA

---

## 4. Orden de ejecución recomendado

El orden correcto es el orden del backlog, salvo decisión explícita y justificada en contrario.

### Orden base

1. `EPIC_00_Setup_Tecnico_MVP.md`
2. `EPIC_01_Data_Foundation_Dataset_Demo.md`
3. `EPIC_02_Reconciliation_Engine_Core.md`
4. `EPIC_03_Exception_Detection_Explanation.md`
5. `EPIC_04_Runs_API_Persistence_Traceability.md`
6. `EPIC_05_UI_Foundation_Setup_Flow.md`
7. `EPIC_06_Summary_Concept_Analysis_UI.md`
8. `EPIC_07_Drilldown_Exports_Traceability.md`
9. `EPIC_08_Demo_Seed_Narrative_Commercial_Flow.md`
10. `EPIC_09_Hardening_QA_Demo_Ready.md`

### Excepción permitida

Solo se altera este orden si:

- una dependencia estaba mal estimada
- una card bloquea el trabajo y se necesita desbloquear otra menor
- se decide explícitamente reordenar por velocidad de demo

Si eso pasa, debe quedar documentado en la sesión.

---

## 5. Forma correcta de ejecutar una Card

Cada card debe seguir esta secuencia:

1. Leer la card completa
2. Entender el objetivo funcional real
3. Leer todas sus tasks
4. Revisar dependencias técnicas inmediatas
5. Implementar primero en local
6. Validar en local
7. Ajustar bordes
8. Hacer commit
9. Recién entonces avanzar

### Regla importante

No se hace commit de trabajo “a medio cerrar” salvo que:

- la sesión termine
- el avance sea valioso y no convenga perderlo
- quede claro que la card sigue en progreso

Pero por defecto:

> **una card se considera sana cuando termina con validación local y commit propio.**

---

## 6. Ejecución siempre primero en local

Toda implementación debe ejecutarse primero en local.

### Secuencia mínima esperada

1. implementar en branch de trabajo
2. correr localmente
3. validar flujo afectado
4. corregir errores
5. recién después considerar push

### Qué significa “validar en local”

No significa solo que “compila”.

Significa, según el tipo de card:

- que el backend levanta
- que el frontend levanta
- que el endpoint responde
- que la pantalla carga
- que el flujo principal no rompe
- que los datos mostrados tienen sentido

Si la card modifica lógica visible, hay que verla funcionar.  
Si modifica backend, hay que probar el caso afectado.  
Si modifica datos o dataset, hay que verificar el impacto resultante.

---

## 7. Testing y verificación

Cada card debe cerrarse con algún tipo de verificación, aunque el nivel varía según su naturaleza.

### Tipos de verificación válidos

- test automatizado
- prueba manual local
- validación visual en UI
- validación de payload/API
- validación de output exportado

### Regla mínima

Toda card debe cerrar con al menos una de estas:

- `tested locally`
- `visually validated`
- `API response verified`
- `dataset output checked`

Si no pudo validarse, debe quedar explícitamente dicho.

### Regla de calidad

No asumir que una card está lista porque “parece correcta leyendo el código”.

Hay que verificar comportamiento.

---

## 8. Git workflow obligatorio

Para este proyecto, la disciplina de branches no es opcional.

### Regla principal

Se trabaja siempre en **branches por épica**.

### Naming recomendado

Usar el prefijo:

- `codex/epic-00-setup`
- `codex/epic-01-data-foundation`
- `codex/epic-02-reconciliation-engine`
- `codex/epic-03-explanation-layer`
- etc.

### Regla de merge

`main` no se toca directamente.

Solo se mergea a `main` cuando:

- la épica completa está terminada
- la épica fue validada integralmente en su branch
- se hizo QA final sobre el branch completo

---

## 9. Commits: granularidad correcta

La lógica de commit de este proyecto debe seguir el backlog.

### Regla recomendada

Idealmente:

- **1 commit por Card cerrada**

No hace falta que sea matemáticamente rígido, pero sí es la referencia correcta.

### Qué evita esto

- commits gigantes difíciles de revisar
- pérdida de trazabilidad
- mezcla de varias cosas no relacionadas
- dificultad para aislar bugs

### Qué favorece

- rollback mental más fácil
- QA más claro
- revisión más simple
- handoff más limpio entre sesiones

### Convención sugerida

Usar mensajes alineados al backlog, por ejemplo:

- `feat(engine): implementar observed totals por concepto y periodo`
- `feat(summary-ui): implementar RunSummaryCards`
- `test(demo): validar wow case meal voucher`

---

## 10. Push: cuándo sí y cuándo no

### Hacer push cuando:

- una card quedó cerrada y validada
- se logró un bloque valioso de avance
- conviene respaldar trabajo de una sesión
- el branch está en estado razonablemente sano

### No hacer push cuando:

- el código está roto
- hay cambios a medio integrar sin contexto
- la card todavía está en estado demasiado inestable

### Regla práctica

`commit` y `push` deben representar progreso real, no simplemente actividad.

---

## 11. QA por épica

Cada épica debe tener un momento explícito de QA final dentro de su branch.

### Qué significa QA final de épica

No es solo revisar la última card.  
Es revisar la **epic como sistema**.

### QA final de épica debería validar:

- que todas las cards comprometidas están hechas
- que los flujos internos de la épica funcionan juntos
- que no hay regressions obvias
- que la épica cumple su criterio de aceptación completo

### Regla de merge

Sin QA final de la épica completa, no se mergea a `main`.

---

## 12. Criterio de “done” por nivel

### Una Task está hecha cuando:

- se ejecutó realmente
- su resultado existe
- no queda pendiente oculta

### Una Card está hecha cuando:

- todas sus tasks están hechas
- el objetivo de la card quedó cumplido
- hubo validación local razonable
- existe commit asociado o avance claramente registrable

### Una Epic está hecha cuando:

- todas sus cards relevantes están completas
- la capacidad end-to-end de la épica funciona
- se realizó QA del branch completo
- está lista para merge a `main`

---

## 13. Modo correcto de trabajo para un agente

Este documento está especialmente pensado para mejorar el trabajo de un agente como ejecutor del backlog.

### La lógica correcta para el agente es:

1. leer el documento de la épica
2. elegir la próxima card no resuelta
3. ejecutar con atención extrema a los detalles
4. no mezclar múltiples cards grandes sin necesidad
5. validar localmente todo cambio relevante
6. hacer commit claro y granular
7. reportar qué se hizo, qué se validó y qué quedó pendiente

### Lo que el agente no debe hacer

- improvisar roadmap paralelo
- mezclar implementaciones de varias épicas en una sola sesión sin razón
- saltar QA local
- trabajar “por arriba” sin cerrar cards de verdad
- tocar `main` directamente
- empujar cambios no verificados como si estuvieran terminados

### Tesis operativa

> **Para que el agente trabaje bien, el proyecto debe ejecutarse con granularidad, disciplina y contexto explícito.**

---

## 14. Regla de atención al detalle

Este proyecto requiere una ejecución cuidadosa.

No alcanza con:

- que algo “más o menos funcione”
- que una pantalla “se vea bien de lejos”
- que una explicación “suene razonable”

Cada card debe trabajarse con atención a:

- consistencia funcional
- claridad visual
- naming
- payloads
- manejo de errores
- continuidad entre pantallas
- alineación con la narrativa del MVP

### Regla simple

Si una decisión parece pequeña pero puede afectar:

- credibilidad del demo
- claridad del flujo
- consistencia del producto

entonces no es un detalle menor.  
Hay que revisarla con cuidado.

---

## 15. Gestión de bloqueos

Si durante una card aparece un bloqueo, la secuencia correcta es:

1. confirmar si el bloqueo es real
2. verificar si la dependencia está documentada en el backlog
3. resolver el bloqueo localmente si es razonable
4. si no se puede, documentarlo de forma concreta

### Un bloqueo bien documentado debe decir:

- qué card se estaba ejecutando
- qué impide completarla
- si el bloqueo es técnico, funcional o de decisión
- cuál sería el siguiente paso para destrabarlo

No alcanza con decir:

> “esto está bloqueado”

Hay que dejar el bloqueo utilizable por la siguiente sesión.

---

## 16. Qué hacer al cerrar una sesión

Cada sesión debería cerrar dejando visible:

- qué epic se trabajó
- qué cards se completaron
- qué validaciones se hicieron
- qué commits se generaron
- qué quedó pendiente
- cuál es la siguiente card sugerida

Esto es clave para continuidad entre sesiones y para trabajo agent-friendly.

### Regla obligatoria de cierre

Al finalizar cada sesión se debe:

1. revisar si `AGENTS.md` necesita actualización
2. crear un documento de cierre con formato `ARD_WS[N]_DDMMAAAA.md`
3. dejar en ese documento:
   - qué se hizo
   - qué se creó o actualizó
   - qué falta
   - cuál es el próximo paso sugerido

Si una sesión termina sin ese handoff, la continuidad del proyecto se degrada.

---

## 17. Criterio final de ejecución del proyecto

La ejecución correcta de este MVP no es:

> “construir muchas cosas rápido”

La ejecución correcta es:

> “cerrar una capacidad a la vez, con buen nivel de detalle, verificación real y control narrativo del producto”

Ese es el estándar que debe seguir cualquier persona o agente que trabaje sobre este backlog.

---

## 18. Resumen operativo

### Regla corta del proyecto

- trabajar por épica
- ejecutar por card
- completar task por task
- correr primero siempre en local
- testear o validar siempre
- commit granular por card
- push solo de trabajo sano
- branch por épica
- merge a `main` solo después de QA final del branch completo

### Si hay duda, usar esta secuencia:

1. leer la card
2. implementar
3. validar local
4. corregir
5. commit
6. push
7. seguir

Ese es el workflow correcto para este proyecto.
