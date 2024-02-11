import bronze.bronze as bronze
import conexionBBDD.conexionBBDD as conBBDD
import os


if __name__ == "__main__":
    conn = conBBDD.crear_conexion()
    bronze.create_bronze_schema(conn)