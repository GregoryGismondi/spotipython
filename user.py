from __future__ import annotations
from typing import Optional


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
        - fav_attribute: The user's favorite attribute about their chosen song, if any.
    """
    song_name: str
    artist_name: str
    diversity_level: Optional[int] = 0
    fav_attribute: Optional[str]

    def __init__(self, song_name: str, artist_name: str, fav_attribute: Optional[str],
                 diversity_level: Optional[int] = 0) -> None:
        """Initialize a new User object. Contains the user's preferences.
        """
        self.song_name = song_name
        self.artist_name = artist_name
        self.diversity_level = diversity_level
        self.fav_attribute = fav_attribute
