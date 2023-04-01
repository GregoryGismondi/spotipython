import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def get_artist_uri(artist_name: str) -> str | None:
    """Get artist uri

    Preconditions: Must write the artist name how it is on their spotify profile
    """
    results = sp.search(q=artist_name, type='artist', limit=1)
    if artist_name == results["artists"]["items"][0]["name"]:
        ids = results["artists"]["items"][0]["id"]
        return ids
    else:
        print("This artist does not exist.")
        return


def artist_5_related(artist_name: str) -> list | None:
    """Get the top 5 most related artists to the artist they're related to."""
    uri = get_artist_uri(artist_name)
    if uri is None:
        return None

    related_artist = sp.artist_related_artists(uri)

    related_users = []
    for external_urls in related_artist['artists']:
        if len(related_users) == 5:
            return related_users
        else:
            related_users.append(external_urls['name'])

    return related_users
