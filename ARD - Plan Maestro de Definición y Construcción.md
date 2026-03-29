# **Accounting Reconciliation Demo**

## **Plan Maestro de Definición y Construcción**

---

# **Fase A: Fundamentos**

# **1\. Contexto y oportunidad**

Las organizaciones multinacionales operan con estructuras complejas donde múltiples sistemas intervienen en la generación, procesamiento y validación de información financiera.

Uno de los procesos críticos es la **conciliación entre RRHH y Contabilidad**, particularmente sobre datos de nómina, beneficios y deducciones.

En la práctica:

* RRHH gestiona la nómina en sistemas como SAP  
* Contabilidad recibe exportes (generalmente CSV)  
* Se requiere validar que los totales por concepto coincidan con valores esperados

Este proceso suele ser:

* manual  
* repetitivo  
* propenso a errores  
* dependiente de conocimiento tácito  
* difícil de auditar

👉 Esto abre una oportunidad clara para una solución que automatice, estandarice y explique este proceso.

---

# **2\. Problema a resolver**

El problema no es únicamente calcular totales.

Es un problema compuesto por tres dimensiones:

## **2.1 Agregación de datos**

* Consolidar miles de registros por empleado  
* Agrupar por concepto, período, entidad, etc.

## **2.2 Conciliación**

* Comparar totales calculados vs valores esperados  
* Determinar si un concepto “netea” o no

## **2.3 Explicación de diferencias**

Cuando no hay match, el desafío es responder:

* cuánto difiere  
* por qué difiere  
* qué registros explican la diferencia  
* qué tipo de error ocurrió

👉 Aquí es donde se concentra el mayor valor del sistema.

---

# **3\. Objetivo del proyecto**

Construir una **demo funcional creíble** que permita:

* simular el proceso real de conciliación  
* demostrar automatización del cálculo  
* evidenciar detección de diferencias  
* mostrar capacidad de explicación  
* generar identificación inmediata con el usuario final

---

## **3.1 Objetivo comercial**

La demo debe:

* generar efecto *“esto es exactamente lo que hacemos hoy”*  
* validar la oportunidad con el cliente  
* habilitar un proyecto de discovery o implementación  
* posicionar al equipo como experto en este tipo de soluciones

---

## **3.2 Objetivo técnico**

Construir un **proto-producto reutilizable** que:

* pueda evolucionar a solución real  
* sea reutilizable con otros clientes  
* sirva como base para futuras extensiones

---

# **4\. Usuario principal y stakeholders**

## **Usuario principal**

**Perfil:**

* Contabilidad / Administración & Finanzas  
* Controller / equipo de cierre contable

## **Necesidades**

* validar rápidamente si los números cuadran  
* entender diferencias sin análisis manual extensivo  
* tener trazabilidad del proceso  
* reducir tiempo operativo

---

## **Stakeholders secundarios**

* RRHH → origen de datos  
* Finanzas → validación de impacto  
* Auditoría → trazabilidad y evidencia  
* IT → integración futura

---

# **5\. Caso de uso central**

El flujo principal que debe cubrir la demo es:

Un usuario de Contabilidad carga un archivo de nómina (CSV), define o visualiza los totales esperados por concepto para un período, ejecuta la conciliación y el sistema le muestra qué conceptos netean, cuáles no y por qué.

---

## **Resultado esperado**

El sistema debe responder:

* estado de conciliación por concepto  
* diferencia absoluta y relativa  
* causas probables de discrepancias  
* registros específicos que explican la diferencia

---

# **6\. Propuesta de solución**

La solución se plantea como una plataforma compuesta por tres capas:

---

## **6.1 Capa de ingesta**

Permite:

* cargar archivos CSV (export SAP)  
* validar estructura  
* normalizar datos

---

## **6.2 Motor de conciliación**

Responsable de:

* agrupar datos  
* calcular totales por concepto  
* comparar contra valores esperados  
* detectar diferencias  
* clasificar excepciones  
* generar explicaciones

---

## **6.3 Capa de visualización (frontend)**

Permite al usuario:

* configurar el proceso  
* ejecutar conciliación  
* visualizar resultados  
* explorar diferencias (drill-down)  
* exportar resultados

---

# **7\. Flujo funcional de alto nivel**

El sistema sigue el siguiente flujo:

### **1\. Ingreso de datos**

* carga de CSV  
* selección de período  
* carga de expected totals

### **2\. Procesamiento**

* validación  
* normalización  
* agrupación

### **3\. Conciliación**

* cálculo de totales  
* comparación  
* clasificación de estados

### **4\. Análisis de diferencias**

* identificación de anomalías  
* clasificación de causas

### **5\. Visualización**

* resumen ejecutivo  
* detalle por concepto  
* drill-down por empleado

### **6\. Output**

* exportable  
* registro de corrida

---

# **8\. Componentes macro de la solución**

## **Frontend**

* interfaz de usuario  
* interacción con el sistema

## **Backend**

* API  
* lógica de procesamiento

## **Motor de conciliación**

* reglas de negocio  
* agregaciones  
* validaciones

## **Capa de datos**

* almacenamiento (opcional en MVP)  
* estructuras de datos

## **Dataset dummy**

* datos simulados  
* anomalías inyectadas

---

# **9\. Alcance del demo (MVP)**

El demo incluirá:

* 1 país o entidad  
* 1 período (mensual)  
* 5–10 conceptos principales  
* dataset de 200–500 empleados  
* conciliación por concepto  
* explicación básica de diferencias  
* interfaz simple pero creíble

---

# **10\. Fuera de alcance (por ahora)**

Para evitar sobreingeniería:

* integración directa con SAP  
* multi-país complejo  
* multi-moneda avanzada  
* motor de reglas configurable por usuario  
* workflows de aprobación  
* seguridad enterprise  
* automatización completa del pipeline

---

# **11\. Principios de diseño**

## **1\. Realismo \> sofisticación**

Debe parecer real, no perfecto.

## **2\. Explicabilidad como core**

No solo detectar diferencias, sino explicarlas.

## **3\. Simplicidad técnica**

Evitar sobrearquitectura en etapa demo.

## **4\. UX orientada a negocio**

Diseño centrado en el usuario contable.

## **5\. Trazabilidad mínima**

Cada resultado debe poder explicarse.

---

# **12\. Criterios de éxito**

La demo es exitosa si logra:

### **A nivel usuario**

* comprensión inmediata  
* identificación con el problema  
* percepción de ahorro de tiempo

### **A nivel negocio**

* interés en avanzar a discovery  
* validación del caso de uso  
* apertura de oportunidad comercial

### **A nivel técnico**

* funcionamiento consistente  
* resultados coherentes  
* explicación creíble de diferencias

# 

# 

# 

# 

# **Fase B: Arquitectura funcional de la solución**

---

## **B.1 Visión funcional general**

La solución debe entenderse como una **plataforma de conciliación asistida** que recibe información operativa de nómina, la transforma en una base conciliable, la compara contra referencias esperadas y devuelve resultados explicables y navegables para el usuario de Contabilidad.

Funcionalmente, el sistema no es solo un visor de archivos ni un dashboard estático. Su lógica está en **tomar un input crudo, procesarlo bajo reglas definidas, producir un juicio de conciliación y explicar el resultado**.

La arquitectura funcional del demo se organiza en **cinco bloques principales**:

### **1\. Bloque de configuración e ingreso**

Donde el usuario carga o define los insumos necesarios para la corrida.

Incluye:

* archivo payroll / nómina exportado  
* período a analizar  
* expected totals por concepto  
* eventualmente tablas auxiliares o mappings

---

### **2\. Bloque de validación y normalización**

Donde el sistema transforma el input en una estructura consistente y utilizable.

Incluye:

* validación de columnas obligatorias  
* validación básica de tipos y consistencia  
* estandarización de nombres/códigos  
* preparación del dataset para conciliación

---

### **3\. Bloque de conciliación**

Donde se ejecuta el corazón del sistema.

Incluye:

* agregación por concepto y período  
* cálculo de totales observados  
* comparación contra valores esperados  
* evaluación de tolerancias  
* asignación de estado de conciliación

---

### **4\. Bloque de análisis y explicación**

Donde el sistema intenta responder por qué existe una diferencia.

Incluye:

* detección de excepciones  
* clasificación de anomalías  
* priorización de causas probables  
* narrativa explicativa  
* sugerencias de revisión

---

### **5\. Bloque de visualización y salida**

Donde el usuario consume el resultado y baja al detalle.

Incluye:

* resumen ejecutivo de corrida  
* tabla por concepto  
* vista explicativa  
* drill-down por empleado / línea  
* exportables

---

### **Definición sintética de la visión funcional**

La solución funciona como un pipeline asistido:

**Input contable-operativo → preparación de datos → conciliación automática → explicación de diferencias → visualización auditable**

Ese es el corazón funcional del demo.

---

## **B.2 Flujo operativo del usuario**

El usuario principal del demo es alguien de **Contabilidad / Administración & Finanzas** que quiere entender rápidamente si los importes de nómina y beneficios cuadran o no para un período determinado.

El flujo operativo ideal debe ser **simple, corto y orientado a resultado**. No queremos una experiencia compleja ni cargada de configuraciones.

### **Paso 1\. Iniciar corrida**

El usuario entra al sistema y comienza una nueva corrida de conciliación.

En este momento el sistema debe permitir:

* identificar el período  
* cargar el archivo principal  
* cargar o visualizar expected totals  
* revisar parámetros básicos

---

### **Paso 2\. Validar insumos**

Antes de correr la conciliación, el sistema valida que el input sea usable.

El usuario debe recibir una respuesta clara del tipo:

* archivo válido  
* archivo inválido  
* faltan columnas  
* hay registros fuera de período  
* hay conceptos no reconocidos

Este paso evita que la demo se perciba como una “caja negra”.

---

### **Paso 3\. Ejecutar conciliación**

El usuario dispara la corrida.

El sistema:

* procesa el archivo  
* agrega datos  
* compara contra expected totals  
* calcula diferencias  
* clasifica resultados

---

### **Paso 4\. Revisar resumen general**

El usuario accede a una vista ejecutiva donde ve:

* cuántos conceptos conciliaron  
* cuántos no conciliaron  
* monto total conciliado  
* monto con diferencias  
* severidad general de la corrida

Este es el primer momento de valor visible.

---

### **Paso 5\. Analizar conceptos con diferencias**

El usuario entra a los conceptos marcados en amarillo o rojo.

Debe poder ver:

* total esperado  
* total calculado  
* diferencia absoluta  
* diferencia relativa  
* estado  
* explicación preliminar

---

### **Paso 6\. Ir al drill-down**

Para un concepto particular, el usuario baja al detalle.

Debe poder ver:

* empleados o registros involucrados  
* anomalías detectadas  
* registros faltantes, duplicados o mal clasificados  
* evidencia que explique el desvío

Este es el principal **wow moment** del demo.

---

### **Paso 7\. Exportar o cerrar la corrida**

Finalmente, el usuario puede:

* exportar resultados  
* guardar la corrida  
* dejar trazabilidad de lo ejecutado

---

### **Principios del flujo operativo**

El flujo debe cumplir con estos criterios:

* **ser guiado**, no exploratorio caótico  
* **llevar rápido al insight**  
* **hacer visible el valor del motor**  
* **minimizar pasos irrelevantes**  
* **parecer un proceso real de trabajo**

---

## **B.3 Entradas del sistema**

La demo necesita un conjunto acotado pero suficiente de inputs para que la lógica tenga credibilidad.

### **B.3.1 Archivo principal de payroll**

Es el input central del sistema.

Representa el extracto exportado desde SAP o sistema equivalente.  
Debe contener múltiples líneas por empleado y por concepto.

Su función es ser la fuente observada a conciliar.

Debe incluir, conceptualmente:

* identificador de empleado  
* período  
* concepto  
* importe  
* entidad  
* centro de costo  
* moneda

---

### **B.3.2 Expected totals**

Representan la referencia contra la cual se compara el resultado calculado.

Funcionalmente, deben actuar como la “verdad esperada” para el período y concepto.

Pueden ser:

* cargados manualmente  
* cargados vía archivo auxiliar  
* predefinidos dentro del demo

Para el MVP/demo, lo más funcional es que el usuario pueda verlos como una tabla simple, editable o cargable.

---

### **B.3.3 Parámetros de corrida**

El sistema también necesita algunos parámetros de contexto.

Ejemplos:

* período de conciliación  
* entidad o sociedad  
* criterio de tolerancia  
* reglas activas

Para el demo, estos parámetros deben ser mínimos y no generar fricción.

---

### **B.3.4 Tablas auxiliares**

Puede haber inputs adicionales que no siempre sean visibles para el usuario, pero que funcionalmente ayuden a sostener la lógica.

Ejemplos:

* maestro de conceptos  
* tabla de mapeo de códigos  
* catálogo de categorías  
* reglas de clasificación de anomalías

---

### **B.3.5 Supuestos de entrada**

Para que el demo sea realista pero manejable, dejamos explícitos estos supuestos:

* existe un archivo principal por corrida  
* el archivo representa un período concreto  
* los expected totals están disponibles  
* los datos tienen errores plausibles, no caos total  
* el usuario no debe diseñar reglas desde cero

---

## **B.4 Procesamiento funcional**

Este bloque describe qué hace el sistema con los inputs, en qué orden y con qué propósito funcional.

### **B.4.1 Validación inicial**

Antes de cualquier conciliación, el sistema valida:

* presencia de columnas obligatorias  
* tipos de dato mínimos  
* existencia de período  
* existencia de importes  
* consistencia básica del archivo

El objetivo no es auditar exhaustivamente el archivo, sino determinar si el sistema puede trabajar con él.

---

### **B.4.2 Normalización**

Una vez validado, el sistema estandariza la información para volverla comparable.

Incluye:

* limpiar nombres de columnas  
* homogeneizar códigos de concepto  
* convertir importes a formato consistente  
* estandarizar período  
* marcar registros sospechosos

