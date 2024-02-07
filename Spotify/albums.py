import utils
import Constantes as Const
import pandas as pd

def get_top_albums(token, num_albums, artists_data):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    albums_data = []    
    for artist in artists_data:
        num_albums_aux = num_albums
        offset=0
        url = Const.API_ARTIST_BASE+artist["id"]+"/albums"
        while num_albums_aux>0:
            if num_albums_aux>=50:
                top_albums = utils.http_request(url, headers, build_params_album(50, offset))
            else:
                top_albums = utils.http_request(url, headers, build_params_album(num_albums_aux, offset))
            albums_data.extend(top_albums['items'])
            num_albums_aux -=50
            offset += 50
    return albums_data



def build_params_album(num_albums, offset):
    return (
            ('limit', num_albums),
            ('offset', offset)
    )
    

def write_top_albums(albums):
    df = pd.DataFrame(columns=['name', 'id', 'album_type', 'artists', 'release_date', 'total_tracks'])
    for album in albums:
        df = add_album_to_df(df, album)
        df['total_tracks'] = df['total_tracks'].astype(int)
    df.to_csv("albums.csv", sep=";", index=False)
    return df

def add_album_to_df(df, album):
    new_album={
        'name': album['name'],
        'id': album['id'],
        'album_type': album['album_type'],
        'artists' : get_artists_album(album),
        'release_date' : album['release_date'],
        'total_tracks' : album['total_tracks']
    }
    df = df._append(new_album, ignore_index=True)
    return df

def get_artists_album(album):
    artists_id = ""
    for i, artist in enumerate(album['artists']):
        artists_id += artist['id']
        if i < len(album['artists']) - 1:
            artists_id += ", "
    return artists_id