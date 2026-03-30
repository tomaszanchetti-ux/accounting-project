# EPIC 04 — Runs API, Persistence & Traceability

## Contexto y objetivo

Hasta este punto, el proyecto ya tiene:

- una base técnica definida
- un universo de datos demo diseñado
- un motor de conciliación operativo
- una capa de detección de excepciones y explicación rule-based

Lo que todavía no existe es la capa que convierte todo eso en un **producto utilizable**: una corrida identificable, persistible, trazable y accesible desde frontend o desde cualquier integración interna del MVP.

Esta epic construye precisamente ese puente.

Su función es transformar una ejecución lógica del motor en una **Run** real del sistema, con:

- identidad propia
- inputs asociados
- estado de procesamiento
- resultados persistidos
- excepciones registradas
- base de drill-down disponible
- endpoints consumibles por UI

Además, esta epic es la que instala la trazabilidad mínima que el proyecto necesita para sentirse serio frente a usuarios de Contabilidad, Finanzas o potenciales stakeholders de auditoría.

La tesis de esta epic es:

> **Una conciliación útil no es solo un cálculo. Es una corrida reproducible con insumos claros, outputs persistidos y una explicación consultable.**

Al terminar esta epic, el sistema debe poder:

- crear una nueva corrida
- asociarle archivos y contexto mínimo
- ejecutar el pipeline de conciliación y explicación
- persistir outputs relevantes
- consultar resumen, resultados por concepto y detalle
- servir endpoints claros para frontend
- dejar traza suficiente para reproducibilidad del demo

## Dominio(s) involucrado(s)

**D4 — Runs API, Persistence & Traceability**

## Dependencias

- **EPIC 01** completada o suficientemente avanzada
- **EPIC 02** completada o suficientemente avanzada
- **EPIC 03** completada o suficientemente avanzada
- **EPIC 00** completada o suficientemente avanzada para DB, backend y storage

## Criterio de aceptación de la Epic completa

- [x] Existe una entidad de corrida (`run`) con metadata mínima
- [x] El sistema puede registrar un payroll file y expected totals asociados a una run
- [x] Existe persistencia de resultados agregados por concepto
- [x] Existe persistencia de excepciones detectadas
- [x] Existe persistencia o staging del payroll normalizado para drill-down
- [x] El backend expone endpoints para crear run, ejecutar run, consultar summary, resultados y drill-down
- [x] La corrida deja trazabilidad suficiente para explicar qué se procesó, cuándo y con qué resultado
- [x] El payload de API es estable y usable por la UI del MVP

## Estado: COMPLETADA

---

## Feature 4.1 — Modelo de corrida del MVP

**Objetivo:** definir la entidad central del sistema operativo: la run de conciliación.

---

### Card 4.1.1 — Definir el modelo lógico `reconciliation_run`

**Descripción:** esta card fija la entidad madre de la capa operativa. Toda conciliación del producto debe poder referenciarse a través de una run concreta.

**Criterio de aceptación:**

- Existe definición explícita de `reconciliation_run`
- El modelo incluye identidad, período, estado y metadata relevante
- La entidad puede sostener trazabilidad funcional del MVP

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir campos mínimos de `reconciliation_run`:
  - `id`
  - `run_label` o `run_name`
  - `period`
  - `status`
  - `overall_status`
  - `source_file_name`
  - `record_count`
  - `concept_count`
  - `created_at`
  - `completed_at`
- [x] Definir si la run tendrá `entity_scope` o `legal_entity_scope` opcional
- [x] Documentar semántica de la entidad
- [ ] Commit sugerido: `docs(runs): definir modelo logico de reconciliation run`

**Resultado de la card:**

- modelo logico documentado en `docs/RUNS_MODEL_MVP.md`
- campos minimos y semantica de `reconciliation_run` cerrados
- `legal_entity_scope` adoptado como scope opcional del MVP

---

### Card 4.1.2 — Definir estados de la corrida

**Descripción:** la run necesita un ciclo de vida claro para ordenar tanto la lógica interna como la futura UX.

**Criterio de aceptación:**

- Existe una lista cerrada de estados de run del MVP
- Cada estado tiene significado funcional claro
- Los estados sirven tanto para backend como para UI

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir estados sugeridos:
  - `DRAFT`
  - `INPUT_VALIDATED`
  - `PROCESSING`
  - `RECONCILED`
  - `RECONCILED_WITH_EXCEPTIONS`
  - `FAILED`
  - `INVALID_INPUT`
- [x] Definir `overall_status` de negocio separado del estado técnico si aplica
- [x] Documentar transiciones válidas entre estados
- [ ] Commit sugerido: `docs(runs): definir estados de corrida del MVP`

**Resultado de la card:**