Este paso es central porque muchas diferencias reales aparecen por inconsistencias de forma, no de fondo.

---

### **B.4.3 Preparación de la base conciliable**

El sistema arma una estructura intermedia orientada a conciliación.

Esto implica:

* seleccionar registros relevantes  
* filtrar el período aplicable  
* enriquecer con metadata funcional  
* vincular con expected totals  
* dejar lista una base agregable

---

### **B.4.4 Agregación**

El sistema consolida importes según la unidad de conciliación definida.

Ejemplo para el MVP:

* sumar montos por concepto y período

Opcionalmente puede considerar otras dimensiones:

* entidad  
* país  
* cost center

La agregación debe producir el **observed total**.

---

### **B.4.5 Comparación**

Una vez obtenido el total observado, el sistema lo compara contra el total esperado.

Debe calcular:

* diferencia absoluta  
* diferencia porcentual  
* estado de conciliación  
* severidad

---

### **B.4.6 Detección de excepciones**

Cuando existe diferencia o cuando el input presenta anomalías relevantes, el sistema activa reglas de análisis.

Busca detectar:

* duplicados  
* faltantes  
* códigos no mapeados  
* outliers  
* registros fuera de período  
* posibles errores de signo o clasificación

---

### **B.4.7 Generación de explicación**

A partir del resultado de conciliación y de las excepciones detectadas, el sistema construye una explicación funcional.

Debe responder:

* qué pasó  
* cuánto impactó  
* qué registros lo explican  
* qué revisar primero

---

### **B.4.8 Preparación de outputs**

Finalmente, el sistema arma la información en formatos consumibles para el front y los exportables.

Incluye:

* resumen general  
* resultados por concepto  
* excepciones  
* tablas de detalle  
* metadata de corrida

---

## **B.5 Salidas del sistema**

El sistema debe producir resultados en varios niveles de lectura, porque no todos los usuarios necesitan el mismo nivel de profundidad.

---

### **B.5.1 Resumen ejecutivo de corrida**

Es la salida más sintética.

Debe mostrar:

* período analizado  
* cantidad de conceptos conciliados  
* cantidad de conceptos con diferencias  
* monto total conciliado  
* monto total no conciliado  
* estado general de la corrida

Esta vista debe responder en segundos:  
**“¿Está bien o hay problemas?”**

---

### **B.5.2 Resultado por concepto**

Es la salida estructural principal del demo.

Cada concepto debe mostrar al menos:

* nombre / código  
* total esperado  
* total calculado  
* diferencia  
* diferencia %  
* estado  
* explicación resumida

Esta tabla es el puente entre la visión ejecutiva y el análisis detallado.

---

### **B.5.3 Vista explicativa**

Para cada concepto con diferencia, el sistema debe generar una explicación entendible.

Ejemplos funcionales:

* diferencia explicada por registros fuera de período  
* presencia de conceptos no mapeados  
* duplicados detectados  
* empleados faltantes o importes atípicos

La explicación no tiene que ser “inteligencia perfecta”; tiene que ser **útil y creíble**.

---

### **B.5.4 Drill-down operativo**

Es la salida de mayor detalle.

Debe permitir ver:

* registros impactantes  
* empleados involucrados  
* importe por línea  
* tipo de excepción  
* observaciones relevantes

Esta capa convierte el sistema en una herramienta de trabajo, no solo en un reporte.

---

### **B.5.5 Exportables**

La demo debe poder producir alguna forma de salida descargable.

Idealmente:

* resumen de conciliación  
* detalle por concepto  
* detalle de excepciones

Esto refuerza la sensación de producto real y útil para auditoría o seguimiento.

---

## **B.6 Persistencia y trazabilidad**

Aunque sea una demo, el sistema gana mucha credibilidad si deja una traza mínima de lo que pasó.

### **B.6.1 Qué conviene persistir**

Para el MVP/demo, conviene guardar al menos:

* metadata de la corrida  
* período  
* archivo utilizado  
* expected totals utilizados  
* fecha/hora de ejecución  
* resultados por concepto  
* excepciones detectadas

---

### **B.6.2 Qué no hace falta persistir en esta etapa**

No es necesario todavía:

* versionado sofisticado de reglas  
* historiales complejos de usuario  
* workflows de aprobación  
* auditoría enterprise completa

---

### **B.6.3 Rol funcional de la persistencia**

Persistir no es un capricho técnico. Cumple tres funciones claras:

#### **1\. Reproducibilidad**

Poder decir qué se corrió y con qué insumos.

#### **2\. Trazabilidad**

Poder mostrar de dónde sale cada resultado.

#### **3\. Sensación de producto real**

Una demo que “recuerda corridas” se percibe mucho más seria.

---

### **B.6.4 Trazabilidad mínima requerida**

Cada corrida debería dejar visible:

* identificador de corrida  
* período procesado  
* timestamp  
* cantidad de registros procesados  
* cantidad de conceptos analizados  
* reglas o parámetros aplicados  
* estado general

---

## **B.7 Estados del proceso**

Definir estados claros ordena tanto la UX como la lógica funcional.

---

### **B.7.1 Estados de la corrida**

La corrida como proceso puede pasar por estados como:

* **Draft / Configuración**  
* **Input Validated**  
* **Processing**  
* **Reconciled**  
* **Reconciled with Exceptions**  
* **Failed / Invalid Input**

Esto ayuda a modelar qué está ocurriendo y qué puede hacer el usuario en cada momento.

---

### **B.7.2 Estados de conciliación por concepto**

Cada concepto debe caer en un estado entendible y accionable.

Propuesta para el MVP:

* **Reconciled**  
  El total observado coincide con el esperado dentro de tolerancia.  
* **Minor Difference**  
  Existe una diferencia baja o tolerable, que no rompe la conciliación total pero merece revisión.  
* **Unreconciled**  
  La diferencia excede la tolerancia y requiere análisis.  
* **Invalid / Incomplete**  
  No hay información suficiente o el input del concepto presenta problemas que impiden evaluarlo correctamente.

---

### **B.7.3 Estados de excepción**

Además del estado de conciliación, algunas observaciones pueden marcarse como excepciones.

Ejemplos:

* duplicate detected  
* unmapped concept  
* out-of-period record  
* outlier amount  
* missing expected total

Estos estados no reemplazan la conciliación, la enriquecen.

---

### **B.7.4 Función funcional de los estados**

Los estados deben servir para:

* priorizar revisión  
* ordenar visualmente los resultados  
* disparar explicaciones  
* hacer más intuitiva la demo

No deben ser demasiados ni ambiguos.

---

# **Conclusión de la Sección B**

La arquitectura funcional del demo queda definida como un sistema con esta lógica:

### **Entradas**

* payroll file  
* expected totals  
* parámetros mínimos

### **Proceso**

* validación  
* normalización  
* agregación  
* comparación  
* detección de excepciones  
* explicación

### **Salidas**

* resumen ejecutivo  
* conciliación por concepto  
* detalle explicativo  
* drill-down operativo  
* exportables

### **Capas funcionales**

1. Configuración e ingreso  
2. Preparación de datos  
3. Conciliación  
4. Explicación  
5. Visualización y salida

---

# **Qué deja cerrado esta sección**

Con esta sección ya queda definido:

* cómo funciona el sistema de punta a punta  
* qué rol tiene el usuario  
* qué inputs necesita la demo  
* qué hace el motor funcionalmente  
* qué outputs debe producir  
* qué nivel mínimo de trazabilidad conviene sostener

Esto ya nos permite avanzar con mucha más precisión a la siguiente capa.

# 

# **Fase C. Modelo de conciliación y reglas de negocio**

La función central del sistema es transformar un archivo operativo de nómina en un **juicio de conciliación explicable**.

Eso implica que el sistema no solo suma importes: también debe decidir **qué comparar**, **cómo compararlo**, **cuándo considerar que netea**, **qué anomalías identificar** y **cómo traducir todo eso en una explicación creíble para Contabilidad**.

Para el MVP/demo, el modelo de conciliación debe cumplir cinco condiciones:

* ser **simple de implementar**  
* ser **realista para el usuario**  
* permitir **casos wow demostrables**  
* generar **resultados consistentes**  
* dejar una base escalable hacia una versión real

---

## **C.1 Unidad de conciliación**

La primera decisión clave es definir **qué unidad exacta estamos conciliando**.

Para este MVP/demo, la unidad principal de conciliación será:

**Concepto de nómina por período de conciliación**

Es decir, el sistema tomará múltiples líneas individuales del payroll file y las consolidará para responder:

**“¿El total observado de este concepto en este período coincide con el total esperado?”**

---

### **Definición funcional de la unidad de conciliación**

Cada unidad conciliable estará compuesta por:

* **período**  
* **concepto**  
* opcionalmente una dimensión organizativa simple, como:  
  * sociedad / legal entity  
  * país  
  * cost center

---

### **Decisión para el MVP**

Para no sobredimensionar el demo, propongo esta lógica:

#### **Nivel principal**

* **período \+ concepto**

#### **Nivel secundario opcional**

* **período \+ concepto \+ legal\_entity**

Esto nos deja una demo suficientemente realista, sin volverla compleja.

---

### **Qué implica esta decisión**

El sistema **no conciliará por empleado individualmente** como unidad principal.

El empleado será una unidad de **explicación/drill-down**, no de conciliación primaria.

Eso es correcto conceptualmente porque el proceso real contable suele buscar primero:

* si el **total** cierra  
* y solo después bajar al detalle individual

---

### **Ventaja de esta elección**

Nos permite tener tres niveles bien diferenciados:

#### **Nivel 1 — Ejecutivo**

¿El concepto netea o no?

#### **Nivel 2 — Analítico**

¿Cuál es la diferencia y cuál podría ser la causa?

#### **Nivel 3 — Operativo**

¿Qué empleados o líneas explican la diferencia?

Ese escalonamiento es ideal para la demo.

---

## **C.2 Dimensiones de agregación**

Una vez definida la unidad conciliable, debemos definir **cómo se agregan los datos observados**.

---

### **Agregación principal**

Para cada combinación conciliable, el sistema debe sumar:

**total observado \= suma de importes payroll válidos para ese concepto y período**

---

### **Dimensiones candidatas**

Podrían existir múltiples dimensiones:

* período  
* concepto  
* legal entity  
* país  
* cost center  
* moneda  
* categoría de beneficio

Pero para el MVP/demo debemos elegir solo las necesarias.

---

### **Definición recomendada para el MVP**

#### **Dimensiones obligatorias**

* `payroll_period`  
* `concept_code` o `concept_name_normalized`

#### **Dimensión opcional recomendada**

* `legal_entity`

#### **Dimensiones visibles pero no determinantes**

* `employee_id`  
* `employee_name`  
* `cost_center`  
* `country`

Estas últimas enriquecen el análisis, pero no son parte obligatoria de la conciliación base.

---

### **Criterio de agregación**

El sistema debe incluir en la suma únicamente registros que:

* pertenezcan al período conciliado  
* tengan concepto reconocido o mapeable  
* tengan importe interpretable  
* no estén excluidos por reglas de invalidación

Esto es importante porque no toda línea del archivo necesariamente entra al cálculo principal.

---

### **Resultado de la agregación**

La agregación debe producir, por cada unidad conciliable:

* total observado  
* cantidad de registros involucrados  
* cantidad de empleados involucrados  
* flags relevantes:  
  * registros fuera de período  
  * conceptos no mapeados  
  * duplicados potenciales  
  * outliers

Eso permite que la conciliación no sea solo matemática, sino también contextual.

---

## **C.3 Totales esperados**

El segundo pilar del modelo es definir qué representa el **expected total**.

En el demo, el expected total será:

**el valor de referencia que Contabilidad espera ver conciliado para un concepto en un período**

Puede representar, según la narrativa:

* un valor informado por RRHH  
* un control interno  
* una referencia de cierre  
* un asiento esperado  
* una liquidación de proveedor de beneficios

No hace falta cerrarlo a una única fuente “real”, pero sí debe quedar funcionalmente claro que es la **verdad de control**.

---

### **Formato funcional del expected total**

Para cada unidad conciliable, el sistema debe disponer de:

* período  
* concepto  
* expected\_amount  
* opcionalmente legal\_entity  
* opcionalmente moneda

---

### **Relación con la unidad de conciliación**

La regla es simple:

Cada unidad conciliable debe tener, idealmente, un total esperado correspondiente.

Si no existe expected total:

* el concepto no puede evaluarse plenamente  
* debe caer en estado **Invalid / Incomplete** o equivalente

---

### **Cómo se cargan en el MVP**

Para el demo, conviene que los expected totals puedan venir de dos maneras:

#### **Modo A — precargados**

Ideal para la demo guiada

#### **Modo B — cargables/editables**

Ideal para hacerla sentir más producto

Mi recomendación:

* tenerlos **precargados**  
* pero presentarlos como si fueran una tabla visible y eventualmente editable

Eso combina control narrativo con sensación de realismo.

---

## **C.4 Definición de “netear”**

Este es el corazón semántico de la conciliación.

Debemos formalizar qué significa que un concepto **netee**.

La definición recomendada para el MVP es:

Un concepto netea cuando la diferencia entre el total observado y el total esperado se encuentra dentro del umbral de tolerancia definido para esa corrida.

---

### **Fórmulas base**

#### **Diferencia absoluta**

`absolute_diff = observed_total - expected_total`

#### **Diferencia relativa**

`relative_diff_pct = absolute_diff / expected_total`

Con resguardos para expected totals igual a cero.

---

### **Lógica conceptual**

La conciliación no debe depender solo de igualdad exacta, porque en procesos reales suelen existir:

* micro diferencias  
* redondeos  
* ajustes menores  
* tolerancias operativas

Por eso conviene introducir bandas.

---

## **C.5 Tolerancias**

La demo necesita tolerancias simples, entendibles y útiles visualmente.

