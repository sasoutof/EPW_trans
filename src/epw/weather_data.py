from dataclasses import dataclass
import pandas as pd

from src.epw.metadata import EPWMetadata


@dataclass
class WeatherData:
    metadata: EPWMetadata
    dataframe: pd.DataFrame

    @classmethod
    def from_csv(cls, csv_path, metadata: EPWMetadata):
        df = pd.read_csv(csv_path)
        return cls(metadata=metadata, dataframe=df)