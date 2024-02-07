import utils
import Constantes as Const
import pandas as pd

def get_top_tracks(token, albums_data):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    tracks_data = []
    for album in albums_data:
        url = Const.API_ALBUMS_BASE+album["id"]+"/tracks"
        num_tracks = album["total_tracks"]
        offset=0
        while num_tracks>0:
            if num_tracks>=50:
                top_tracks = utils.http_request(url, headers, build_params_track(50, offset))
            else:
                top_tracks = utils.http_request(url, headers, build_params_track(num_tracks, offset))
            for top_track in top_tracks['items']:
                top_track['album_id'] = album["id"]
            tracks_data.extend(top_tracks['items'])
            num_tracks -=50
            offset += 50
    return tracks_data

def build_params_track(num_albums, offset):
    return (
            ('limit', num_albums),
            ('offset', offset)
    )
def write_top_tracks(tracks):
    df = pd.DataFrame(columns=['name', 'id', 'album_id', 'artists', 'disc_number', 'track_number', 'duration_ms', 'type'])
    for track in tracks:
        df = add_track_to_df(df, track)
    df.to_csv("tracks.csv", sep=";", index=False)

def add_track_to_df(df, track):
    new_track={
        'name': track['name'],
        'id': track['id'],
        'album_id': track['album_id'],
        'artists' : get_artists_track(track),
        'disc_number' : track['disc_number'],
        'track_number' : track['track_number'],
        'duration_ms' : track['duration_ms'],
        'type' : track['type']
    }
    df = df._append(new_track, ignore_index=True)
    return df



def get_artists_track(track):
    artists_id = ""
    for i, artist in enumerate(track['artists']):
        artists_id += artist['id']
        if i < len(track['artists']) - 1:
            artists_id += ", "
    return artists_id
    