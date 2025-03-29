import pandas as pd
from .utils import load_data, save_data

def clean_nulls(df):
    """
    Elimina las filas que solo contienen valores nulos en todas las columnas.

    :param df: DataFrame que contiene los datos a limpiar
    :return: DataFrame después de eliminar las filas con valores nulos en todas las columnas
    """
    df.dropna(how='all', inplace=True)
    return df


def get_new_customer_id(existing_ids, start_id):
    """
    Genera un nuevo ID de cliente que no esté presente en el conjunto de IDs existentes.

    :param existing_ids: Conjunto de IDs de cliente ya existentes
    :param start_id: El valor inicial para el nuevo ID de cliente
    :return: Un nuevo ID de cliente único
    """
    new_id = start_id
    while new_id in existing_ids:
        new_id += 1
    return new_id


def clean_customer_ids(df, existing_ids):
    """
    Limpia los valores de la columna 'cliente_id' en el DataFrame, asegurando que sean enteros únicos.

    :param df: DataFrame que contiene los datos de los clientes
    :param existing_ids: Conjunto de IDs de cliente ya existentes, para evitar duplicados
    :return: Tupla con el DataFrame limpio y el conjunto de IDs actualizado
    """
    new_ids = []

    for index, row in df.iterrows():
        customer_id = row['cliente_id']

        if not isinstance(customer_id, (int, float)) or customer_id != int(customer_id):
            new_id = get_new_customer_id(existing_ids, 1)
            existing_ids.add(new_id)
            new_ids.append(new_id)
        else:
            new_ids.append(int(customer_id))
            existing_ids.add(int(customer_id))

    df['cliente_id'] = new_ids
    return df, existing_ids


def clean_ages(df):
    """
    Limpia y ajusta los valores de la columna 'edad' para asegurarse de que sean válidos.
    - Si la edad es mayor a 100, se limita a los dos primeros dígitos.
    - Convierte las edades no válidas a NaN y luego las reemplaza con 18 si están fuera del rango válido.

    :param df: DataFrame que contiene los datos de edad
    :return: DataFrame con la columna 'edad' limpia y ajustada
    """
    df['edad'] = df['edad'].apply(lambda x: str(x)[:2] if isinstance(x, (int, float)) and x > 100 else x)
    df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
    df['edad'] = df['edad'].apply(lambda x: x if 18 <= x <= 100 else 18)
    df['edad'] = df['edad'].astype(int)
    return df


def clean_genders(df):
    """
    Limpia y normaliza los valores de la columna 'genero', convirtiéndolos a mayúsculas
    y asignando los valores 'Masculino', 'Femenino' u 'Otro' dependiendo de la entrada.

    :param df: DataFrame que contiene los datos de género
    :return: DataFrame con la columna 'genero' normalizada
    """
    df['genero'] = df['genero'].str.upper()
    df['genero'] = df['genero'].apply(lambda x: 'Masculino' if x == 'M' else ('Femenino' if x == 'F' else 'Otro'))
    return df


def clean_locations(df):
    """
    Limpia la columna 'ubicacion' capitalizando correctamente cada palabra en la ubicación.

    :param df: DataFrame que contiene los datos de ubicación
    :return: DataFrame con la columna 'ubicacion' capitalizada correctamente
    """
    df['ubicacion'] = df['ubicacion'].apply(lambda x: ' '.join([word.capitalize() for word in str(x).split()]))
    return df


def clean_names(df):
    """
    Limpia la columna 'nombre' eliminando los espacios en blanco al inicio y final,
    y convirtiendo cada palabra a título (primera letra en mayúsculas).

    :param df: DataFrame que contiene los datos de nombres
    :return: DataFrame con la columna 'nombre' limpia y formateada correctamente
    """
    df['nombre'] = df['nombre'].str.strip().str.title()
    return df


def clean_duplicates(df):
    """
    Elimina las filas duplicadas basadas en la columna 'cliente_id'.

    :param df: DataFrame que contiene los datos de clientes
    :return: DataFrame sin las filas duplicadas basadas en 'cliente_id'
    """
    return df.drop_duplicates(subset=['cliente_id'])


def clean_customers_data(input_path, output_path):
    """
    Procesa el archivo de datos de clientes, limpiando los valores nulos, ajustando IDs, edades, géneros, ubicaciones,
    nombres y eliminando duplicados, luego guarda el DataFrame limpio en un archivo de salida.

    :param input_path: Ruta del archivo de entrada (CSV) con los datos de clientes
    :param output_path: Ruta del archivo de salida (CSV) donde se guardarán los datos limpios
    """
    df = load_data(input_path)

    existing_ids = set(df['cliente_id'])

    df = clean_nulls(df)
    df, existing_ids = clean_customer_ids(df, existing_ids)
    df = clean_ages(df)
    df = clean_genders(df)
    df = clean_locations(df)
    df = clean_names(df)
    df = clean_duplicates(df)

    save_data(df, output_path)

if __name__ == "__main__":
    clean_customers_data("data/clientes.csv", "output/clientes_limpios.csv")
