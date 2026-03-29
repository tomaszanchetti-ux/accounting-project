# **Accounting Reconciliation MVP**

## **Executive Handoff / Reminder (Post-Session)**

---

# **1\. Qué estamos construyendo**

Estamos diseñando un **MVP funcional (demo vendible)** de:

**Sistema de conciliación entre RRHH (payroll) y Contabilidad, con capacidad de explicación de diferencias**

No es un ejercicio técnico.  
Es un **asset comercial** para:

* validar oportunidad con multinacional  
* cerrar proyecto de discovery / implementación  
* posicionarnos como expertos en Data \+ AI aplicado a procesos financieros

---

# **2\. Qué problema resolvemos**

Hoy el proceso es:

* CSV desde SAP  
* conciliación manual por concepto  
* análisis manual de diferencias  
* baja trazabilidad  
* alto esfuerzo operativo

👉 Nuestro sistema hace:

* agregación automática  
* conciliación contra expected totals  
* detección de anomalías  
* **explicación de diferencias (core value)**  
* drill-down a registros

---

# **3\. Qué hace especial esta solución**

No estamos construyendo:

❌ un dashboard  
❌ un ETL  
❌ un simple reconciler

Estamos construyendo:

👉 una capa que **explica por qué los números no cierran**

Ese es el diferencial.

---

# **4\. Estado actual del diseño**

El MVP está **conceptualmente cerrado** en 6 dimensiones:

---

## **A. Concepto y arquitectura macro**

* problema claro (conciliación payroll vs contabilidad)  
* usuario: contabilidad / controller  
* flujo: upload → run → summary → explanation → drill-down

---

## **B. Arquitectura funcional**

Componentes definidos:

* Ingesta (CSV \+ expected totals)  
* Normalización  
* Motor de conciliación  
* Detección de excepciones  
* Generación de explicación  
* Visualización

---

## **C. Reglas de negocio**

Totalmente definidas:

### **Conciliación**

* agregación por concepto  
* comparación expected vs observed  
* estados: reconciled / minor / unreconciled

### **Anomalías**

* duplicates  
* unmapped concept  
* out-of-period  
* missing population  
* outlier  
* sign error (opcional)

### **Explicación**

* rule-based  
* template-based  
* ranking de causas  
* impacto estimado

---

## **D. Dataset dummy**

Diseñado con intención (no random):

### **Estructura**

* payroll.csv  
* expected\_totals.csv  
* concept\_master.csv  
* employee\_reference.csv (opcional)

### **Volumen**

* \~360 empleados  
* \~3.000–4.000 líneas

### **Conceptos clave**

* MEAL\_VOUCHER (wow principal)  
* CHILDCARE (missing population)  
* OVERTIME (outlier)

### **Distribución**

* mayoría OK  
* algunos minor  
* pocos errores relevantes

👉 dataset diseñado para **control narrativo del demo**

---

## **E. UX y demo flow**

Definido como experiencia guiada:

### **Pantallas**

1. Setup  
2. Summary  
3. Concept Analysis  
4. Drill-down

### **Momento WOW**

* abrir concepto con diferencia  
* ver causas  
* bajar a registros

### **Narrativa comercial**

Demo de 5–8 minutos orientada a insight

---

## **F. Arquitectura técnica (MVP realista)**

### **Stack elegido**

* **Frontend:** Next.js (Vercel)  
* **Backend:** FastAPI (Vercel Functions)  
* **DB:** Supabase (Postgres)  
* **Storage:** Supabase Storage

### **Motor**

* Python \+ pandas  
* reglas explícitas  
* explicación template-based

### **Persistencia**

* runs  
* results  
* exceptions  
* staging payroll

👉 arquitectura simple, rápida y creíble

---

# **5\. Principios clave (no olvidar)**

## **1\. Esto es un MVP vendible**

No sobreingenierizar.

## **2\. Explicación \> cálculo**

El valor está en el “por qué”.

## **3\. Control narrativo**

El dataset y la UX están diseñados para contar una historia.

## **4\. Realismo suficiente**

Debe sentirse real, no perfecto.

## **5\. Time-to-demo manda**

Decisiones técnicas subordinadas a velocidad.

---

# **6\. Decisiones importantes ya tomadas**

* no microservicios  
* no async complejo  
* no auth enterprise  
* no infra pesada  
* sí reglas explícitas  
* sí persistencia  
* sí UI real  
* sí trazabilidad

---

# **7\. Qué falta (próximo paso)**

## **👉 G. Backlog de construcción**

Convertir todo esto en:

* épicas  
* tasks  
* dependencias  
* orden de implementación

Objetivo:

pasar de diseño → ejecución sin ambigüedad

---

# **8\. Cómo retomar rápido**

Cuando volvamos:

1. leer este documento  
2. ir directo a sección G  
3. empezar a descomponer en backlog  
4. priorizar quick wins (setup \+ run \+ summary)

---

# **9\. Norte del proyecto**

Si en algún momento dudamos:

“¿Esto ayuda a que un controller entienda por qué no le cierran los números en segundos?”

Si la respuesta es sí → vamos bien  
Si no → estamos desviándonos

---

# **10\. TL;DR**

Estamos construyendo:

👉 una demo funcional que convierte un CSV de payroll en una conciliación explicable, con foco en detectar y explicar diferencias de forma inmediata.

---

**Estado:** listo para pasar a construcción  
**Bloque siguiente:** backlog  
**Objetivo inmediato:** demo vendible