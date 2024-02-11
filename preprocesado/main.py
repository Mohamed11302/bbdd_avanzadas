import preprocesado.bronze as bronze
import preprocesado.silver as silver
import conexionBBDD.conexionBBDD as conBBDD


if __name__ == "__main__":
    conn_str = conBBDD.get_bbdd_url()
    #bronze.create_bronze_schema(conn_str)
    silver.preprocess_silver_scheme(conn_str)