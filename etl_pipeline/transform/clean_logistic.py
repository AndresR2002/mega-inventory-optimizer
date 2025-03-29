import pandas as pd
from .utils import load_data, save_data, replace_dates_with_time_id


def clean_nulls(df):
    """
    Elimina las filas que están completamente vacías (sin ningún valor).

    :param df: DataFrame que contiene los datos a limpiar
    :return: DataFrame con las filas vacías eliminadas
    """
    return df.dropna(how='all')


def clean_dates(df):
    """
    Convierte la columna 'fecha_envio' a formato datetime y elimina las filas con fechas inválidas.

    :param df: DataFrame que contiene los datos a limpiar
    :return: DataFrame con fechas válidas y filas con fechas inválidas eliminadas
    """
    df['fecha_envio'] = pd.to_datetime(df['fecha_envio'], errors='coerce')
    return df.dropna(subset=['fecha_envio'])


def clean_state(df):
    """
    Filtra las filas para mantener solo aquellos estados de envío válidos.

    :param df: DataFrame que contiene los datos a limpiar
    :return: DataFrame con los estados de envío válidos ('Retrasado', 'Entregado', 'En tránsito', 'Cancelado')
    """
    valid_status = {'Retrasado', 'Entregado', 'En tránsito', 'Cancelado'}
    return df[df['estado_envio'].isin(valid_status)]


def convert_to_int(value):
    """
    Convierte un valor a entero si es posible. Si el valor no puede convertirse, devuelve None.

    :param value: Valor que se va a convertir a entero
    :return: Entero si es posible, de lo contrario None
    """
    try:
        value = float(value)
        if value.is_integer():
            return int(value)
        else:
            return None
    except (ValueError, TypeError):
        return None


def get_new_logistic_id(existing_ids, start_id=1):
    """
    Genera un nuevo ID único para la logística que no esté presente en los IDs existentes.

    :param existing_ids: Conjunto de IDs existentes
    :param start_id: ID de inicio para la generación
    :return: Un nuevo ID único
    """
    while start_id in existing_ids:
        start_id += 1
    existing_ids.add(start_id)
    return start_id


def validate_logistic_ids(df):
    """
    Valida y corrige los IDs de logística, generando un nuevo ID cuando sea necesario.

    :param df: DataFrame que contiene los datos de logística
    :return: DataFrame con los IDs de logística validados
    """
    existing_ids = set(df['envio_id'].dropna().astype(int))
    df['envio_id'] = df['envio_id'].apply(lambda x: convert_to_int(x) or get_new_logistic_id(existing_ids))
    return df


def validate_sales_id(df, existing_sales_ids):
    """
    Valida los IDs de ventas, eliminando los inválidos y reseteando el índice.

    :param df: DataFrame que contiene los datos de ventas
    :param existing_sales_ids: Conjunto de IDs de ventas válidos
    :return: DataFrame con los IDs de ventas validados y con el índice reseteado
    """
    df['venta_id'] = df['venta_id'].fillna(0).astype(int)
    df = df[df['venta_id'].isin(existing_sales_ids)].copy()
    df['venta_id'] = df['venta_id'].astype(str)
    df.reset_index(drop=True, inplace=True)
    return df


def validate_suppliers_ids(df, existing_supplier_ids):
    """
    Valida los IDs de proveedores, eliminando los inválidos y reseteando el índice.

    :param df: DataFrame que contiene los datos de proveedores
    :param existing_supplier_ids: Conjunto de IDs de proveedores válidos
    :return: DataFrame con los IDs de proveedores validados y con el índice reseteado
    """
    df['proveedor_id'] = df['proveedor_id'].fillna(0).astype(int)
    df = df[df['proveedor_id'].isin(existing_supplier_ids)].copy()
    df['proveedor_id'] = df['proveedor_id'].astype(str)
    df.reset_index(drop=True, inplace=True)
    return df


def clean_logistics_data(input_path, sales_path, providers_path, time_path, output_path):
    """
    Carga los datos logísticos, realiza el proceso de limpieza y guarda los datos limpios en un archivo de salida.

    :param input_path: Ruta del archivo CSV con los datos logísticos
    :param sales_path: Ruta del archivo CSV con los datos de ventas
    :param providers_path: Ruta del archivo CSV con los datos de proveedores
    :param time_path: Ruta del archivo CSV con los datos de tiempo
    :param output_path: Ruta del archivo CSV donde se guardarán los datos limpios
    """
    df = load_data(input_path)
    sales_df = load_data(sales_path)
    suppliers_df = load_data(providers_path)

    valid_sales_ids = set(sales_df['venta_id'].dropna().astype(int))
    valid_suppliers_ids = set(suppliers_df['proveedor_id'].dropna().astype(int))

    df = validate_logistic_ids(df)
    df = validate_sales_id(df, valid_sales_ids)
    df = validate_suppliers_ids(df, valid_suppliers_ids)

    df = clean_nulls(df)
    df = clean_dates(df)
    df = clean_state(df)

    df = replace_dates_with_time_id(df, time_path, 'fecha_envio')

    save_data(df, output_path)


if __name__ == "__main__":
    clean_logistics_data("data/logistica.csv", "output/ventas_limpias.csv", "data/proveedores.csv",
                         "output/logistica_limpia.csv")
