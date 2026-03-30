# Backend

## Stack base

- Python 3.13+
- FastAPI
- Uvicorn
- Pydantic
- pandas
- python-multipart

## Entorno local

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoint inicial

- `GET /health`

## Configuracion base

El backend toma estos valores desde entorno:

- `ENVIRONMENT`
- `API_HOST`
- `API_PORT`
- `CORS_ALLOW_ORIGINS`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_DB_URL`
- `STORAGE_BUCKET_RAW_INPUTS`
- `STORAGE_BUCKET_RUN_EXPORTS`

## Archivo de entorno local

Crear `backend/.env` con este set minimo:

```env
ENVIRONMENT=local
API_HOST=0.0.0.0
API_PORT=8000
CORS_ALLOW_ORIGINS=http://localhost:3000
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_DB_PASSWORD=your-db-password
SUPABASE_DB_URL=postgresql://postgres:postgres@db.your-project.supabase.co:5432/postgres
STORAGE_BUCKET_RAW_INPUTS=accounting-mvp-raw-inputs
STORAGE_BUCKET_RUN_EXPORTS=accounting-mvp-run-exports
```

## Convencion inicial de storage

- raw inputs: `runs/<run_id>/inputs/<filename>`
- exports: `runs/<run_id>/exports/<filename>`

## API de runs ya disponible

- `POST /runs`
- `POST /runs/{run_id}/upload`
- `POST /runs/{run_id}/execute`
- `GET /runs/{run_id}/summary`
- `GET /runs/{run_id}/results`
- `GET /runs/{run_id}/results/{result_id}`
- `GET /runs/{run_id}/results/{result_id}/drilldown`

## Nota sobre upload

`POST /runs/{run_id}/upload` acepta:

- JSON para registrar referencias de archivo existentes
- multipart para subir archivo real a Supabase Storage
