# Workflow de Arranque de Cada WS

## Objetivo

Estandarizar como se retoma el proyecto en cada nueva working session (`WS`) para evitar drift entre el estado local, GitHub y el backlog operativo.

## Secuencia obligatoria al iniciar una WS

1. Ubicar el repo local oficial:
   - `/Users/tzanchetti/Documents/Proyectos Claudio/accounting-project`
2. Entrar al repo y revisar rama actual:
   - `git branch --show-current`
3. Traer cambios remotos antes de empezar:
   - `git pull origin <branch>`
4. Leer documentos base del proyecto:
   - `AGENTS.md`
   - `Backlog/INDICE.md`
   - `Backlog/WORKFLOW_EJECUCION.md`
   - `Backlog/RESUMEN_MAESTRO.md`
   - la ultima `ARD_WS[N]_DDMMAAAA.md`
   - la epic a ejecutar
5. Hacer reporte de status de arranque:
   - que se hizo hasta ahora
   - que esta pendiente
   - cual es la proxima card recomendada
   - riesgos o bloqueos visibles
6. Recien despues de eso empezar a ejecutar trabajo de la card elegida.

## Regla operativa

Ninguna WS deberia arrancar implementando "en frio".

Siempre primero:

- sync con repo
- lectura de contexto
- status report
- recien despues ejecucion

## Formato esperado del status report

El reporte de arranque debe dejar claro:

- estado general del proyecto
- ultima sesion ejecutada
- avances concretos ya materializados
- proximo paso sugerido

## Regla de cierre

Al terminar cada WS se debe:

1. actualizar documentos madre si aplica
2. crear una nueva nota `ARD_WS[N]_DDMMAAAA.md`
3. dejar explicito que quedo hecho y que sigue
4. commitear y pushear si el avance tiene valor de continuidad

