"""CSC111: Spotipython Project - Creator File

This Python module contains the create_user() and create_app()
functions.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Amy Li, Brittany Lansang, and Gregory Gismondi.

"""

from __future__ import annotations
# Comment out this line when you aren't using check_contracts
# from python_ta.contracts import check_contracts

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from user import User


def create_user() -> User:
    """Prompts the user to answer some questions and creates a User object
    for the given user input

    Asks for the user's favorite song, its corresponding artist, and the user's desired
    diversity level.

    Preconditions:
    - The user's input for song_name and corresponding artist_name are valid names in Spotify.

    Representation Invariants:
    - div_level == '' or div_level.isdigit()
    - fav_attribute == 'danceability' or fav_attribute == 'valence' or \n
    fav_attribute == 'tempo' or fav_attribute == 'instrumentalness' or fav_attribute == 'energy' or \n
    fav_attribute == 'acousticness' or fav_attribute == ''

    """
    song_name = input('Enter the name of your favorite song as it appears on Spotify: ')
    artist_name = input('Enter the name of the song\'s corresponding artist as it appears on Spotify: ')
    div_level = input('Diversity level represents how diverse you want your song recommendations to be. \n'
                      'The higher the number, the more recommendations you will get. We recommend an integer \n'
                      'that does not exceed 2 in order to get a timely output. Enter an integer \n'
                      'greater than or equal to zero, or press the \'Enter\' key if you choose not to \n'
                      'specify. Note - This will result in a default diversity level of zero: ')
    fav_attribute = input('Enter your favorite attribute of the song out of the following list: \n'
                          'danceability, valence, tempo, instrumentalness, energy, acousticness. \n'
                          'Or, press the \'Enter\' key if you have no preference: ')
    if div_level == '':
        div_level = 0
    else:
        div_level = int(div_level)  # before div_level was a str representation of an int

    if fav_attribute == '':
        return User(song_name, artist_name, None, div_level)
    else:
        return User(song_name, artist_name, fav_attribute.lower(), div_level)


def create_app() -> spotipy.Spotify:
    """Creates a Spotify API class using Spotipy funcitons
    """
    app_client_id = "10ad55033d8d48dc9b90c9aa1e6d074c"
    app_client_secret = "1aa0b1b3d6a94f00a1125c24394a886e"

    client_credentials_manager = SpotifyClientCredentials(client_id=app_client_id, client_secret=app_client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return spotify


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['random', 'spotipy', 'user', 'spotipy.oauth2'],
        'allowed-io': ['input']
    })
