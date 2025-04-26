import logging
import json
import time
from pathlib import Path

from ETL.Raw.Extract import extract_yellow_taxi_data
from ETL.Trusted.Transform import clean_and_validate
from ETL.Refined.Load import enrich_and_calculate_kpis

import pandas as pd

# Configurar logging global
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def main():
    start_time = time.time()
    report = {}

    try:
        logging.info("🚀 Iniciando pipeline ETL Yellow Taxi...")

        # Pedir año al usuario
        year_input = input("🔢 Ingrese el año que desea procesar (por ejemplo 2023): ").strip()
        if not year_input.isdigit():
            raise ValueError("El año ingresado no es válido. Debe ser un número.")
        year = int(year_input)

        # Crear carpeta de data si no existe
        Path("data").mkdir(exist_ok=True)

        # ETAPA EXTRACT
        t0 = time.time()
        df_raw = extract_yellow_taxi_data(year)
        df_raw.to_parquet(f"data/yellow_taxi_raw_{year}.parquet", index=False)
        t1 = time.time()

        # ETAPA TRANSFORM
        df_trusted = clean_and_validate(df_raw)
        df_trusted.to_parquet(f"data/yellow_taxi_trusted_{year}.parquet", index=False)
        t2 = time.time()

        # ETAPA LOAD
        kpis = enrich_and_calculate_kpis(df_trusted)
        t3 = time.time()

        # Reporte
        report = {
            "year": year,
            "total_records_raw": len(df_raw),
            "total_records_trusted": len(df_trusted),
            "records_discarded": len(df_raw) - len(df_trusted),
            "time_extract_sec": round(t1 - t0, 2),
            "time_transform_sec": round(t2 - t1, 2),
            "time_load_sec": round(t3 - t2, 2),
            "total_time_sec": round(time.time() - start_time, 2),
            "kpis": kpis,
        }

        with open(f"data/execution_report_{year}.json", "w") as f:
            json.dump(report, f, indent=4)

        logging.info("✅ Pipeline ejecutado exitosamente.")
        logging.info(f"Reporte generado en data/execution_report_{year}.json")

    except Exception as e:
        logging.error(f"Fallo en ejecución del pipeline: {e}")

if __name__ == "__main__":
    main()
