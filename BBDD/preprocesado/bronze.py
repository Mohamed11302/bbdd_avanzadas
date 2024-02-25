import BBDD.conexionBBDD.conexionBBDD as conBBDD
import BBDD.conexionBBDD.constantesBBDD as const
import pandas as pd

def create_bronze_schema(conn_str):
    df_channels = pd.read_csv(const.YT_CHANNELS)
    df_videos = pd.read_csv(const.YT_VIDEOS)

    conBBDD.guardar_df_en_tabla(df_channels, 'channel', 'bronze', conn_str)
    conBBDD.guardar_df_en_tabla(df_videos, 'video', 'bronze', conn_str)
