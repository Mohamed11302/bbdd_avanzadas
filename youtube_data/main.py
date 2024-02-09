import pandas as pd
import utils
import constantes as const
import youtube_api.channel as channel
import youtube_api.video as video





if __name__ == "__main__":
    api_key = utils.get_api_key()

    #PASO 1: COMPROBAR LOS IDS
    #utils.check_ids(api_key)

    #PASO 2: BUSCAR LOS CANALES DE LOS IDS VALIDOS
    df = pd.read_csv(const.YT_IDS_CHECK)
    df.drop(df[df['Exist'] == 0].index, inplace=True)
    #df.to_csv(const.YT_IDS_CHECK, index=False)
    channel.get_channel_info(df, api_key)

    #PASO 3: BUSCAR LOS VIDEOS DE LOS CANALES
    #df = pd.read_csv(const.YT_IDS_CHECK)
    #video.get_top50_videos(df, api_key)

