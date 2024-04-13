from crear_tablas import crear_bbdd
from insertar_datos import insertar_datos

def main():
    path_db = 'fondos.db'
    crear_bbdd(path_db)  
    insertar_datos(path_db)

    print("Proceso completado con éxito!")

if __name__ == '__main__':
    main()