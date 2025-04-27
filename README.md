# Practical_DA_Qind

Este repositorio es para la prueba practica de Quind.io

# NYC Yellow Taxi Data Pipeline 🚕

Este proyecto implementa un pipeline ETL modular para procesar datos de taxis amarillos de Nueva York (NYC TLC).

## Estructura de carpetas

Como se pidio en el ejercicio estructuramos el proyecto con diferentes capas de procesamiento de datos equivalentes a un ETL(Extract,Transform,Load) donde cada capa es un diferente nivel de medallón.

# Raw

contiene Extraction.py, este script busca descargar y procesar los parquets encontrados en el bucket S3 de AWS según el año en un dataframe para el proceso

# Trusted

La carpeta Trusted representa la segunda etapa del pipeline ETL. Aquí los datos extraídos en Raw son limpiados, validados y corregidos para garantizar su confiabilidad antes de cualquier análisis más avanzado.

# Refined

La carpeta Refined representa la última etapa del pipeline ETL. Aquí es donde los datos ya validados son enriquecidos y se les calcula métricas o KPIs para su análisis final.

# Data

La carpeta data es el repositorio local de almacenamiento donde el pipeline guarda los datasets generados en cada etapa (Raw, Trusted, Refined), así como otros archivos auxiliares como reportes. Esta carpeta es parte del .gitignore y solo se generara al final del proceso de un pipeline.

## Pasos para ejecutar

Los procesos de dependencias son manejados en el requirement, para poder ejecutar el pipeline se puede ejecutar desde terminal con los siguientes comandos

# 1

python -m pip install -r requirements.txt | Esto instalara las librerias necesarias para poder empezar los scripts

# 2

python Main.py | Esto ejectura el main script que hace llamado a cada capa dentro del ETL y procesa los datos juntos a sus KPI, de parte de input te preguntara por un año en especifico para poder sacar los datos de los taxi amarillos.
