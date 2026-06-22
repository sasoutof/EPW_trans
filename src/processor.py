import pandas as pd
import numpy as np

from src.constants import AVAILABLE_VARIABLES, TIMEZONE
from src.era5_downloader import clean_name


def saturation_vapour_pressure(temp_c):
    return 6.112 * np.exp((17.67 * temp_c) / (temp_c + 243.5))


def relative_humidity_from_t_td(t_c, td_c):
    e = saturation_vapour_pressure(td_c)
    es = saturation_vapour_pressure(t_c)
    return np.clip(100 * e / es, 0, 100)


def detect_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col

    raise ValueError(f"No se encontró ninguna columna válida entre: {candidates}")


def find_column_by_era5_name(df, era5_name):
    candidates = [
        era5_name,
        era5_name.replace("2m_temperature", "t2m"),
        era5_name.replace("2m_dewpoint_temperature", "d2m"),
        era5_name.replace("surface_pressure", "sp"),
        era5_name.replace("10m_u_component_of_wind", "u10"),
        era5_name.replace("10m_v_component_of_wind", "v10"),
        era5_name.replace("total_precipitation", "tp"),
        era5_name.replace("surface_solar_radiation_downwards", "ssrd"),
    ]

    return detect_column(df, candidates)


def add_variable_to_result(result, df, key):
    if key == "1":
        col = find_column_by_era5_name(df, "2m_temperature")
        result["temperatura_seca_C"] = df[col] - 273.15

    elif key == "2":
        col = find_column_by_era5_name(df, "2m_dewpoint_temperature")
        result["temperatura_rocio_C"] = df[col] - 273.15

    elif key == "3":
        temp_col = find_column_by_era5_name(df, "2m_temperature")
        dew_col = find_column_by_era5_name(df, "2m_dewpoint_temperature")

        temp_c = df[temp_col] - 273.15
        dew_c = df[dew_col] - 273.15

        result["humedad_relativa_pct"] = relative_humidity_from_t_td(temp_c, dew_c)

    elif key == "4":
        col = find_column_by_era5_name(df, "surface_pressure")
        result["presion_superficial_Pa"] = df[col]
        result["presion_superficial_hPa"] = df[col] / 100

    elif key == "5":
        u_col = find_column_by_era5_name(df, "10m_u_component_of_wind")
        v_col = find_column_by_era5_name(df, "10m_v_component_of_wind")

        result["viento_u_10m_ms"] = df[u_col]
        result["viento_v_10m_ms"] = df[v_col]
        result["velocidad_viento_10m_ms"] = np.sqrt(df[u_col] ** 2 + df[v_col] ** 2)

    elif key == "6":
        col = find_column_by_era5_name(df, "total_precipitation")
        result["precipitacion_total_m"] = df[col]
        result["precipitacion_total_mm"] = df[col] * 1000

    elif key == "7":
        col = find_column_by_era5_name(df, "surface_solar_radiation_downwards")
        result["radiacion_solar_superficie_J_m2"] = df[col]
        result["radiacion_solar_superficie_Wh_m2"] = df[col] / 3600

    else:
        variable = AVAILABLE_VARIABLES.get(key)
        raise ValueError(f"Variable no procesada: {variable}")

    return result


def process_era5_csv(point_name, raw_csv, year, out_dir, selected_keys):
    point_clean = clean_name(point_name)

    print(f"Procesando {raw_csv}...")

    df = pd.read_csv(raw_csv)

    print("Columnas detectadas:")
    print(df.columns.tolist())

    time_col = detect_column(df, ["valid_time", "time", "date", "datetime"])

    result = pd.DataFrame()
    result["fecha_hora_UTC"] = pd.to_datetime(df[time_col], utc=True)
    result["fecha_hora_local"] = result["fecha_hora_UTC"].dt.tz_convert(TIMEZONE)

    for key in selected_keys:
        result = add_variable_to_result(result, df, key)

    for col in result.columns:
        if col not in ["fecha_hora_UTC", "fecha_hora_local"]:
            result[col] = result[col].round(3)

    final_csv = out_dir / f"{point_clean}_serie_climatologica_{year}.csv"
    result.to_csv(final_csv, index=False, encoding="utf-8-sig")

    print(f"CSV final generado: {final_csv}")

    return final_csv