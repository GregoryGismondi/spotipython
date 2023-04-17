# spotipython - The Python Spotify Song Recommender
This project was made by Amy Li, Brittany Lansang, and Gregory Gismondi for CSC111 Final Group Project.

This project uses the Spotify Web API and Tree ADT to recommend users songs based on their favourite song's characteristics in comparison to the songs of related artists.
Users can specify the song they want, the song's artist, how deep of a search they want to do, 
and if they want to focus on a specific characteristic of their favourite song (danceability, valence, tempo, instrumentalness, energy, and acousticness)

Before using, please make sure the spotipy library is downloaded. 
The other libraries in requirements.txt were required inclusions for final submission, but not necessary to run the program.

To run the program, call the recommend_song() function from the main.py file and input based on the promts given.

To run an example of the program, call the example_recommend() function from the main.py file, which gives the input of 'Cruel Summer' by Taylor Swift,
a diversity level of 1, and a focus on the 'danceability' of the song.

As this was completed for a group project, there will most likely not be any future updates for bug fixes or extra features.
