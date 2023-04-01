""" Contains the SongNode and SongTree Class"""
from typing import Optional

class SongNode:
    """
    A node in a tree.
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
      - tempo: The average tempo of a track in beats per minute (BPM). Unlike the others, this # goes past 1.0
      - instrumentalness: Predicts whether a track contains no vocals.
        The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content.
      - energy: a measure from 0.0 to 1.0 represending a measure of intensity and activity.
        Typically, energetic tracks feel fast, loud, and noisy. A higher number represents higher energy.
      - acoustic: A measure from 0.0 to 1.0 of whether the track is acoustic.
        1.0 represents high confidence the track is acoustic.
    """
    song_name: str
    artist_name: str
    danceability: float
    valence: float
    tempo: float
    instrumentalness: float
    energy: float
    acoustic: float

    def __init__(self, song_name: str, artist_name: str, danceability: float,
    valence: float, tempo: float, instrumentalness: float, energy: float, acoustic: float) -> None:

        """Initialize a new SongNode.
        """
        self.song_name = song_name
        self.artist_name = artist_name
        self.danceability = danceability
        self.valence = valence
        self.tempo = tempo
        self.instrumentalness = instrumentalness
        self.energy = energy
        self.acoustic = acoustic

class SongTree:
    """A tree representing the user's favorite song as the root, and its similar songs as the subtrees.

        Each node in the tree is a SongNode

        Instance Attributes:
            - song: the current node of the tree
            - depth: the current depth of the tree
        """
    song: SongNode
    depth: int

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the recommended songs given its parent node.
    #      _subtrees will be None if we reach the user's given diversity level
    _subtrees: Optional[list[SongNode]]

    def __init__(self, song: SongNode, depth: int, _subtrees: Optional[list[SongNode]]) -> None:
        """Initialize a new song tree.

        Note that this initializer uses optional arguments.

        """
        self.song = song
        self.depth = depth
        self._subtrees = _subtrees
