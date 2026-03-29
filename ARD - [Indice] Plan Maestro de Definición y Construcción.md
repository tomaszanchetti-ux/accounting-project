# **Accounting Reconciliation Demo**

## **Plan Maestro de Definición y Construcción**

### **Índice estructurado de trabajo**

---

# **A. Fundamentos del producto demo**

Este bloque busca dejar completamente cerrada la definición madre del proyecto antes de entrar en piezas funcionales o técnicas.

## **A.1 Propósito del demo**

Definir con precisión para qué existe esta demo y qué tiene que lograr.

### **Debe cerrar:**

* objetivo principal del demo  
* objetivo comercial  
* objetivo funcional  
* objetivo narrativo  
* qué impresión debe dejar en el cliente

---

## **A.2 Problema de negocio que resuelve**

Formalizar el dolor real que estamos simulando resolver.

### **Debe cerrar:**

* problema operativo central  
* impacto en tiempo, errores y trazabilidad  
* por qué duele en multinacionales  
* por qué vale la pena automatizarlo

---

## **A.3 Usuario principal y actores involucrados**

Identificar quién usa la solución y quiénes orbitan el proceso.

### **Debe cerrar:**

* usuario primario  
* stakeholders secundarios  
* qué necesita ver cada actor  
* qué nivel de detalle requiere cada uno

---

## **A.4 Caso de uso central**

Definir el flujo principal exacto que la demo debe representar.

### **Debe cerrar:**

* situación inicial  
* input que recibe el usuario  
* acción que ejecuta  
* output esperado  
* “momento wow” del flujo

---

## **A.5 Alcance del MVP / Demo**

Delimitar claramente qué incluye y qué no incluye esta versión.

### **Debe cerrar:**

* alcance funcional del demo  
* profundidad de la simulación  
* límites para evitar scope creep  
* nivel de realismo esperado

---

## **A.6 Criterios de éxito**

Definir cómo sabremos que el demo está bien diseñado.

### **Debe cerrar:**

* criterios de éxito de negocio  
* criterios de éxito funcional  
* criterios de éxito narrativo  
* criterios de éxito técnico mínimos

---

# **B. Arquitectura funcional de la solución**

Este bloque define cómo funciona el sistema de punta a punta, sin entrar todavía en bajo nivel técnico.

## **B.1 Visión funcional general**

Describir la solución como sistema: qué entra, qué procesa y qué sale.

### **Debe cerrar:**

* visión end-to-end del producto demo  
* bloques funcionales principales  
* relación entre los bloques

---

## **B.2 Flujo operativo del usuario**

Mapear paso a paso qué hace el usuario dentro del sistema.

### **Debe cerrar:**

* secuencia de uso  
* eventos clave  
* decisiones del usuario  
* outputs intermedios y finales

---

## **B.3 Entradas del sistema**

Definir todos los inputs que necesita la demo para operar.

### **Debe cerrar:**

* archivos de entrada  
* parámetros manuales  
* expected totals  
* maestros o tablas auxiliares  
* supuestos sobre calidad del input

---

## **B.4 Procesamiento funcional**

Definir qué transformaciones y validaciones realiza el sistema.

### **Debe cerrar:**

* validación de esquema  
* normalización  
* agregación  
* conciliación  
* análisis de excepciones  
* generación de explicación

---

## **B.5 Salidas del sistema**

Definir qué resultados produce el sistema y cómo se estructuran.

### **Debe cerrar:**

* resumen ejecutivo  
* resultado por concepto  
* detalle explicativo  
* drill-down por registro o empleado  
* exportables

---

## **B.6 Persistencia y trazabilidad**

Definir qué información debe quedar guardada en la demo y con qué objetivo.

### **Debe cerrar:**

* qué se persiste  
* qué no se persiste  
* necesidad de historial de corridas  
* bitácora mínima de auditoría  
* trazabilidad de inputs, reglas y resultados

---

## **B.7 Estados del proceso**

Definir los estados funcionales del sistema y de la conciliación.

### **Debe cerrar:**

* estado de carga  
* estado de validación  
* estado de conciliación  
* estado por concepto  
* estado general de corrida

---

# **C. Modelo de conciliación y reglas de negocio**

Este es uno de los núcleos del proyecto. Aquí definimos la lógica real que hará que el demo se sienta serio.

## **C.1 Unidad de conciliación**

Definir exactamente qué estamos conciliando.

### **Debe cerrar:**

* nivel de análisis principal  
* entidad de conciliación  
* dimensiones relevantes  
* granularidad mínima y máxima

---

## **C.2 Dimensiones de agregación**

Definir cómo se consolidan los datos.

### **Debe cerrar:**

* agrupación por concepto  
* agrupación por período  
* sociedad / entidad / país  
* centro de costo u otras dimensiones  
* cuáles aplican al MVP y cuáles no

---

## **C.3 Totales esperados**

Definir qué representa el valor esperado contra el cual comparamos.

### **Debe cerrar:**

* origen conceptual del expected total  
* formato de carga  
* nivel de agregación  
* relación con el concepto conciliado  
* supuestos de consistencia

---

