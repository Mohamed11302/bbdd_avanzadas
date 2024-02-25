import BBDD.preprocesado.bronze as bronze
import BBDD.preprocesado.silver as silver
import BBDD.diseno.gold as gold
import BBDD.consultas.consultas as consultas
import BBDD.conexionBBDD.conexionBBDD as conBBDD


def transformacion_y_carga():
    print("Transformacion y carga")
    conn_str = conBBDD.get_bbdd_url()
    #bronze.create_bronze_schema(conn_str)
    #silver.preprocess_silver_scheme(conn_str)
    #gold.diseno_gold(conn_str)

if __name__ == "__main__":
    transformacion_y_carga()
    conn_str = conBBDD.get_bbdd_url()
    consultas.consultas(conn_str)

