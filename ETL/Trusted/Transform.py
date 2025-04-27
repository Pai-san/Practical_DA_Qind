import logging
import pandas as pd

def clean_and_validate(df: pd.DataFrame) -> pd.DataFrame:
    initial_count = len(df)
    try:
        df_clean = df.copy()

        # Filtrar nulos en columnas obligatorias
        required_columns = [
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "passenger_count",
            "trip_distance",
            "fare_amount",
            "PULocationID"
        ]
        df_clean = df_clean.dropna(subset=required_columns)

        # Validaciones básicas
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

        # === Enriquecimiento con Taxi Zone Lookup ===
        logging.info("Enriqueciendo datos con Taxi Zone Lookup...")

        try:
            # Descargar o cargar la tabla de zonas
            taxi_zone_url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"
            taxi_zone_lookup = pd.read_csv(taxi_zone_url)

            # Hacer join (PULocationID -> LocationID)
            df_clean = df_clean.merge(
                taxi_zone_lookup[["LocationID", "Borough", "Zone"]],
                how="left",
                left_on="PULocationID",
                right_on="LocationID"
            )

            # Opcional: eliminar la columna extra 'LocationID' si no la quieres
            df_clean.drop(columns=["LocationID"], inplace=True)

            logging.info("Enriquecimiento exitoso.")

        except Exception as e:
            logging.warning(f"No se pudo enriquecer con Taxi Zone Lookup: {e}")

        return df_clean

    except Exception as e:
        logging.error(f"Error en limpieza y validación: {e}")
        return pd.DataFrame()
