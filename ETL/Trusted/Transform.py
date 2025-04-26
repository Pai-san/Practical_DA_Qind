import logging
import pandas as pd

def clean_and_validate(df: pd.DataFrame) -> pd.DataFrame:
    initial_count = len(df)
    try:
        df_clean = df.copy()
        required_columns = ["tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count", "trip_distance", "fare_amount"]
        df_clean = df_clean.dropna(subset=required_columns)

        df_clean = df_clean[
            (df_clean["passenger_count"] > 0) &
            (df_clean["trip_distance"] > 0) &
            (df_clean["fare_amount"] > 0)
        ]

        filtered_count = len(df_clean)
        discarded = initial_count - filtered_count

        logging.info(f"Registros iniciales: {initial_count}")
        logging.info(f"Registros después de validaciones: {filtered_count}")
        logging.info(f"Registros descartados: {discarded}")

        return df_clean

    except Exception as e:
        logging.error(f"Error en limpieza y validación: {e}")
        return pd.DataFrame()
