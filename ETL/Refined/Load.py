import logging
import pandas as pd

def enrich_and_calculate_kpis(df: pd.DataFrame) -> dict:
    try:
        df_enriched = df.copy()

        # Convertir timestamps
        df_enriched["tpep_pickup_datetime"] = pd.to_datetime(df_enriched["tpep_pickup_datetime"])
        df_enriched["tpep_dropoff_datetime"] = pd.to_datetime(df_enriched["tpep_dropoff_datetime"])

        # Enriquecer datos: duración del viaje en minutos
        df_enriched["trip_duration_minutes"] = (
            (df_enriched["tpep_dropoff_datetime"] - df_enriched["tpep_pickup_datetime"]).dt.total_seconds() / 60
        )

        # Extraer hora y día de la semana
        df_enriched["pickup_hour"] = df_enriched["tpep_pickup_datetime"].dt.hour
        df_enriched["pickup_day_of_week"] = df_enriched["tpep_pickup_datetime"].dt.day_name()

        # KPIs Globales
        avg_trip_duration = df_enriched["trip_duration_minutes"].mean()
        avg_distance = df_enriched["trip_distance"].mean()
        avg_fare = df_enriched["fare_amount"].mean()
        total_trips = len(df_enriched)

        # === 1. Patrón de Demanda y Tiempos Pico ===
        demand_by_hour = df_enriched.groupby("pickup_hour").size().to_dict()
        demand_by_day = df_enriched.groupby("pickup_day_of_week").size().to_dict()

        # === 2. Eficiencia Geográfica y Económica ===
        df_enriched["fare_per_mile"] = df_enriched["fare_amount"] / df_enriched["trip_distance"]
        df_enriched["speed_mph"] = df_enriched["trip_distance"] / (df_enriched["trip_duration_minutes"] / 60)

        geo_efficiency = (
            df_enriched.groupby("Borough")
            .agg(
                avg_fare_per_mile=("fare_per_mile", "mean"),
                avg_speed_mph=("speed_mph", "mean"),
                total_trips=("fare_amount", "count"),
            )
            .reset_index()
            .sort_values(by="avg_fare_per_mile", ascending=False)
            .to_dict(orient="records")
        )

        # === 3. Impacto de la Calidad de Datos ===
        # Este KPI se calcula en el main, pero aquí preparamos una estructura base
        data_quality_impact = {
            "note": "Debe ser calculado en función de registros iniciales vs registros validados"
        }

        # Consolidar KPIs
        kpis = {
            "global_metrics": {
                "avg_trip_duration_minutes": round(avg_trip_duration, 2),
                "avg_distance_miles": round(avg_distance, 2),
                "avg_fare_amount_usd": round(avg_fare, 2),
                "total_trips": total_trips,
            },
            "demand_pattern": {
                "trips_by_hour": demand_by_hour,
                "trips_by_day": demand_by_day,
            },
            "geo_efficiency": geo_efficiency,
            "data_quality_impact": data_quality_impact,
        }

        logging.info("=== KPIs Calculados ===")
        for section, metrics in kpis.items():
            logging.info(f"{section}: {metrics}")

        return kpis

    except Exception as e:
        logging.error(f"Error en enriquecimiento y cálculo de KPIs: {e}")
        return {}
