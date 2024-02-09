import pandas as pd
import utils
import youtube_api.channel as channel
import constantes as const





if __name__ == "__main__":
    api_key = utils.get_api_key()
    df = pd.read_csv(const.YT_IDS)
    #df = utils.check_ids(df, api_key)
    df.drop(df[df['Exist'] == 0].index, inplace=True)
    #df.reset_index(inplace=True)
    channel.get_channel_info(df, api_key)
    #print(len(df))
    #print(channel.obtener_lista_ids(df, 4620, 4630))



