from src.constants import (
    PROJECT_NAME,
    DATASET,
    BASE_DIR,
    TIMEZONE,
    AVAILABLE_VARIABLES,
)

from src.input_cli import get_user_input
from src.era5_downloader import clean_name, download_era5_timeseries
from src.processor import process_era5_csv
from src.checks import quality_check


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

    print("\nProceso finalizado correctamente.")