- estados tecnicos del MVP documentados en `docs/RUNS_MODEL_MVP.md`
- separacion entre `status` tecnico y `overall_status` de negocio definida
- transiciones validas cerradas para backend y UI

---

### Card 4.1.3 — Definir metadata mínima de trazabilidad

**Descripción:** antes de persistir resultados, conviene cerrar qué metadata debe quedar registrada por corrida para que la demo se sienta defendible.

**Criterio de aceptación:**

- Existe una lista explícita de metadata obligatoria por run
- La metadata responde preguntas de reproducibilidad
- No se cae en auditoría enterprise excesiva

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir metadata mínima:
  - archivo utilizado
  - timestamp
  - período procesado
  - cantidad de registros
  - cantidad de conceptos
  - reglas/tolerancias aplicadas
  - versión del motor o `rules_version`
- [x] Documentar qué queda fuera del MVP
- [ ] Commit sugerido: `docs(runs): definir metadata minima de trazabilidad`

**Resultado de la card:**

- metadata minima de trazabilidad documentada en `docs/RUNS_MODEL_MVP.md`
- reglas y versionado funcional delimitados para reproducibilidad del demo
- limites del MVP explicitados para evitar sobrediseño

---

## Feature 4.2 — Modelo de datos persistente del MVP

**Objetivo:** definir las entidades persistidas que permitirán consultar corridas, resultados, excepciones y detalle operativo.

---

### Card 4.2.1 — Definir entidad `expected_totals_used`

**Descripción:** no alcanza con saber qué expected totals existen teóricamente. La corrida debe saber exactamente qué referencia utilizó.

**Criterio de aceptación:**

- Existe una entidad o patrón para persistir expected totals usados en una run
- La relación con la run es clara
- La entidad permite reproducibilidad básica

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir tabla/entidad para expected totals utilizados por run
- [x] Incluir campos mínimos:
  - `run_id`
  - `period`
  - `concept_code_normalized`
  - `expected_amount`
  - `currency`
  - `legal_entity` opcional
- [x] Documentar si se guarda snapshot completo o referencia al archivo
- [ ] Commit sugerido: `docs(db): definir expected totals persistidos por run`

**Resultado de la card:**

- entidad documentada en `docs/RUNS_PERSISTENCE_MODEL.md`
- snapshot filtrado por periodo definido e implementado
- relacion directa con `run_id` cerrada para reproducibilidad

---

### Card 4.2.2 — Definir entidad `reconciliation_result`

**Descripción:** representa el resultado agregado por unidad conciliable. Es la tabla central para summary, concept analysis y parte de los exportables.

**Criterio de aceptación:**

- Existe una entidad persistente para resultados por concepto
- La entidad contiene métricas y estado suficientes para UI y API
- La relación con la run es directa y clara

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir campos mínimos:
  - `id`
  - `run_id`
  - `period`
  - `concept_code_normalized`
  - `concept_name_normalized`
  - `observed_amount`
  - `expected_amount`
  - `absolute_diff`
  - `relative_diff_pct`
  - `status`
  - `record_count`
  - `employee_count`
  - `summary_explanation`
- [x] Definir relación con `legal_entity` opcional
- [x] Preparar compatibilidad con future UI
- [ ] Commit sugerido: `docs(db): definir entidad reconciliation_result`

**Resultado de la card:**

- entidad documentada en `docs/RUNS_PERSISTENCE_MODEL.md`
- tabla fisica implementada en `backend/app/models/runs_schema.sql`
- payload persistido alineado con summary, detail y future UI

---

### Card 4.2.3 — Definir entidad `reconciliation_exception`

**Descripción:** persiste anomalías detectadas por la capa explicativa. Debe servir tanto para summary como para drill-down.

**Criterio de aceptación:**

- Existe entidad persistente para excepciones
- La entidad soporta excepciones por concepto y por registro
- Contiene tipo, severidad, impacto y observación

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir campos mínimos:
  - `id`
  - `run_id`
  - `result_id`
  - `record_id` opcional
  - `employee_id` opcional
  - `exception_type`
  - `severity`
  - `estimated_impact_amount`
  - `observation`
  - `created_at`
- [x] Definir nivel de granularidad por excepción
- [x] Documentar uso para UI y export
- [ ] Commit sugerido: `docs(db): definir entidad reconciliation_exception`

**Resultado de la card:**

- entidad documentada en `docs/RUNS_PERSISTENCE_MODEL.md`
- soporte a excepciones por concepto y por registro implementado
- relacion opcional con `result_id` cerrada para detail y export

---

### Card 4.2.4 — Definir entidad `run_payroll_line`

**Descripción:** persiste el payroll normalizado de la corrida para poder hacer drill-down sin recalcular todo desde el archivo bruto.

