# Estrategia de Deploy del Backend

## Decision

Para el MVP, la estrategia recomendada para el backend es:

- **Plataforma:** Railway
- **Runtime:** servicio web Python
- **App server:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Motivo de la decision

Esta opcion privilegia:

- setup rapido
- costo razonable para demo
- buena compatibilidad con FastAPI
- configuracion simple de variables
- salida publica HTTPS sin infraestructura extra

## Compatibilidad con el stack actual

La estrategia es compatible con:

- FastAPI
- Supabase Postgres
- Supabase Storage
- frontend desplegado en Vercel

## URL productiva objetivo

La URL base productiva objetivo para el backend se define como:

- `https://accounting-project-api.up.railway.app`

Esta URL debe cargarse en Vercel como:

- `NEXT_PUBLIC_API_BASE_URL=https://accounting-project-api.up.railway.app`

## Variables requeridas en el backend desplegado

- `ENVIRONMENT=production`
- `API_HOST=0.0.0.0`
- `API_PORT=$PORT`
- `CORS_ALLOW_ORIGINS=https://accounting-project-blond.vercel.app`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_DB_URL`
- `STORAGE_BUCKET_RAW_INPUTS`
- `STORAGE_BUCKET_RUN_EXPORTS`

## Verificaciones minimas esperadas

Antes de considerar el backend como desplegado para demo:

1. `/health` debe responder `200`
2. el frontend en Vercel debe poder llegar al backend
3. CORS debe permitir el dominio publico del frontend
4. la conexion a Supabase Postgres debe seguir operativa
5. Storage debe seguir operativo desde el servicio desplegado

## Nota operativa

Mientras el backend productivo no exista, el frontend puede seguir desplegado usando una URL placeholder o una variable pendiente de actualizar.

