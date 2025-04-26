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

        # Crear carpeta de data si no existe
        Path("data").mkdir(exist_ok=True)

        # ETAPA EXTRACT
        t0 = time.time()
        df_raw = extract_yellow_taxi_data(2023)
        df_raw.to_parquet("data/yellow_taxi_raw.parquet", index=False)
        t1 = time.time()

        # ETAPA TRANSFORM
        df_trusted = clean_and_validate(df_raw)
        df_trusted.to_parquet("data/yellow_taxi_trusted.parquet", index=False)
        t2 = time.time()

        # ETAPA LOAD
        kpis = enrich_and_calculate_kpis(df_trusted)
        t3 = time.time()

        # Reporte
        report = {
            "total_records_raw": len(df_raw),
            "total_records_trusted": len(df_trusted),
            "records_discarded": len(df_raw) - len(df_trusted),
            "time_extract_sec": round(t1 - t0, 2),
            "time_transform_sec": round(t2 - t1, 2),
            "time_load_sec": round(t3 - t2, 2),
            "total_time_sec": round(time.time() - start_time, 2),
            "kpis": kpis,
        }

        with open("data/execution_report.json", "w") as f:
            json.dump(report, f, indent=4)

        logging.info("✅ Pipeline ejecutado exitosamente.")
        logging.info(f"Reporte generado en data/execution_report.json")

    except Exception as e:
        logging.error(f"Fallo en ejecución del pipeline: {e}")

if __name__ == "__main__":
    main()
