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


@check_contracts
def create_user() -> main_classes.User:
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
                      'The higher the number, the more recommendations you will get. Enter an integer \n'
                      'greater than or equal to zero, or press the \'Enter\' key if you choose not to \n'
                      'specify. Note: This will result in a default diversity level of zero.')
    fav_attribute = input('Enter your favorite attribute of the song out of the following list: \n'
                          'danceability, valence, tempo, instrumentalness, energy, acousticness. \n'
                          'Or, press the \'Enter\' key if you have no preference.')
    if div_level == '':
        div_level = 0
    else:
        div_level = int(div_level)  # before div_level was a str representation of an int
    
    if fav_attribute == '':
        return main_classes.User(song_name, artist_name, div_level)
    else:
        return main_classes.User(song_name, artist_name, div_level, fav_attribute)
    
def difference_score(user: main_classes.User, og_song: main_classes.SongInfo, new_song: main_classes.SongInfo) -> float:
    """ Calculates a difference score from 0.0 (very similar) to 1.0 (very different) between the original
    song and the new song based on the difference in values between each attribute of the song.
    If the user chose a particular characteristic they liked about the original song, it will make up 50%
    of the weighting when calculating the difference score, while the 5 other attributes would make up the
    rest, at 10% each. If no characteristic was chosen, then all characteristics are weighed equally.

    This score is calculated by finding the absolute value of the difference for each attribute, applying the
    appropriate weighting, summing up the values, and dividing the entire thing by the number of attributes
    there are.

    Updates the new_song info to contain its score.
    """
    diff_danceability = abs(og_song.danceability - new_song.danceability)
    diff_valence = abs(og_song.valence - new_song.valence)
    diff_tempo = abs(og_song.tempo - new_song.valence)
    diff_instrumentalness = abs(og_song.instrumentalness - new_song.instrumentalness)
    diff_energy = abs(og_song.energy - new_song.energy)
    diff_acousticness = abs(og_song.acousticness - new_song.acousticness)
    
    if user.fav_attribute is None:
        total = diff_danceability + diff_valence + diff_tempo + diff_instrumentalness + diff_energy + diff_acousticness
        avg = total/6
        new_song.difference_score = avg
        return avg
    elif user.fav_attribute == 'danceability':
        avg = diff_danceability*0.5 + diff_valence*0.1 + diff_tempo*0.1 + diff_instrumentalness*0.1 + \
              diff_energy*0.1 + diff_acousticness*0.1
        new_song.difference_score = avg
        return avg
    elif user.fav_attribute == 'valence':
        avg = diff_danceability * 0.1 + diff_valence * 0.5 + diff_tempo * 0.1 + diff_instrumentalness * 0.1 + \
              diff_energy * 0.1 + diff_acousticness * 0.1
        return avg
    elif user.fav_attribute == 'tempo':
        avg = diff_danceability * 0.1 + diff_valence * 0.1 + diff_tempo * 0.5 + diff_instrumentalness * 0.1 + \
              diff_energy * 0.1 + diff_acousticness * 0.1
        new_song.difference_score = avg
        return avg
    elif user.fav_attribute == 'instrumentalness':
        avg = diff_danceability * 0.1 + diff_valence * 0.1 + diff_tempo * 0.1 + diff_instrumentalness * 0.5 + \
              diff_energy * 0.1 + diff_acousticness * 0.1
        new_song.difference_score = avg
        return avg
    elif user.fav_attribute == 'energy':
        avg = diff_danceability * 0.1 + diff_valence * 0.1 + diff_tempo * 0.1 + diff_instrumentalness * 0.1 + \
              diff_energy * 0.5 + diff_acousticness * 0.1
        new_song.difference_score = avg
        return avg
    elif user.fav_attribute == 'acousticness':
        avg = diff_danceability * 0.1 + diff_valence * 0.1 + diff_tempo * 0.1 + diff_instrumentalness * 0.1 + \
              diff_energy * 0.1 + diff_acousticness * 0.5
        new_song.difference_score = avg
        return avg
