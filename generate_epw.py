from pathlib import Path

from src.epw.metadata import EPWMetadata
from src.epw.weather_data import WeatherData
from src.epw.writer import write_epw


csv_file = Path.home() / "Documentos" / "CDS" / "ESTUDIO_CLIMATICO" / "Murcia" / "Murcia_serie_climatologica_2024.csv"

output_file = Path("data/output/Murcia_2024.epw")

metadata = EPWMetadata(
    city="Murcia",
    country="ESP",
    source="ERA5",
    latitude=37.9922,
    longitude=-1.1307,
    timezone=1.0,
    elevation=43,
)

weather_data = WeatherData.from_csv(csv_file, metadata)

write_epw(weather_data, output_file)