No conviene sobrediseñar esto con reglas por concepto todavía.

---

### **Modelo de tolerancia recomendado**

Propongo un esquema de tres bandas:

#### **Verde — Reconciled**

El concepto netea.

#### **Amarillo — Minor Difference**

Existe diferencia, pero dentro de una banda menor.

#### **Rojo — Unreconciled**

La diferencia excede la tolerancia aceptable.

---

### **Reglas sugeridas para el MVP**

#### **Reconciled**

Se cumple cualquiera de estas dos:

* `abs(absolute_diff) = 0`  
* o `abs(relative_diff_pct) <= 0.5%`

#### **Minor Difference**

* `0.5% < abs(relative_diff_pct) <= 2%`

#### **Unreconciled**

* `abs(relative_diff_pct) > 2%`

---

### **Complemento con umbral absoluto**

Para evitar distorsiones cuando el expected total es pequeño, conviene usar también umbral absoluto.

Ejemplo:

#### **Reconciled**

* diferencia absoluta \<= 50 EUR  
  o diferencia relativa \<= 0.5%

#### **Minor Difference**

* diferencia absoluta \<= 500 EUR  
  o diferencia relativa \<= 2%

#### **Unreconciled**

* excede ambos criterios menores

---

### **Recomendación final de tolerancia**

Para el demo, recomiendo una lógica híbrida:

* usar **umbral absoluto y relativo**  
* tomar el estado más favorable dentro de una banda razonable  
* mantenerlo simple de explicar

Ejemplo de política:

#### **Reconciled**

* `abs(diff) <= 50` **o** `abs(diff_pct) <= 0.5%`

#### **Minor Difference**

* `abs(diff) <= 500` **o** `abs(diff_pct) <= 2%`

#### **Unreconciled**

* cualquier caso por encima de eso

Eso hace la demo mucho más realista.

---

## **C.6 Estados de conciliación**

Los estados deben ser pocos, claros y accionables.

---

### **Estados propuestos**

#### **1\. Reconciled**

El total observado concilia con el esperado dentro de tolerancia.

#### **2\. Minor Difference**

Existe una diferencia menor que no invalida totalmente el cierre, pero merece revisión.

#### **3\. Unreconciled**

La diferencia es material o significativa y requiere análisis.

#### **4\. Invalid / Incomplete**

No hay suficiente información o el input está incompleto / inconsistente para evaluar correctamente.

---

### **Uso funcional de estos estados**

Cada estado debe servir para:

* ordenar la tabla principal  
* asignar color/semaforización  
* priorizar revisión  
* activar explicación  
* dar tono a la narrativa del sistema

---

### **Condiciones de asignación**

#### **Reconciled**

* hay observed total  
* hay expected total  
* el diff cae dentro de tolerancia verde  
* no existe bloqueo crítico de calidad

#### **Minor Difference**

* hay observed total  
* hay expected total  
* el diff cae en banda amarilla  
* no existe bloqueo crítico

#### **Unreconciled**

* hay observed total  
* hay expected total  
* el diff cae en banda roja

#### **Invalid / Incomplete**

Se da alguno de estos casos:

* falta expected total  
* concepto no reconocible  
* input insuficiente  
* moneda inconsistente  
* período no determinable  
* error estructural que invalida el cálculo

---

## **C.7 Tipos de excepciones**

Además del estado de conciliación, el sistema debe identificar **excepciones** que ayuden a explicar por qué pasó lo que pasó.

Estas excepciones son la base del wow moment.

---

### **Catálogo recomendado de excepciones para el MVP**

#### **1\. Duplicate Record**

Posible duplicación de línea de payroll.

#### **2\. Missing Record / Missing Population**

Registros o empleados esperables no presentes en el archivo observado.

#### **3\. Unmapped Concept**

Código o nombre de concepto no mapeado al catálogo normalizado.

#### **4\. Out-of-Period Record**

Registro cuya fecha o período no corresponde al período conciliado.

#### **5\. Outlier Amount**

Importe anormalmente alto o bajo respecto a la distribución esperada.

#### **6\. Sign Error**

Registro con signo posiblemente invertido.

#### **7\. Misclassified Concept**

Registro cargado en un concepto que aparenta pertenecer a otro.

#### **8\. Missing Expected Total**

Existe observed total pero no referencia esperada.

#### **9\. Invalid Amount / Data Quality Issue**

Importe nulo, texto inválido, formato no interpretable o dato crítico faltante.

---

### **Qué rol cumplen las excepciones**

Las excepciones no reemplazan el estado de conciliación. Cumplen cuatro funciones:

* explican desvíos  
* priorizan el análisis  
* hacen visible la calidad del dato  
* permiten narrativa automática útil

---

## **C.8 Lógica de detección de excepciones**

Ahora toca definir **cómo** detecta el sistema cada excepción.

No buscamos perfección estadística; buscamos reglas plausibles, demostrables y auditables.

---

### **C.8.1 Duplicate Record**

Se detecta cuando dos o más líneas comparten una combinación muy similar de atributos clave, por ejemplo:

* employee\_id  
* payroll\_period  
* concept\_code  
* amount  
* legal\_entity

#### **Lógica funcional**

Si la combinación se repite idénticamente, marcar como posible duplicado.

#### **Impacto estimable**

El sistema puede calcular cuánto aporta el duplicado a la diferencia.

---

### **C.8.2 Missing Record / Missing Population**

En una demo sin fuente maestra externa completa, esta excepción debe inferirse cuidadosamente.

Dos opciones:

#### **Modo simple para MVP**

Comparar población de empleados presente en expected logic vs payroll file auxiliar o baseline predefinido.

#### **Modo demo controlado**

Diseñar casos donde se sabe que ciertos empleados deberían estar y no están.

Mi recomendación:

* usar una **tabla auxiliar demo** o una lista de casos esperados para conceptos puntuales

---

### **C.8.3 Unmapped Concept**

Se detecta cuando:

* el concept\_code no existe en el catálogo  
* o el concept\_name no puede normalizarse

#### **Lógica funcional**

Marcar la línea como no mapeada y excluirla o tratarla separadamente del cálculo conciliable principal.

---

### **C.8.4 Out-of-Period Record**

Se detecta cuando el registro presenta:

* fecha perteneciente a otro mes  
* payroll\_period distinto al período analizado  
* metadata temporal inconsistente

#### **Lógica funcional**

Marcar la línea como fuera de período y, según regla, excluirla del total observado conciliable.

---

### **C.8.5 Outlier Amount**

Se detecta comparando un importe individual con una referencia simple.

#### **Métodos posibles**

* umbral fijo por concepto  
* ratio respecto a mediana  
* z-score simplificado  
* múltiplos del promedio del concepto

#### **Recomendación MVP**

Usar regla simple por concepto:

* marcar como outlier si el valor supera, por ejemplo, 3x o 5x la mediana del concepto

Eso es suficientemente creíble y fácil de explicar.

---

### **C.8.6 Sign Error**

Se detecta cuando:

* el concepto normalmente debería ser positivo y aparece negativo  
* o viceversa

#### **Lógica funcional**

Cada concepto puede tener una polaridad esperada:

* beneficios: generalmente positivos  
* descuentos/impuestos: generalmente negativos o según convención definida

Si el signo contradice la convención, marcar.

---

### **C.8.7 Misclassified Concept**

Se detecta cuando:

* un nombre/código sugiere pertenecer a otra categoría  
* o el patrón del importe no coincide con el concepto actual

Para el MVP, esto conviene usarlo de forma controlada y no exagerar su uso.

#### **Recomendación**

Usarlo solo en uno o dos casos demo, muy construidos, para no complejizar demasiado.

---

### **C.8.8 Missing Expected Total**

Se detecta cuando:

* existe observed total o líneas observadas válidas  
* pero no existe registro expected para esa unidad conciliable

#### **Tratamiento**

Debe derivar en estado **Invalid / Incomplete** o similar.

---

### **C.8.9 Invalid Amount / Data Quality Issue**

Se detecta cuando:

* amount nulo  
* amount no numérico  
* currency faltante si fuese obligatoria  
* concepto faltante  
* employee\_id faltante en línea que debería ser trazable

---

### **Prioridad entre excepciones**

Cuando una línea presenta múltiples problemas, conviene establecer prioridad.

#### **Prioridad sugerida**

1. Invalid data / structural issue  
2. Out-of-period  
3. Unmapped concept  
4. Duplicate  
5. Sign error  
6. Outlier  
7. Misclassification

Esto ayuda a que la explicación no se vuelva caótica.

---

## **C.9 Lógica de explicación de diferencias**

Este es el diferencial del sistema.

La explicación no debe ser “mágica”; debe ser una **síntesis estructurada y creíble** basada en reglas y evidencia.

---

### **Objetivo de la explicación**

Para cada concepto con diferencia o anomalías, el sistema debe responder:

* qué diferencia existe  
* cuáles son las principales causas probables  
* cuánto aporta cada causa, cuando sea posible  
* qué revisar primero

---

### **Modelo de explicación recomendado**

La explicación debe construirse en tres capas.

#### **Capa 1 — Statement principal**

Una frase simple de resumen.

Ejemplo:

“El concepto Meal Voucher presenta una diferencia de EUR 3.200 frente al valor esperado.”

#### **Capa 2 — Causas probables**

Lista priorizada de causas detectadas.

Ejemplo:

* 12 registros fuera de período  
* 3 posibles duplicados  
* 5 líneas con concepto no mapeado

#### **Capa 3 — Recomendación**

Siguiente paso sugerido.

Ejemplo:

“Se recomienda revisar primero los registros fuera de período y luego validar el mapeo de conceptos.”

---

### **Cómo priorizar causas**

Las causas deben ordenarse por:

1. impacto estimado en monto  
2. severidad funcional  
3. confianza de la detección

---

### **Cómo combinar múltiples causas**

Una diferencia puede tener más de una causa.

La explicación debe poder decir algo como:

“La diferencia se explica principalmente por registros fuera de período y líneas no mapeadas. Adicionalmente, se detectaron dos posibles duplicados con impacto menor.”

Eso es mucho mejor que intentar una sola causa rígida.

---

### **Estimación de impacto por causa**

Cuando sea posible, el sistema debe calcular:

* monto asociado a duplicados  
* monto asociado a registros fuera de período  
* monto asociado a líneas no mapeadas  
* monto de outliers relevantes

No hace falta exactitud perfecta, pero sí consistencia interna.

---

### **Nivel de certeza**

Conviene evitar tono absoluto cuando la lógica sea inferencial.

Mejor usar frases como:

* “se detectaron indicios de…”  
* “la diferencia se explica principalmente por…”  
* “posibles causas identificadas…”

Eso protege la credibilidad del demo.

---

## **C.10 Recomendaciones de revisión**

El sistema gana mucho valor si no solo explica, sino que además orienta la acción.

---

### **Objetivo funcional**

Transformar el resultado en una siguiente acción lógica para el usuario.

---

### **Modelo recomendado**

Cada excepción o combinación de excepciones puede disparar una recomendación simple.

#### **Ejemplos**

* **Unmapped Concept**  
  “Validar el mapeo del código de concepto y su inclusión en el catálogo contable.”  
* **Out-of-Period Record**  
  “Revisar si el archivo contiene líneas de otro período y confirmar el criterio de corte.”  
* **Duplicate Record**  
  “Verificar posible duplicación en la exportación o en la consolidación del archivo.”  
* **Outlier Amount**  
  “Analizar el registro atípico y confirmar si corresponde a un pago extraordinario.”  
* **Missing Expected Total**  
  “Completar o validar la referencia esperada antes de cerrar la conciliación.”

---

### **Tono recomendado**

Las recomendaciones deben ser:

* concretas  
* profesionales  
* no alarmistas  
* orientadas a revisión, no a sentencia

---

# **Modelo lógico integrado del MVP**

Con todo lo anterior, el modelo de conciliación del demo queda así:

---

## **1\. Se toma el payroll file**

Con múltiples líneas por empleado y concepto.

## **2\. Se normaliza**

Conceptos, período, importes y datos clave.

## **3\. Se construye la base conciliable**

Filtrando registros válidos y marcando anomalías.

## **4\. Se agrega**

Por período \+ concepto  
(opcionalmente \+ legal entity)

## **5\. Se compara**

Observed total vs expected total.

## **6\. Se asigna un estado**

* Reconciled  
* Minor Difference  
* Unreconciled  
* Invalid / Incomplete

## **7\. Se detectan excepciones**

* duplicate  
* unmapped  
* out-of-period  
* outlier  
* sign error  
* etc.

## **8\. Se genera explicación**

Resumen \+ causas probables \+ recomendación.

---

# **Decisiones cerradas que deja esta sección**

Con esta sección quedan definidas las decisiones más importantes del motor lógico del MVP:

### **Unidad de conciliación**

* período \+ concepto  
* opcionalmente \+ legal entity

### **Grano de análisis operativo**

* empleado/línea como drill-down, no como conciliación primaria

### **Comparación base**

* observed total vs expected total

### **Tolerancias**

* bandas verde / amarillo / rojo  
* lógica híbrida absoluta \+ relativa

### **Estados**

* Reconciled  
* Minor Difference  
* Unreconciled  
* Invalid / Incomplete

### **Excepciones MVP**

* duplicados  
* faltantes  
* conceptos no mapeados  
* fuera de período  
* outliers  
* errores de signo  
* misclassification puntual  
* missing expected total  
* data quality issues

### **Explicación**

* basada en reglas  
* con múltiples causas  
* con recomendaciones

---

# **Mi lectura honesta sobre la Sección C**

Esto ya deja un núcleo bastante sólido y vendible. Tiene tres virtudes:

## **1\. Es creíble**

Suena y funciona como un proceso real de conciliación.

## **2\. Es implementable**

No nos estamos metiendo en una locura técnica.

## **3\. Es wow-friendly**

Da lugar a explicaciones ricas, drill-down y narrativa fuerte.

# **Fase D: Diseño del dataset dummy**

