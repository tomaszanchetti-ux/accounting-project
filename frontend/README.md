## Frontend

Frontend base del proyecto **Accounting Reconciliation MVP**.

## Variables de entorno

Crear `frontend/.env.local` con este set minimo:

```env
NEXT_PUBLIC_APP_NAME=Accounting Reconciliation MVP
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

## Arranque local

```bash
npm run dev
```

Abrir `http://localhost:3000`.

Si `3000` ya está ocupado por otra app local:

```bash
npm run dev -- --port 3001
```

Y abrir `http://localhost:3001`.

## Notas

- La base URL del backend se resuelve desde `NEXT_PUBLIC_API_BASE_URL`.
- Las variables publicas de Supabase se leen desde `NEXT_PUBLIC_SUPABASE_URL` y `NEXT_PUBLIC_SUPABASE_ANON_KEY`.
- Los helpers de API viven en `frontend/lib/api/`.
- Los demo seed files ahora se suben al backend como archivos reales al iniciar una run; ya no dependen de `local_path` compartidos entre frontend y backend.
