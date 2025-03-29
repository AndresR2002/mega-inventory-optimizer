import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

db_url = os.getenv("DATABASE_URL")

def load_csv_to_postgresql(csv_file_path, table_name, if_exists='append', id_columns=None):
    """
    Carga un archivo CSV en una tabla de PostgreSQL.

    :param csv_file_path: Ruta del archivo CSV a cargar.
    :param table_name: Nombre de la tabla de destino en la base de datos.
    :param if_exists: Comportamiento si la tabla ya existe. Puede ser 'append', 'replace', o 'fail'.
    :param id_columns: Lista de columnas de IDs que deben ser tratadas como cadenas.
    """
    dtype = {col: str for col in id_columns} if id_columns else {}

    df = pd.read_csv(csv_file_path, dtype=dtype)

    engine = create_engine(db_url)

    df.to_sql(table_name, engine, if_exists=if_exists, index=False)

    print(f"✅ Datos cargados en la tabla '{table_name}' desde {csv_file_path}")

def execute_sql_from_file(sql_file_path):
    with open(sql_file_path, 'r') as sql_file:
        sql_commands = sql_file.read()

    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()

    try:
        cursor.execute(sql_commands)
        connection.commit()
        print(f"✅ Ejecutado {sql_file_path} con éxito")
    except Exception as e:
        print(f"❌ Error al ejecutar el archivo SQL '{sql_file_path}': {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
