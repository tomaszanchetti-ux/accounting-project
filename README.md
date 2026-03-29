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

## Dependencias externas del setup

- Node.js 24+
- Python 3.13+
- proyecto Supabase activo
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

- revisar `Backlog/EPIC_00_Setup_Tecnico_MVP.md`
- continuar desde la siguiente card pendiente de `EPIC 00`

