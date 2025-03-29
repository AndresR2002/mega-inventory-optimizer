from .utils import load_data, save_data
import re

def clean_nulls(df):
    """
    Elimina las filas que solo contienen valores nulos en todas las columnas.

    :param df: DataFrame que contiene los datos a limpiar
    :return: DataFrame después de eliminar las filas con valores nulos en todas las columnas
    """
    df.dropna(how='all', inplace=True)
    return df


def get_new_supplier_id(existing_ids, start_id):
    """
    Genera un nuevo ID de proveedor que no esté presente en el conjunto de IDs existentes.

    :param existing_ids: Conjunto de IDs de proveedor ya existentes
    :param start_id: El valor inicial para el nuevo ID de proveedor
    :return: Un nuevo ID de proveedor único
    """
    new_id = start_id
    while new_id in existing_ids:
        new_id += 1
    return new_id


def clean_suppliers_ids(df, existing_ids):
    """
    Limpia los valores de la columna 'proveedor_id' en el DataFrame, asegurando que sean enteros únicos.

    :param df: DataFrame que contiene los datos de proveedores
    :param existing_ids: Conjunto de IDs de proveedor ya existentes, para evitar duplicados
    :return: Tupla con el DataFrame limpio y el conjunto de IDs actualizado
    """
    new_ids = []

    for index, row in df.iterrows():
        supplier_id = row['proveedor_id']

        if not isinstance(supplier_id, (int, float)) or supplier_id != int(supplier_id):
            new_id = get_new_supplier_id(existing_ids, 1)
            existing_ids.add(new_id)
            new_ids.append(new_id)
        else:
            new_ids.append(int(supplier_id))
            existing_ids.add(int(supplier_id))

    df['proveedor_id'] = new_ids
    return df, existing_ids


def clean_names(df):
    """
    Limpia la columna 'nombre_proveedor' eliminando los espacios en blanco al inicio y final,
    y convirtiendo cada palabra a título (primera letra en mayúsculas).

    :param df: DataFrame que contiene los datos de proveedores
    :return: DataFrame con la columna 'nombre_proveedor' limpia y formateada correctamente
    """
    df['nombre_proveedor'] = df['nombre_proveedor'].str.strip().str.title()
    return df


def clean_emails(df):
    """
    Limpia la columna 'contacto' asegurando que contenga un correo electrónico válido.
    Si no es válido, reemplaza el valor por 'contacto@desconocido.com'.

    :param df: DataFrame que contiene los datos de proveedores
    :return: DataFrame con la columna 'contacto' validada
    """
    def is_valid_email(email):
        """
        Verifica si un correo electrónico es válido utilizando una expresión regular.

        :param email: Cadena de texto con el correo electrónico
        :return: True si el correo es válido, False en caso contrario
        """
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    df['contacto'] = df['contacto'].apply(lambda x: x if is_valid_email(x) else 'contacto@desconocido.com')
    return df


def clean_locations(df):
    """
    Limpia la columna 'ubicacion' capitalizando correctamente cada palabra de la ubicación.

    :param df: DataFrame que contiene los datos de ubicación
    :return: DataFrame con la columna 'ubicacion' capitalizada correctamente
    """
    df['ubicacion'] = df['ubicacion'].apply(lambda x: ' '.join([word.capitalize() for word in str(x).split()]))
    return df


def clean_duplicates(df):
    """
    Elimina las filas duplicadas basadas en la columna 'proveedor_id'.

    :param df: DataFrame que contiene los datos de proveedores
    :return: DataFrame sin las filas duplicadas basadas en 'proveedor_id'
    """
    return df.drop_duplicates(subset=['proveedor_id'])


def clean_suppliers_data(ruta_entrada, ruta_salida):
    """
    Procesa el archivo de datos de proveedores, limpiando los valores nulos, ajustando IDs, nombres,
    correos electrónicos, ubicaciones y eliminando duplicados, luego guarda el DataFrame limpio en un archivo de salida.

    :param ruta_entrada: Ruta del archivo de entrada (CSV) con los datos de proveedores
    :param ruta_salida: Ruta del archivo de salida (CSV) donde se guardarán los datos limpios
    """
    df = load_data(ruta_entrada)

    existing_ids = set(df['proveedor_id'])

    df = clean_nulls(df)
    df, existing_ids = clean_suppliers_ids(df, existing_ids)
    df = clean_names(df)
    df = clean_locations(df)
    df = clean_emails(df)
    df = clean_duplicates(df)

    save_data(df, ruta_salida)


if __name__ == "__main__":
    clean_suppliers_data("data/proveedores.csv", "output/proveedores_limpios.csv")
