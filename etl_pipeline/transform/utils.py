import pandas as pd

def load_data(ruta):
    """
    Carga un archivo CSV en un DataFrame de pandas.

    :param ruta: Ruta del archivo CSV a cargar
    :return: DataFrame con los datos cargados desde el archivo CSV
    """
    return pd.read_csv(ruta)

def save_data(df, ruta_salida):
    """
    Guarda un DataFrame en un archivo CSV.

    :param df: DataFrame que contiene los datos a guardar
    :param ruta_salida: Ruta del archivo CSV donde se guardarán los datos
    """
    df.to_csv(ruta_salida, index=False)

def format_ids_in_csv(file_path, output_path, id_columns, length=10):
    """
    Formatea los IDs en un archivo CSV, agregando ceros a la izquierda hasta alcanzar el largo especificado.

    :param file_path: Ruta del archivo CSV de entrada
    :param output_path: Ruta del archivo CSV de salida con IDs formateados
    :param id_columns: Lista de nombres de columnas que contienen IDs a formatear
    :param length: Longitud deseada para los IDs (por defecto 10 caracteres)
    """
    df = pd.read_csv(file_path)

    for col in id_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.zfill(length)

    df.to_csv(output_path, index=False)


def replace_dates_with_time_id(df, time_df_path, date_column):
    """
    Reemplaza las fechas en el DataFrame con el ID de tiempo correspondiente.

    :param df: DataFrame de ventas o logística con una columna de fecha a transformar.
    :param time_df_path: Ruta del DataFrame con la relación fecha -> tiempo_id.
    :param date_column: Nombre de la columna que contiene la fecha en df ('fecha' o 'fecha_envio').
    :return: DataFrame con la columna de fecha reemplazada por 'tiempo_id'.
    """
    time_df = load_data(time_df_path)

    df[date_column] = pd.to_datetime(df[date_column], errors='coerce', format='%Y-%m-%d %H:%M:%S')
    time_df['fecha'] = pd.to_datetime(time_df['fecha'], errors='coerce', format='%Y-%m-%d')

    time_df['hora'] = pd.to_datetime(time_df['hora'], errors='coerce', format='%H:%M:%S').dt.time

    time_dict = {
        (row['fecha'].date(), row['hora']): row['tiempo_id']
        for _, row in time_df.iterrows()
    }

    def get_time_id(row):
        key = (row[date_column].date(), row[date_column].time().replace(second=0))
        time_id = time_dict.get(key, None)

        if time_id is None:
            print(f"⚠️ No se encontró tiempo_id para {key}")

        return time_id

    df['tiempo_id'] = df.apply(get_time_id, axis=1)

    df.dropna(subset=['tiempo_id'], inplace=True)

    df['tiempo_id'] = df['tiempo_id'].astype(int)

    df.drop(columns=[date_column], inplace=True)

    return df

