import requests
import os
import json
from dotenv import load_dotenv
from .GetImageFromId import get_image_from_id
from .UpdateAccessToken import update_access_token

def get_current_song(access_token):
    """
    Gets the currently playing song.

    Args:
        access_token (str): The user's access token.

    Returns:
        dict: Dictionary containing song information:
            {
                playing (bool): Playing status.
                song_name (str): The song title.
                artist_name (str): The artists' names.
                album_id (str): The album ID.
                album_url (str): The album image URL.
                error (bool): Error status.
            }
    """
    load_dotenv()

    current_play = {}

    url = "https://api.spotify.com/v1/me/player/currently-playing"

    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }

    # Gets currently playing song
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = json.loads(response.text)

        # If song is currently playing
        if data['is_playing']:
            current_play["playing"] = True

            # Get song name
            current_play["songName"] = data['item']['name']

            # Get song artist
            # List all the artists
            artists = data['item']['artists']
            current_play["artistName"] = ', '.join([artist['name'] for artist in artists])

            #get the album ID 
            current_play["albumId"] = data['item']['album']['id']

            # Get album URL
            current_play["albumUrl"] = get_image_from_id(current_play["albumId"], access_token)
    
        # If not playing
        else:
            current_play["playing"] = False       
    
    # If access token revoked
    elif response.status_code == 401:
        tokens = update_access_token(None, os.getenv('RT')) 
        return get_current_song(tokens["AT"])

    else:
        current_play["error"] = True

    return current_play