**Criterio de aceptación:**

- Existe una staging table o entidad equivalente para líneas normalizadas por run
- La entidad conserva trazabilidad suficiente a nivel línea
- El diseño facilita futuras queries de detalle

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir campos mínimos:
  - `id`
  - `run_id`
  - `record_id`
  - `employee_id`
  - `employee_name`
  - `legal_entity`
  - `country`
  - `cost_center`
  - `payroll_period`
  - `posting_date`
  - `concept_code_raw`
  - `concept_code_normalized`
  - `concept_name_raw`
  - `concept_name_normalized`
  - `amount`
  - `currency`
  - `is_valid`
  - `exception_flags`
- [x] Definir estrategia de persistencia de flags
- [x] Documentar por qué esta tabla entra al MVP
- [ ] Commit sugerido: `docs(db): definir staging run_payroll_line`

**Resultado de la card:**

- staging table documentada en `docs/RUNS_PERSISTENCE_MODEL.md`
- flags e invalid reasons persistidos como listas JSON
- base lista para drill-down sin recalculo desde CSV bruto

---

### Card 4.2.5 — Definir entidad `uploaded_file`

**Descripción:** registra metadata de archivos cargados por la run, aunque el contenido viva en storage.

**Criterio de aceptación:**

- Existe entidad de metadata de archivo
- La relación con la run y storage es explícita
- Permite trazabilidad del input utilizado

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir campos mínimos:
  - `id`
  - `run_id`
  - `file_name`
  - `file_type`
  - `storage_path`
  - `uploaded_at`
- [x] Definir tipos de archivo válidos del MVP
- [ ] Commit sugerido: `docs(db): definir metadata de archivos cargados`

**Resultado de la card:**

- entidad documentada en `docs/RUNS_PERSISTENCE_MODEL.md`
- soporte a `local_path` y `supabase_storage` definido en metadata
- tipos `payroll`, `expected_totals`, `concept_master` y `employee_reference` cerrados

---

## Feature 4.3 — Persistencia física y schema del backend

**Objetivo:** bajar el modelo lógico a implementación real en base de datos.

---

### Card 4.3.1 — Implementar tablas del dominio de runs

**Descripción:** crear las tablas físicas o modelos ORM correspondientes a la capa de runs.

**Criterio de aceptación:**

- Las tablas/modelos existen en la DB del MVP
- Las relaciones están correctamente definidas
- El backend puede leer y escribir sobre ellas

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Implementar `reconciliation_runs`
- [x] Implementar `expected_totals_used`
- [x] Implementar `reconciliation_results`
- [x] Implementar `reconciliation_exceptions`
- [x] Implementar `run_payroll_lines`
- [x] Implementar `uploaded_files`
- [x] Aplicar migraciones o creación de schema
- [ ] Commit sugerido: `feat(db): crear tablas de runs y resultados del MVP`

**Resultado de la card:**

- schema SQL creado en `backend/app/models/runs_schema.sql`
- tablas listas para uso desde repositorio psycopg
- inicializacion pragmatica del schema integrada al backend MVP

---

### Card 4.3.2 — Implementar índices y constraints mínimos

**Descripción:** aunque el MVP no necesita tuning sofisticado, sí conviene dejar índices mínimos para consultas frecuentes y consistencia.

**Criterio de aceptación:**

- Existen índices o constraints básicos sobre campos críticos
- Las queries principales del MVP son razonables
- El schema mantiene integridad mínima

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Indexar `run_id` en tablas hijas
- [x] Indexar `concept_code_normalized` y `status` donde tenga sentido
- [x] Agregar constraints básicos de relación e integridad
- [ ] Commit sugerido: `chore(db): agregar indices y constraints minimos`

**Resultado de la card:**

- indices base incluidos en `backend/app/models/runs_schema.sql`
- constraints de relacion agregados sobre `run_id` y `result_id`
- integridad minima lista para consultas del MVP

---

## Feature 4.4 — Repositorios y acceso a datos

**Objetivo:** encapsular la lectura y escritura de la capa de runs para evitar lógica de persistencia dispersa.

---

### Card 4.4.1 — Crear repositorio de runs

**Descripción:** concentra operaciones de creación, actualización de estado y consulta básica de corridas.

**Criterio de aceptación:**

- Existe módulo/repositorio para runs
- Las operaciones básicas están centralizadas
- La lógica de API no escribe directo a la DB en múltiples sitios

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Implementar crear run
- [x] Implementar actualizar estado de run
- [x] Implementar obtener run por id
- [x] Implementar listar runs básicas si conviene
- [ ] Commit sugerido: `feat(runs): crear repositorio base de runs`

**Resultado de la card:**

- repositorio base implementado en `backend/app/repositories/runs.py`
- creacion, lookup y cambios de estado centralizados
- upload y API ya no escriben directo estructuras sueltas

