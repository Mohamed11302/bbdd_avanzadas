import youtube_data.main as extraer_data
import BBDD.main as transformacion_y_carga
import BBDD.consultas.consultas as consultas


if __name__ == "__main__":
    extraer_data.extraer_data()
    print("Extraccion de datos de youtube completada")
    transformacion_y_carga.transformacion_y_carga()
    print("Transformación y carga completada")
    consultas.consultas()
    print("Consultas completadas")
