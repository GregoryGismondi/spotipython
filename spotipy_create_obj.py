"""Functions that create SongInfo objects and User objects"""

from __future__ import annotations
from typing import Optional
# Comment out this line when you aren't using check_contracts
from python_ta.contracts import check_contracts

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy_main_classes as main_classes

app_client_id = "10ad55033d8d48dc9b90c9aa1e6d074c"
app_client_secret = "1aa0b1b3d6a94f00a1125c24394a886e"

client_credentials_manager = SpotifyClientCredentials(client_id=app_client_id, client_secret=app_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def create_song_info(song_name: str, artist_name: str) -> main_classes.SongInfo:
    """Creates a SongInfo object for the given song and its corresponding artist.

    Preconditions: The song and artist must be valid and written the way it is on spotify.
    """
    tracks = sp.search(q=song_name, type='track')['tracks']
    items = tracks['items']
    for item in items:
        if item['name'] == song_name and item['artists'][0]['name'] == artist_name:
            features = sp.audio_features(item['id'])[0]
            new_song = main_classes.SongInfo(song_name, artist_name, features['danceability'],
                 features['valence'], features['tempo'], features['instrumentalness'],
                 features['energy'], features['acousticness'])
            return new_song
        else:
            print("No corresponding song and artist on spotify.")

@check_contracts
def create_user_preference() -> main_classes.User:
    """Prompts the user to answer some questions and creates a UserPreference object
    for the given user input

    Asks for the user's favorite song, its corresponding artist, and the user's desired
    diversity level.

    Representation Invariants:
    - div_level == '' or div_level.isdigit()

    """
    song_name = input('Enter the name of your favorite song as it appears on Spotify: ')
    artist_name = input('Enter the name of the song\'s corresponding artist as it appears on Spotify: ')
    div_level = input('Diversity level represents how diverse you want your song recommendations to be. \n'
                      'The higher the number, the more recommendations you will get. Enter an integer \n'
                      'greater than or equal to zero, or press the \'Enter\' key if you choose not to \n'
                      'specify. Note: This will result in a default diversity level of zero.')
    if div_level == '':
        div_level = 0
    else:
        div_level = int(div_level)  # before div_level was a str representation of an int
    return main_classes.User(song_name, artist_name, div_level)
