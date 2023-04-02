""" Contains the SongInfo, ArtistNode, and ArtistTree Class"""
from __future__ import annotations
from typing import Optional

# Comment out this line when you aren't using check_contracts
from python_ta.contracts import check_contracts

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from test import artist_five_tracks, artist_id

app_client_id = "10ad55033d8d48dc9b90c9aa1e6d074c"
app_client_secret = "1aa0b1b3d6a94f00a1125c24394a886e"

client_credentials_manager = SpotifyClientCredentials(client_id=app_client_id, client_secret=app_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class User:
    """
    Information about the user's preferences.
    Contains the user's favorite song, the corresponding artist, the user's desired diversity level,
    and the user's favorite attribute about their favorite song, if any.

    Instance Attributes:
        - song_name: The name of the user's favorite song
        - artist_name: The name of the corresponding artist to song_name
        - diversity_level: an integer greater than or equal to zero. This integer corresponds to the depth
        of the artist tree, with a larger level of 'diversity' representing a deeper depth into the tree of artists.
        If the user chooses not to input a number, 'diversity' defaults to 0.
    """
    song_name: str
    artist_name: str
    diversity_level: Optional[int] = 0

    def __init__(self, song_name: str, artist_name: str, diversity_level: Optional[int] = 0) -> None:
        """Initialize a new User object. Contains the user's preferences.
        """
        self.song_name = song_name
        self.artist_name = artist_name
        self.diversity_level = diversity_level


class SongInfo:
    """
    Information about a song.
    Contains the attributes of a song. In particular, it contains the song name, the artist name, and
    the 5 song attributes below.


    Credit for the descriptions of the last 5 instance attributes is attributed to the Spotify Developer documentation:
    https://developer.spotify.com/documentation/web-api/reference/get-audio-features

    Instance Attributes:
      - song_name: The name of this song
      - artist_name: The name of the artist who wrote this song
      - danceability: how suitable a track is for dancing based on a combination of musical elements.
        A value of 0.0 is least danceable and 1.0 is most danceable.
      - valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track.
        Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric),
        while tracks with low valence sound more negative (e.g. sad, depressed, angry).
      - tempo: The average tempo of a track in beats per minute (BPM). Unlike the others, this number goes past 1.0
      - instrumentalness: Predicts whether a track contains no vocals.
        The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content.
      - energy: a measure from 0.0 to 1.0 represending a measure of intensity and activity.
        Typically, energetic tracks feel fast, loud, and noisy. A higher number represents higher energy.
      - acousticness: A measure from 0.0 to 1.0 of whether the track is acoustic.
        1.0 represents high confidence the track is acoustic.
    """
    song_name: str
    artist_name: str
    danceability: float
    valence: float
    tempo: float
    instrumentalness: float
    energy: float
    acousticness: float

    def __init__(self, song_name: str, artist_name: str) -> None:
        """Initialize a new SongNode.
        """
        tracks = sp.search(q=song_name, type='track')['tracks']
        items = tracks['items']
        for item in items:
            if item['name'] == song_name and item['artists'][0]['name'] == artist_name:
                features = sp.audio_features(item['id'])[0]
                self.song_name = song_name
                self.artist_name = artist_name
                self.danceability = features['danceability']
                self.valence = features['valence']
                self.tempo = features['tempo']
                self.instrumentalness = features['instrumentalness']
                self.energy = features['energy']
                self.acousticness = features['acousticness']


class ArtistNode:
    """
       A node in the ArtistTree.
       Contains the name of the artist, the artist's id, and their top tracks.

       Instance Attributes:
         - artist_name: the name of the artist
         - artist_id: the id of the artist
         - top_tracks: the top tracks of the artist
       """
    artist_name: str
    artist_id: str
    top_tracks: list[SongInfo]

    def __init__(self, artist_name) -> None:
        """Initialize a new ArtistNode.
        """
        self.artist_name = artist_name
        self.artist_id = artist_id(artist_name)
        top_tracks = artist_five_tracks(artist_name)
        song_info_tracks = [SongInfo(song_name, top_tracks[song_name]) for song_name in top_tracks]
        self.top_tracks = song_info_tracks


class ArtistTree:
    """A tree representing the user's favorite song's artist as the root, and similar artists as the subtrees.

        Each node in the tree is an ArtistNode

        Instance Attributes:
            - artist: the current node of the tree
            - depth: the current depth of the tree
        """
    artist: ArtistNode
    depth: int

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent similar artists to its parent node.
    #      _subtrees will be None if we reach the user's given diversity level
    _subtrees: Optional[list[ArtistNode]]

    def __init__(self, artist: ArtistNode, depth: int, _subtrees: Optional[list[ArtistNode]]) -> None:
        """Initialize a new artist tree.

        Note that this initializer uses optional arguments.

        """
        self.artist = artist
        self.depth = depth
        self._subtrees = _subtrees

    def get_subtrees(self) -> list[ArtistTree]:
        """Return the subtrees of this artist tree."""
        return list(tree for tree in self._subtrees)

    def insert_subtrees(self, artists: list[ArtistNode], parent_node: ArtistNode) -> None:
        """Inserts the subtree(s) as subtrees of the parent node.
        Note: artists are the related artists to the parent node"""
        self._subtrees = artists


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120
    # })
