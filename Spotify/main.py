import utils
import artists
import albums
import tracks
import Constantes as Const

if __name__ == "__main__":
    client_id, client_secret = utils.get_id_and_secrets()
    token = utils.get_token(client_id, client_secret)
    artists_data = artists.get_top_artists(token, Const.NUM_ARTISTS)
    artists.write_top_artists(artists_data)
    print("Artists saved")
    albums_data = albums.get_top_albums(token, Const.NUM_ALBUMS, artists_data)
    albums.write_top_albums(albums_data)
    print("Albums saved")
    tracks_data = tracks.get_top_tracks(token, albums_data)
    tracks.write_top_tracks(tracks_data)
    print("Tracks saved")