---

### Card 4.4.2 — Crear repositorio de resultados y excepciones

**Descripción:** encapsula persistencia y lectura de resultados agregados y excepciones explicativas.

**Criterio de aceptación:**

- Existe acceso estructurado a resultados y excepciones
- Las lecturas para summary y concept analysis están cubiertas
- La persistencia puede hacerse en lote de forma clara

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Implementar persistencia bulk de resultados
- [x] Implementar persistencia bulk de excepciones
- [x] Implementar lecturas por `run_id`
- [x] Implementar lectura por `result_id`
- [ ] Commit sugerido: `feat(runs): crear repositorio de resultados y excepciones`

**Resultado de la card:**

- persistencia bulk implementada para resultados y excepciones
- lecturas por run y por result disponibles para summary y detail
- orden de salida alineado con severidad operativa del MVP

---

### Card 4.4.3 — Crear repositorio de drill-down y staging lines

**Descripción:** encapsula consultas a líneas normalizadas por run, que serán la base de drill-down operativo.

**Criterio de aceptación:**

- Existe acceso estructurado a `run_payroll_lines`
- Se pueden filtrar líneas por concepto, excepción y empleado
- La capa queda lista para la UI de detalle

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Implementar persistencia bulk de staging lines
- [x] Implementar query por concepto
- [x] Implementar query por empleado
- [x] Implementar query por exception flags si aplica
- [ ] Commit sugerido: `feat(runs): crear repositorio de drilldown y staging`

**Resultado de la card:**

- staging lines persistidas en lote junto con la ejecucion
- consultas por concepto ya habilitan el drill-down del MVP
- exception flags quedan disponibles para evolucionar filtros ligeros

---

## Feature 4.5 — Gestión de archivos y storage

**Objetivo:** formalizar cómo se cargan, guardan y referencian los archivos del MVP.

---

### Card 4.5.1 — Definir convención de storage por run

**Descripción:** los archivos del MVP deben quedar organizados de forma estable y fácil de inspeccionar.

**Criterio de aceptación:**

- Existe convención explícita de paths en storage
- La convención es simple y compatible con el modelo de run
- Puede convivir con múltiples corridas sin ambigüedad

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir path base por `run_id`
- [x] Definir nombres para:
  - payroll file
  - expected totals
  - exportables futuros
- [x] Documentar convenciones de storage
- [ ] Commit sugerido: `docs(storage): definir convención de archivos por run`

**Resultado de la card:**

- convencion documentada en `docs/RUNS_PERSISTENCE_MODEL.md`
- path base fijado en `runs/<run_id>/inputs/<filename>`
- naming compatible con multiples corridas y buckets del MVP

---

### Card 4.5.2 — Implementar upload y registro de archivos

**Descripción:** el backend debe poder recibir un archivo, guardarlo en storage y persistir su metadata en la run.

**Criterio de aceptación:**

- El backend puede registrar archivos asociados a una run
- El archivo queda disponible en storage
- La metadata queda persistida en DB

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Implementar servicio de upload a Supabase Storage
- [x] Persistir metadata en `uploaded_files`
- [x] Asociar archivo con la run
- [x] Manejar errores de upload de forma estructurada
- [ ] Commit sugerido: `feat(storage): implementar upload y registro de archivos por run`

**Resultado de la card:**

- endpoint soporta referencias JSON y multipart upload real
- archivos se guardan en Supabase Storage bajo `runs/<run_id>/inputs/<filename>`
- metadata persiste en `uploaded_files` y queda lista para ejecucion posterior

---

## Feature 4.6 — Servicio de ejecución de runs

**Objetivo:** encapsular el flujo completo que toma una run, ejecuta el pipeline y persiste sus outputs.

---

### Card 4.6.1 — Diseñar el orquestador `execute_run`

**Descripción:** esta card define la función o servicio principal que hace el puente entre archivos persistidos, motor, explicación y base de datos.

**Criterio de aceptación:**

- Existe una función principal `execute_run`
- El flujo de ejecución está claramente definido
- El diseño contempla estados y errores de la run

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Diseñar secuencia de ejecución:
  - cargar metadata de run
  - leer archivos
  - ejecutar validación + normalización + motor
  - ejecutar excepciones + explicación
  - persistir resultados
  - actualizar estados
- [x] Definir inputs y outputs del orquestador
- [x] Documentar estrategia de manejo de errores
- [ ] Commit sugerido: `docs(runs): diseñar orquestador execute_run`

**Resultado de la card:**

- orquestador implementado en `backend/app/services/runs.py`
- secuencia de validacion, engine y persistencia quedo unificada
- estrategia basica de estados y errores ya quedo codificada

---

