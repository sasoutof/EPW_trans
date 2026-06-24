import zipfile
import cdsapi

from src.constants import DATASET


def clean_name(text):
    return text.strip().replace(" ", "_")


def make_variable_tag(era5_variables):
    return "_".join(
        [
            v.replace("2m_", "")
            .replace("10m_", "")
            .replace("_component_of_wind", "")
            .replace("_", "")
            for v in era5_variables
        ]
    )


def download_era5_timeseries(point_name, lat, lon, year, out_dir, era5_variables):
    point_clean = clean_name(point_name)
    variable_tag = make_variable_tag(era5_variables)

    zip_file = out_dir / f"{point_clean}_ERA5_timeseries_{year}_{variable_tag}.zip"
    raw_csv = out_dir / f"{point_clean}_ERA5_timeseries_{year}_{variable_tag}_raw.csv"

    if raw_csv.exists():
        print(f"CSV bruto ya existe: {raw_csv}")
        return raw_csv

    request = {
        "variable": era5_variables,
        "date": [f"{year}-01-01/{year}-12-31"],
        "location": {
            "latitude": lat,
            "longitude": lon,
        },
        "data_format": "csv",
    }

    print(f"\nDescargando {point_name} - {year}...")

    client = cdsapi.Client()
    client.retrieve(DATASET, request).download(str(zip_file))

    print(f"ZIP descargado: {zip_file}")

    with zipfile.ZipFile(zip_file, "r") as z:
        csv_files = [name for name in z.namelist() if name.endswith(".csv")]

        if not csv_files:
            raise ValueError("No se encontró ningún CSV dentro del ZIP.")

        extracted_name = csv_files[0]
        z.extract(extracted_name, out_dir)

        extracted_path = out_dir / extracted_name

        if raw_csv.exists():
            raw_csv.unlink()

        extracted_path.rename(raw_csv)

    print(f"CSV extraído: {raw_csv}")

    return raw_csv