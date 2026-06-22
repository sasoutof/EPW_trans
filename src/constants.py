from pathlib import Path

PROJECT_NAME = "ESTUDIO_CLIMATICO"
DATASET = "reanalysis-era5-single-levels-timeseries"
BASE_DIR = Path.home() / "Documentos" / "CDS"
TIMEZONE = "Europe/Madrid"

AVAILABLE_VARIABLES = {
    "1": {
        "name": "Temperatura seca 2 m",
        "era5": "2m_temperature",
        "unit": "ºC",
    },
    "2": {
        "name": "Temperatura de rocío 2 m",
        "era5": "2m_dewpoint_temperature",
        "unit": "ºC",
    },
    "3": {
        "name": "Humedad relativa calculada",
        "era5": None,
        "unit": "%",
        "requires": ["2m_temperature", "2m_dewpoint_temperature"],
    },
    "4": {
        "name": "Presión superficial",
        "era5": "surface_pressure",
        "unit": "Pa / hPa",
    },
    "5": {
        "name": "Viento 10 m",
        "era5": [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
        ],
        "unit": "m/s",
    },
    "6": {
        "name": "Precipitación total",
        "era5": "total_precipitation",
        "unit": "m / mm",
    },
    "7": {
        "name": "Radiación solar superficial descendente",
        "era5": "surface_solar_radiation_downwards",
        "unit": "J/m² / Wh/m²",
    },
}