### Card 4.6.2 — Implementar ejecución sincrónica del MVP

**Descripción:** para este stage del producto, el camino correcto es una ejecución simple y sin workers complejos. Esta card lo implementa.

**Criterio de aceptación:**

- Una run puede ejecutarse de forma sincrónica
- El backend actualiza su estado durante la ejecución
- El resultado final queda persistido en una sola operación lógica

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Implementar cambio de estado a `PROCESSING`
- [x] Ejecutar pipeline completo desde el orquestador
- [x] Persistir resultados, excepciones y staging lines
- [x] Actualizar estado final de la run
- [ ] Commit sugerido: `feat(runs): implementar ejecucion sincronica de runs`

**Resultado de la card:**

- ejecucion sincronica operativa para el MVP
- outputs persistidos en una sola operacion logica por run
- estado final derivado del overall status del engine

---

### Card 4.6.3 — Manejar errores y estados fallidos de corrida

**Descripción:** el sistema debe fallar de forma explícita y útil, no silenciosa.

**Criterio de aceptación:**

- Las runs fallidas quedan en estado consistente
- Se registra error o motivo de invalidación
- El sistema distingue input inválido de fallo técnico

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Diferenciar `INVALID_INPUT` de `FAILED`
- [x] Persistir mensaje o detalle de error estructurado
- [x] Evitar runs huérfanas en `PROCESSING`
- [ ] Commit sugerido: `feat(runs): manejar errores y estados fallidos`

**Resultado de la card:**

- invalid input y fallo tecnico quedan separados en estados distintos
- error message queda persistido a nivel run
- la run siempre cierra en estado terminal conocido

---

## Feature 4.7 — API pública del backend para runs

**Objetivo:** exponer endpoints claros y estables que permitan operar la capa de corridas desde frontend.

---

### Card 4.7.1 — Implementar endpoint `POST /runs`

**Descripción:** crea una nueva corrida con metadata inicial y la deja lista para recibir archivos o configuración.

**Criterio de aceptación:**

- Existe endpoint para crear run
- La run queda persistida con estado inicial consistente
- La respuesta es utilizable por frontend

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir request/response schema
- [x] Persistir run en estado inicial
- [x] Devolver `run_id` y metadata básica
- [ ] Commit sugerido: `feat(api): agregar endpoint POST /runs`

**Resultado de la card:**

- endpoint implementado en `backend/app/api/routes/runs.py`
- respuesta utilizable para frontend desde el primer paso del setup
- metadata inicial de la run ya queda persistida

---

### Card 4.7.2 — Implementar endpoint `POST /runs/{run_id}/upload`

**Descripción:** permite subir o registrar archivos asociados a una corrida.

**Criterio de aceptación:**

- Existe endpoint para asociar archivos a la run
- El endpoint soporta al menos payroll y expected totals
- La respuesta informa estado y metadata útil

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir contrato para upload o referencia de archivos
- [x] Integrar servicio de storage
- [x] Persistir metadata en DB
- [x] Asociar archivo con la run
- [x] Manejar errores de upload de forma estructurada
- [ ] Commit sugerido: `feat(api): agregar endpoint de upload por run`

**Resultado de la card:**

- endpoint soporta referencias JSON y multipart upload real
- archivos se guardan en Supabase Storage bajo `runs/<run_id>/inputs/<filename>`
- metadata persiste en `uploaded_files` y queda lista para ejecucion posterior

---

### Card 4.7.3 — Implementar endpoint `POST /runs/{run_id}/execute`

**Descripción:** dispara la ejecución completa de la corrida.

**Criterio de aceptación:**

- Existe endpoint para ejecutar una run
- La ejecución usa el orquestador del dominio
- La respuesta deja claro el estado resultante o en progreso

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Validar precondiciones de la run
- [x] Invocar `execute_run`
- [x] Devolver payload claro de resultado o error
- [ ] Commit sugerido: `feat(api): agregar endpoint POST /runs/{run_id}/execute`

**Resultado de la card:**

- endpoint operativo sobre el orquestador del dominio
- devuelve estado final, metadata y mensajes claros
- soporta invalid input y failure de forma diferenciada

---

### Card 4.7.4 — Implementar endpoint `GET /runs/{run_id}/summary`

**Descripción:** expone el resumen ejecutivo de la corrida para la Summary UI futura.

**Criterio de aceptación:**

- Existe endpoint para consultar summary de una run
- El payload incluye KPIs y estado general
- La respuesta es estable y lista para UI

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Diseñar response schema de summary
- [x] Leer resultados persistidos y agregarlos
- [x] Incluir `overall_status` y conteos por estado
- [ ] Commit sugerido: `feat(api): agregar endpoint GET /runs/{run_id}/summary`

**Resultado de la card:**

