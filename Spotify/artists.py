import pandas as pd
import utils
import Constantes as Const

def get_top_artists(token, num_artists):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    artists_data = []
    offset = 0
    while num_artists>0:
        if num_artists>=50:
            top_artists_data = utils.http_request(Const.API_SEARCH, headers, build_params_artist(50, offset))
        else:
            top_artists_data = utils.http_request(Const.API_SEARCH, headers, build_params_artist(num_artists, offset))
        artists_data.extend(top_artists_data['artists']['items'])
        num_artists -= 50
        offset +=50
    return artists_data


def build_params_artist(num_artists, offset):
    return (
            ('q', 'year:2024'),  # Busca artistas que hayan lanzado música entre 2020 y 2024
            ('type', 'artist'),  # Estamos buscando artistas
            ('limit', num_artists),  # Limita la búsqueda a 'num_artists' artistas
            ('offset', offset),  # Añade el offset
            #('market', 'ES')
        )


def write_top_artists(artists_data):
    df = pd.DataFrame(columns=['name', 'id', 'popularity', 'followers', 'genres'])
    for artist in artists_data:
            new_artist = {
                'name': artist["name"],
                'id': artist["id"],
                'popularity': artist["popularity"], 
                'followers': artist["followers"]["total"],
                'genres': ", ".join(artist["genres"])
            }
            df = df._append(new_artist, ignore_index=True)
    df.to_csv("artists.csv", sep=";", index=False)