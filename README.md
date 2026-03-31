# Accounting Reconciliation MVP

MVP de conciliacion entre payroll/RRHH y contabilidad con foco en:

- agregacion automatica
- comparacion contra expected totals
- deteccion de diferencias
- explicacion rule-based
- drill-down a registros concretos

## Estructura del proyecto

- `frontend/`: app Next.js
- `backend/`: API FastAPI
- `data/`: insumos locales de trabajo
- `docs/`: documentacion tecnica complementaria
- `Backlog/`: ejecucion por epicas, features y cards

## Documentos clave para el motor

- `docs/DATASET_DEMO_FOUNDATION.md`
- `docs/DEMO_CASE_VALIDATION.md`
- `docs/DEMO_READINESS_REPORT.md`
- `docs/DEMO_SEED_STRATEGY.md`
- `docs/DEMO_WALKTHROUGH.md`
- `docs/RECONCILIATION_ENGINE_CONTRACT.md`
- `docs/RUNS_MODEL_MVP.md`
- `docs/RUNS_PERSISTENCE_MODEL.md`
- `docs/RUNS_UI_PAYLOADS.md`
- `docs/RUN_EVENTS_TRACEABILITY.md`
- `Backlog/EPIC_02_Reconciliation_Engine_Core.md`

## Dependencias externas del setup

- Node.js 24+
- Python 3.13+
- proyecto Supabase activo
- cuenta activa en Vercel para frontend
- buckets creados:
  - `accounting-mvp-raw-inputs`
  - `accounting-mvp-run-exports`

## Variables requeridas

Referencia versionable:

- `/.env.example`

Archivos locales no versionados:

- `frontend/.env.local`
- `backend/.env`

Variables principales:

- `NEXT_PUBLIC_API_BASE_URL`
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_DB_URL`
- `STORAGE_BUCKET_RAW_INPUTS`
- `STORAGE_BUCKET_RUN_EXPORTS`

## Arranque local

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend local:

- `http://localhost:3000`
- si `3000` está ocupado: `cd frontend && npm run dev -- --port 3001`

### Backend

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend local:

- `http://localhost:8000`
- docs: `http://localhost:8000/docs`

## Chequeos minimos

```bash
make check
```

Comandos individuales:

- frontend: `cd frontend && npm run lint`
- backend: `cd backend && .venv/bin/ruff check app`

## Deploy

- frontend publico esperado: `https://accounting-project-blond.vercel.app/`
- estrategia del backend: `docs/DEPLOY_BACKEND.md`
- mientras el backend productivo no exista, `NEXT_PUBLIC_API_BASE_URL` puede quedar temporalmente con placeholder

## Rutina de arranque de cada WS

1. entrar al repo oficial
2. hacer `git pull`
3. leer `AGENTS.md`
4. leer `Backlog/INDICE.md`
5. leer `Backlog/WORKFLOW_EJECUCION.md`
6. leer `Backlog/RESUMEN_MAESTRO.md`
7. leer la ultima `ARD_WS[N]_DDMMAAAA.md`
8. emitir status de lo hecho y lo pendiente
9. recien despues seguir con la proxima card

## Estado actual recomendado

Para retomar el proyecto hoy:

- `EPIC 00` ya esta cerrada
- `EPIC 01` ya esta cerrada
- `EPIC 02` ya esta completada
- `EPIC 03` ya esta completada
- `EPIC 04` ya esta completada
- `EPIC 05` ya esta completada y mergeada a `main`
- `EPIC 06` ya esta completada
- `EPIC 07` ya esta completada
- `EPIC 08` esta completada
- revisar `docs/DEMO_SEED_STRATEGY.md`
- revisar `docs/DEMO_CASE_VALIDATION.md`
- revisar `docs/DEMO_WALKTHROUGH.md`
- revisar `docs/DEMO_READINESS_REPORT.md`
- `EPIC 09` ya quedó completada
- revisar `docs/EPIC09_FINAL_DEMO_READY_EVALUATION.md`
- revisar `docs/EPIC09_DEMO_READY_CHECKLIST.md`
- siguiente paso recomendado: resolver/preparar el entorno final de demo y cerrar branch/merge de `EPIC 09`
- branch activa recomendada: `codex/epic-09-hardening-qa`
