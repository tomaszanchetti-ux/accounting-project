# EPIC 09 Run Errors, Empty States and Export Resilience QA

## Objetivo

Documentar la validacion y el hardening aplicado sobre las cards:

- `9.2.1 — Revisar errores de carga y ejecución de runs`
- `9.2.2 — Revisar empty states y not found states`
- `9.2.3 — Revisar resiliencia básica de exportables`

## Entorno validado

- fecha de validacion: `2026-03-31`
- branch de trabajo: `codex/epic-09-hardening-qa`
- frontend local: `http://localhost:3000`
- backend local: `http://localhost:8000`

## Alcance

### Card 9.2.1

Se cubrieron tres bordes previsibles del flujo de runs:

- ejecución sin archivos requeridos
- expected totals sin filas para el período objetivo
- fallo técnico controlado del motor durante ejecución

### Card 9.2.2

Se revisaron y reforzaron estados vacíos y `404` en:

- summary de run
- concept analysis
- drill-down
- empty state de drill-down filtrado

### Card 9.2.3

Se revisó la descarga de exportables en:

- summary export
- detail export desde concept analysis
- detail export desde drill-down

## Cambios aplicados

### 1. Hardening de ejecución en setup

El setup ahora interpreta correctamente estados de `execute`:

- `INVALID_INPUT` ya no se muestra como éxito
- `FAILED` ya no se muestra como éxito
- el feedback visible usa `run.error_message` cuando existe
- no se intenta cargar summary si la ejecución terminó inválida o fallida

### 2. Cobertura automatizada para errores previsibles

Se agregaron tests para validar:

- `INVALID_INPUT` cuando faltan referencias requeridas
- `INVALID_INPUT` cuando expected totals no contiene el período objetivo
- `FAILED` con `500` cuando el motor rompe de forma controlada

Fixture agregada:

- `backend/tests/fixtures/expected_totals_2026_02_only.csv`

### 3. Estados vacíos y not-found más claros

Se unificó la jerarquía visual de estados con un panel de estado dedicado.

Mejoras visibles:

- summary ahora distingue `run not found` de error general de carga
- concept analysis tiene recuperación explícita para `404` y error de payload
- drill-down tiene recuperación explícita para `404` y error de payload
- el summary vacío queda con CTA clara de retorno a setup

### 4. Exportables con feedback inline

Los exports dejaron de depender solo de links directos.

Ahora:

- la descarga se hace vía fetch controlado desde frontend
- el botón muestra estado `Exporting...`
- si la descarga falla, el usuario ve el error en el mismo contexto de pantalla
- si la descarga funciona, se muestra confirmación con el filename recibido

## Validaciones ejecutadas

### Backend

Comando:

```bash
PYTHONPATH=backend backend/.venv/bin/python -m unittest backend.tests.test_runs_api_flow
```

Resultado:

- `5 / 5` tests OK

### Frontend + backend lint

Comando:

```bash
make check
```

Resultado:

- frontend lint OK
- backend `ruff check app` OK

## Conclusion

Las cards `9.2.1`, `9.2.2` y `9.2.3` quedan validadas para alcance MVP.

El producto ahora responde mejor en tres áreas críticas de demo:

- errores previsibles de runs
- navegación vacía o inválida
- feedback de exportables

## Siguiente paso recomendado

Avanzar con `Card 9.3.1 — Revisar consistencia visual entre pantallas clave`.
