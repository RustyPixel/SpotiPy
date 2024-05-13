import requests
import base64
import os

from dotenv import load_dotenv
from .UpdateEnv import update_env_var
from .GetAccessToken import get_spotify_access_token

def update_access_token(auth_code, refresh_token):
    """
    Updates the user's access token and saves it to environment.

    Args:
        auth_code (str): The user's authorization code.
        refresh_token (str): The user's refresh token.

    Returns:
        dict: Dictionary containing access token ('AT') and refresh token ('RT').
    """

    # Reloads .env file
    load_dotenv()

    # Get user's access token
    tokens = get_spotify_access_token(auth_code, refresh_token)

    # Add access token to environment
    update_env_var("AT", tokens["AT"])

    # If refresh token present
    if tokens["RT"] is not None:
        # Add refresh token to environment
        update_env_var("RT", tokens["RT"])

    return tokens
