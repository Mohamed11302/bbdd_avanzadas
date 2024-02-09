import constantes as const
import utils
import pandas as pd



def get_video_playlist(channel_id, api_key):
    params = {
            'part': 'snippet,statistics',
            'id': channel_id,
            'key': api_key
    }
    response = utils.http_request_yt(const.YT_API_PLAYLISTS, params)
    return response

def get_top50_videos(df, api_key):
    for fila in range(0, len(df)):
        #get_video_playlist(df.loc[fila, 'ID'], api_key)
        if fila<2:
            print(df.loc[fila, 'ID'])