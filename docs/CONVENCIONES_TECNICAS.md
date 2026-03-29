# Convenciones Tecnicas del MVP

## Objetivo

Este documento fija las convenciones base del proyecto **Accounting Reconciliation MVP** para que frontend, backend, Supabase y despliegue usen un lenguaje comun desde el inicio.

Estas convenciones priorizan:

- claridad operativa
- setup local simple
- continuidad entre sesiones
- consistencia entre capas

## Naming base

- Nombre del proyecto: `accounting-reconciliation-mvp`
- Carpeta del frontend: `frontend/`
- Carpeta del backend: `backend/`
- Carpeta de datos locales: `data/`
- Carpeta de documentacion tecnica: `docs/`

## URLs y puertos locales

- Frontend local: `http://localhost:3000`
- Backend local: `http://localhost:8000`
- API docs local: `http://localhost:8000/docs`

## Variables de entorno esperadas

### Compartidas / infraestructura

- `ENVIRONMENT`: entorno actual (`local`, `staging`, `production`)
- `SUPABASE_URL`: URL del proyecto Supabase
- `SUPABASE_SERVICE_ROLE_KEY`: clave server-side para backend
- `SUPABASE_ANON_KEY`: clave publica para frontend si hiciera falta
- `SUPABASE_DB_URL`: string de conexion Postgres para backend

### Frontend

- `NEXT_PUBLIC_APP_NAME`: nombre visible de la app
- `NEXT_PUBLIC_API_BASE_URL`: base URL del backend
- `NEXT_PUBLIC_SUPABASE_URL`: URL publica de Supabase
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: anon key publica

### Backend

- `API_HOST`: host de uvicorn
- `API_PORT`: puerto de FastAPI
- `CORS_ALLOW_ORIGINS`: origenes permitidos separados por coma
- `STORAGE_BUCKET_RAW_INPUTS`: bucket de archivos fuente
- `STORAGE_BUCKET_RUN_EXPORTS`: bucket de exports y artefactos

## Convencion de archivos de entorno

- `frontend/.env.local` para desarrollo local del frontend
- `backend/.env` para desarrollo local del backend
- `/.env.example` como inventario de variables requeridas

No se deben commitear secretos reales.

## Convencion de naming en Supabase

### Buckets

- Bucket de archivos subidos: `accounting-mvp-raw-inputs`
- Bucket de salidas/exportaciones: `accounting-mvp-run-exports`

### Tablas sugeridas

- `runs`
- `run_inputs`
- `run_results`
- `reconciliation_summary`
- `reconciliation_exceptions`

### Servicios/modulos internos

- frontend app: `accounting-mvp-web`
- backend api: `accounting-mvp-api`
- engine: `reconciliation-engine`

## Regla de consistencia

Si en una sesion futura hace falta ajustar algun nombre, el cambio debe reflejarse en:

1. este documento
2. `.env.example`
3. la configuracion real afectada
4. la nota `ARD_WS...` de cierre de sesion

