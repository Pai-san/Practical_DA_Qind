import os
import pandas as pd
import requests
import logging
from time import sleep
from pathlib import Path
from io import BytesIO

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def extract_yellow_taxi_data(year: int, retries: int = 3) -> pd.DataFrame:
    """
    Extrae datos de taxis amarillos para el año indicado.
    """
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
    monthly_data = []
    total_raw_rows = 0

    for month in range(1, 13):
        month_str = f"{month:02d}"
        file_name = f"yellow_tripdata_{year}-{month_str}.parquet"
        url = base_url + file_name

        for attempt in range(1, retries + 1):
            try:
                logging.info(f"Descargando {file_name} (intento {attempt})")
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                df = pd.read_parquet(BytesIO(response.content))
                row_count = len(df)
                total_raw_rows += row_count

                logging.info(f"{file_name}: {row_count} registros extraídos")
                monthly_data.append(df)
                break  # éxito, salir del loop de reintentos

            except requests.exceptions.RequestException as e:
                logging.warning(f"Error al descargar {file_name}: {e}")
                if attempt == retries:
                    logging.error(f"Fallo permanente al descargar {file_name} tras {retries} intentos")
                else:
                    sleep(2)

            except Exception as e:
                logging.error(f"Error procesando {file_name}: {e}")
                break

    if not monthly_data:
        logging.error("No se pudieron cargar datos de ningún mes.")
        return pd.DataFrame()

    final_df = pd.concat(monthly_data, ignore_index=True)

    logging.info("=== KPI de Extracción ===")
    logging.info(f"Total registros extraídos (sin filtrar): {total_raw_rows}")

    return final_df
