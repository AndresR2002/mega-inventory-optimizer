import pandas as pd
from .utils import load_data, save_data, replace_dates_with_time_id

def clean_nulls(df):
    """
    Elimina las filas que solo contienen valores nulos en todas las columnas.

    :param df: DataFrame que contiene los datos a limpiar
    :return: DataFrame después de eliminar las filas con valores nulos en todas las columnas
    """
    df.dropna(how='all', inplace=True)
    return df


def clean_dates(df):
    """
    Convierte la columna 'fecha' al formato de fecha y hora y elimina los valores nulos.

    :param df: DataFrame que contiene los datos de ventas
    :return: DataFrame con la columna 'fecha' limpia y convertida al formato adecuado
    """
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce', format='%Y-%m-%d %H:%M:%S')
    df.dropna(subset=['fecha'], inplace=True)
    df['fecha'] = df['fecha'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return df


def validate_product_id(df, products_dict):
    """
    Valida los IDs de productos en el DataFrame comparándolos con un diccionario de productos.
    Si el ID no es válido, se intenta encontrar un producto con el mismo precio unitario.

    :param df: DataFrame que contiene los datos de ventas
    :param products_dict: Diccionario con los IDs de productos como claves y los precios como valores
    :return: DataFrame con la columna 'producto_id' validada
    """
    def correct_product(row):
        product_id = row['producto_id']
        unit_price = row['precio_unitario']

        if product_id in products_dict:
            return int(product_id)

        unit_price_int = int(unit_price)
        possible = [p_id for p_id, p_price in products_dict.items() if int(p_price) == unit_price_int]

        return possible[0] if possible else None

    df['producto_id'] = df.apply(correct_product, axis=1)
    df.dropna(subset=['producto_id'], inplace=True)

    df['producto_id'] = df['producto_id'].astype(int)

    return df


def validate_customers_ids(df, existing_customers_ids):
    """
    Valida los IDs de los clientes asegurando que existan en el conjunto de clientes válidos.

    :param df: DataFrame que contiene los datos de ventas
    :param existing_customers_ids: Conjunto de IDs de clientes válidos
    :return: DataFrame con los IDs de clientes validados
    """
    valid_customer_ids = []

    for index, row in df.iterrows():
        customer_id = row['cliente_id']

        customer_id = int(customer_id) if isinstance(customer_id, (int, float)) and customer_id == int(
            customer_id) else None

        if customer_id is not None and customer_id in existing_customers_ids:
            valid_customer_ids.append(int(customer_id))

    df = df[df['cliente_id'].isin(valid_customer_ids)].copy()

    df.loc[:, 'cliente_id'] = df['cliente_id'].astype(int)

    return df


def convert_branch_id(df):
    """
    Convierte la columna 'sucursal_id' a tipo entero.

    :param df: DataFrame que contiene los datos de ventas
    :return: DataFrame con la columna 'sucursal_id' convertida a tipo entero
    """
    df['sucursal_id'] = df['sucursal_id'].astype(int)
    return df


def clean_totals(df):
    """
    Limpia y calcula los totales en la venta. Asegura que 'cantidad' y 'precio_unitario' sean números y calcula 'total'.

    :param df: DataFrame que contiene los datos de ventas
    :return: DataFrame con las columnas 'cantidad', 'precio_unitario' y 'total' limpiadas y calculadas
    """
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce').fillna(0).astype(int)

    df['total'] = df['cantidad'] * df['precio_unitario']
    df['total'] = df['total'].round(2)

    df = df[df['total'].round(2) == df['total']]

    df['precio_unitario'] = df['precio_unitario'].round(2)
    df['total'] = df['total'].round(2)

    return df


def get_new_sale_id(existing_ids, start_id=1):
    """
    Genera un nuevo ID de venta que no esté presente en el conjunto de IDs existentes.

    :param existing_ids: Conjunto de IDs de ventas ya existentes
    :param start_id: El valor inicial para el nuevo ID de venta
    :return: Un nuevo ID de venta único
    """
    new_id = start_id
    while new_id in existing_ids:
        new_id += 1
    return new_id


def validate_sales_ids(df):
    """
    Valida los IDs de venta en el DataFrame. Si el ID no es válido, genera un nuevo ID único.

    :param df: DataFrame que contiene los datos de ventas
    :return: DataFrame con los IDs de venta validados o generados
    """
    existing_ids = set(df['venta_id'])
    new_ids = []

    for index, row in df.iterrows():
        sale_id = row['venta_id']

        if not isinstance(sale_id, (int, float)) or sale_id != int(sale_id):
            new_id = get_new_sale_id(existing_ids)
            existing_ids.add(new_id)
            new_ids.append(new_id)
        else:
            new_ids.append(int(sale_id))

    df['venta_id'] = new_ids
    return df


def clean_sales_data(sales_path, products_path, customers_path, time_path, output_path):
    """
    Limpia los datos de ventas, productos y clientes, y guarda el DataFrame limpio en un archivo de salida.

    :param sales_path: Ruta del archivo CSV con los datos de ventas
    :param products_path: Ruta del archivo CSV con los datos de productos
    :param customers_path: Ruta del archivo CSV con los datos de clientes
    :param time_path: Ruta del archivo CSV con los datos de tiempo
    :param output_path: Ruta del archivo CSV donde se guardarán los datos limpios
    """
    sales = load_data(sales_path)
    products = load_data(products_path)
    customers = load_data(customers_path)

    products_dict = products.set_index('producto_id')['precio_base'].to_dict()
    valid_customers = set(customers['cliente_id'])

    sales = clean_nulls(sales)
    sales = validate_sales_ids(sales)
    sales = clean_dates(sales)
    sales = validate_product_id(sales, products_dict)
    sales = validate_customers_ids(sales, valid_customers)
    sales = convert_branch_id(sales)
    sales = clean_totals(sales)
    sales = replace_dates_with_time_id(sales, time_path, 'fecha')

    save_data(sales, output_path)


if __name__ == "__main__":
    clean_sales_data("data/ventas.csv", "data/productos.csv", "data/clientes.csv", "output/ventas_limpias.csv")