El dataset dummy no es un accesorio del demo.  
Es una de sus piezas más importantes.

Si el dataset está mal pensado:

* la conciliación se siente artificial  
* las diferencias parecen forzadas  
* la explicación pierde credibilidad  
* el usuario no se identifica con el problema

Si el dataset está bien diseñado:

* el demo se percibe real  
* los errores parecen plausibles  
* el motor “luce inteligente”  
* el cliente entiende rápidamente el valor

Por eso, este bloque debe construirse con una lógica muy clara:

**Fake data, real problem, believable behavior**

El dataset debe parecer un extracto real de nómina exportado desde SAP o sistema similar, con suficiente complejidad para demostrar:

* agregación por concepto  
* conciliación contra expected totals  
* detección de anomalías  
* explicación de diferencias  
* drill-down al nivel empleado/línea

---

## **D.1 Objetivo del dataset**

El objetivo del dataset no es simular todo un ecosistema real de payroll.  
El objetivo es crear un universo de datos **suficientemente realista** como para que la demo soporte una narrativa de producto seria.

---

### **Funciones que debe cumplir el dataset**

## **1\. Dar realismo operativo**

Debe parecer el tipo de archivo que Contabilidad efectivamente recibe.

## **2\. Alimentar el motor de conciliación**

Debe contener la estructura mínima necesaria para:

* agrupar  
* sumar  
* comparar  
* marcar desvíos

## **3\. Habilitar casos explicables**

Debe incluir anomalías que el sistema pueda detectar de manera creíble.

## **4\. Sostener el wow moment**

Debe haber al menos 2 o 3 conceptos donde el sistema muestre un análisis claro y potente.

## **5\. Permitir control narrativo**

Aunque parezca real, el dataset debe estar diseñado para que nosotros controlemos:

* qué netea  
* qué no netea  
* por qué  
* cómo se explica

---

### **Principio rector del dataset**

El dataset debe verse como un archivo realista, pero estar construido de forma deliberada para que la demo tenga sentido.

No buscamos caos total.  
Buscamos una mezcla de:

* mayoría de casos sanos  
* algunos casos con diferencias leves  
* pocos casos con diferencias interesantes y explicables

---

## **D.2 Estructura de archivos**

Para el MVP/demo, recomiendo que el universo de datos esté compuesto por **3 archivos principales** y **1 archivo opcional auxiliar**.

Esto da suficiente riqueza sin sobrecomplicar.

---

### **D.2.1 Archivo 1 — Payroll file principal**

Es el archivo más importante.

Representa el export mensual de nómina / beneficios.

Debe contener:

* múltiples empleados  
* múltiples conceptos  
* múltiples líneas por empleado  
* importes variados  
* estructura tabular tipo CSV

Es la **fuente observada**.

---

### **D.2.2 Archivo 2 — Expected totals**

Es la tabla o CSV que representa los valores esperados para la conciliación.

Debe tener, al menos:

* período  
* concepto  
* expected\_amount  
* opcionalmente legal\_entity

Es la **fuente de control**.

---

### **D.2.3 Archivo 3 — Concept master / mapping table**

Es un maestro simple de conceptos para normalización.

Debe contener:

* concept\_code\_raw  
* concept\_code\_normalized  
* concept\_name\_normalized  
* category  
* expected\_sign  
* reconciliation\_group

Su función es:

* mapear códigos alternativos  
* normalizar conceptos  
* habilitar excepciones como unmapped concept o sign error

---

### **D.2.4 Archivo opcional — Expected employee baseline / reference population**

Este archivo no es estrictamente obligatorio, pero puede ayudar mucho para ciertos casos wow.

Puede contener:

* employee\_id  
* expected\_active\_in\_period  
* legal\_entity  
* eligibility flags por concepto

Su función sería sostener mejor casos como:

* missing population  
* empleados faltantes  
* elegibilidad esperada de beneficios

---

### **Recomendación práctica**

Para el MVP base:

#### **Obligatorios**

* payroll.csv  
* expected\_totals.csv  
* concept\_master.csv

#### **Opcional pero valioso**

* employee\_reference.csv

---

## **D.3 Esquema de datos del payroll**

El archivo principal debe tener una estructura que parezca real, pero que no vuelva el demo innecesariamente complejo.

---

### **D.3.1 Columnas recomendadas del payroll**

Propongo este esquema base:

* `record_id`  
* `employee_id`  
* `employee_name`  
* `legal_entity`  
* `country`  
* `cost_center`  
* `payroll_period`  
* `posting_date`  
* `concept_code`  
* `concept_name`  
* `amount`  
* `currency`

---

### **D.3.2 Rol funcional de cada campo**

#### **record\_id**

Identificador único de línea.  
Útil para trazabilidad y drill-down.

#### **employee\_id**

Clave del empleado.  
Central para drill-down y detección de duplicados.

#### **employee\_name**

No es imprescindible lógicamente, pero ayuda mucho a la credibilidad visual.

#### **legal\_entity**

Permite enriquecer el análisis y abrir la puerta a segmentación futura.

#### **country**

Da sensación de multinacional, aunque no sea una dimensión principal del MVP.

#### **cost\_center**

No es clave para la conciliación principal, pero suma realismo.

#### **payroll\_period**

Campo central para filtrar período conciliado.

#### **posting\_date**

Ayuda a construir casos out-of-period.

#### **concept\_code**

Campo principal para mapear y agrupar.

#### **concept\_name**

Permite mostrar el dato más “humano” y generar casos de mapping.

#### **amount**

Importe a conciliar.

#### **currency**

Aporta realismo; para el MVP conviene usar una sola moneda principal.

---

### **D.3.3 Tipos de dato sugeridos**

* `record_id`: string  
* `employee_id`: string  
* `employee_name`: string  
* `legal_entity`: string  
* `country`: string  
* `cost_center`: string  
* `payroll_period`: string tipo `YYYY-MM`  
* `posting_date`: date  
* `concept_code`: string  
* `concept_name`: string  
* `amount`: decimal  
* `currency`: string

---

### **D.3.4 Convenciones de formato**

Para que el demo sea sólido, conviene definir convenciones explícitas:

* `payroll_period` normalizado como `2026-03`  
* moneda principal única: `EUR`  
* importes con 2 decimales  
* `concept_code` en mayúsculas  
* `legal_entity` con set limitado y consistente

---

### **D.3.5 Esquema extendido opcional**

Si quisiéramos enriquecer más adelante, se podrían agregar:

* `department`  
* `employment_status`  
* `hire_date`  
* `benefit_provider`  
* `source_system`

Pero no lo recomiendo para el primer MVP.

---

## **D.4 Universo de empleados**

El demo necesita una base de empleados suficientemente grande para sentirse real, pero no tan grande como para complicar el análisis o la UI.

---

### **D.4.1 Tamaño recomendado**

Mi recomendación para el MVP/demo:

**300 a 500 empleados**

Más específicamente:

* ideal: **360 empleados**

Es un número muy bueno porque:

* ya da sensación de volumen real  
* permite miles de líneas  
* sigue siendo controlable para generar dataset y casos wow

---

### **D.4.2 Distribución organizativa sugerida**

Para reforzar la idea de multinacional o estructura corporativa, propongo una distribución simple:

#### **Legal entities**

* `Iberia Services SL`  
* `Iberia Operations SL`  
* `Europe Shared Services BV`

#### **Country**

* principalmente `ES`  
* opcionalmente algún subconjunto en `PT` o `NL` si queremos sabor multinacional  
* pero para MVP conviene que el análisis principal sea España

---

### **D.4.3 Cost centers**

Propongo usar entre 5 y 8 cost centers:

* `FIN-001`  
* `HR-001`  
* `OPS-001`  
* `OPS-002`  
* `SALES-001`  
* `TECH-001`  
* `TECH-002`

Esto da riqueza visual para drill-down sin volverlo relevante en exceso.

---

### **D.4.4 Tipología de empleados**

El universo no debe ser totalmente homogéneo.

Conviene tener:

* empleados estándar  
* algunos con beneficios adicionales  
* algunos con montos variables  
* algunos con situación especial diseñada para anomalías

---

### **D.4.5 Casos especiales recomendados**

Dentro del universo, conviene inyectar pocos casos particulares:

* 1 empleado con importe muy alto en un concepto  
* 2 o 3 empleados con registros duplicados  
* 5 a 10 empleados faltantes en algún concepto puntual  
* 2 o 3 empleados con concepto mal mapeado  
* 1 pequeño grupo con registros fuera de período

Esto permite narrativa sin saturar el dataset.

---

## **D.5 Universo de conceptos**

La selección de conceptos es clave porque la demo gira alrededor de ellos.

Conviene elegir conceptos que:

* sean intuitivos  
* se entiendan rápido  
* permitan diversidad de comportamientos  
* sean creíbles en contexto enterprise

---

### **D.5.1 Número recomendado de conceptos**

Para el MVP:

**8 a 10 conceptos**

Suficientes para mostrar variedad, pero no demasiados.

---

### **D.5.2 Lista recomendada de conceptos**

Propongo este set:

* `BASE_SALARY`  
* `BONUS`  
* `MEAL_VOUCHER`  
* `CHILDCARE`  
* `TRANSPORT`  
* `HEALTH_INSURANCE`  
* `SOCIAL_SECURITY`  
* `INCOME_TAX`  
* `OVERTIME`  
* `OTHER_ADJUSTMENT`

---

### **D.5.3 Racional por concepto**

#### **BASE\_SALARY**

Da volumen y realismo, pero no necesariamente debe ser protagonista del wow.

#### **BONUS**

Sirve para introducir dispersión y algunos importes variables.

#### **MEAL\_VOUCHER**

Excelente concepto wow: fácil de entender y muy bueno para casos faltantes o de mapping.

#### **CHILDCARE**

Muy útil porque solo aplica a parte de la población; ideal para diferencias explicables.

#### **TRANSPORT**

Bueno para mostrar concepto simple con diferencia menor.

#### **HEALTH\_INSURANCE**

Permite casos sanos o alguna diferencia moderada.

#### **SOCIAL\_SECURITY**

Aporta sabor contable/nomina más serio, pero quizás conviene mantenerlo limpio.

#### **INCOME\_TAX**

Lo mismo: aporta realismo, pero mejor no usarlo como wow principal.

#### **OVERTIME**

Excelente para introducir outliers.

#### **OTHER\_ADJUSTMENT**

Útil como contenedor de algún caso raro, pero con cuidado para no volverlo ambiguo.

---

### **D.5.4 Conceptos estrella para la demo**

Recomiendo elegir desde ya 3 conceptos protagonistas:

#### **1\. MEAL\_VOUCHER**

Caso wow principal

#### **2\. CHILDCARE**

Caso explicable con población elegible

#### **3\. OVERTIME**

Caso atípico / outlier

---

### **D.5.5 Conceptos sanos**

Conviene que varios conceptos neteen bien para dar credibilidad.

Ejemplo:

* `BASE_SALARY`  
* `SOCIAL_SECURITY`  
* `HEALTH_INSURANCE`

---

## **D.6 Período y contexto temporal**

La demo debe girar alrededor de un único período principal, para mantener foco.

---

### **D.6.1 Período principal recomendado**

Usar:

**2026-03**

Es contemporáneo al contexto actual de conversación y da naturalidad.

---

### **D.6.2 Lógica temporal del demo**

Todo el sistema debe estar armado para analizar:

* payroll period objetivo: `2026-03`  
* expected totals de `2026-03`  
* mayoría de líneas pertenecientes a `2026-03`

Y luego inyectar pocos casos fuera de período:

* `2026-02`  
* o fecha de posting inconsistente

---

### **D.6.3 Reglas temporales recomendadas**

Para el motor:

* la corrida se ejecuta sobre `2026-03`  
* registros con `payroll_period != 2026-03` deben marcarse  
* posting dates inconsistentes pueden reforzar la anomalía

---

### **D.6.4 Uso narrativo del tiempo**

El tiempo puede ayudar mucho en la explicación:

Ejemplo:

“Se detectaron 8 líneas de Meal Voucher correspondientes a febrero 2026 dentro del archivo de marzo 2026.”

Eso se entiende rápido y vende bien.

---

## **D.7 Casos normales**

Uno de los errores más comunes al diseñar demos es meter demasiados errores.

Eso hace que el dataset parezca falso.

La realidad es que en un archivo real:

* muchas cosas están bien  
* algunas tienen diferencias menores  
* pocas tienen diferencias importantes

---

### **D.7.1 Proporción recomendada**

Mi sugerencia:

* **60%–70% de los conceptos:** reconciled  
* **20%–25%:** minor difference  
* **10%–20%:** unreconciled con explicación interesante

Como vamos a tener unos 8 a 10 conceptos, esto puede verse así:

#### **Reconciled**

5 o 6 conceptos

#### **Minor Difference**

2 conceptos

#### **Unreconciled**

2 conceptos fuertes

---

### **D.7.2 Qué logra esta distribución**

* la demo no se ve exagerada  
* el sistema demuestra que no “todo está roto”  
* el rojo se vuelve más importante cuando aparece  
* el usuario percibe criterio, no dramatización

---

### **D.7.3 Casos normales sugeridos**

Podrían netear:

* `BASE_SALARY`  
* `SOCIAL_SECURITY`  
* `HEALTH_INSURANCE`  
* `INCOME_TAX`  
* quizás `BONUS`

Y quedar con diferencias menores:

* `TRANSPORT`  
* `OTHER_ADJUSTMENT`

Y con diferencias interesantes:

* `MEAL_VOUCHER`  
* `CHILDCARE`  
* `OVERTIME`

---

## **D.8 Anomalías inyectadas**

Este es uno de los puntos más importantes del diseño.

Las anomalías no deben ponerse al azar.  
Deben construirse como piezas que el motor pueda detectar y explicar.

---

### **D.8.1 Principios para inyectar anomalías**

## **1\. Pocas pero claras**

