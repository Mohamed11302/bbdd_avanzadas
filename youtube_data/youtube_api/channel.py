import youtube_data.constantes as const
import youtube_data.utils
import pandas as pd


def get_channel_info(df, api_key):
    salto=10
    df_channels = pd.DataFrame(columns=['name', 'id', 'creationdate', 'language', 'country', 'subscribers', 'viewcount', 'numvideos'])
    df['Channel']=0
    for fila in range(0, len(df), salto):
        print(fila)
        indice1 = fila
        indice2 = fila+salto-1
        ids = utils.obtener_lista_ids_df(df,'ID', indice1, indice2)
        params = {
            'part': 'snippet,statistics',
            'id': ids,
            'key': api_key
        }
        response = utils.http_request_yt(const.YT_API_CHANNELS, params)    
        if response != None:
            for response in response['items']:
                '''
                print(response)
                print(f"id: {response['id']}")
                print(f"title: {response['snippet']['title']}")
                print(f"description: {response['snippet']['description']}")
                print(f"creation: {response['snippet']['publishedAt']}")
                print(f"default language: {response.get('snippet', {}).get('defaultLanguage')}")
                print(f"country: {response.get('snippet', {}).get('country')}")
                print(f"viewCount: {response['statistics']['viewCount']}")
                print(f"Subscribers: {response['statistics']['subscriberCount']}")
                print(f"Num of videos: {response['statistics']['videoCount']}")
                '''
                df_channels = df_channels._append({
                    'name': response['snippet']['title'],
                    'id': response['id'],
                    #'description': response['snippet']['description'],
                    'creationdate': response['snippet']['publishedAt'],
                    'language': response.get('snippet', {}).get('defaultLanguage'),
                    'country': response.get('snippet', {}).get('country'),
                    'subscribers': response['statistics']['subscriberCount'],
                    'viewcount': response['statistics']['viewCount'],
                    'numvideos': response['statistics']['videoCount']
                }, ignore_index=True)
            df.loc[indice1:indice2, 'Channel'] = 1
            df.to_csv(const.YT_IDS_CHECK, index=False)
            df_channels.to_csv(const.YT_CHANNELS, index=False)