- endpoint operativo con KPIs persistidos y preview de resultados
- `overall_status` y run metadata quedan disponibles para UI
- respuesta estable alineada al vertical slice del MVP

---

### Card 4.7.5 — Implementar endpoint `GET /runs/{run_id}/results`

**Descripción:** lista resultados agregados por concepto para tabla principal y navegación a detalle.

**Criterio de aceptación:**

- Existe endpoint para listar resultados por concepto
- El payload es ordenable y estable
- La salida soporta filtros básicos futuros si hiciera falta

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Implementar listado por `run_id`
- [x] Definir orden por severidad/estado
- [x] Exponer explicación resumida y métricas relevantes
- [ ] Commit sugerido: `feat(api): agregar endpoint GET /runs/{run_id}/results`

**Resultado de la card:**

- listado agregado por concepto operativo para tabla principal
- orden por severidad ya definido en repositorio
- explicacion resumida y metricas relevantes expuestas

---

### Card 4.7.6 — Implementar endpoint `GET /runs/{run_id}/results/{result_id}`

**Descripción:** devuelve el detalle de un concepto específico, incluyendo explicación y causas probables.

**Criterio de aceptación:**

- Existe endpoint de detalle por concepto
- La respuesta incluye métricas, explicación y resumen de causas
- Sirve como base directa para Concept Analysis UI

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Leer `reconciliation_result` por id
- [x] Leer excepciones asociadas
- [x] Construir payload de detalle del concepto
- [ ] Commit sugerido: `feat(api): agregar endpoint GET detalle de resultado`

**Resultado de la card:**

- detalle por concepto operativo para Concept Analysis UI
- respuesta incluye resultado persistido y excepciones asociadas
- base lista para enriquecer payload visual mas adelante

---

### Card 4.7.7 — Implementar endpoint `GET /runs/{run_id}/results/{result_id}/drilldown`

**Descripción:** expone líneas concretas que explican el resultado de un concepto.

**Criterio de aceptación:**

- Existe endpoint de drill-down operativo
- La respuesta puede devolver registros impactados y metadata útil
- El payload es compatible con filtros ligeros futuros

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Filtrar `run_payroll_lines` por concepto o referencia relevante
- [x] Asociar exception flags u observaciones
- [x] Diseñar response schema para tabla de detalle
- [ ] Commit sugerido: `feat(api): agregar endpoint GET de drilldown por concepto`

**Resultado de la card:**

- drill-down operativo a partir de staging persistido
- exception flags incluidos por fila
- payload base ya sirve para tabla de detalle del MVP

---

### Card 4.7.8 — Implementar endpoint `GET /health`

**Descripción:** endpoint mínimo de salud del backend para debugging, deploy y chequeo rápido.

**Criterio de aceptación:**

- Existe endpoint de health
- La respuesta es simple y estable
- Puede usarse desde frontend o monitoreo básico

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Exponer `GET /health`
- [x] Incluir estado básico del servicio
- [ ] Commit sugerido: `feat(api): exponer health check estable`

**Resultado de la card:**

- health check ya disponible en FastAPI
- contrato simple y estable mantenido para deploy y debugging

---

## Feature 4.8 — Summary model y payloads de UI

**Objetivo:** fijar contratos de respuesta que sirvan directamente a la capa visual del MVP, sin obligar al frontend a reinterpretar demasiado.

---

### Card 4.8.1 — Diseñar payload de Summary UI

**Descripción:** el frontend necesita una estructura clara para renderizar KPIs, overall status y tabla resumida.

**Criterio de aceptación:**

- Existe contrato explícito del payload de summary
- El payload cubre KPIs, status y preview de tabla
- La UI futura puede consumirlo casi directo

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir KPIs mínimos:
  - reconciled concepts
  - minor differences
  - unreconciled concepts
  - total amount reconciled
  - amount pending explanation
- [x] Incluir `overall_run_status`
- [x] Incluir metadata visible de la run
- [ ] Commit sugerido: `docs(api): diseñar payload de summary UI`

**Resultado de la card:**

- contrato materializado en `backend/app/schemas/runs.py`
- summary response ya expone KPIs, overall status y preview de resultados
- payload usable por UI sin reinterpretacion pesada

---

### Card 4.8.2 — Diseñar payload de Concept Analysis UI

**Descripción:** esta card fija la estructura que necesitará la vista detallada por concepto.

**Criterio de aceptación:**

- Existe contrato explícito del payload de concept analysis
- Incluye KPIs, explicación y evidencia resumida
- El payload sirve también para exportables futuros

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir campos del payload:
  - header del concepto
  - KPIs del concepto
  - statement principal
  - top causes
  - recommended action
  - evidence summary
