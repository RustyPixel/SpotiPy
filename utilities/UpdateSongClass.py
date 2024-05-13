import os
from dotenv import load_dotenv
from .GetPlaying import get_current_song


class Worker:
    """
    Class to update the currently playing song.
    """

    switch = False
    unit_of_work = 0

    def __init__(self, socketio):
        """
        Initialize Worker object.

        Args:
            socketio: (socketio) The socketio socket.
        """
        # Initialize class variables
        self.socketio = socketio
        self.switch = True
        

    def update_song(self, app, socketio):
        """
        Updates the currently playing song.

        Args:
            app (dict): The current app object.
            socketio (socketio): The socketio socket.
        """
        with app.app_context():
            # Reloads .env file
            load_dotenv()

            # If access token is present
            if "AT" in os.environ:
                # While socket still open
                while self.switch:
                    load_dotenv()
                    currently_playing = get_current_song(os.getenv("AT"))
                    socketio.emit('updateSong', {'data':  currently_playing})
                    socketio.sleep(10)

    def stop(self):
        """
        Stops the update_song function.
        """
        # Stop the loop
        self.switch = False
