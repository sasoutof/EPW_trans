from dataclasses import dataclass


@dataclass
class EPWMetadata:
    city: str
    country: str = "ESP"
    source: str = "ERA5"
    latitude: float = 0.0
    longitude: float = 0.0
    timezone: float = 1.0
    elevation: float = 0.0