- [x] Garantizar consistencia con capa explicativa
- [ ] Commit sugerido: `docs(api): diseñar payload de concept analysis`

**Resultado de la card:**

- contrato documentado en `docs/RUNS_UI_PAYLOADS.md`
- payload materializado en `backend/app/schemas/runs.py`
- detalle de resultado ya expone estructura directa para Concept Analysis UI

---

### Card 4.8.3 — Diseñar payload de Drill-down UI

**Descripción:** fija la estructura de respuesta para la tabla de registros afectados.

**Criterio de aceptación:**

- Existe contrato explícito del payload de drill-down
- Incluye filas, resumen e información de filtro
- La UI futura podrá renderizarlo sin lógica excesiva

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir columnas base del drill-down:
  - `record_id`
  - `employee_id`
  - `employee_name`
  - `legal_entity`
  - `concept`
  - `amount`
  - `period`
  - `exception_type`
  - `observation`
- [x] Definir summary superior del drill-down
- [x] Preparar compatibilidad con filtros ligeros
- [ ] Commit sugerido: `docs(api): diseñar payload de drilldown UI`

**Resultado de la card:**

- contrato documentado en `docs/RUNS_UI_PAYLOADS.md`
- drill-down response ya incluye `summary` y `filter_context`
- payload listo para renderizar tabla y filtros ligeros en UI

---

## Feature 4.9 — Trazabilidad operativa del MVP

**Objetivo:** asegurar que el sistema pueda explicar qué se corrió, con qué insumos y qué devolvió.

---

### Card 4.9.1 — Persistir `rules_version` y contexto mínimo de ejecución

**Descripción:** incluso en MVP, conviene poder decir con qué versión de reglas se generó un resultado.

**Criterio de aceptación:**

- La run guarda `rules_version` o equivalente
- Se registran parámetros mínimos relevantes
- La metadata permite reproducibilidad básica

**Complejidad:** Baja

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir campo `rules_version`
- [x] Persistir parámetros relevantes del execution context
- [x] Exponer metadata en consultas de run si corresponde
- [ ] Commit sugerido: `feat(traceability): persistir rules version y contexto de ejecucion`

**Resultado de la card:**

- `rules_version` y `tolerance_profile_label` persisten en la run
- metadata ya viaja en responses de create, execute y summary
- trazabilidad minima de contexto ya queda cubierta

---

### Card 4.9.2 — Diseñar bitácora mínima de eventos de corrida

**Descripción:** sin construir un audit trail enterprise, el MVP puede beneficiarse de una bitácora mínima de eventos relevantes.

**Criterio de aceptación:**

- Existe un diseño mínimo de eventos de run
- La bitácora es opcionalmente persistible o logueable
- Los eventos ayudan a debugging y narrativa interna

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Definir eventos mínimos:
  - run created
  - file uploaded
  - validation started
  - processing started
  - results persisted
  - run failed/completed
- [x] Definir si la bitácora vive en tabla o en logs estructurados del MVP
- [ ] Commit sugerido: `docs(traceability): diseñar bitacora minima de corrida`

**Resultado de la card:**

- diseño documentado en `docs/RUN_EVENTS_TRACEABILITY.md`
- timeline minima materializada como payload derivado de la run
- summary, detail y drill-down ya exponen `event_log`

---

## Feature 4.10 — Validación integral de la capa operativa

**Objetivo:** probar que la capa de runs, persistencia y API funciona end-to-end sobre el stack real del MVP.

---

### Card 4.10.1 — Probar flujo completo `create -> upload -> execute -> query summary`

**Descripción:** esta es la prueba operativa central de la epic. Verifica que el sistema ya funciona como producto mínimo y no solo como librería interna.

**Criterio de aceptación:**

- El flujo completo funciona sin intervención manual extraña
- La run cambia de estado de forma consistente
- El summary resultante es consultable

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Crear run vía API
- [x] Asociar archivos
- [x] Ejecutar run
- [x] Consultar summary
- [x] Verificar consistencia de datos persistidos
- [ ] Commit sugerido: `test(runs): validar flujo completo create-upload-execute-summary`

**Resultado de la card:**

- flujo validado en `backend/tests/test_runs_api_flow.py`
- create, upload por referencia, execute y summary ya quedan cubiertos
- consistencia base del vertical slice verificada en tests

---

### Card 4.10.2 — Probar lectura de resultados y drill-down

**Descripción:** valida que los endpoints de consulta realmente sirven a la operación del producto.

**Criterio de aceptación:**

- Se puede listar resultados por concepto
- Se puede abrir un resultado individual
- Se puede consultar drill-down asociado

**Complejidad:** Alta

**Estado:** COMPLETADA

**Tasks:**

