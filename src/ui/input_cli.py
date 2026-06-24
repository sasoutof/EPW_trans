from src.constants import AVAILABLE_VARIABLES


def ask_float(message, example, min_value=None, max_value=None, optional=False):
    while True:
        value = input(f"{message} Ejemplo: {example}: ").strip().replace(",", ".")

        if optional and value == "":
            return None

        try:
            value = float(value)
        except ValueError:
            print("Valor no válido. Introduce un número.")
            continue

        if min_value is not None and value < min_value:
            print(f"El valor debe ser mayor o igual que {min_value}.")
            continue

        if max_value is not None and value > max_value:
            print(f"El valor debe ser menor o igual que {max_value}.")
            continue

        return value


def ask_int(message, example, min_value=None, max_value=None):
    while True:
        value = input(f"{message} Ejemplo: {example}: ").strip()

        try:
            value = int(value)
        except ValueError:
            print("Valor no válido. Introduce un número entero.")
            continue

        if min_value is not None and value < min_value:
            print(f"El valor debe ser mayor o igual que {min_value}.")
            continue

        if max_value is not None and value > max_value:
            print(f"El valor debe ser menor o igual que {max_value}.")
            continue

        return value


def ask_variables():
    print("\n====================================")
    print("VARIABLES DISPONIBLES")
    print("====================================")

    for key, data in AVAILABLE_VARIABLES.items():
        print(f"{key} - {data['name']} [{data['unit']}]")

    print("\nEjemplos:")
    print("  1,3       -> Temperatura seca y humedad relativa")
    print("  1,2,3,4   -> Temperatura seca, rocío, HR y presión")
    print("  1,3,4,5,7 -> Variables recomendadas para HVAC")

    while True:
        selection = input("\nSelección de variables: ").strip()

        selected_keys = [
            item.strip()
            for item in selection.split(",")
            if item.strip() != ""
        ]

        if not selected_keys:
            print("Debes seleccionar al menos una variable.")
            continue

        invalid = [key for key in selected_keys if key not in AVAILABLE_VARIABLES]

        if invalid:
            print(f"Selección no válida: {invalid}")
            continue

        selected_keys = list(dict.fromkeys(selected_keys))
        break

    era5_variables = []

    for key in selected_keys:
        variable = AVAILABLE_VARIABLES[key]

        if "requires" in variable:
            era5_variables.extend(variable["requires"])
        else:
            era5_name = variable["era5"]

            if isinstance(era5_name, list):
                era5_variables.extend(era5_name)
            elif era5_name is not None:
                era5_variables.append(era5_name)

    era5_variables = sorted(list(set(era5_variables)))

    return selected_keys, era5_variables


def get_user_input():
    print("\n====================================")
    print("CONFIGURACIÓN DEL ESTUDIO")
    print("====================================")
    print("1 - Introducir ciudad y coordenadas aproximadas")
    print("2 - Introducir coordenadas exactas")

    while True:
        mode = input("\nModo de entrada (1/2): ").strip()
        if mode in ["1", "2"]:
            break
        print("Opción no válida. Introduce 1 o 2.")

    if mode == "1":
        point_name = input("Ciudad o nombre del punto. Ejemplo: Murcia: ").strip()
        if point_name == "":
            point_name = "Punto_climatico"

        print("\nIntroduce coordenadas aproximadas.")
        print("Ejemplo Murcia: latitud 37.9922 / longitud -1.1307")

    else:
        point_name = input("Nombre identificativo del punto. Ejemplo: Murcia_Centro: ").strip()
        if point_name == "":
            point_name = "Punto_climatico"

        print("\nIntroduce coordenadas exactas.")
        print("Puedes obtenerlas desde Google Maps, QGIS o cualquier visor cartográfico.")

    lat = ask_float(
        "Latitud en grados decimales",
        "37.9922",
        min_value=-90,
        max_value=90,
    )

    lon = ask_float(
        "Longitud en grados decimales",
        "-1.1307",
        min_value=-180,
        max_value=180,
    )

    altitude = ask_float(
        "Altitud opcional en metros. Pulsa Enter si no quieres indicarla",
        "43",
        optional=True,
    )

    year_start = ask_int(
        "Año inicial",
        "2024",
        min_value=1940,
        max_value=2100,
    )

    year_end = ask_int(
        "Año final",
        "2025",
        min_value=1940,
        max_value=2100,
    )

    while year_end < year_start:
        print("El año final no puede ser menor que el año inicial.")
        year_end = ask_int(
            "Año final",
            str(year_start),
            min_value=1940,
            max_value=2100,
        )

    years = list(range(year_start, year_end + 1))

    selected_keys, era5_variables = ask_variables()

    print("\n====================================")
    print("RESUMEN DE LA CONFIGURACIÓN")
    print("====================================")
    print(f"Punto: {point_name}")
    print(f"Latitud: {lat}")
    print(f"Longitud: {lon}")
    print(f"Altitud: {altitude if altitude is not None else 'no especificada'}")
    print(f"Años: {years}")

    print("\nVariables de salida:")
    for key in selected_keys:
        print(f"  - {AVAILABLE_VARIABLES[key]['name']}")

    confirm = input("\n¿Los datos son correctos? (s/n): ").strip().lower()

    if confirm != "s":
        print("Proceso cancelado.")
        exit()

    return point_name, lat, lon, altitude, years, selected_keys, era5_variables