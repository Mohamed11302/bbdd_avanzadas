import pandas as pd
import youtube_data.utils as utils
import youtube_data.constantes as const
import youtube_data.youtube_api.channel as channel
import youtube_data.youtube_api.video as video



def extraer_data():
    api_key = utils.get_api_key()
    print("Extrayendo data de la api de youtube")
"""
    #PASO 1: COMPROBAR LOS IDS
    utils.check_ids(api_key)

    #PASO 2: BUSCAR LOS CANALES DE LOS IDS VALIDOS
    df = pd.read_csv(const.YT_IDS_CHECK)
    df = df.head(2000)
    df.drop(df[df['Exist'] == 0].index, inplace=True)
    df.to_csv(const.YT_IDS_CHECK, index=False)
    channel.get_channel_info(df, api_key)

    #PASO 3: BUSCAR LOS VIDEOS DE LOS CANALES
    df = pd.read_csv(const.YT_IDS_CHECK)
    df['Video'] = -1
    video.get_last_videos(df, api_key)
    df_videos = pd.read_csv(const.YT_VIDEOS)
    video.eliminar_videos_duplicados(df_videos)
"""





if __name__ == "__main__":
    extraer_data()