Mejor 6 anomalías bien pensadas que 20 caóticas.

## **2\. Distribuidas**

No meter todo en un solo concepto.

## **3\. Explicables**

Cada anomalía debe tener una historia posible.

## **4\. Cuantificables**

Idealmente, el sistema debe poder estimar su impacto.

---

### **D.8.2 Catálogo de anomalías a inyectar**

Para el MVP recomiendo estas:

* duplicados  
* concepto no mapeado  
* registros fuera de período  
* outlier  
* faltantes / población ausente  
* error de signo (solo si queremos un caso adicional)  
* missing expected total (opcional, no imprescindible)

---

### **D.8.3 Propuesta concreta por concepto**

#### **MEAL\_VOUCHER**

Concepto principal del wow.

Anomalías recomendadas:

* 8 líneas fuera de período  
* 3 duplicados  
* 5 líneas con `MEAL_VCHR` no mapeado

Esto permite una explicación rica y visual.

---

#### **CHILDCARE**

Concepto muy bueno para faltantes.

Anomalías recomendadas:

* 6 empleados elegibles ausentes  
* 2 registros con importe incorrecto  
* quizás 1 línea mal clasificada

La explicación puede enfocarse en población faltante.

---

#### **OVERTIME**

Concepto ideal para outlier.

Anomalías recomendadas:

* 1 empleado con importe 5x mediana  
* 1 posible error de signo o ajuste anómalo

Eso da un drill-down muy demostrable.

---

#### **TRANSPORT**

Concepto para diferencia menor.

Anomalías recomendadas:

* 2 o 3 pequeñas diferencias  
* un redondeo o microdesvío  
* nada escandaloso

Sirve para el amarillo.

---

#### **OTHER\_ADJUSTMENT**

Opcional, con un caso menor o limpio.

---

### **D.8.4 Volumen de anomalías**

No hay que exagerar.

Para un payroll de 3.000–4.500 líneas, bastaría con algo así:

* 3–5 duplicados  
* 5–8 unmapped  
* 6–10 out-of-period  
* 1–2 outliers claros  
* 5–10 faltantes controlados

Eso ya da muchísimo juego.

---

## **D.9 Casos wow**

Acá diseñamos deliberadamente los momentos donde la demo tiene que brillar.

No basta con “hay diferencias”.  
Tiene que haber casos que el sistema pueda contar bien.

---

### **D.9.1 Caso wow principal — Meal Voucher**

Debe ser el ejemplo estrella.

#### **Narrativa**

El concepto no concilia, y el sistema explica que la diferencia se debe principalmente a:

* registros fuera de período  
* líneas no mapeadas  
* posibles duplicados

#### **Por qué funciona**

* el concepto es fácil de entender  
* mezcla múltiples causas  
* permite explicación cuantificada  
* el drill-down es intuitivo

#### **Ejemplo de mensaje**

“Meal Voucher presenta una diferencia de EUR 3.180 frente al valor esperado. La diferencia se explica principalmente por 8 líneas correspondientes a febrero 2026, 5 registros con código no mapeado y 3 posibles duplicados.”

Eso es excelente demo material.

---

### **D.9.2 Caso wow secundario — Childcare**

Debe ser más de negocio que técnico.

#### **Narrativa**

El concepto no concilia porque parte de la población elegible no está presente o fue cargada parcialmente.

#### **Por qué funciona**

* conecta con lógica humana  
* demuestra que el sistema no solo detecta errores “de archivo”  
* se siente muy cercano a realidad operativa

#### **Ejemplo de mensaje**

“Childcare presenta una diferencia de EUR 1.450. Se identificaron 6 empleados elegibles sin registro para el período y 2 importes inferiores al valor esperado.”

---

### **D.9.3 Caso wow analítico — Overtime**

Debe mostrar capacidad para detectar rarezas.

#### **Narrativa**

Hay un empleado con overtime muy superior al patrón normal.

#### **Por qué funciona**

* se entiende visualmente  
* permite mostrar outlier detection  
* es excelente para drill-down

#### **Ejemplo**

“Overtime presenta una diferencia material impulsada principalmente por 1 registro atípico cuyo importe multiplica por 5 la mediana del concepto.”

---

### **D.9.4 Caso amarillo — Transport**

Sirve para mostrar criterio.

#### **Narrativa**

El sistema detecta una diferencia menor, no crítica.

Esto es importante porque:

* demuestra bandas de tolerancia  
* muestra que no todo es rojo  
* se siente más realista

---

## **D.10 Relación entre dataset y expected totals**

Esta parte es crítica: si los expected totals no están diseñados con coherencia, la demo se rompe.

---

### **D.10.1 Principio general**

Los expected totals no deben ser completamente aleatorios ni completamente derivados sin intervención.

La mejor lógica para el demo es:

**dataset observado base \+ ajustes deliberados para generar estados definidos**

---

### **D.10.2 Método recomendado de construcción**

## **Paso 1**

Construir primero el payroll observado “como debería venir”.

## **Paso 2**

Definir expected totals coherentes con ese universo.

## **Paso 3**

Inyectar anomalías en el payroll observado o ajustar expected totals en ciertos conceptos.

## **Paso 4**

Verificar que el resultado final produzca:

* conceptos verdes  
* conceptos amarillos  
* conceptos rojos

---

### **D.10.3 Regla de diseño**

Para cada concepto, debemos saber de antemano:

* expected total  
* observed total final esperado  
* diff target  
* estado target  
* anomalías target  
* explicación target

Eso evita improvisación y hace el dataset extremadamente controlable.

---

### **D.10.4 Ejemplo de diseño por concepto**

Podríamos tener una tabla de diseño interno como esta:

| Concepto | Expected | Observed | Diff | Estado | Explicación principal |
| ----- | ----- | ----- | ----- | ----- | ----- |
| BASE\_SALARY | 1,200,000 | 1,200,010 | \+10 | Reconciled | Redondeo insignificante |
| MEAL\_VOUCHER | 42,000 | 38,820 | \-3,180 | Unreconciled | Out-of-period \+ unmapped \+ duplicates |
| CHILDCARE | 18,500 | 17,050 | \-1,450 | Unreconciled | Missing eligible population |
| TRANSPORT | 21,000 | 20,760 | \-240 | Minor Difference | Diferencias menores |
| OVERTIME | 14,000 | 16,300 | \+2,300 | Unreconciled | Outlier principal |

Esta tabla sería oro para construir el dataset.

---

## **D.11 Diseño cuantitativo recomendado del dataset**

Acá cierro una propuesta concreta y aterrizada de cómo debería verse el MVP.

---

### **Payroll file**

* **360 empleados**  
* **8–10 conceptos**  
* promedio de **8 a 12 líneas por empleado**  
* total estimado: **3.200 a 4.000 líneas**

---

### **Expected totals**

* 1 fila por concepto por período  
* opcionalmente segmentado por legal\_entity  
* total: **8 a 20 filas**, según complejidad elegida

---

### **Concept master**

* 10 a 15 filas  
* incluye variantes raw y normalized  
* incluye expected sign y category

---

### **Employee reference (opcional)**

* 360 filas  
* flags de elegibilidad para childcare y meal voucher  
* útil para casos faltantes

---

## **D.12 Decisiones cerradas que deja esta sección**

Con esta sección ya queda definido:

### **Archivos del demo**

* payroll.csv  
* expected\_totals.csv  
* concept\_master.csv  
* employee\_reference.csv opcional

### **Período**

* `2026-03`

### **Volumen**

* 360 empleados  
* 3.200–4.000 líneas aprox.

### **Conceptos principales**

* 8 a 10 conceptos  
* con 3 protagonistas claros

### **Distribución de estados**

* mayoría verde  
* algunos amarillos  
* pocos rojos fuertes

### **Casos wow**

* `MEAL_VOUCHER`  
* `CHILDCARE`  
* `OVERTIME`

### **Anomalías MVP**

* duplicates  
* unmapped concept  
* out-of-period  
* missing population  
* outlier  
* sign error opcional

### **Lógica de diseño**

* expected totals y dataset construidos deliberadamente para sostener narrativa controlada

---

# **Mi lectura sobre la Sección D**

Esta sección ya deja una base bastante seria para construir el demo de manera inteligente.

Lo más valioso es que ahora no estamos diciendo solo “hagamos data dummy”, sino que ya definimos:

* qué archivos existen  
* qué columnas tienen  
* qué volumen buscamos  
* qué conceptos usar  
* qué anomalías inyectar  
* qué casos wow queremos contar

Eso reduce muchísimo el caos posterior.

# 

# **E. UX funcional y Demo Flow**

La UX del MVP no debe diseñarse como si estuviéramos resolviendo todos los casos futuros del producto.

Debe diseñarse como una experiencia **mínima, guiada y convincente**, pensada para que un usuario entienda rápidamente:

1. qué se carga  
2. qué analiza el sistema  
3. qué resultado devuelve  
4. por qué eso genera valor

Eso implica dos principios rectores:

---

## **Principio 1 — UX orientada a flujo**

El sistema debe guiar al usuario por un camino claro:

**Setup → Run → Summary → Explanation → Drill-down → Export**

No necesitamos navegación compleja ni múltiples módulos.

---

## **Principio 2 — UX orientada a insight**

La pantalla más importante no es la de carga: es la de resultados y explicación.

La UX debe estar diseñada para que el valor del sistema aparezca rápido y sin fricción.

---

# **E.1 Objetivo de UX**

La experiencia del MVP debe lograr cinco cosas al mismo tiempo:

## **1\. Claridad**

Que el usuario entienda de inmediato qué está viendo.

## **2\. Seriedad**

Que la demo se perciba como una herramienta enterprise creíble, aunque sea liviana.

## **3\. Velocidad**

Que el usuario llegue rápido al resultado.

## **4\. Explicabilidad**

Que el valor del sistema no sea solo “calcular”, sino “explicar”.

## **5\. Control narrativo**

Que durante una reunión podamos conducir el recorrido hacia los puntos más fuertes del demo.

---

### **Qué sensación debe dejar**

La sensación ideal es algo así:

“Esto simplifica un proceso real, me muestra rápido dónde están los problemas y me deja entender por qué ocurren.”

No queremos que la reacción sea:

* “qué dashboard lindo”  
* ni “qué demo técnica”

Queremos:

* “esto sí me ayudaría a trabajar”

---

# **E.2 Flujo de pantallas**

Para el MVP, recomiendo una arquitectura de UX de **4 pantallas principales** \+ **1 acción de exportación**.

Eso es más que suficiente para una demo potente.

---

## **Pantalla 1 — Setup / New Reconciliation Run**

Pantalla inicial donde el usuario prepara la corrida.

## **Pantalla 2 — Reconciliation Summary**

Vista ejecutiva de resultados generales.

## **Pantalla 3 — Concept Analysis**

Vista por concepto con estados, diferencias y acceso a explicación.

## **Pantalla 4 — Exception Drill-down**

Vista detallada para entender registros/empleados causantes.

## **Acción adicional — Export**

Salida descargable de resultados.

---

### **Por qué esta cantidad es correcta para un MVP**

Porque permite mostrar:

* input  
* proceso  
* output  
* detalle  
* evidencia

sin crear complejidad innecesaria.

---

# **E.3 Pantalla de carga y configuración**

Esta es la puerta de entrada al sistema.

No tiene que ser espectacular, pero sí clara, limpia y seria.

---

## **Objetivo funcional**

Permitir al usuario iniciar una corrida de conciliación con los insumos mínimos necesarios.

---

## **Elementos que debe incluir**

### **1\. Título de pantalla**

Algo como:

**New Reconciliation Run**  
o  
**Payroll Reconciliation Setup**

Eso ya da framing de producto.

---

### **2\. Selector de período**

Campo visible para indicar el período a conciliar.

Para el MVP puede venir:

* precompletado con `2026-03`  
* editable si queremos sensación de producto

---

### **3\. Carga del payroll file**

Módulo de upload para `payroll.csv`

Debe mostrar:

* nombre del archivo  
* estado de carga  
* cantidad de registros detectados  
* validación básica

---

### **4\. Carga o visualización de expected totals**

Puede funcionar de dos maneras:

#### **Opción A — Upload**

Subir `expected_totals.csv`

#### **Opción B — Tabla precargada visible**

Ver expected totals ya listados

Para el MVP, recomiendo una mezcla:

* precargados por defecto  
* visibles como tabla

Eso hace la demo más fluida.

---

### **5\. Parámetros mínimos**

No conviene meter demasiados settings.

Solo algunos, si realmente suman:

* legal entity scope (opcional)  
* tolerance profile (opcional)  
* include exceptions analysis: activado por default

Mi recomendación MVP:

* mostrar pocos parámetros  
* dejar casi todo precargado

---

### **6\. Validación pre-run**

Antes de ejecutar, la pantalla debe confirmar algo como:

* file uploaded successfully  
* schema validated  
* 3,842 records detected  
* 10 concepts identified  
* 1 target period selected

Ese pequeño bloque da mucha confianza.

---

### **7\. CTA principal**

Botón fuerte, claro y único:

**Run Reconciliation**

Ese botón debe ser el foco visual.

---

## **Qué NO debe tener esta pantalla**

Para mantener el MVP limpio, no debería incluir:

* creación manual compleja de reglas  
* demasiados filtros  
* configuración avanzada  
* múltiples tabs  
* wizard largo

---

## **Qué valor transmite esta pantalla**

No vende sofisticación.  
Vende orden y facilidad de uso.

Debe comunicar:

“Con pocos insumos, el sistema está listo para analizar.”

---

# **E.4 Pantalla de resumen ejecutivo**

Esta es una de las pantallas más importantes del MVP.

Es donde el usuario debe sentir, en segundos, que el sistema ya hizo trabajo valioso.

---

## **Objetivo funcional**

Ofrecer una visión inmediata del resultado general de la corrida.

---

## **Preguntas que debe responder**

Esta pantalla debe permitir responder rápidamente:

