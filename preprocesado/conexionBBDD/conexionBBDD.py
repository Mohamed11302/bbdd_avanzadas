import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
from urllib.parse import urlparse
import os
import conexionBBDD.constantesBBDD as const
def verificar_conexion(url):
    try:
        # Parsea la URL de conexión
        url_parsed = urlparse(url)

        # Extrae los componentes de la URL
        usuario = url_parsed.username
        contrasena = url_parsed.password
        host = url_parsed.hostname
        puerto = url_parsed.port
        base_datos = url_parsed.path.lstrip('/')

        # Intenta establecer una conexión
        with psycopg2.connect(
            user=usuario,
            password=contrasena,
            host=host,
            port=puerto,
            database=base_datos,
            sslmode='require'
        ) as conn:
            # La conexión fue exitosa
            return conn
    except Exception as e:
        print(f'Error al conectar a la base de datos: {str(e)}')
        return None

def create_schema(conexion, nombre_esquema):
    try:
        # Crear un cursor para ejecutar comandos SQL
        with conexion.cursor() as cursor:
            # Verificar si el esquema existe
            cursor.execute(sql.SQL("SELECT 1 FROM pg_namespace WHERE nspname = %s;"), (nombre_esquema,))
            existe_esquema = cursor.fetchone()

            if not existe_esquema:
                # Si el esquema no existe, crearlo
                cursor.execute(sql.SQL("CREATE SCHEMA {};").format(sql.Identifier(nombre_esquema)))
                print(f"Esquema '{nombre_esquema}' creado correctamente.")
            else:
                print(f"El esquema '{nombre_esquema}' ya existe.")

        # Confirmar los cambios en la base de datos
        conexion.commit()

    except psycopg2.Error as e:
        print(f"Error al crear el esquema: {e}")




def guardar_df_en_tabla(df, nombre_tabla, nombre_esquema, conexion_str):
    try:
        engine = create_engine(conexion_str)
        df.to_sql(name=nombre_tabla, con=engine, schema=nombre_esquema, if_exists='replace', index=False)

        print(f"DataFrame guardado en la tabla '{nombre_esquema}.{nombre_tabla}' correctamente.")

    except Exception as e:
        print(f"Error al guardar el DataFrame en la tabla: {e}")

def crear_conexion():
    url_db = os.getenv(const.BBDD_URL)
    conn = verificar_conexion(url_db)
    return conn


