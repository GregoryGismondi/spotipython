"""CSC111: Spotipython Project - Main File

"""
import spotipy
import recommender
import spotipy_main_classes
from spotipy.oauth2 import SpotifyClientCredentials


def create_app() -> spotipy.Spotify:
    """Creates a Spotify API class using Spotipy funcitons
    """
    app_client_id = "10ad55033d8d48dc9b90c9aa1e6d074c"
    app_client_secret = "1aa0b1b3d6a94f00a1125c24394a886e"

    client_credentials_manager = SpotifyClientCredentials(client_id=app_client_id, client_secret=app_client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


def recommend_song(song_name: str, d: int = 1):
    # STEP 1: GET ARTIST FROM SONG

    # temp variables - Taylor Swift's Daylight
    artist_id = '06HL4z0CvFAxyc27GXpf02'
    song_id = '1fzAuUVbzlhZ1lJAx9PtY6'
    song_info = {'danceability': 0.557, 'energy': 0.496, 'key': 0, 'loudness': -9.602,
                 'mode': 1, 'speechiness': 0.0563, 'acousticness': 0.808, 'instrumentalness': 0.000173,
                 'liveness': 0.0772, 'valence': 0.265, 'tempo': 149.983}

    # STEP 2: CREATE TREE OF ARTISTS
    root_artist = spotipy_main_classes.ArtistNode('Taylor Swift', artist_id)
    artist_tree = spotipy_main_classes.ArtistTree(root_artist, [])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sp = create_app()
