# EPIC 00 — Setup Técnico del MVP

## Contexto y objetivo

Esta epic construye la base técnica del producto antes de entrar en lógica de conciliación, dataset o UX de negocio. El objetivo no es tener funcionalidad visible todavía, sino dejar una plataforma mínima, seria y costo-eficiente sobre la cual las demás épicas puedan implementarse sin fricción.

La decisión rectora del proyecto ya está tomada:

- **Frontend:** Next.js
- **Backend:** FastAPI
- **DB:** Supabase Postgres
- **Storage:** Supabase Storage
- **Deploy:** Vercel + Supabase

Esto sigue la misma lógica operativa usada en Obsydian: stack simple, creíble para demo, barato de operar y rápido de construir.

Al terminar esta epic, el proyecto debe quedar preparado para:

- correr frontend y backend en local sin hacks
- conectarse a una base de datos real
- persistir archivos de entrada del demo
- sostener el desarrollo incremental de las épicas siguientes

## Dominio(s) involucrado(s)

Ningún dominio funcional del producto. Esta epic es infraestructura transversal.

## Dependencias

Ninguna. Es la primera epic del backlog.

## Criterio de aceptación de la Epic completa

- [ ] Existe una app frontend en Next.js corriendo en local sin errores
- [ ] Existe un backend en FastAPI corriendo en local sin errores
- [ ] Frontend y backend comparten una convención clara de estructura de carpetas
- [ ] La base de datos de Supabase está conectada correctamente desde el backend
- [ ] Existe un bucket de storage configurado para archivos del MVP
- [ ] Las variables de entorno están organizadas para local y producción
- [ ] El proyecto puede desplegarse en una configuración simple de demo
- [ ] Hay documentación mínima de setup para retomar el proyecto sin ambigüedad

## Estado: EN PROGRESO

---

## Feature 0.1 — Estructura inicial del repositorio

**Objetivo:** dejar una base de carpetas y convenciones consistente con un proyecto de doble capa (`frontend` + `backend`) y lista para crecer sin improvisación.

---

### Card 0.1.1 — Crear estructura raíz del proyecto

**Descripción:** definir una estructura simple, explícita y fácil de operar. No se busca mono-repo sofisticado ni tooling innecesario; solo orden suficiente para que el build sea sostenible.

**Criterio de aceptación:**

- Existe una carpeta `frontend/` para Next.js
- Existe una carpeta `backend/` para FastAPI
- Existe una carpeta `docs/` o equivalente para documentación técnica futura si hiciera falta
- Existe una carpeta `data/` o `assets/` para inputs locales de trabajo
- La estructura es entendible sin explicación oral adicional

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir estructura raíz recomendada:
  - `frontend/`
  - `backend/`
  - `data/`
  - `Backlog/` (ya creada)
- [x] Crear `.gitkeep` en carpetas vacías si hace falta
- [x] Validar que la estructura sirva tanto para desarrollo local como para demo
- [ ] Commit sugerido: `chore: crear estructura base del proyecto accounting-mvp`

---

### Card 0.1.2 — Definir convención de entorno y nombres

**Descripción:** antes de instalar herramientas, conviene fijar convenciones explícitas para evitar drift entre frontend, backend, Supabase y despliegue.

**Criterio de aceptación:**

- Existe una convención clara para variables de entorno
- Existe una convención clara para nombres de servicios y puertos locales
- La app tiene un naming consistente entre frontend, backend y Supabase

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir nombres base:
  - proyecto: `accounting-reconciliation-mvp`
  - frontend local: `http://localhost:3000`
  - backend local: `http://localhost:8000`
- [x] Definir variables de entorno mínimas esperadas para todo el proyecto
- [x] Documentar convención de naming para buckets, tablas y servicios
- [ ] Commit sugerido: `docs: definir convenciones base de entorno y naming`

---

## Feature 0.2 — Frontend base en Next.js

**Objetivo:** crear una app frontend real, limpia y ligera, preparada para la UX del demo.

---

### Card 0.2.1 — Inicializar app Next.js

**Descripción:** crear la app del frontend con App Router, TypeScript y una base moderna que permita construir la demo sin fricción.

