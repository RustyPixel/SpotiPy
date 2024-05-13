import os
import dotenv

def generate_auth_url():
    """
    Generates the authentication URL for Spotify.

    Returns:
        str: The authentication URL.
    """
    # Finds and loads .env file
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    # Generates authentication URL
    redirect_url = f"http://{os.getenv('IP')}:{os.getenv('PORT')}/callback"
    scopes = ["user-library-read", "user-read-playback-state", "user-read-recently-played"]
    auth_url = f"https://accounts.spotify.com/authorize?client_id={os.getenv('CLIENT_ID')}&response_type=code&redirect_uri={redirect_url}&scope={'+'.join(scopes)}"

    return auth_url
