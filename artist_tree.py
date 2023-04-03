"""CSC111: Spotipython Project - ArtistTree File

This Python module contains the SongInfo, ArtistNode, and ArtistTree class.
It also defines other methods within these classes, and functions outside the classes. 

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Amy Li, Brittany Lansang, and Gregory Gismondi.
"""

from __future__ import annotations
from typing import Optional

# Comment out this line when you aren't using check_contracts
# from python_ta.contracts import check_contracts

import random
import spotipy
from user import User


class SongAttributes:
    """
    Information about a song's attributes

    Instance Attributes:
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
    danceability: float
    valence: float
    tempo: float
    instrumentalness: float
    energy: float
    acousticness: float

    def __init__(self, features: dict) -> None:
        self.danceability = features['danceability']
        self.valence = features['valence']
        self.tempo = features['tempo']
        self.instrumentalness = features['instrumentalness']
        self.energy = features['energy']
        self.acousticness = features['acousticness']


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
      - difference_score: The difference score between this song and the original song at the root of Artist_Tree
      - track_arritubtes: A datatype that stores the attributes of the song from Spotify's dataset
      - sp: an instance of the Spotify API class from the spotipy library
      - user: the user datatype holding the user's inputs
    """
    song_name: str
    artist_name: str
    difference_score: Optional[float]
    track_attributes: SongAttributes
    sp: spotipy.Spotify
    user: User

    def __init__(self, song_name: str, artist_name: str, user: User, sp: spotipy.Spotify) -> None:
        """Initialize a new SongNode.
        """
        self.sp = sp
        self.user = user
        tracks = sp.search(q=song_name + ' - ' + artist_name, type='track')['tracks']
        item = tracks['items'][0]
        features = sp.audio_features(item['id'])[0]
        if features is not None:
            self.song_name = song_name
            self.artist_name = artist_name
            self.track_attributes = SongAttributes(features)

    def difference_scorer(self, curr_user: User, og_song: SongInfo) -> None:
        """ Calculates a difference score between the original song and the new song based on the difference in values
        between each attribute of the song. This 'score' is a non-negative float. A score of 0.0 means the new song
        is very similar to the original song, while a higher score indicates the new_song is more different from the
        original. If the user chose a particular characteristic they liked about the original song, it will make up 50%
        of the weighting when calculating the difference score, while the 5 other attributes would make up the
        rest, at 10% each. If no characteristic was chosen, then all characteristics are weighed equally.

        This score is calculated by finding the absolute value of the difference for each attribute, applying the
        appropriate weighting, summing up the values, and dividing the entire thing by the number of attributes
        there are.

        Updates the new_song info to contain its score.
        """
        diff_danceability = abs(og_song.track_attributes.danceability - self.track_attributes.danceability)
        diff_valence = abs(og_song.track_attributes.valence - self.track_attributes.valence)
        # The difference in tempo is much greater, therefore we have to nerf its power by diving by 100
        diff_tempo = abs(og_song.track_attributes.tempo - self.track_attributes.tempo) / 50
        diff_instrumentalness = abs(og_song.track_attributes.instrumentalness - self.track_attributes.instrumentalness)
        diff_energy = abs(og_song.track_attributes.energy - self.track_attributes.energy)
        diff_acousticness = abs(og_song.track_attributes.acousticness - self.track_attributes.acousticness)

        if curr_user.fav_attribute is None:
            total = diff_danceability + diff_valence + diff_tempo + diff_instrumentalness
            total += diff_energy + diff_acousticness
            avg = total / 6
            self.difference_score = avg
            return
        elif curr_user.fav_attribute == 'danceability':
            avg = diff_danceability * 0.5 + diff_valence * 0.1 + diff_tempo * 0.1 + diff_instrumentalness * 0.1
            avg += diff_energy * 0.1 + diff_acousticness * 0.1
            self.difference_score = avg
            return
        elif curr_user.fav_attribute == 'valence':
            avg = diff_danceability * 0.1 + diff_valence * 0.5 + diff_tempo * 0.1 + diff_instrumentalness * 0.1
            avg += diff_energy * 0.1 + diff_acousticness * 0.1
            self.difference_score = avg
            return
        elif curr_user.fav_attribute == 'tempo':
            avg = diff_danceability * 0.1 + diff_valence * 0.1 + diff_tempo * 0.5 + diff_instrumentalness * 0.1
            avg += diff_energy * 0.1 + diff_acousticness * 0.1
            self.difference_score = avg
            return
        elif curr_user.fav_attribute == 'instrumentalness':
            avg = diff_danceability * 0.1 + diff_valence * 0.1 + diff_tempo * 0.1 + diff_instrumentalness * 0.5
            avg += diff_energy * 0.1 + diff_acousticness * 0.1
            self.difference_score = avg
            return
        elif curr_user.fav_attribute == 'energy':
            avg = diff_danceability * 0.1 + diff_valence * 0.1 + diff_tempo * 0.1 + diff_instrumentalness * 0.1
            avg += diff_energy * 0.5 + diff_acousticness * 0.1
            self.difference_score = avg
            return
        elif curr_user.fav_attribute == 'acousticness':
            avg = diff_danceability * 0.1 + diff_valence * 0.1 + diff_tempo * 0.1 + diff_instrumentalness * 0.1
            avg += diff_energy * 0.1 + diff_acousticness * 0.5
            self.difference_score = avg
            return


