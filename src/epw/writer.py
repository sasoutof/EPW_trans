from pathlib import Path
import pandas as pd

from src.epw.header import build_epw_header
from src.epw.weather_data import WeatherData
from src.epw.validator import validate_weather_dataframe


def _safe_value(row, column, default):
    if column in row and pd.notna(row[column]):
        return row[column]
    return default


def _build_epw_row(row):
    dt = pd.to_datetime(row["fecha_hora_local"])

    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour + 1
    minute = 60

    dry_bulb = round(_safe_value(row, "temperatura_seca_C", 99.9), 1)
    dew_point = round(_safe_value(row, "temperatura_rocio_C", 99.9), 1)
    rh = round(_safe_value(row, "humedad_relativa_pct", 999), 0)
    pressure = round(_safe_value(row, "presion_superficial_Pa", 999999), 0)

    wind_speed = round(_safe_value(row, "velocidad_viento_10m_ms", 999), 1)
    wind_direction = round(_safe_value(row, "direccion_viento_10m_grados", 999), 0)

    ghi = round(_safe_value(row, "radiacion_solar_superficie_Wh_m2", 9999), 0)

    return [
        year, month, day, hour, minute,
        "?9?9?9?9",
        dry_bulb,
        dew_point,
        rh,
        pressure,
        9999,
        9999,
        9999,
        ghi,
        9999,
        9999,
        999999,
        999999,
        999999,
        9999,
        wind_direction,
        wind_speed,
        99,
        99,
        9999,
        99999,
        9,
        999999999,
        999,
        999,
        999,
        99,
        999,
        999,
        99,
    ]


def write_epw(weather_data: WeatherData, output_path, strict=False):
    df = weather_data.dataframe.copy()

    validate_weather_dataframe(df, strict=strict)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    header = build_epw_header(weather_data.metadata)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        for line in header:
            f.write(line + "\n")

        for _, row in df.iterrows():
            epw_row = _build_epw_row(row)
            f.write(",".join(map(str, epw_row)) + "\n")

    print(f"Archivo EPW generado: {output_path}")

    return output_path