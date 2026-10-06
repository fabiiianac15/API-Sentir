import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()


def obtener_conexion():
    """Abre una conexión a PostgreSQL. Las filas se devuelven como diccionarios."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        cursor_factory=RealDictCursor,
    )


def get_db():
    """Dependencia de FastAPI: abre la conexión y SIEMPRE la cierra al terminar."""
    conexion = obtener_conexion()
    try:
        yield conexion
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


# Prueba manual: python con_db.py
if __name__ == "__main__":
    conn = obtener_conexion()
    print("Conexión exitosa a la base de datos")
    conn.close()