class ArtistNode:
    """
       A node in the ArtistTree.
       Contains the name of the artist, the artist's id, and their top tracks.

       Instance Attributes:
         - artist_name: the name of the artist
         - artist_id: the id of the artist
         - top_tracks: the top tracks of the artist
         - user: the user datatype holding the user's inputs
       """
    artist_name: str
    artist_id: str
    top_tracks: list[SongInfo]
    user: User

    def __init__(self, artist_name: str, artist_id: Optional[str], user: User, sp: spotipy.Spotify) -> None:
        """Initialize a new ArtistNode.
        """
        self.artist_name = artist_name
        if artist_id is None:
            self.artist_id = get_artist_id(artist_name, sp)
        else:
            self.artist_id = artist_id
        self.user = user
        top_tracks = artist_five_tracks(self.artist_name, self.artist_id, user, sp)
        song_info_tracks = [SongInfo(song_name, top_tracks[song_name], user, sp) for song_name in top_tracks]
        user_song = SongInfo(user.song_name, user.artist_name, user, sp)

        song_info_tracks_correct = []

        for song_info in song_info_tracks:
            if hasattr(song_info, 'track_attributes'):
                song_info_tracks_correct.append(song_info)

        for song_info in song_info_tracks_correct:
            song_info.difference_scorer(user, user_song)

        self.top_tracks = song_info_tracks


