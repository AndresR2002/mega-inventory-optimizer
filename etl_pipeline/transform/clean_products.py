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


def get_new_product_id(existing_ids, start_id):
    """
    Genera un nuevo ID de producto que no esté presente en el conjunto de IDs existentes.

    :param existing_ids: Conjunto de IDs de producto ya existentes
    :param start_id: El valor inicial para el nuevo ID de producto
    :return: Un nuevo ID de producto único
    """
    new_id = start_id
    while new_id in existing_ids:
        new_id += 1
    return new_id


def clean_products_ids(df, existing_ids):
    """
    Limpia los valores de la columna 'producto_id' en el DataFrame, asegurando que sean enteros únicos.

    :param df: DataFrame que contiene los datos de productos
    :param existing_ids: Conjunto de IDs de producto ya existentes, para evitar duplicados
    :return: Tupla con el DataFrame limpio y el conjunto de IDs actualizado
    """
    new_ids = []

    for index, row in df.iterrows():
        product_id = row['producto_id']

        if not isinstance(product_id, (int, float)) or product_id != int(product_id):
            new_id = get_new_product_id(existing_ids, 1)
            existing_ids.add(int(new_id))
            new_ids.append(int(new_id))
        else:
            new_ids.append(int(product_id))
            existing_ids.add(int(product_id))

    df['producto_id'] = new_ids
    return df, existing_ids


def clean_names(df):
    """
    Limpia la columna 'nombre_producto' eliminando los espacios en blanco al inicio y final,
    y convirtiendo cada palabra a título (primera letra en mayúsculas).

    :param df: DataFrame que contiene los datos de productos
    :return: DataFrame con la columna 'nombre_producto' limpia y formateada correctamente
    """
    df['nombre_producto'] = df['nombre_producto'].str.strip().str.title()
    return df


def clean_categories(df):
    """
    Limpia la columna 'categoria' capitalizando correctamente cada palabra en la categoría.

    :param df: DataFrame que contiene los datos de categoría
    :return: DataFrame con la columna 'categoria' capitalizada correctamente
    """
    df['categoria'] = df['categoria'].apply(lambda x: ' '.join([word.capitalize() for word in str(x).split()]))
    return df


def clean_prices(df):
    """
    Limpia la columna 'precio_base', convirtiéndola a un número y reemplazando los valores no válidos por 0.
    Redondea los valores de precios a dos decimales.

    :param df: DataFrame que contiene los datos de precios
    :return: DataFrame con la columna 'precio_base' limpia y redondeada
    """
    df['precio_base'] = pd.to_numeric(df['precio_base'], errors='coerce')
    df['precio_base'].fillna(0, inplace=True)
    df['precio_base'] = df['precio_base'].apply(lambda x: round(x, 2) if isinstance(x, (int, float)) else 0)
    return df


def clean_duplicates(df):
    """
    Elimina las filas duplicadas basadas en la columna 'producto_id'.

    :param df: DataFrame que contiene los datos de productos
    :return: DataFrame sin las filas duplicadas basadas en 'producto_id'
    """
    return df.drop_duplicates(subset=['producto_id'])


def clean_products_data(ruta_entrada, ruta_salida):
    """
    Procesa el archivo de datos de productos, limpiando los valores nulos, ajustando IDs, nombres, categorías,
    precios y eliminando duplicados, luego guarda el DataFrame limpio en un archivo de salida.

    :param ruta_entrada: Ruta del archivo de entrada (CSV) con los datos de productos
    :param ruta_salida: Ruta del archivo de salida (CSV) donde se guardarán los datos limpios
    """
    df = load_data(ruta_entrada)

    existing_ids = set(df['producto_id'])

    df = clean_nulls(df)
    df, existing_ids = clean_products_ids(df, existing_ids)
    df = clean_names(df)
    df = clean_categories(df)
    df = clean_prices(df)
    df = clean_duplicates(df)

    save_data(df, ruta_salida)


if __name__ == "__main__":
    clean_products_data("data/productos.csv", "output/productos_limpios.csv")