## **C.4 Definición de “netear”**

Formalizar qué significa conciliación exitosa.

### **Debe cerrar:**

* igualdad exacta vs tolerancia  
* umbrales absolutos  
* umbrales relativos  
* cuándo un concepto se considera conciliado

---

## **C.5 Tolerancias**

Definir reglas de tolerancia para el MVP.

### **Debe cerrar:**

* tolerancia cero o no  
* bandas de severidad  
* amarillo vs rojo  
* criterio de materialidad demo

---

## **C.6 Estados de conciliación**

Definir semánticamente los resultados.

### **Debe cerrar:**

* reconciled  
* minor difference  
* unreconciled  
* invalid input  
* not enough information

---

## **C.7 Tipos de excepciones**

Definir qué anomalías será capaz de detectar el sistema.

### **Debe cerrar:**

* duplicados  
* faltantes  
* concepto no mapeado  
* período incorrecto  
* outlier  
* signo invertido  
* errores de clasificación  
* otros posibles casos MVP

---

## **C.8 Lógica de detección de excepciones**

Definir cómo identifica el sistema cada tipo de anomalía.

### **Debe cerrar:**

* reglas de detección  
* prioridad entre reglas  
* evidencia necesaria para disparar una excepción  
* relación entre excepciones y explicación final

---

## **C.9 Lógica de explicación de diferencias**

Definir cómo el sistema pasa de “hay diff” a “esta podría ser la causa”.

### **Debe cerrar:**

* explicación basada en reglas  
* estructura narrativa  
* ranking de causas probables  
* combinación de múltiples causas  
* qué nivel de certeza se mostrará

---

## **C.10 Recomendaciones de revisión**

Definir si el sistema sugiere próximos pasos al usuario.

### **Debe cerrar:**

* tipo de recomendación  
* tono de la recomendación  
* nivel de accionabilidad  
* relación entre excepción y sugerencia

---

# **D. Diseño del dataset dummy**

Este bloque es crítico porque la credibilidad de la demo depende muchísimo de la calidad del dataset.

## **D.1 Objetivo del dataset**

Definir qué rol cumple el dataset dentro del demo.

### **Debe cerrar:**

* para qué existe  
* cuánto realismo necesita  
* qué historia debe contar  
* cómo soporta el wow moment

---

## **D.2 Estructura de archivos**

Definir qué archivos/tablas componen el universo de datos demo.

### **Debe cerrar:**

* payroll file principal  
* expected totals  
* maestros de conceptos  
* tablas auxiliares opcionales  
* estructura mínima viable

---

## **D.3 Esquema de datos del payroll**

Definir columnas y formato del archivo principal.

### **Debe cerrar:**

* campos obligatorios  
* tipos de dato  
* convenciones  
* llaves lógicas  
* supuestos de calidad

---

## **D.4 Universo de empleados**

Definir el tamaño y composición de la base simulada.

### **Debe cerrar:**

* cantidad de empleados  
* distribución por entidad  
* distribución por centro de costo  
* casos especiales  
* representatividad demo

---

## **D.5 Universo de conceptos**

Definir los conceptos de nómina que existirán en el demo.

### **Debe cerrar:**

* lista de conceptos  
* categorías  
* importancia relativa  
* conceptos “limpios” vs problemáticos  
* conceptos candidatos a wow

---

## **D.6 Período y contexto temporal**

Definir cómo se simula el tiempo en la demo.

### **Debe cerrar:**

* período principal  
* posibles registros fuera de período  
* lógica de corte  
* consistencia temporal esperada

---

## **D.7 Casos normales**

Definir qué porción del dataset debe conciliar correctamente.

### **Debe cerrar:**

* porcentaje de conceptos que netean  
* proporción de registros sanos  
* baseline de comportamiento esperado

---

## **D.8 Anomalías inyectadas**

Definir de forma deliberada los errores que harán interesante la demo.

### **Debe cerrar:**

* qué anomalías se inyectan  
* en qué volumen  
* en qué conceptos  
* con qué severidad  
* con qué lógica narrativa

---

## **D.9 Casos wow**

Diseñar las discrepancias más demostrables del demo.

### **Debe cerrar:**

* concepto estrella para drill-down  
* combinación de causas  
* caso más visual  
* caso más explicable  
* caso que mejor vende el valor

---

## **D.10 Relación entre dataset y expected totals**

Definir cómo se construyen ambos para que el demo tenga coherencia interna.

### **Debe cerrar:**

* expected totals derivados vs diseñados  
* consistencia matemática  
* diferencias deliberadas  
* equilibrio entre realismo y control narrativo

---

# **E. UX funcional y Demo Flow**

Este bloque define cómo se ve y se vive la demo.

## **E.1 Objetivo de UX**

Definir qué sensación debe dejar la experiencia.

### **Debe cerrar:**

* simplicidad  
* claridad  
* seriedad enterprise  
* orientación a negocio  
* velocidad de comprensión

---

## **E.2 Flujo de pantallas**

Definir la secuencia de navegación principal.

### **Debe cerrar:**

* pantalla de ingreso  
* pantalla de setup  
* pantalla de resultados  
* pantalla de detalle  
* export / cierre