* ¿La corrida salió bien?  
* ¿Cuántos conceptos netearon?  
* ¿Cuántos requieren revisión?  
* ¿Dónde están los principales desvíos?  
* ¿Qué tan material es el problema?

---

## **Bloques recomendados**

### **1\. Header de corrida**

Debe mostrar metadata clave:

* run ID  
* período analizado  
* timestamp  
* archivo procesado  
* entidad o scope si aplica

No hace falta exceso de detalle, pero sí suficiente trazabilidad visual.

---

### **2\. KPI cards**

Recomiendo entre **4 y 5 tarjetas principales**.

Ejemplo:

* **Concepts Reconciled**  
* **Concepts with Minor Differences**  
* **Unreconciled Concepts**  
* **Total Amount Reconciled**  
* **Amount Pending Explanation**

Estas tarjetas son muy MVP-friendly: rápidas de leer y muy efectivas.

---

### **3\. Estado general de la corrida**

Un bloque visual simple que diga algo como:

* **Overall Run Status: Reconciled with Exceptions**  
* o **Attention Required**  
* o **Partially Reconciled**

Eso ayuda a sintetizar el resultado.

---

### **4\. Tabla resumida por concepto**

Esta tabla debe ser visible ya en esta pantalla o inmediatamente debajo.

Columnas mínimas recomendadas:

* Concept  
* Expected  
* Observed  
* Diff  
* Diff %  
* Status

Opcional:

* short explanation preview

---

### **5\. Priorización visual**

La tabla debe estar ordenada para llevar el ojo a:

* rojos primero  
* luego amarillos  
* luego verdes

Esto sirve tanto al usuario como al storytelling de la demo.

---

### **6\. CTA secundarios**

Desde acá el usuario debe poder:

* abrir un concepto  
* ver explicación  
* exportar resultados

---

## **Principio visual de esta pantalla**

Debe sentirse:

* limpia  
* ejecutiva  
* muy legible  
* no recargada

No conviene meter charts innecesarios si no agregan valor real.

---

## **¿Conviene usar gráficos?**

Para el MVP, solo si son extremadamente útiles.

Mi recomendación:

* **sí** a un pequeño summary visual tipo status distribution  
* **no** a dashboards llenos de charts

Ejemplo útil:

* barra horizontal con cantidad de conceptos por estado

Eso suma sin distraer.

---

## **Qué valor transmite esta pantalla**

Esta pantalla vende:

“El sistema resume en segundos el estado de conciliación de todo el período.”

---

# **E.5 Pantalla de resultado por concepto**

Esta pantalla es el puente entre la visión ejecutiva y el análisis detallado.

Puede ser una pantalla separada o una vista expandida desde la tabla principal.  
Para el MVP, cualquiera de las dos funciona, pero conceptualmente es importante definirla.

---

## **Objetivo funcional**

Permitir analizar un concepto individual en mayor profundidad.

---

## **Qué debe mostrar**

### **1\. Header del concepto**

Ejemplo:

**Meal Voucher**  
Período: 2026-03  
Status: Unreconciled

---

### **2\. KPIs del concepto**

Recomiendo mostrar:

* Expected Total  
* Observed Total  
* Absolute Difference  
* Difference %  
* Records Analyzed  
* Employees Affected

Esto hace que el concepto “tome entidad propia”.

---

### **3\. Explicación resumida**

Acá ya debe aparecer una narrativa más útil, por ejemplo:

“The observed total is below expected by EUR 3,180. The main drivers identified are out-of-period records, unmapped concept lines, and possible duplicates.”

Eso ya es una mini demostración del valor del motor.

---

### **4\. Lista de causas detectadas**

Idealmente en formato simple y muy legible:

* 8 out-of-period records  
* 5 unmapped concept records  
* 3 potential duplicates

Y, si podemos:

* monto estimado por causa

---

### **5\. Evidencia resumida**

Pequeño bloque que diga algo como:

* Highest impact anomaly: out-of-period records  
* Top impacted legal entity: Iberia Services SL  
* Top employee impact: Employee E-1048

No hace falta exagerar. Solo lo suficiente para mostrar inteligencia funcional.

---

### **6\. Acceso al drill-down**

Botón o CTA claro:

**View Detailed Records**

---

## **Qué NO debe hacer esta pantalla**

No debe convertirse en un backoffice complejo.

No queremos:

* edición avanzada  
* comentarios  
* workflow de aprobación  
* demasiados módulos

---

## **Qué valor transmite**

Esta pantalla vende:

“El sistema no solo detecta que hay una diferencia; además te dice de qué está compuesta.”

---

# **E.6 Pantalla de explicación**

Aunque conceptualmente se parece a la anterior, vale la pena distinguirla como pieza UX porque es donde realmente mostramos el diferencial.

En el MVP, esta “pantalla” puede ser:

* una sección dentro de la vista del concepto  
* un panel lateral  
* una tarjeta expandida

No tiene que ser una página completamente separada si no hace falta.

---

## **Objetivo funcional**

Traducir resultados técnicos en una narrativa de negocio entendible.

---

## **Estructura recomendada de la explicación**

### **1\. Statement principal**

Una frase inicial, simple y directa.

Ejemplo:

“Meal Voucher does not reconcile for March 2026\. The observed amount is EUR 3,180 below expected.”

---

### **2\. Top causes**

Bloque principal con ranking de causas probables.

Ejemplo:

1. Out-of-period records: estimated impact EUR 1,620  
2. Unmapped concept lines: estimated impact EUR 1,050  
3. Potential duplicates: estimated impact EUR 510

Esto es oro para la demo.

---

### **3\. Confidence / framing**

No conviene sonar absoluto si la explicación es inferencial.

Podemos usar una línea sutil como:

* “Main probable causes identified”  
* “Most relevant anomalies detected”  
* “Analysis based on current records and reconciliation rules”

Eso protege credibilidad.

---

### **4\. Recommended review actions**

Ejemplo:

* Review records tagged with payroll period 2026-02  
* Validate concept mapping for code `MEAL_VCHR`  
* Check duplicate lines for repeated employee/concept combinations

---

### **5\. Impact summary**

Mini bloque con:

* total impacted records  
* impacted employees  
* estimated explained amount

---

## **Tono de la explicación**

Debe ser:

* profesional  
* claro  
* sobrio  
* útil  
* no demasiado técnico

No queremos que parezca:

* chatbot  
* auditor agresivo  
* log de sistema

Queremos que parezca:

* capa inteligente de soporte al análisis

---

## **Qué valor transmite**

Esta parte vende exactamente la promesa del producto:

“No solo reconciliamos. También explicamos.”

---

# **E.7 Drill-down operacional**

Este es el momento donde el sistema demuestra que puede bajar del resumen al detalle sin perder coherencia.

Es uno de los momentos más fuertes del MVP.

---

## **Objetivo funcional**

Permitir revisar los registros concretos que explican una diferencia.

---

## **Qué debe mostrar**

### **1\. Tabla de registros**

Columnas recomendadas:

* Record ID  
* Employee ID  
* Employee Name  
* Legal Entity  
* Concept  
* Amount  
* Period  
* Exception Type  
* Observation

Eso ya es suficiente para una demo muy buena.

---

### **2\. Filtros livianos**

No hace falta poner demasiados, pero algunos sí ayudan:

* filter by exception type  
* filter by employee  
* filter by legal entity

Con 2 o 3 filtros simples alcanza.

---

### **3\. Ordenamiento**

Muy útil ordenar por:

* highest amount  
* anomaly severity  
* employee ID

---

### **4\. Highlight visual**

Las filas con anomalías deben estar marcadas claramente:

* badge de exception type  
* ícono simple  
* color sutil por severidad

Sin sobrecargar.

---

### **5\. Resumen arriba de la tabla**

Ejemplo:

* 16 impacted records  
* 12 affected employees  
* 3 anomaly types detected

Esto le da contexto al detalle.

---

## **Qué hace fuerte esta pantalla**

Permite demostrar que el sistema puede responder la pregunta más importante de todas:

“Ok, pero muéstrame exactamente qué registros explican la diferencia.”

Y cuando el demo puede responder eso, gana muchísimo peso.

---

# **E.8 Exportables**

Aunque no sea lo más sexy, esto suma mucho a la percepción de producto real.

---

## **Objetivo funcional**

Permitir que el usuario se lleve evidencia o resultados del análisis.

---

## **Exportables mínimos recomendados para el MVP**

### **1\. Reconciliation Summary Export**

Archivo simple con:

* concepto  
* expected  
* observed  
* diff  
* status

### **2\. Exception Detail Export**

Archivo con:

* registros impactados  
* exception type  
* observaciones  
* concepto asociado

---

## **Formato recomendado**

Para el MVP:

* **Excel / CSV**

PDF puede esperar.

Excel tiene más sentido operativo para este tipo de usuario.

---

## **Cuándo se accede**

Desde:

* summary screen  
* concept analysis screen  
* optionally drill-down screen

---

## **Qué valor transmite**

Exportar refuerza tres ideas:

* utilidad real  
* trazabilidad  
* continuidad post-demo

---

# **E.9 Storytelling comercial de la demo**

Esto es crítico. La UX no vive sola; vive dentro de una reunión.

Por eso el flujo visual debe estar diseñado también para ser contado.

---

## **Objetivo**

Construir una narrativa corta, lógica y convincente para mostrar el MVP.

---

## **Secuencia recomendada de demo**

### **Paso 1 — Contexto**

Abrir con una frase de dolor real:

“Tomamos un proceso que hoy suele hacerse manualmente a partir de exportes de nómina y lo convertimos en una conciliación explicable.”

---

### **Paso 2 — Setup**

Mostrar rápidamente la pantalla de carga:

* archivo  
* período  
* expected totals

Sin demorarse demasiado.

Mensaje:

“Partimos de un extracto tipo SAP y una referencia esperada para el período.”

---

### **Paso 3 — Run**

Ejecutar la corrida.

Esto puede ser instantáneo o con una micro señal visual de procesamiento.

---

### **Paso 4 — Summary**

Ir directo a la vista ejecutiva.

Mensaje:

“En segundos, el sistema resume qué conceptos conciliaron, cuáles no y dónde conviene enfocar la revisión.”

---

### **Paso 5 — Caso wow principal**

Abrir `MEAL_VOUCHER`.

Mensaje:

“Acá ya no nos quedamos solo con la diferencia; el sistema identifica causas probables y estima su impacto.”

---

### **Paso 6 — Drill-down**

Bajar a registros concretos.

Mensaje:

“Y si hace falta, se puede bajar al nivel de línea para revisar exactamente qué registros están explicando el desvío.”

---

### **Paso 7 — Cierre**

Cerrar con valor de negocio.

Ejemplo:

“Esto permite reducir tiempo manual, mejorar trazabilidad y estandarizar una validación que hoy depende mucho del análisis manual.”

---

## **Duración ideal de la demo**

Para una reunión comercial, el walkthrough ideal debería durar:

**5 a 8 minutos**

Más que eso, empieza a perder foco.

---

## **Momento wow real**

El wow no está en el upload.  
Está en esta secuencia:

* ver un rojo en summary  
* abrir el concepto  
* mostrar causas probables  
* bajar al detalle exacto

Ese es el núcleo dramático del MVP.

---

# **E.10 Principios de diseño visual del MVP**

Además del flujo, conviene dejar cerrados algunos principios visuales.

---

## **1\. Enterprise clean**

Diseño limpio, sobrio y profesional.

## **2\. Data-first**

La información debe dominar sobre lo decorativo.

## **3\. Color con propósito**

Verde / amarillo / rojo solo para estados, no para adornar.

## **4\. Jerarquía clara**

KPI → tabla → explicación → detalle

## **5\. Baja densidad de ruido**

Evitar charts, widgets y adornos que no agreguen valor.

---

# **E.11 Qué NO debe incluir el MVP**

Para proteger foco y evitar scope creep, conviene dejar explícito lo que no entra.

---

## **No incluir por ahora**

* login complejo  
* múltiples roles  
* comments / collaboration  
* workflows de aprobación  
* dashboards históricos avanzados  
* motor visual de reglas  
* configuración libre por usuario  
* multi-country real con lógica diferente  
* visualizaciones complejas innecesarias

---

# **E.12 Decisiones cerradas que deja esta sección**

Con esta sección queda definido:

## **Pantallas principales**

1. Setup / New Run  
2. Reconciliation Summary  
3. Concept Analysis  
4. Exception Drill-down

## **Acciones clave**

* Run reconciliation  
* View concept analysis  
* View detailed records  
* Export results

## **Núcleo de valor UX**

* insight rápido  
* explicación clara  
* detalle navegable

## **Momento wow**

* abrir concepto con diferencia  
* ver causas  
* bajar a registros concretos

## **Tono de UX**

* serio  
* sobrio  
* ejecutivo-operativo  
* orientado a contabilidad

## **Límite de MVP**

* experiencia guiada  
* baja complejidad  
* sin módulos accesorios

---

# **Mi lectura sobre la Sección E**

Con esto ya tenemos bastante bien cerrada la capa de experiencia del MVP.

Lo bueno es que no caímos en diseñar “una plataforma completa”, sino una UX muy enfocada en el objetivo real:

demostrar valor rápido con una conciliación explicable

Y además ya queda claro algo muy importante:

* qué pantallas existen  
* en qué orden aparecen  
* qué muestra cada una  
* dónde está el wow  
* cómo contar la demo comercialmente

# **F. Arquitectura técnica mínima**

La arquitectura técnica del MVP debe sostener cinco capacidades fundamentales:

1. **ingestar archivos**  
2. **procesar y normalizar datos**  
3. **ejecutar conciliación y detección de excepciones**  
4. **persistir una traza mínima**  
5. **presentar resultados en una UI limpia**

La mejor forma de resolver esto, para este caso, es con una arquitectura simple de **3 capas principales**:

* **Frontend**  
* **Backend / API**  
* **Motor de procesamiento \+ persistencia**