**Criterio de aceptación:**

- La app levanta en local en `http://localhost:3000`
- Usa App Router
- TypeScript está activo
- Hay una página inicial funcional

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Crear app en `frontend/` con `create-next-app`
- [x] Activar TypeScript, App Router y Tailwind
- [x] Configurar alias de imports
- [x] Reemplazar el contenido inicial por una pantalla mínima de placeholder del MVP
- [x] Verificar `npm run dev`
- [ ] Commit sugerido: `chore(frontend): inicializar app Next.js del MVP`

---

### Card 0.2.2 — Configurar base visual mínima

**Descripción:** aunque el design system detallado se baje en una epic de UI, desde el setup conviene dejar listo el baseline técnico de estilos y componentes.

**Criterio de aceptación:**

- Tailwind funciona correctamente
- Existe una convención mínima de estilos globales
- El frontend está listo para incorporar componentes reutilizables

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Limpiar estilos de ejemplo del scaffold inicial
- [x] Dejar `globals.css` con una base simple y neutra
- [x] Crear carpeta para componentes propios del proyecto
- [x] Evaluar si conviene instalar una librería de componentes liviana desde el inicio
- [ ] Commit sugerido: `chore(frontend): configurar base visual mínima`

---

### Card 0.2.3 — Definir estrategia de consumo de API

**Descripción:** el frontend debe quedar preparado para consumir el backend FastAPI sin mezclar lógica de negocio ni crear acoplamiento prematuro.

**Criterio de aceptación:**

- Existe una configuración base de `API_URL`
- Hay un patrón inicial para llamadas HTTP
- Queda claro dónde vivirán los clientes o helpers de fetch

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Crear convención de `NEXT_PUBLIC_API_BASE_URL`
- [x] Crear carpeta o módulo para clientes API
- [x] Implementar un health check simple desde frontend hacia backend
- [ ] Commit sugerido: `chore(frontend): preparar patrón base de consumo de API`

---

## Feature 0.3 — Backend base en FastAPI

**Objetivo:** dejar corriendo una API simple, tipada y preparada para crecer hacia el motor de conciliación.

---

### Card 0.3.1 — Inicializar proyecto FastAPI

**Descripción:** crear el backend en Python con una estructura simple y productiva. El foco es legibilidad y velocidad, no arquitectura compleja.

**Criterio de aceptación:**

- El backend levanta en `http://localhost:8000`
- FastAPI responde correctamente
- Existe una estructura mínima de carpetas

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Crear proyecto Python en `backend/`
- [x] Definir herramienta de entorno y dependencias
- [x] Instalar `fastapi`, `uvicorn`, `pydantic`, `pandas`
- [x] Crear app principal y ruta `GET /health`
- [x] Verificar arranque local
- [ ] Commit sugerido: `chore(backend): inicializar backend FastAPI`

---

### Card 0.3.2 — Crear estructura modular inicial del backend

**Descripción:** separar desde el inicio lo necesario para evitar que el backend termine como un único archivo grande. Debe quedar listo para absorber engine, persistencia y API.

**Criterio de aceptación:**

- Existe una estructura inicial clara para `api`, `services`, `schemas`, `models` o equivalente
- La organización es suficientemente simple para MVP
- La ruta de health sigue funcionando dentro de esa estructura

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Crear estructura sugerida:
  - `app/api/`
  - `app/core/`
  - `app/services/`
  - `app/schemas/`
  - `app/models/`
- [ ] Mover la app a esa estructura
- [ ] Validar imports y arranque
- [ ] Commit sugerido: `chore(backend): crear estructura modular inicial`

---

### Card 0.3.3 — Configurar CORS y settings base

**Descripción:** dejar preparada la comunicación entre frontend y backend y centralizar configuración básica del servicio.

**Criterio de aceptación:**

- El backend acepta requests desde el frontend local
- Existe un módulo central de settings
- La configuración no está hardcodeada en múltiples archivos

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Configurar CORS para desarrollo local
- [ ] Crear settings con Pydantic o equivalente
- [ ] Mover variables sensibles a entorno
- [ ] Commit sugerido: `chore(backend): configurar settings base y cors`