class ArtistTree:
    """A tree representing the user's favorite song's artist as the root, and similar artists as the subtrees.

        Each node in the tree is an ArtistNode

        Instance Attributes:
            - sp: an instance of the Spotify API class from the spotipy library
        """
    sp: spotipy.Spotify

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent similar artists to its parent node.
    #      _subtrees will be None if we reach the user's given diversity level
    #  - _artist: the current node of the tree
    #  - _user: the user datatype holding the user's inputs
    _subtrees: list[ArtistTree]
    _artist: Optional[ArtistNode]
    _user: User

    def __init__(self, _artist: Optional[ArtistNode], _subtrees: list[ArtistTree],
                 user: User, sp: spotipy.Spotify) -> None:
        """Initialize a new artist tree.

        Note that this initializer uses optional arguments.

        """
        self._artist = _artist
        self._subtrees = _subtrees
        self._user = user
        self.sp = sp

    def __contains__(self, artist: ArtistNode) -> bool:
        """Return whether this tree contains given the given ArtistNode
        """
        if self.is_empty():
            return False
        elif not self._subtrees:
            return self._artist.artist_id == artist.artist_id
        else:
            if self._artist.artist_id == artist.artist_id:
                return True
            for subtree in self._subtrees:
                if subtree.__contains__(artist):
                    return True
            return False

    def is_empty(self) -> bool:
        """Return whether this tree is empty.
        """
        return self._artist is None

    def min_difference_score(self, min_song: dict | None, d: int = 0) -> dict[int: SongInfo]:
        """Finds and returns the SongInfo with the least difference_score at each depth.

        The SongInfo will be returned with a dictionary, with the key being the depth of the SongInfo
        object in the ArtistTree and the associated value being the SongInfo object with the least_difference
        score at the depth of its key value.

        If there is a tie, it will recommend the first song
        """
        if self.is_empty():
            return {}

        if min_song is None:
            min_song = {}

        differences_root = {}

        for song in self._artist.top_tracks:
            if hasattr(song, 'difference_score'):
                differences_root[song.difference_score] = song

        differences_root = {song_info.difference_score: song_info for song_info in self._artist.top_tracks}
        least_difference_root = differences_root[min(differences_root)]

        if d in min_song:
            if min_song[d].difference_score > least_difference_root.difference_score:
                min_song[d] = least_difference_root
        else:
            min_song[d] = least_difference_root

        for subtree in self._subtrees:
            rec_value = subtree.min_difference_score(min_song, d + 1)
            if d + 1 in min_song:
                if rec_value != {} and min_song[d + 1].difference_score > rec_value[d + 1].difference_score:
                    min_song[d + 1] = rec_value[d + 1]
            else:
                min_song[d + 1] = rec_value[d + 1]
        return min_song

    def populate_subtrees(self, d: int, original_tree: Optional[ArtistTree] = None) -> None:
        """Recurssivly adds related artists as subtrees until the tree has a height of d

        Preconetions:
        - d >= 0
        """
        if self.is_empty():
            return

        if d > 0:
            if original_tree is None:
                original_tree = ArtistTree(self._artist, self._subtrees, self._user, self.sp)

            self._populate_subtree(self._artist, original_tree)

        if d - 1 > 0:
            for subtree in self._subtrees:
                subtree.populate_subtrees(d - 1, original_tree)

    def _populate_subtree(self, artist: ArtistNode, original_tree: ArtistTree) -> None:
        """Adds related artists as subtrees to the tree whose root is the given artist
        """
        related_artists_dict = artist_five_related(artist, self.sp)
        related_artists_list = []

        for related_artist in related_artists_dict:
            related_artist_node = ArtistNode(related_artist, related_artists_dict[related_artist], self._user, self.sp)
            if related_artist_node not in original_tree:
                related_artists_list.append(related_artist_node)

        self._insert_subtrees(related_artists_list, artist)

    def _insert_subtrees(self, artists: list[ArtistNode], parent_node: ArtistNode) -> None:
        """Inserts the subtree(s) as subtrees of the parent node.
        Note: artists are the related artists to the parent node"""
        if self.is_empty() or artists == []:
            return None

        elif self._artist == parent_node:
            for artist in artists:
                artist_tree = ArtistTree(artist, [], self._user, self.sp)
                self._subtrees.append(artist_tree)
            return None

        else:
            for subtree in self._subtrees:
                subtree._insert_subtrees(artists, parent_node)
            return None


def artist_five_related(artist: ArtistNode, sp: spotipy.Spotify) -> dict:
    """Get the top 5 most related artists to the input artist. Return a dictionary where the key is the artist's
    name and the value is the artist's id.
    """
    related_artist = sp.artist_related_artists(artist.artist_id)

    related_users = {}
    for external_urls in related_artist['artists']:
        if len(related_users) == 5:
            return related_users
        else:
            related_users[external_urls['name']] = external_urls['id']

    return related_users


def get_artist_id(artist_name: str, sp: spotipy.Spotify) -> str:
    """Get the given artit's id.

    Preconditions:
    - The artist_name must be written the way it is on their spotify profile.
    """
    results = sp.search(q=artist_name, type='artist', limit=1)
    ids = results["artists"]["items"][0]["id"]
    return ids


def artist_five_tracks(artist_name: str, artist_id: str, user: User, sp: spotipy.Spotify, country: str = 'CA') \
        -> dict:
    """Return 5 random top tracks from the given artist.
    """
    top_tracks = sp.artist_top_tracks(artist_id, country)

    track_names = {}
    for item in top_tracks['tracks']:
        if user.song_name not in item['name']:
            track_names[item['name']] = artist_name

    if len(list(track_names.items())) >= 5:
        random_five = random.sample(list(track_names.items()), k=5)
        return dict(random_five)
    else:
        return track_names


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
        'extra-imports': ['random', 'spotipy', 'user']
    })