No hace falta separar todavía microservicios, colas, workers distribuidos, rule engines complejos ni infraestructura sofisticada.

---

## **F.1 Principios de arquitectura técnica**

Antes de elegir stack, conviene dejar cerrados los principios que van a gobernar las decisiones.

---

### **F.1.1 Simplicidad primero**

La arquitectura debe minimizar complejidad accidental.

Eso implica:

* pocas piezas  
* responsabilidades claras  
* mínima infraestructura necesaria  
* pocas dependencias críticas

---

### **F.1.2 Modularidad razonable**

Aunque sea MVP, no conviene hacer una masa única de código.

Debemos separar al menos:

* UI  
* API  
* lógica de conciliación  
* acceso a datos

Eso permite crecer luego sin rehacer todo.

---

### **F.1.3 Credibilidad de producto**

Aunque internamente sea simple, externamente debe percibirse como un sistema serio.

Eso favorece decisiones como:

* frontend real  
* backend API real  
* persistencia mínima real  
* corridas guardadas  
* exportables

---

### **F.1.4 Velocidad de implementación**

La arquitectura debe privilegiar time-to-demo.

Eso nos lleva a elegir herramientas:

* conocidas  
* rápidas  
* buenas para manipulación de datos  
* con bajo overhead de setup

---

### **F.1.5 Escalabilidad razonable, no prematura**

No construimos para miles de clientes hoy.

Pero sí conviene evitar decisiones que cierren todas las puertas.

La arquitectura debe poder evolucionar luego hacia:

* más reglas  
* más datasets  
* más pantallas  
* múltiples corridas  
* multi-entity real

---

### **F.1.6 Auditabilidad mínima**

Como el caso de uso roza Contabilidad, incluso el MVP debe dejar cierta trazabilidad técnica:

* qué archivo se procesó  
* qué parámetros se usaron  
* qué resultados produjo  
* cuándo se ejecutó

Eso es más importante que sofisticar infraestructura.

---

## **F.2 Arquitectura general recomendada**

La propuesta técnica recomendada para el MVP es esta:

### **1\. Frontend web**

Una aplicación liviana pero real, pensada para:

* carga de archivos  
* ejecución de corrida  
* visualización de resultados  
* drill-down  
* export

### **2\. Backend API**

Un servicio backend que:

* recibe requests del front  
* gestiona uploads  
* orquesta corridas  
* persiste metadata/resultados  
* expone resultados al frontend

### **3\. Motor de conciliación**

Un módulo interno del backend o capa separada dentro del mismo servicio que:

* valida inputs  
* normaliza datos  
* corre las reglas  
* calcula resultados  
* genera excepciones y explicaciones

### **4\. Base de datos**

Persistencia relacional simple para:

* corridas  
* expected totals  
* resultados  
* excepciones  
* metadata

### **5\. File storage simple**

No hace falta storage distribuido.  
Para MVP puede bastar con:

* disco local del proyecto  
* o almacenamiento simple de archivos subidos

---

### **Arquitectura conceptual resumida**

**Frontend**  
⬇  
**API Backend**  
⬇  
**Reconciliation Service / Engine**  
⬇  
**Database \+ Uploaded Files**

Ese esquema es suficiente y correcto para un MVP funcional.

---

## **F.3 Frontend**

La decisión del frontend es importante porque queremos que la demo se sienta producto real.

---

### **F.3.1 Recomendación**

Mi recomendación principal es:

**React \+ Next.js**

---

### **Por qué Next.js tiene sentido**

Porque nos da:

* UI moderna y seria  
* velocidad de desarrollo  
* estructura limpia  
* fácil manejo de pantallas y componentes  
* buen fit para dashboards y tablas  
* look “producto” más creíble que soluciones demasiado rápidas tipo Streamlit

---

### **F.3.2 Alternativa posible**

Una alternativa más rápida sería:

* React simple con Vite

También es válida.

Pero entre ambas, para una demo que querés vender, **Next.js** tiene mejor framing de producto.

---

### **F.3.3 Qué NO recomiendo como principal**

Para este caso no iría con:

* Streamlit como solución final de demo comercial  
* herramientas no-code  
* UI demasiado prototípica

Streamlit puede servir para exploración interna, pero si la meta es impresionar a una multinacional, prefiero una app web real.

---

### **F.3.4 Responsabilidades del frontend**

El frontend del MVP debe encargarse de:

* mostrar pantalla de setup  
* subir archivo  
* gatillar corrida  
* listar resultados  
* navegar por conceptos  
* mostrar drill-down  
* disparar exports

No debería implementar lógica de negocio compleja.

---

### **F.3.5 Componentes principales del frontend**

A nivel conceptual, los componentes serían:

* `RunSetupForm`  
* `UploadBox`  
* `ExpectedTotalsPreview`  
* `RunSummaryCards`  
* `ConceptResultsTable`  
* `ConceptExplanationPanel`  
* `ExceptionDrilldownTable`  
* `ExportActions`

Esto ordena mucho el build.

---

### **F.3.6 Estado del frontend**

Para el MVP, el manejo de estado puede ser simple:

* estado local para formularios  
* fetch a API para resultados  
* quizá una librería ligera como React Query para data fetching

No hace falta Redux ni nada grande.

---

## **F.4 Backend**

El backend debe ser la capa que unifica:

* uploads  
* persistencia  
* ejecución de lógica  
* exposición de resultados

---

### **F.4.1 Recomendación**

Mi recomendación principal es:

**Python \+ FastAPI**

---

### **Por qué FastAPI**

Porque tiene un fit excelente con este caso:

* Python es ideal para procesamiento de datos  
* FastAPI permite APIs limpias y rápidas  
* buena validación de input/output  
* documentación automática útil  
* setup liviano  
* excelente velocidad de desarrollo

---

### **F.4.2 Por qué Python es la mejor elección**

Porque el corazón del sistema es:

* parsing de CSV  
* normalización  
* agregación  
* comparación  
* excepciones  
* explicación basada en reglas

Todo eso encaja muy bien en Python con:

* pandas  
* pydantic  
* SQLAlchemy

Hacerlo en Node sería posible, pero menos natural para este problema.

---

### **F.4.3 Responsabilidades del backend**

El backend del MVP debe resolver:

* endpoint de health/status  
* endpoint de upload  
* endpoint de creación de corrida  
* endpoint de ejecución de conciliación  
* endpoint de consulta de resultados  
* endpoint de consulta de detalle  
* endpoint de export

---

### **F.4.4 Estructura lógica del backend**

Recomiendo separar internamente el backend en módulos como:

* `api/`  
* `services/`  
* `reconciliation/`  
* `repositories/`  
* `models/`  
* `schemas/`  
* `utils/`

Eso mantiene orden sin complicarse.

---

### **F.4.5 Qué NO hacer en el MVP**

No hace falta:

* separar varios servicios desplegados  
* colas asíncronas  
* jobs distribuidos  
* autenticación compleja  
* feature flags sofisticados

Todo eso puede esperar.

---

## **F.5 Motor de procesamiento**

Este es el núcleo lógico del producto.

Aunque técnicamente puede vivir dentro del backend, conceptualmente conviene tratarlo como una capa propia.

---

### **F.5.1 Recomendación**

Implementarlo en **Python**, dentro del backend, como un módulo claramente separado.

---

### **F.5.2 Librerías recomendadas**

Para el MVP:

* **pandas** para manipulación tabular  
* utilidades Python estándar para reglas  
* opcionalmente SQLAlchemy para persistencia  
* opcionalmente numpy para algunas operaciones estadísticas simples

---

### **F.5.3 Por qué pandas tiene sentido**

Porque para este MVP vamos a trabajar con:

* archivos CSV  
* tablas medianas (3.000–4.000 líneas)  
* reglas de agregación simples  
* detección de duplicados, outliers y anomalías

pandas es perfecto para esto:

* rápido de implementar  
* muy flexible  
* muy legible si se estructura bien

No hace falta montar Spark, dbt ni pipelines complejos.

---

### **F.5.4 Responsabilidades del motor**

El motor debe tener submódulos o funciones claras para:

1. **schema validation**  
2. **normalization**  
3. **concept mapping**  
4. **dataset preparation**  
5. **aggregation**  
6. **comparison with expected totals**  
7. **exception detection**  
8. **explanation generation**  
9. **result packaging**

---

### **F.5.5 Diseño modular interno recomendado**

Recomiendo pensar módulos como:

* `validators.py`  
* `normalizers.py`  
* `mappers.py`  
* `aggregators.py`  
* `comparators.py`  
* `exceptions.py`  
* `explanations.py`  
* `orchestrator.py`

Esto evita que todo termine en una función monstruo.

---

### **F.5.6 Orquestación del proceso**

La corrida debería ejecutarse en un orden claro:

#### **1\. Parse input**

leer CSV y tablas auxiliares

#### **2\. Validate**

validar columnas y formato

#### **3\. Normalize**

normalizar conceptos, períodos e importes

#### **4\. Prepare dataset**

marcar anomalías preliminares y dejar base conciliable

#### **5\. Aggregate**

calcular observed totals

#### **6\. Compare**

calcular diff y estado

#### **7\. Detect exceptions**

marcar anomalías

#### **8\. Explain**

armar narrativa y recomendaciones

#### **9\. Persist**

guardar outputs relevantes

#### **10\. Return**

devolver resumen al frontend

---

### **F.5.7 Explicación basada en reglas**

Para el MVP, la generación de explicación debe ser:

**rule-based \+ template-based**

No hace falta meter LLM todavía.

Eso significa:

* reglas detectan causas  
* templates producen narrativa

Ejemplo:

* si hay out-of-period \+ unmapped \+ duplicates  
* generar un texto priorizado con esos elementos

Eso es mucho más controlable, más auditable y más fácil de construir.

---

### **F.5.8 Outliers**

Para outliers, recomiendo una lógica sencilla y robusta:

* mediana por concepto  
* marcar si importe individual \> 3x o 5x mediana

Simple y suficiente.

---

## **F.6 Base de datos**

Aunque sea MVP, sí recomiendo usar base de datos.

No por volumen, sino por credibilidad y trazabilidad.

---

### **F.6.1 Recomendación**

Mi recomendación principal es:

**PostgreSQL**

---

### **Por qué Postgres**

Porque:

* es estándar y serio  
* fácil de levantar  
* da sensación de producto real  
* soporta perfectamente el volumen del MVP  
* deja buen camino de evolución

---

### **F.6.2 Alternativa posible**

**SQLite** sería válido para máxima velocidad.

Pero si el objetivo es demo funcional vendible, prefiero **Postgres** por framing técnico y orden estructural.

---

### **F.6.3 Qué se guarda en DB**

No hace falta guardar todo raw de forma obsesiva, pero sí al menos:

* corridas  
* metadata de archivos  
* expected totals usados  
* resultados por concepto  
* excepciones detectadas  
* detalles explicativos

---

### **F.6.4 Qué puede quedar fuera**

Para el MVP, el raw CSV podría:

* guardarse como archivo  
* y no necesariamente persistirse línea por línea en tablas permanentes si eso complica demasiado

Aunque también sería aceptable cargarlo a una tabla staging si lo vemos útil.

---

### **F.6.5 Recomendación práctica**

Mi recomendación MVP es:

* guardar el archivo original en storage local  
* persistir en DB:  
  * metadata de corrida  
  * summary por concepto  
  * excepciones  
  * referencias necesarias para drill-down

Eso alcanza.

---

## **F.7 Modelo de datos lógico**

Acá conviene dejar cerradas las entidades principales del sistema.

---

### **F.7.1 Entidad: reconciliation\_runs**

Representa una corrida de conciliación.

Campos sugeridos:

* `id`  
* `run_name` o `run_label`  
* `period`  
* `status`  
* `source_file_name`  
* `record_count`  
* `concept_count`  
* `created_at`  
* `completed_at`  
* `overall_status`

---

### **F.7.2 Entidad: expected\_totals**

Representa la referencia esperada utilizada.

Campos sugeridos:

* `id`  
* `run_id`  
* `period`  
* `legal_entity` (nullable)  
* `concept_code_normalized`  
* `expected_amount`  
* `currency`

---

### **F.7.3 Entidad: reconciliation\_results**

Resultado agregado por unidad conciliable.

Campos sugeridos:

* `id`  
* `run_id`  
* `period`  
* `legal_entity` (nullable)  
* `concept_code_normalized`  
* `concept_name_normalized`  
* `observed_amount`  
* `expected_amount`  
* `absolute_diff`  
* `relative_diff_pct`  
* `status`  
* `impacted_record_count`  
* `impacted_employee_count`  
* `summary_explanation`

---

### **F.7.4 Entidad: reconciliation\_exceptions**

Excepciones detectadas por concepto o línea.

Campos sugeridos:

* `id`  
* `run_id`  
* `result_id`  
* `record_id` (nullable si es excepción agregada)  
* `employee_id` (nullable)  
* `exception_type`  
* `severity`  
* `estimated_impact_amount`  
* `observation`  
* `created_at`

---

### **F.7.5 Entidad: uploaded\_files**

Metadata del archivo cargado.

Campos sugeridos:

* `id`  
* `run_id`  
* `file_name`  
* `file_type`  
* `storage_path`  
* `uploaded_at`

---

### **F.7.6 Entidad opcional: concept\_master**

Puede estar persistida o vivir como archivo/config.

Campos:

* `raw_code`  
* `normalized_code`  
* `normalized_name`  
* `category`  
* `expected_sign`  
* `reconciliation_group`

---

### **F.7.7 Entidad opcional: drilldown\_records**

Si queremos facilitar el detalle, podría existir una tabla derivada para registros relevantes.

Pero para MVP, esto puede resolverse sin crear una tabla adicional fija, dependiendo de cómo queramos implementar el detalle.

---

## **F.8 Persistencia del detalle y drill-down**

Este punto merece definición propia porque afecta la implementación.

---

