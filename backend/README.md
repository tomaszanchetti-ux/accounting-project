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

