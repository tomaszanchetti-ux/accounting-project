# Backend

## Stack base

- Python 3.13+
- FastAPI
- Uvicorn
- Pydantic
- pandas

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

## Convencion inicial de storage

- raw inputs: `runs/<run_id>/inputs/<filename>`
- exports: `runs/<run_id>/exports/<filename>`