### **Opción A — Recalcular detalle desde archivo**

Pros:

* menos persistencia  
* menos tablas

Contras:

* más complejidad al servir drill-down  
* menos trazabilidad

---

### **Opción B — Persistir una staging table del payroll**

Pros:

* facilita drill-down  
* facilita reproducibilidad  
* simplifica queries de detalle

Contras:

* más trabajo inicial

---

### **Recomendación MVP**

Yo recomiendo una solución intermedia:

**persistir el payroll normalizado de la corrida en una tabla staging simple**

Por ejemplo:

* `run_payroll_lines`

Eso nos da muchas ventajas para el demo.

---

### **Entidad recomendada: run\_payroll\_lines**

Campos sugeridos:

* `id`  
* `run_id`  
* `record_id`  
* `employee_id`  
* `employee_name`  
* `legal_entity`  
* `country`  
* `cost_center`  
* `payroll_period`  
* `posting_date`  
* `concept_code_raw`  
* `concept_code_normalized`  
* `concept_name_raw`  
* `concept_name_normalized`  
* `amount`  
* `currency`  
* `is_valid`  
* `exception_flags`

Esto hace muchísimo más fácil el drill-down.

---

## **F.9 Endpoints del backend**

Conviene dejar una primera definición funcional de API.

---

### **F.9.1 Crear corrida**

`POST /runs`

Crea una nueva corrida y registra metadata inicial.

---

### **F.9.2 Subir archivo**

`POST /runs/{run_id}/upload`

Sube payroll file.

---

### **F.9.3 Ver expected totals**

`GET /runs/{run_id}/expected-totals`

Obtiene expected totals cargados/precargados.

---

### **F.9.4 Ejecutar conciliación**

`POST /runs/{run_id}/execute`

Corre validación, procesamiento, conciliación y persistencia.

---

### **F.9.5 Obtener resumen**

`GET /runs/{run_id}/summary`

Devuelve:

* KPIs  
* overall status  
* resumen ejecutivo

---

### **F.9.6 Obtener resultados por concepto**

`GET /runs/{run_id}/results`

Lista resultados agregados por concepto.

---

### **F.9.7 Obtener detalle de concepto**

`GET /runs/{run_id}/results/{result_id}`

Devuelve:

* KPIs del concepto  
* explicación  
* causas detectadas

---

### **F.9.8 Obtener drill-down**

`GET /runs/{run_id}/results/{result_id}/drilldown`

Devuelve líneas/empleados asociados.

---

### **F.9.9 Exportar**

`GET /runs/{run_id}/export/summary`  
`GET /runs/{run_id}/export/exceptions`

---

### **F.9.10 Estado de salud**

`GET /health`

Simple pero útil.

---

## **F.10 Trazabilidad técnica**

Incluso para un MVP, esta parte suma muchísimo.

---

### **F.10.1 Qué debemos poder responder**

Después de una corrida, el sistema debería poder responder:

* qué archivo se usó  
* cuándo se corrió  
* qué período se analizó  
* cuántos registros entraron  
* qué conceptos se detectaron  
* qué resultados salieron  
* qué excepciones se marcaron

---

### **F.10.2 Metadata mínima de ejecución**

Cada corrida debería registrar:

* `run_id`  
* `created_at`  
* `completed_at`  
* `source_file_name`  
* `record_count`  
* `normalized_record_count`  
* `invalid_record_count`  
* `reconciled_concept_count`  
* `minor_diff_concept_count`  
* `unreconciled_concept_count`

---

### **F.10.3 Versión de reglas**

Aunque sea simple, conviene guardar algo como:

* `rules_version = "mvp_v1"`

Eso es pequeño pero muy valioso conceptualmente.

---

## **F.11 Estrategia de almacenamiento de archivos**

No necesitamos cloud storage complejo para el MVP.

---

### **Recomendación**

Usar almacenamiento local estructurado, por ejemplo:

* `/uploads/{run_id}/payroll.csv`  
* `/uploads/{run_id}/expected_totals.csv`

Eso es más que suficiente al inicio.

---

### **Ventaja**

* simple  
* rápido  
* controlable  
* fácil de inspeccionar

---

### **Desventaja aceptada**

No es arquitectura productiva enterprise, pero para MVP está perfecto.

---

## **F.12 Estrategia de despliegue del MVP**

Conviene también definir cómo lo imaginaríamos corriendo.

---

### **Opción recomendada**

Despliegue simple con:

* frontend web  
* backend API  
* Postgres  
* todo dockerizado

---

### **Por qué Docker tiene sentido**

Porque permite:

* demo consistente  
* setup reproducible  
* facilidad para mostrar/local/dev  
* escalón natural hacia cloud luego

---

### **Arquitectura de despliegue MVP**

Podría ser:

* `frontend` container  
* `backend` container  
* `postgres` container

Y listo.

No hace falta más.

---

## **F.13 Seguridad y autenticación**

Acá es importante no sobrediseñar.

---

### **Para el MVP**

No hace falta login enterprise completo.

Opciones:

* sin autenticación real si es demo guiada  
* autenticación dummy muy simple si queremos framing de producto

---

### **Mi recomendación**

Para MVP demo comercial:

* sin login complejo  
* acceso directo controlado

Eso evita fricción y acelera mucho.

---

## **F.14 Logging y observabilidad**

No necesitamos observabilidad enterprise, pero sí algo básico.

---

### **Mínimo recomendado**

* logs del backend  
* logs de ejecución de corrida  
* errores capturados  
* tiempos de ejecución simples

Eso ayuda mucho a depurar.

---

## **F.15 Decisiones técnicas del MVP**

Acá cierro las decisiones recomendadas de forma explícita.

---

### **Frontend**

* **Next.js**  
* UI limpia, tablas y vistas simples

### **Backend**

* **Python \+ FastAPI**

### **Motor**

* **pandas \+ reglas en Python**  
* explicación template-based

### **Base de datos**

* **PostgreSQL**

### **Persistencia de archivos**

* almacenamiento local por `run_id`

### **Modelo de persistencia**

* corridas  
* expected totals  
* resultados  
* excepciones  
* payroll staging normalizado

### **Infraestructura**

* **Docker Compose** con 3 servicios

### **Autenticación**

* mínima o inexistente en esta etapa

### **Escalabilidad**

* razonable, no prematura

---

## **F.16 Qué NO debe incluir esta arquitectura MVP**

Para proteger foco, dejo explícito lo que no entra:

* microservicios  
* event-driven architecture  
* colas  
* workers asíncronos complejos  
* multi-tenant real  
* configuración libre de reglas  
* versionado sofisticado de datasets  
* data lake  
* pipelines cloud complejos  
* observabilidad avanzada  
* RBAC enterprise  
* integración real con SAP

Todo eso puede venir después.

---

## **F.17 Riesgos aceptados del MVP**

Conviene dejar honestamente los riesgos asumidos.

---

### **1\. Lógica rule-based limitada**

Aceptamos que la explicación no será “inteligente” en todos los casos, sino controlada.

### **2\. Almacenamiento local**

Aceptamos que no es arquitectura cloud enterprise.

### **3\. Volumen acotado**

Aceptamos que la solución está optimizada para demo y no para escala masiva.

### **4\. UX enfocada**

Aceptamos que la app no cubrirá flujos complejos ni múltiples roles.

### **5\. Datos controlados**

Aceptamos que el dataset está diseñado para mostrar valor, no para representar todo el caos real.

---

# **Resumen técnico integrado del MVP**

La arquitectura técnica recomendada queda así:

## **Frontend**

Aplicación web en **Next.js**

## **Backend**

API en **FastAPI**

## **Motor de conciliación**

Módulo Python con:

* pandas  
* validación  
* normalización  
* agregación  
* comparación  
* detección de excepciones  
* explicación basada en templates

## **Persistencia**

**PostgreSQL** para:

* runs  
* expected totals  
* results  
* exceptions  
* run payroll lines

## **Storage**

Archivos locales por corrida

## **Deploy**

**Docker Compose**

---

# **Decisiones cerradas que deja esta sección**

Con esta sección queda definido:

* stack MVP realista  
* capas técnicas principales  
* responsabilidades por capa  
* entidades lógicas principales  
* forma de servir UI y resultados  
* estrategia de persistencia  
* endpoints base  
* despliegue simple

Esto ya nos deja en una posición muy buena para pasar al siguiente nivel.

---

# **Mi lectura sobre la Sección F**

Acá ya tenemos prácticamente el esqueleto completo del MVP:

* ya definimos el problema  
* la lógica funcional  
* las reglas  
* el dataset  
* la UX  
* y ahora la arquitectura técnica

En otras palabras:  
**ya no estamos imaginando una idea; ya estamos definiendo un sistema construible**.

Y eso nos deja listos para la fase donde todo esto se traduce a ejecución real.

Sí — **es una excelente decisión para este MVP**. De hecho, es probablemente el **setup más coherente con todo lo que venimos construyendo**: rápido, limpio, vendible y con muy buen “look & feel” de producto.

Te doy una lectura clara (estratégica \+ técnica) para que tengas total confianza 👇

---

# **✅ Stack propuesto**

* **Frontend:** Vercel (Next.js)  
* **Backend:** FastAPI en Vercel Functions  
* **DB:** Supabase (PostgreSQL)  
* **Storage:** Vercel Blob *o* Supabase Storage

👉 Esto está **perfectamente alineado con un MVP demo vendible**

---

# **🧠 Por qué esta combinación es ideal (para este caso)**

## **1\. Velocidad brutal de implementación**

Ya conoces:

* Vercel  
* Supabase

👉 Eso reduce muchísimo:

* setup time  
* debugging  
* fricción mental

Y eso, en este tipo de proyecto, vale oro.

---

## **2\. Look & feel de producto real**

Esto es clave para tu objetivo.

Con este stack:

* URL pública prolija  
* UI fluida  
* performance rápida  
* deploy continuo

👉 No parece un prototipo → **parece producto**

---

## **3\. Arquitectura simple pero creíble**

Aunque es MVP, este stack comunica:

* separación frontend/backend  
* DB real (Postgres)  
* API estructurada  
* persistencia  
* escalabilidad potencial

👉 A ojos de un cliente enterprise: ✔️

---

## **4\. Supabase encaja perfecto con el modelo que definimos**

Todo lo que diseñamos en F.7 cae directo en Supabase:

* `reconciliation_runs`  
* `expected_totals`  
* `reconciliation_results`  
* `reconciliation_exceptions`  
* `run_payroll_lines`

👉 No hay fricción conceptual → implementación directa

---

## **5\. Evitas infra innecesaria**

Comparado con:

* montar GCP/AWS completo  
* manejar Docker infra  
* levantar servicios manuales

👉 esto es:

* más rápido  
* más barato  
* más mantenible en MVP

---

# **⚠️ Lo único a tener en cuenta (muy importante)**

No es un “pero”, es un **ajuste fino para que todo funcione bien**:

---

## **1\. FastAPI en Vercel → usarlo correctamente**

FastAPI en Vercel corre como función serverless.

👉 Implica:

* no hay procesos largos  
* no hay estado persistente en memoria  
* todo debe ser relativamente rápido

### **💡 Traducción práctica:**

Tu motor de conciliación debe ser:

* síncrono  
* rápido (\< segundos)  
* sin dependencias pesadas

👉 Y esto está PERFECTO para tu caso (3k–4k rows con pandas)

---

## **2\. Procesamiento de archivos**

No dependas de:

* guardar archivos localmente en Vercel

👉 Mejor usar:

### **Opción A (recomendada)**

**Supabase Storage**

Ventajas:

* ya estás en el ecosistema  
* fácil integración  
* persistente  
* simple

---

### **Opción B**

**Vercel Blob**

También válido, pero:

* ya estás usando Supabase → menos fragmentación

👉 Yo usaría **Supabase Storage**

---

## **3\. DB: usar Supabase bien estructurado**

Evita caer en:

* usar Supabase como "dump de JSON"

👉 Mantené lo que definimos:

* tablas limpias  
* relaciones claras  
* queries simples

Eso hace que:

* el demo sea más creíble  
* el sistema escale mejor

---

## **4\. Evitar jobs largos / async complejos**

Para MVP:

❌ no usar:

* queues  
* workers  
* background jobs complejos

✅ hacer:

* `POST /execute` → procesa → responde

---

## **5\. Tamaño del archivo**

Mantener CSVs razonables:

* \< 5–10 MB

👉 Más que suficiente para demo

---

# **🧱 Arquitectura final (adaptada a Vercel \+ Supabase)**

Queda así:

## **Frontend (Vercel)**

* Next.js  
* UI completa  
* consumo de API

## **Backend (Vercel Functions)**

* FastAPI  
* endpoints REST  
* motor de conciliación embebido

## **Database (Supabase Postgres)**

* runs  
* results  
* exceptions  
* staging payroll

## **Storage (Supabase Storage)**

* payroll.csv  
* expected\_totals.csv

---

# **🔥 Insight importante (muy alineado con tu perfil)**

Esto que estás armando ya tiene características de:

👉 **proto-producto repetible**

Y este stack:

* Vercel  
* Supabase

es exactamente el stack que usan muchísimos:

* SaaS early-stage  
* productos AI-first  
* herramientas internas que luego escalan

👉 Estás construyendo algo que puede:

* cerrar este deal  
* replicarse en otros  
* evolucionar a producto real

---

# **⚖️ Trade-off consciente (y correcto)**

Estás eligiendo:

### **✔️ Ganar**

* velocidad  
* simplicidad  
* demo quality  
* costo bajo

### **❌ Aceptar**

* no es arquitectura enterprise final  
* límites de serverless  
* menos control infra

👉 Para este stage → decisión perfecta

---

# **🚀 Conclusión**

👉 **Sí, Vercel \+ Supabase es la mejor decisión para este MVP.**

No solo es correcta técnicamente, sino que está:

* alineada al objetivo comercial  
* alineada a tu experiencia previa  
* optimizada para execution speed

