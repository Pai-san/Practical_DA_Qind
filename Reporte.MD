# ✍️ Decisiones Técnicas Tomadas en el Desarrollo del ETL

## 1. Infraestructura y Herramientas a Utilizar

Durante la planificación y construcción del proceso ETL para el dataset de NYC Yellow Taxi, se consideraron varias alternativas basadas en eficiencia, escalabilidad y facilidad de implementación.

### Opción 1: Servicios Cloud - AWS (Athena + Glue)

- **Idea inicial:** Desarrollar el pipeline utilizando servicios administrados en la nube como **AWS Athena** (para consultas sobre datos en S3) y **AWS Glue** (para automatizar ETL mediante crawlers y jobs Spark).
- **Ventajas esperadas:**
  - Gestión automática de infraestructura.
  - Escalabilidad bajo demanda.
  - Posibilidad de orquestar pipelines vía Glue Workflows.
- **Razón de descarte:**
  - Restricciones de presupuesto.
  - Acceso limitado a las credenciales de los servicios cloud necesarios.
  - Tiempo adicional requerido para la configuración de IAM roles, S3 buckets y Workflows.

---

### Opción 2: Apache Spark (PySpark)

- **Segunda alternativa:** Construir el pipeline ETL localmente utilizando **PySpark**, como sugería el enunciado de la prueba.
- **Pasos realizados:**
  - Configuración inicial de una **SparkSession** usando `SparkSession.builder`.
  - Intento de correr procesos Spark en local mode (`master("local[*]")`).
- **Problemas encontrados:**
  - **Alto tiempo de inicialización** de la sesión, incluso para datasets medianos (~700MB).
  - **Consumo elevado de recursos** de CPU y RAM.
  - Creación de una imagen Docker personalizada para Spark:
    - Incluía Java (OpenJDK 8), Hadoop binaries, PySpark.
    - **Tamaño total** de la imagen > **15GB**.
    - El proceso de build y ejecución de contenedores era muy pesado y lento en entornos de hardware moderado.

---

### Opción 3: Python Nativo + Pandas

- **Decisión final:**  
  Utilizar **Python puro** con **Pandas** como motor de procesamiento de datos.

- **Justificación técnica:**

  - Pandas es altamente eficiente para datasets de tamaño pequeño a medio (hasta varios GB en RAM).
  - El entorno de trabajo requería **velocidad de prototipado** y **simplicidad** en la ejecución.
  - Amplia experiencia previa trabajando con Pandas, permitiendo aplicar rápidamente técnicas de:
    - Limpieza y validación de datos (`dropna`, filtros condicionales).
    - Transformaciones de columnas (`apply`, `groupby`, `agg`).
    - Escritura y lectura de archivos en formato **Parquet**, aprovechando la eficiencia de almacenamiento de este formato columnar.
  - Uso de librerías auxiliares como:
    - `pyarrow` para mejorar el performance al leer y escribir Parquet.
    - `pathlib` para manejo robusto de rutas de archivos.
    - `logging` para trazabilidad y observabilidad del pipeline.

- **Resultado:**  
  Aunque Pandas no ofrece paralelismo distribuido como Spark, para los volúmenes de datos tratados (menos de 2GB), el rendimiento fue aceptable y permitió mantener el control total del pipeline y su observabilidad.

---

# 📋 Resumen de Tecnologías Usadas

| Herramienta     | Uso                            | Motivo                                        |
| :-------------- | :----------------------------- | :-------------------------------------------- |
| **Python 3.11** | Lenguaje base                  | Versatilidad y soporte de librerías modernas. |
| **Pandas**      | ETL (Extract, Transform, Load) | Procesamiento eficiente en memoria.           |
| **PyArrow**     | I/O de archivos Parquet        | Mayor velocidad de serialización.             |
| **Logging**     | Observabilidad                 | Registro de eventos, errores y tiempos.       |
| **Pathlib**     | Manejo de rutas                | Abstracción multiplataforma de archivos.      |

---

# 🚀 Conclusión

Aunque inicialmente se planeaba usar Spark o infraestructura cloud, se priorizó **una solución funcional, mantenible y eficiente** basada en las herramientas que mejor se adaptaban a las restricciones del proyecto y los limites de mi conocimiento y herramientas.  
El pipeline desarrollado permite escalar relativamente bien a volúmenes moderados de datos y sirve como una base sólida para migraciones futuras a soluciones distribuidas si el tamaño del dataset o las necesidades de negocio lo requieren.