---

## **E.3 Pantalla de carga y configuración**

Definir qué ve el usuario al comenzar.

### **Debe cerrar:**

* upload de archivo  
* selección de período  
* carga de expected totals  
* validaciones previas  
* CTA principal

---

## **E.4 Pantalla de resumen ejecutivo**

Definir la vista principal post-conciliación.

### **Debe cerrar:**

* KPIs principales  
* conceptos conciliados vs no conciliados  
* monto total reconciliado  
* monto pendiente  
* visual principal de estado

---

## **E.5 Pantalla de resultado por concepto**

Definir cómo se muestra la conciliación a nivel concepto.

### **Debe cerrar:**

* columnas  
* estados  
* diff absoluto y relativo  
* ordenamiento  
* foco visual

---

## **E.6 Pantalla de explicación**

Definir cómo se presenta el valor diferencial del sistema.

### **Debe cerrar:**

* narrativa explicativa  
* causas probables  
* evidencia asociada  
* recomendaciones  
* tono del mensaje

---

## **E.7 Drill-down operacional**

Definir cómo baja el usuario desde el resumen al detalle.

### **Debe cerrar:**

* navegación al detalle  
* tabla por empleado / registro  
* anomalía asociada  
* filtros  
* experiencia de análisis

---

## **E.8 Exportables**

Definir qué evidencia o reporte puede extraer el usuario.

### **Debe cerrar:**

* export Excel  
* resumen de corrida  
* detalle de diferencias  
* formato y utilidad del export

---

## **E.9 Storytelling comercial de la demo**

Definir cómo se presenta la solución durante la reunión.

### **Debe cerrar:**

* orden narrativo  
* tiempos  
* momento wow  
* mensaje de negocio  
* cierre comercial

---

# **F. Arquitectura técnica mínima**

Aquí sí aterrizamos decisiones tecnológicas, pero al nivel justo para un MVP/demo.

## **F.1 Principios de arquitectura técnica**

Definir criterios rectores de diseño técnico.

### **Debe cerrar:**

* simplicidad  
* modularidad  
* credibilidad  
* velocidad de implementación  
* escalabilidad razonable

---

## **F.2 Frontend**

Definir cómo se construirá la capa visual.

### **Debe cerrar:**

* framework  
* tipo de app  
* complejidad necesaria  
* componentes principales  
* criterio de elección

---

## **F.3 Backend**

Definir la capa de servicios y orquestación.

### **Debe cerrar:**

* lenguaje  
* framework  
* responsabilidades  
* endpoints clave  
* relación con motor de conciliación

---

## **F.4 Motor de procesamiento**

Definir cómo se implementará la lógica de negocio.

### **Debe cerrar:**

* procesamiento con Python  
* uso de pandas / SQL  
* servicios internos  
* secuencia de ejecución  
* modularidad de reglas

---

## **F.5 Base de datos**

Definir si persistimos y cómo.

### **Debe cerrar:**

* Postgres vs SQLite  
* necesidad real de persistencia  
* tablas mínimas  
* criterio para demo creíble

---

## **F.6 Modelo de datos lógico**

Definir las entidades principales del sistema.

### **Debe cerrar:**

* payroll\_lines  
* expected\_totals  
* reconciliation\_runs  
* reconciliation\_results  
* reconciliation\_exceptions  
* otras entidades necesarias

---

## **F.7 Trazabilidad técnica**

Definir cómo se registran inputs, reglas y outputs.

### **Debe cerrar:**

* metadata de corrida  
* archivo utilizado  
* timestamp  
* versión de reglas  
* reproducibilidad mínima

---

## **F.8 Decisiones técnicas del MVP**

Cerrar explícitamente qué elegimos y por qué.

### **Debe cerrar:**

* stack final  
* simplificaciones aceptadas  
* riesgos conscientes  
* deudas técnicas toleradas

---

# **G. Construcción del backlog**

Este bloque traduce todo lo anterior a ejecución.

## **G.1 Épicas del proyecto**

Definir grandes bloques de construcción.

### **Debe cerrar:**

* data foundation  
* reconciliation engine  
* exception detection  
* explanation layer  
* UI  
* dummy data  
* demo storytelling

---

## **G.2 Cards funcionales**

Traducir cada épica en entregables concretos.

### **Debe cerrar:**

* unidades de trabajo visibles  
* dependencias  
* criterio de completitud

---

## **G.3 Tasks técnicas**

Bajar cada card a tareas implementables.

### **Debe cerrar:**

* tareas de front  
* tareas de back  
* tareas de data  
* tareas de QA  
* tareas de demo prep

---

## **G.4 Secuencia de implementación**

Ordenar el build de forma inteligente.

### **Debe cerrar:**

* qué construir primero  
* dependencias críticas  
* quick wins  
* orden para llegar rápido a demo funcional

---

## **G.5 Criterios de “demo-ready”**

Definir cuándo el MVP está listo para mostrarse.

### **Debe cerrar:**

* condiciones mínimas funcionales  
* calidad visual mínima  
* estabilidad mínima  
* guión de demo validado