REQUIRED_COLUMNS = [
    "fecha_hora_local",
    "temperatura_seca_C",
    "temperatura_rocio_C",
    "humedad_relativa_pct",
]

RECOMMENDED_COLUMNS = [
    "presion_superficial_Pa",
    "velocidad_viento_10m_ms",
]


def validate_weather_dataframe(df, strict=False):
    missing_required = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_required:
        raise ValueError(
            "Faltan columnas obligatorias para generar el EPW: "
            + ", ".join(missing_required)
        )

    missing_recommended = [col for col in RECOMMENDED_COLUMNS if col not in df.columns]

    if missing_recommended:
        print("\nAviso: faltan columnas recomendadas para un EPW completo:")
        for col in missing_recommended:
            print(f"  - {col}")

        print("Se usarán valores por defecto en esas columnas.")

        if strict:
            raise ValueError(
                "Faltan columnas recomendadas para generar el EPW en modo estricto: "
                + ", ".join(missing_recommended)
            )

    if df.empty:
        raise ValueError("El DataFrame climático está vacío.")

    return True