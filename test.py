import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app_client_id = "10ad55033d8d48dc9b90c9aa1e6d074c"
app_client_secret = "1aa0b1b3d6a94f00a1125c24394a886e"


client_credentials_manager = SpotifyClientCredentials(client_id=app_client_id, client_secret=app_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def artist_id(artist_name: str) -> str | None:
    """Get the given artit's id. 
    
    Preconditions: The artist_name must be written the way it is on their spotify profile.
    """
    results = sp.search(q=artist_name, type='artist', limit=1)
    if artist_name == results["artists"]["items"][0]["name"]:
        ids = results["artists"]["items"][0]["id"]
        return ids
    else:
        print("This artist does not exist.")
        return


def artist_5_related(artist_name: str) -> dict | None:
    """Get the top 5 most related artists to the input artist. Return a dictionary where the key is the artist's 
    name and the value is the artist's id.
    """
    ids = artist_id(artist_name)
    if ids is None:
        return 

    related_artist = sp.artist_related_artists(ids)

    related_users = {}
    for external_urls in related_artist['artists']:
        if len(related_users) == 5:
            return related_users
        else:
            related_users[external_urls['name']] = external_urls['id']

    return related_users


def artist_5_top_songs(artist_name: str, country: str = 'CA') -> dict | None:
    ids = artist_id(artist_name)
    if ids is None:
        return

    top_tracks = sp.artist_top_tracks(ids, country)

    top_five = {}
    for item in top_tracks['tracks']:
        if len(top_five) == 5:
            return top_five
        else:
            top_five[item['name']] = artist_name
