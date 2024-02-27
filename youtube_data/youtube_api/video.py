import youtube_data.constantes as const
import youtube_data.utils as utils
import pandas as pd
import requests
import json
def get_video_playlist(channel_id, api_key):
    params = {
            'part': 'snippet,statistics',
            'id': channel_id,
            'key': api_key
    }
    response = utils.http_request_yt(const.YT_API_PLAYLISTS, params)
    return response

def get_top50_videos(df, api_key):
    channel_id = "UCq-Fj5jknLsUf-MWSy4_brA"
    url = f"https://www.googleapis.com/youtube/v3/channels/list?part=snippet,contentDetails,statistics&id={channel_id}&maxResults=50&order=viewCount&key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.content)

        for video in data["items"]:
            print(video["snippet"]["title"])
            print(video["statistics"]["viewCount"])
    else:
        print("Error:", response.headers)
    return None
    for fila in range(0, len(df)):
        #get_video_playlist(df.loc[fila, 'ID'], api_key)
        if fila<2:
            print(df.loc[fila, 'ID'])
            print(get_playlist_videos_id(df.loc[fila, 'ID']))

def get_playlist_videos_id(channel_id):
    return 'UU' + channel_id[2:]

def get_last_videos(df, api_key):
    num_videos = 100
    #df_videos = pd.DataFrame(columns=['title', 'id', 'channelId', 'publishedAt', 'tags', 'categoryId', 'liveBroadcastContent', 'duration', 'defaultAudioLanguage', 'viewCount', 'likeCount', 'commentCount'])
    df_videos = pd.read_csv(const.YT_VIDEOS)
    for fila in range(0, len(df)):
        print(f"{fila}: {df.loc[fila, 'ID']}")
        playlist_id = get_playlist_videos_id(df.loc[fila, 'ID'])
        videos = []
        page_token = None
        while True:
            params = {
                "part": "snippet",
                "playlistId": playlist_id,
                "maxResults": 50,
                "key": api_key,
                "pageToken": page_token
            }
            videos_ids = utils.http_request_yt(const.YT_API_PLAYLISTSITEMS, params=params)
            if videos_ids == None:
                print("\n****************************ERROR SEARCH************************************************\n")
                break
            else:
                video_ids = [item['snippet']['resourceId']['videoId'] for item in videos_ids['items'] if 'snippet' in item and 'resourceId' in item['snippet']]
                videos_info= get_video_info(video_ids, api_key)                
                videos.extend(videos_info)
                if len(videos)<num_videos:
                    page_token = videos_ids.get('nextPageToken')
                    if not page_token:
                        break
                else:
                    break
        if len(videos)>=num_videos:
            df_videos = procesar_video(df_videos, videos)
            df.loc[fila, 'Video'] = 1
            df.to_csv(const.YT_IDS_CHECK, index=False)
            if fila%5==0:
                df_videos.to_csv(const.YT_VIDEOS, index=False)


def get_video_info(video_ids, api_key):
    videos = []
    salto = 10
    for indice in range(0, len(video_ids), salto):
        indice1 = indice
        indice2 = indice+salto-1
        ids = utils.obtener_lista_ids_lista(video_ids, indice1, indice2)
        params_video = {
            "part": "snippet,contentDetails,statistics",
            "id": ids,
            "key": api_key
        }
        video_response = utils.http_request_yt(const.YT_API_VIDEOS, params=params_video)
        if video_response != None:
            for video in video_response['items']:
                videos.append(video)                   
    return videos

def procesar_video(df_videos, videos):
    for video in videos:
        new_row = {
            'title': video.get('snippet', {}).get('title'),
            'id': video.get('id'),
            'channelId': video.get('snippet', {}).get('channelId'),
            'publishedAt': video.get('snippet', {}).get('publishedAt'),
            'tags': video.get('snippet', {}).get('tags'),
            'categoryId': video.get('snippet', {}).get('categoryId'),
            'liveBroadcastContent': video.get('snippet', {}).get('liveBroadcastContent'),
            'duration': video.get('contentDetails', {}).get('duration'),
            'defaultAudioLanguage': video.get('snippet', {}).get('defaultAudioLanguage'),
            'viewCount': video.get('statistics', {}).get('viewCount'),
            'likeCount': video.get('statistics', {}).get('likeCount'),
            'commentCount': video.get('statistics', {}).get('commentCount')
        }
        df_videos = df_videos._append(new_row, ignore_index=True)
    return df_videos

def eliminar_videos_duplicados(df):
    df_filtrado = df.drop_duplicates(subset=['id'], keep='first')
    df_filtrado.to_csv(const.YT_VIDEOS, index=False)
    print(df_filtrado['id'].value_counts())
