from pathlib import Path

from src.constants import (
    PROJECT_NAME,
    DATASET,
    BASE_DIR,
    TIMEZONE,
    AVAILABLE_VARIABLES,
)

from src.ui.input_cli import get_user_input
from src.climate.era5_downloader import clean_name, download_era5_timeseries
from src.climate.processor import process_era5_csv
from src.climate.checks import quality_check

from src.epw.metadata import EPWMetadata
from src.epw.weather_data import WeatherData
from src.epw.writer import write_epw


def save_metadata(
    point_name,
    lat,
    lon,
    altitude,
    years,
    selected_keys,
    era5_variables,
    out_dir,
):
    metadata_file = out_dir / f"{clean_name(point_name)}_metadata.txt"

    with open(metadata_file, "w", encoding="utf-8") as f:
        f.write("METADATOS DEL ESTUDIO CLIMATOLÓGICO\n")
        f.write("===================================\n\n")
        f.write(f"Nombre del punto: {point_name}\n")
        f.write(f"Latitud: {lat}\n")
        f.write(f"Longitud: {lon}\n")

        if altitude is not None:
            f.write(f"Altitud indicada por el usuario: {altitude} m\n")
        else:
            f.write("Altitud indicada por el usuario: no especificada\n")

        f.write(f"Años descargados: {years}\n")
        f.write(f"Dataset: {DATASET}\n")
        f.write(f"Zona horaria local: {TIMEZONE}\n\n")

        f.write("Variables de salida seleccionadas:\n")
        for key in selected_keys:
            variable = AVAILABLE_VARIABLES[key]
            f.write(f"  - {variable['name']} [{variable['unit']}]\n")

        f.write("\nVariables solicitadas a ERA5:\n")
        for variable in era5_variables:
            f.write(f"  - {variable}\n")

        f.write("\nNotas:\n")
        f.write("- ERA5 Timeseries utiliza latitud y longitud para localizar el punto.\n")
        f.write("- La altitud se guarda como metadato, pero no se envía a ERA5.\n")
        f.write("- La humedad relativa se calcula a partir de temperatura seca y temperatura de rocío.\n")

    print(f"Metadatos guardados: {metadata_file}")


def ask_generate_epw():
    print("\n======================================")
    print("GENERACIÓN DE ARCHIVO EPW")
    print("======================================")
    answer = input("¿Quieres generar también archivo EPW? (s/n): ").strip().lower()
    return answer == "s"


def generate_epw_from_csv(
    csv_file,
    point_name,
    lat,
    lon,
    altitude,
    year,
):
    output_dir = Path("data") / "output" / clean_name(point_name)
    output_file = output_dir / f"{clean_name(point_name)}_{year}.epw"

    metadata = EPWMetadata(
        city=point_name,
        country="ESP",
        source="ERA5",
        latitude=lat,
        longitude=lon,
        timezone=1.0,
        elevation=altitude if altitude is not None else 0.0,
    )

    weather_data = WeatherData.from_csv(csv_file, metadata)

    write_epw(
        weather_data=weather_data,
        output_path=output_file,
        strict=False,
    )


def main():
    (
        point_name,
        lat,
        lon,
        altitude,
        years,
        selected_keys,
        era5_variables,
    ) = get_user_input()

    out_dir = BASE_DIR / PROJECT_NAME / clean_name(point_name)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("\n======================================")
    print(f"ERA5 TIMESERIES - {point_name}")
    print("======================================")
    print(f"Carpeta de salida: {out_dir}")

    save_metadata(
        point_name=point_name,
        lat=lat,
        lon=lon,
        altitude=altitude,
        years=years,
        selected_keys=selected_keys,
        era5_variables=era5_variables,
        out_dir=out_dir,
    )

    generate_epw = ask_generate_epw()

    for year in years:
        raw_csv = download_era5_timeseries(
            point_name=point_name,
            lat=lat,
            lon=lon,
            year=year,
            out_dir=out_dir,
            era5_variables=era5_variables,
        )

        final_csv = process_era5_csv(
            point_name=point_name,
            raw_csv=raw_csv,
            year=year,
            out_dir=out_dir,
            selected_keys=selected_keys,
        )

        quality_check(final_csv, year)

        if generate_epw:
            generate_epw_from_csv(
                csv_file=final_csv,
                point_name=point_name,
                lat=lat,
                lon=lon,
                altitude=altitude,
                year=year,
            )

    print("\nProceso finalizado correctamente.")