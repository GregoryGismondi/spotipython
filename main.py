"""CSC111: Spotipython Project - Main File

This Python file contains the recommend_song() function
which is responsible for recommending a song.

This file also contains the main block, consisting of
the code necessary to run our program.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Amy Li, Brittany Lansang, and Gregory Gismondi.
"""

import artist_tree
import creator
import user as user_py


def recommend_song() -> None:
    """Recommends song based off of user's input
    """
    user = creator.create_user()
    app = creator.create_app()

    user_artist = artist_tree.ArtistNode(user.artist_name, None, user, app)
    user_tree = artist_tree.ArtistTree(user_artist, [], user, app)

    user_tree.populate_subtrees(user.diversity_level, None)
    least_difference = user_tree.min_difference_score(None)

    for depth in least_difference:
        print("\nThe recommended song at depth " + str(depth) + " is " + least_difference[depth].song_name + " by " +
              least_difference[depth].artist_name)


def example_recommend() -> None:
    """An example of recommend_song() that does not take in any user input.

    The example is for the song Cruel Summer by Taylor Swift, with a diveristy score of 1
    and the favourite characteristic being dancability
    """
    user = user_py.User('Cruel Summer', 'Taylor Swift', 'danceability', 1)
    app = creator.create_app()

    user_artist = artist_tree.ArtistNode(user.artist_name, None, user, app)
    user_tree = artist_tree.ArtistTree(user_artist, [], user, app)

    user_tree.populate_subtrees(user.diversity_level, None)
    least_difference = user_tree.min_difference_score(None)

    for depth in least_difference:
        print("\nThe recommended song at depth " + str(depth) + " is " + least_difference[depth].song_name + " by " +
              least_difference[depth].artist_name)


# Press the green button in the gutter to run the script.
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
    #     'max-line-length': 120,
    #     'extra-imports': ['random', 'spotipy', 'user', 'artist_tree', 'creator'],
    #     'allowed-io': ['print']
    # })

    # This function will take the user's input:
    recommend_song()

    # This function uses an example song (Cruel Summer by Taylor Swift)
    # example_recommend()
