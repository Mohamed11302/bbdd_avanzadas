import preprocesado.bronze as bronze
import preprocesado.silver as silver
import diseno.gold as gold
import conexionBBDD.conexionBBDD as conBBDD
if __name__ == "__main__":
    conn_str = conBBDD.get_bbdd_url()
    test_conexion = conBBDD.verificar_conexion(conn_str)
    if test_conexion != None:
        print("Conexion establecida con el servidor")
    #bronze.create_bronze_schema(conn_str)
    #silver.preprocess_silver_scheme(conn_str)
    gold.diseno_gold(conn_str)

