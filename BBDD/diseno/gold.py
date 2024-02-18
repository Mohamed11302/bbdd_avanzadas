import conexionBBDD.conexionBBDD as conBBDD
import pandas as pd

def diseno_gold(conn_str):
    df_video = pd.read_csv('video.csv')
    df_channel= pd.read_csv('channel.csv')
    print("Leidos df_video y df_channel")
    