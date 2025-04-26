import logging
import pandas as pd

def enrich_and_calculate_kpis(df: pd.DataFrame) -> dict:
    try:
        df_enriched = df.copy()
        df_enriched["trip_duration_minutes"] = (
            (pd.to_datetime(df_enriched["tpep_dropoff_datetime"]) - pd.to_datetime(df_enriched["tpep_pickup_datetime"]))
            .dt.total_seconds() / 60
        )

        avg_trip_duration = df_enriched["trip_duration_minutes"].mean()
        avg_distance = df_enriched["trip_distance"].mean()
        avg_fare = df_enriched["fare_amount"].mean()
        total_trips = len(df_enriched)

        kpis = {
            "avg_trip_duration_minutes": round(avg_trip_duration, 2),
            "avg_distance_miles": round(avg_distance, 2),
            "avg_fare_amount": round(avg_fare, 2),
            "total_trips": total_trips,
        }

        logging.info("=== KPIs Calculados ===")
        for key, value in kpis.items():
            logging.info(f"{key}: {value}")

        return kpis

    except Exception as e:
        logging.error(f"Error en enriquecimiento y cálculo de KPIs: {e}")
        return {}