---

## Feature 0.4 — Base de datos y storage en Supabase

**Objetivo:** dejar operativa la persistencia del MVP sin agregar infraestructura innecesaria.

---

### Card 0.4.1 — Crear proyecto Supabase del MVP

**Descripción:** crear el proyecto de Supabase que alojará Postgres y Storage. Esta es la base persistente de todo el producto demo.

**Criterio de aceptación:**

- Existe proyecto Supabase creado
- Se dispone de credenciales y URLs necesarias
- El entorno está listo para conectarse desde backend

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Crear proyecto Supabase para este MVP
- [ ] Guardar `project URL`, `anon key`, `service role key` y credenciales de DB
- [ ] Verificar acceso al panel
- [ ] Commit sugerido: no aplica si no hay cambios en repo

---

### Card 0.4.2 — Configurar conexión Postgres desde el backend

**Descripción:** preparar el backend para conectarse a Supabase Postgres. La solución debe ser simple, estable y compatible con las épicas de persistencia que vienen después.

**Criterio de aceptación:**

- El backend puede abrir conexión a la base
- Existe una estrategia definida para acceso a datos
- La conexión está encapsulada y no dispersa

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Elegir librería/patrón de acceso a DB para MVP
- [ ] Crear módulo de conexión base
- [ ] Probar conexión real con Supabase Postgres
- [ ] Dejar lista la base para definir tablas en la epic correspondiente
- [ ] Commit sugerido: `chore(db): configurar conexión base a Supabase Postgres`

---

### Card 0.4.3 — Configurar Supabase Storage

**Descripción:** el MVP necesita persistir archivos cargados por corrida. Storage debe quedar listo desde el inicio para evitar deuda operativa después.

**Criterio de aceptación:**

- Existe bucket para archivos del MVP
- El backend puede subir y recuperar un archivo de prueba
- La convención de paths queda definida

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Crear bucket de storage para uploads del MVP
- [ ] Definir convención de paths por `run_id`
- [ ] Probar upload y acceso de archivo de prueba
- [ ] Commit sugerido: `chore(storage): configurar bucket y convención de archivos`

---

## Feature 0.5 — Variables de entorno y configuración compartida

**Objetivo:** dejar ordenadas todas las variables necesarias para local y deploy, evitando configuraciones frágiles.

---

### Card 0.5.1 — Definir variables de entorno del frontend

**Descripción:** centralizar las variables públicas que necesita el frontend.

**Criterio de aceptación:**

- Existe `.env.local` documentado para frontend
- Las variables públicas están nombradas consistentemente
- El frontend no depende de valores hardcodeados

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir `NEXT_PUBLIC_API_BASE_URL`
- [ ] Definir cualquier URL pública necesaria de Supabase si aplica
- [ ] Crear ejemplo de entorno si conviene
- [ ] Commit sugerido: `chore(frontend): definir variables de entorno base`

---

### Card 0.5.2 — Definir variables de entorno del backend

**Descripción:** centralizar las variables privadas que necesita el backend para DB, Storage y settings operativos.

**Criterio de aceptación:**

- Existe archivo de entorno del backend
- Las credenciales no quedan expuestas
- El backend arranca leyendo configuración solo desde entorno

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Definir variables para DB
- [ ] Definir variables para Supabase Storage
- [ ] Definir variables para CORS y ambiente
- [ ] Documentar el set mínimo requerido
- [ ] Commit sugerido: `chore(backend): definir variables de entorno base`

---

## Feature 0.6 — Despliegue costo-eficiente del MVP

**Objetivo:** dejar operativo el camino de despliegue más simple y barato posible para este stage del producto.

---

### Card 0.6.1 — Desplegar frontend en Vercel

**Descripción:** el frontend debe tener un deploy público limpio para demo. Vercel es la opción natural por velocidad y fit con Next.js.

**Criterio de aceptación:**

- Existe deploy funcional del frontend
- El entorno de Vercel tiene variables configuradas
- La app responde públicamente

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Conectar repo o carpeta frontend a Vercel
- [ ] Configurar variables necesarias
- [ ] Verificar deploy exitoso
- [ ] Commit sugerido: no aplica si el cambio es solo de plataforma

