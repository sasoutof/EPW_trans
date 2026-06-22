import pandas as pd
import numpy as np


def quality_check(csv_file, year):
    df = pd.read_csv(csv_file)

    print(f"\nCONTROL DE CALIDAD {year}")
    print("============================")
    print(f"Número de registros: {len(df)}")

    print("\nValores nulos:")
    print(df.isna().sum())

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if numeric_cols:
        print("\nResumen estadístico:")
        print(df[numeric_cols].describe())