- [x] Probar `GET /runs/{run_id}/results`
- [x] Probar `GET /runs/{run_id}/results/{result_id}`
- [x] Probar `GET /runs/{run_id}/results/{result_id}/drilldown`
- [x] Verificar consistencia entre summary, detail y drill-down
- [ ] Commit sugerido: `test(api): validar consultas de resultados y drilldown`

**Resultado de la card:**

- resultados, detail y drill-down ya validados por test automatizado
- consistencia entre capas de consulta cubierta en el vertical slice
- base lista para conectar UI sobre endpoints reales

---

### Card 4.10.3 — Validar trazabilidad de una corrida demo

**Descripción:** esta prueba verifica que una run pueda explicarse retrospectivamente usando solo los datos persistidos.

**Criterio de aceptación:**

- Se puede identificar input, período, resultados y excepciones de una run
- La metadata persistida es suficiente para demo y debugging
- No quedan huecos críticos de trazabilidad

**Complejidad:** Media

**Estado:** COMPLETADA

**Tasks:**

- [x] Verificar metadata de run
- [x] Verificar archivos asociados
- [x] Verificar resultados y excepciones persistidos
- [x] Verificar staging lines para concepto wow
- [ ] Commit sugerido: `test(traceability): validar trazabilidad minima de corrida demo`

**Resultado de la card:**

- trazabilidad demo validada en `backend/tests/test_runs_api_flow.py`
- metadata, archivos, resultados y excepciones quedan verificables desde API y repositorio
- no quedan huecos criticos de explicabilidad retrospectiva para el MVP

---

## Resumen de commits esperados en EPIC 04

- `docs(runs): definir modelo logico de reconciliation run`
- `docs(runs): definir estados de corrida del MVP`
- `docs(runs): definir metadata minima de trazabilidad`
- `docs(db): definir expected totals persistidos por run`
- `docs(db): definir entidad reconciliation_result`
- `docs(db): definir entidad reconciliation_exception`
- `docs(db): definir staging run_payroll_line`
- `docs(db): definir metadata de archivos cargados`
- `feat(db): crear tablas de runs y resultados del MVP`
- `chore(db): agregar indices y constraints minimos`
- `feat(runs): crear repositorio base de runs`
- `feat(runs): crear repositorio de resultados y excepciones`
- `feat(runs): crear repositorio de drilldown y staging`
- `docs(storage): definir convención de archivos por run`
- `feat(storage): implementar upload y registro de archivos por run`
- `docs(runs): diseñar orquestador execute_run`
- `feat(runs): implementar ejecucion sincronica de runs`
- `feat(runs): manejar errores y estados fallidos`
- `feat(api): agregar endpoint POST /runs`
- `feat(api): agregar endpoint de upload por run`
- `feat(api): agregar endpoint POST /runs/{run_id}/execute`
- `feat(api): agregar endpoint GET /runs/{run_id}/summary`
- `feat(api): agregar endpoint GET /runs/{run_id}/results`
- `feat(api): agregar endpoint GET detalle de resultado`
- `feat(api): agregar endpoint GET de drilldown por concepto`
- `feat(api): exponer health check estable`
- `docs(api): diseñar payload de summary UI`
- `docs(api): diseñar payload de concept analysis`
- `docs(api): diseñar payload de drilldown UI`
- `feat(traceability): persistir rules version y contexto de ejecucion`
- `docs(traceability): diseñar bitacora minima de corrida`
- `test(runs): validar flujo completo create-upload-execute-summary`
- `test(api): validar consultas de resultados y drilldown`
- `test(traceability): validar trazabilidad minima de corrida demo`

---

## Notas técnicas

### Decisión estructural clave

Esta epic consolida una decisión importante del MVP:

> **persistir el payroll normalizado de la corrida sí vale la pena**

Aunque agrega trabajo inicial, simplifica muchísimo:

- drill-down
- reproducibilidad
- exports
- debugging
- credibilidad de producto

### Decisión de arquitectura del MVP

La ejecución sigue siendo **sincrónica** y **simple**.

No entran todavía:

- workers
- colas
- background jobs
- polling complejo de backend
- arquitecturas distribuidas

Si una run del MVP tarda segundos, eso está bien. Esta epic debe optimizar claridad operativa, no sofisticación infra.

### Regla rectora de implementación

Cada decisión de esta epic debería pasar este filtro:

> “¿Esto hace que la corrida sea más reproducible, más visible y más fácil de consumir desde UI?”

Si no lo hace, probablemente no corresponde meterlo todavía.

### Qué no entra en esta epic

- export manager completo
- historial multi-run sofisticado
- filtros avanzados de portfolio
- auth enterprise sobre runs
- observabilidad avanzada
- scheduler o automatización recurrente

Todo eso puede venir después. Esta epic deja una capa operativa sólida, simple y suficiente para sostener la demo.
