# Estrategia de Deploy del Backend

## Decision

Para el MVP, la estrategia recomendada para el backend es:

- **Plataforma:** Railway
- **Runtime:** servicio web Python
- **App server:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Build source:** root del repo usando `Dockerfile` y `railway.toml`

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

Tambien queda alineada con el monorepo actual porque:

- Railway puede desplegar desde el root del repo sin depender de un `rootDirectory`
- el `Dockerfile` empaqueta el backend correcto y expone `uvicorn` sobre `PORT`
- `railway.toml` declara `healthcheckPath=/health` y reinicio en fallo
- el frontend ya no registra demo seeds por `local_path`; ahora los sube al backend como archivos reales

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
6. el setup flow debe poder iniciar una run subiendo `expected_totals`, `concept_master` y `employee_reference` como multipart

## Archivos de deploy incluidos en el repo

- `Dockerfile`
- `railway.toml`

Estos archivos dejan el backend listo para que Railway construya el servicio
correcto aun cuando el deploy parta desde el root del monorepo.

## Nota operativa

Si el servicio actual de Railway sigue devolviendo `404` en `/health`, el paso
operativo pendiente no es de código sino de re-deploy o re-vinculación del
servicio usando esta configuración.
