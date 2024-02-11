import conexionBBDD.conexionBBDD as conBBDD
import conexionBBDD.constantesBBDD as const
import pandas as pd

def create_bronze_schema(conn):
    #conBBDD.create_schema(conn, 'bronze')
    df = pd.read_csv(const.YT_CHANNELS)
    print(df)
    