---

### Card 0.6.2 — Definir estrategia de despliegue del backend

**Descripción:** para este MVP conviene dejar explícita la estrategia de deploy del backend antes de implementar demasiada lógica. Debe privilegiar simplicidad y costo.

**Criterio de aceptación:**

- Existe una estrategia de deploy definida y documentada
- La estrategia elegida es compatible con FastAPI y Supabase
- Queda claro cómo se conectará desde el frontend productivo

**Complejidad:** Media

**Estado:** PENDIENTE

**Tasks:**

- [ ] Evaluar despliegue simple del backend para MVP
- [ ] Definir URL base productiva del backend
- [ ] Verificar compatibilidad con CORS, DB y storage
- [ ] Documentar la decisión para no reabrirla más adelante
- [ ] Commit sugerido: `docs(deploy): definir estrategia de despliegue del backend`

---

## Feature 0.7 — Calidad mínima y documentación de arranque

**Objetivo:** asegurar que el proyecto pueda retomarse sin fricción y que el baseline técnico no se degrade desde el comienzo.

---

### Card 0.7.1 — Configurar calidad mínima del código

**Descripción:** dejar linter, formatter y convenciones mínimas activas en las capas donde apliquen.

**Criterio de aceptación:**

- Frontend tiene lint funcionando
- Backend tiene convención básica de formato/lint definida
- El proyecto puede validarse rápidamente antes de seguir construyendo

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Verificar y ajustar ESLint en frontend
- [ ] Definir formatter o lint básico para backend
- [ ] Crear comandos de chequeo mínimos
- [ ] Commit sugerido: `chore: configurar calidad mínima de código`

---

### Card 0.7.2 — Crear documentación mínima de setup

**Descripción:** dejar por escrito cómo levantar el proyecto, qué servicios requiere y qué falta para retomar trabajo en cualquier sesión futura.

**Criterio de aceptación:**

- Existe README o documento equivalente de arranque
- Se documentan pasos de frontend, backend, Supabase y variables
- Otra sesión puede retomar el proyecto sin depender de memoria oral

**Complejidad:** Baja

**Estado:** PENDIENTE

**Tasks:**

- [ ] Crear README técnico mínimo del proyecto
- [ ] Documentar cómo levantar frontend y backend
- [ ] Documentar variables requeridas
- [ ] Documentar dependencias externas del setup
- [ ] Commit sugerido: `docs: agregar guía mínima de setup del MVP`

---

## Resumen de commits esperados en EPIC 00

- `chore: crear estructura base del proyecto accounting-mvp`
- `docs: definir convenciones base de entorno y naming`
- `chore(frontend): inicializar app Next.js del MVP`
- `chore(frontend): configurar base visual mínima`
- `chore(frontend): preparar patrón base de consumo de API`
- `chore(backend): inicializar backend FastAPI`
- `chore(backend): crear estructura modular inicial`
- `chore(backend): configurar settings base y cors`
- `chore(db): configurar conexión base a Supabase Postgres`
- `chore(storage): configurar bucket y convención de archivos`
- `chore(frontend): definir variables de entorno base`
- `chore(backend): definir variables de entorno base`
- `docs(deploy): definir estrategia de despliegue del backend`
- `chore: configurar calidad mínima de código`
- `docs: agregar guía mínima de setup del MVP`

---

## Notas técnicas

### Guardrail principal de esta epic

No convertir el setup en un proyecto en sí mismo. Esta epic debe dejar una base confiable, no una infraestructura “perfecta”.

### Decisión de costo-eficiencia

La referencia para esta epic no es una arquitectura final enterprise, sino una arquitectura:

- suficientemente seria para vender
- suficientemente simple para construir rápido
- suficientemente barata para operar en etapa MVP

### Qué no entra en esta epic

- autenticación enterprise
- colas o workers complejos
- observabilidad avanzada
- CI/CD sofisticado
- infraestructura multiambiente formal
- modelado completo de tablas de negocio

Todo eso solo entra si se vuelve necesario para llegar a demo funcional, no antes.
