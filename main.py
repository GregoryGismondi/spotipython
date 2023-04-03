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
        print("\nThe recommended song at depth " + str(depth) + " is: " + least_difference[depth].song_name + " by " +
              least_difference[depth].artist_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    recommend_song()
