"""CSC111: Spotipython Project - Main File

"""
import spotipy
import artist_tree
import spotipy_create_obj
from spotipy.oauth2 import SpotifyClientCredentials


def create_app() -> spotipy.Spotify:
    """Creates a Spotify API class using Spotipy funcitons
    """
    app_client_id = "10ad55033d8d48dc9b90c9aa1e6d074c"
    app_client_secret = "1aa0b1b3d6a94f00a1125c24394a886e"

    client_credentials_manager = SpotifyClientCredentials(client_id=app_client_id, client_secret=app_client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


def recommend_song():
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sp = create_app()
