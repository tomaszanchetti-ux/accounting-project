# EPIC 09 Residual Risks and Accepted Limits

## Objetivo

Documentar:

- riesgos funcionales residuales aceptados del MVP
- límites UX y operativos aceptados para demo

Este documento cierra las cards:

- `9.5.1 — Documentar riesgos funcionales residuales`
- `9.5.2 — Documentar límites UX y operativos aceptados`

## Principio de lectura

Estos puntos no describen bugs críticos pendientes.

Describen límites conscientes del MVP para proteger:

- claridad comercial
- expectativas correctas
- foco en demo vendible

## Riesgos funcionales residuales aceptados

### 1. La explicación sigue siendo rule-based

El MVP explica diferencias con reglas explícitas y templates controlados.

Qué implica:

- muy buena auditabilidad
- buena consistencia para demo
- menor flexibilidad ante casos ambiguos o combinaciones no previstas

Qué no prometer todavía:

- explicación abierta de cualquier caso complejo sin ampliar reglas
- interpretación semántica libre fuera del modelo actual

### 2. El dataset demo sigue siendo controlado

La narrativa está apoyada en un dataset sembrado para mostrar casos comerciales
concretos.

Qué implica:

- fuerte control del walkthrough
- repetibilidad alta
- menor representatividad de toda la variedad de payroll real

Qué no prometer todavía:

- cobertura natural de cualquier estructura o calidad de datos externa
- robustez universal frente a archivos arbitrarios no modelados

### 3. La ejecución sigue siendo sincrónica

Las runs se ejecutan en un flujo simple y lineal.

Qué implica:

- simplicidad operativa
- buen fit para demo y QA local
- sensibilidad mayor a latencia o payloads pesados en ambientes fríos

Qué no prometer todavía:

- procesamiento asíncrono sofisticado
- colas, monitoreo distribuido o control avanzado de concurrencia

### 4. Los exportables son básicos pero suficientes

El producto exporta summary y detail CSV de forma consistente.

Qué implica:

- salida útil para demo y seguimiento
- formato simple y portable
- sin capa extra de reporting o distribución avanzada

Qué no prometer todavía:

- paquetes ejecutivos ricos
- templates complejos de reporting
- versionado o sharing sofisticado de exportables

### 5. El walkthrough fuerte depende de entorno pre-calentado

El producto funciona bien en local y el flujo principal fue validado, pero el
drill-down sigue siendo la parte más pesada del recorrido.

Qué implica:

- conviene abrir el entorno antes de una reunión
- el walkthrough es más sólido si la demo se prepara unos minutos antes

Qué no prometer todavía:

- misma sensación de velocidad sin preparación en cualquier entorno frío

## Límites UX y operativos aceptados

### 1. El MVP es desktop-first

La experiencia está pensada para desktop y sharing de pantalla.

Qué implica:

- buena lectura en demo y review operativa
- menor prioridad de optimización profunda para móvil

### 2. No hay auth enterprise como parte del valor demo

La autenticación no es el foco del MVP comercial actual.

Qué implica:

- menor complejidad de flujo
- foco total en conciliación, explicación y evidencia

Qué no prometer todavía:

- permisos complejos por rol
- SSO enterprise
- auditoría de acceso avanzada

### 3. No existe un historial sofisticado de runs

La trazabilidad actual es suficiente para demo, pero no pretende ser un módulo
maduro de operaciones históricas.

Qué implica:

- hay contexto y eventos mínimos
- no hay exploración histórica rica ni gestión avanzada de corridas

### 4. No existe configuración avanzada por usuario

La UX no está diseñada como producto altamente parametrizable.

Qué implica:

- menos fricción para demo
- más control narrativo

Qué no prometer todavía:

- preferencias persistentes por usuario
- perfiles de configuración avanzados
- personalización extensa de reglas desde UI

### 5. La demo sigue priorizando linealidad sobre profundidad operativa

El producto está diseñado para ir de setup a insight y evidencia con la menor
fricción posible.

Qué implica:

- excelente historia comercial en pocos minutos
- menor cobertura de flujos secundarios o exploración libre

## Cómo defender estos límites sin improvisar

Mensaje recomendado:

> El MVP está optimizado para demostrar valor rápido en conciliación,
> explicabilidad y trazabilidad. Los límites actuales no contradicen esa
> promesa; simplemente evitan sobreingeniería antes de validar la oportunidad.

## Conclusión

Los riesgos y límites listados arriba son aceptables para el alcance demo del
MVP.

No invalidan el valor principal del producto y ayudan a proteger expectativas
correctas frente a una audiencia comercial o de discovery.

## Siguiente paso recomendado

Avanzar con la definición formal del checklist final de `demo-ready`.
