from flask import Flask, render_template, request, redirect, send_from_directory, make_response, current_app
from flask_socketio import SocketIO, emit
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import os

from utilities.GetIp import get_ip  # Importing function to get IP address
from utilities.UpdateEnv import update_env_var  # Importing function to update environment variables
from utilities.GenerateAuthUrl import generate_auth_url  # Importing function to generate authentication URL
from utilities.UpdateSongClass import Worker  # Importing Worker class to update song
from utilities.UpdateAccessToken import update_access_token  # Importing function to update access token

# Set up the root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO) # DEBUG or INFO

# Configure logging to file
log_file = 'app.log'
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 10, backupCount=10)
file_handler.setFormatter(formatter)

# Configure logging to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Set up logging to console based on a configuration flag
log_to_console = True  # Set to False to turn off logging to console

if log_to_console:
    root_logger.addHandler(console_handler)

# Set up logging to file based on a configuration flag
log_to_file = False  # Set to False to turn off logging to file

if log_to_file:
    root_logger.addHandler(file_handler)

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')  # Set async_mode to 'gevent'

# Load environment variables from .env file
load_dotenv()

HOST = os.environ.get('IP', '0.0.0.0')
PORT = int(os.environ.get('PORT', '8000'))

@app.route("/")
def index():
    load_dotenv()
    if "AT" in os.environ:
        return render_template("index.html", currentlyPlaying={})  # Render index.html template
    else:
        return redirect("/auth-app")  # Redirect to authentication page if access token is not present

@app.route("/auth-app")
def auth_app():
    auth_url = generate_auth_url()  # Generate authentication URL
    return render_template("authApp.html", authUrl=auth_url)  # Render authApp.html template with auth URL

@app.route("/callback")
def callback():
    load_dotenv()
    auth_code = request.args.get("code")  # Get authorization code from callback
    update_access_token(auth_code, None)  # Update access token using authorization code
    return redirect("/")  # Redirect to root URL

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static/images"), "SpotiPy.ico", mimetype='image/vnd.microsoft.icon')

@app.before_first_request
def initialize_app_variables():
    load_dotenv()
    if 'IP' not in os.environ:
        update_env_var("IP", get_ip())  # Update IP environment variable if not present
    if 'PORT' not in os.environ:
        os.environ['PORT'] = '8000'
        update_env_var("PORT", '8000')  # Update PORT environment variable if not present
    current_app.config['workers'] = {}  # Initialize workers dictionary in app configuration

@socketio.on('connect')
def test_connect(auth):
    emit('my response', {'data': 'Connected'})  # Emit 'my response' event on connection

@socketio.on('disconnect')
def test_disconnect():
    sid = request.sid  # Get session ID
    if "workers" in current_app.config and sid in current_app.config['workers']:
        current_app.config['workers'][sid].stop()  # Stop worker associated with session ID on disconnection

@socketio.on("message")
def handle_message(data):
    sid = request.sid  # Get session ID
    worker = Worker(socketio)  # Create Worker instance
    socketio.start_background_task(worker.update_song, current_app._get_current_object(), socketio)  # Start background task to update song
    if "workers" in current_app.config:
        current_app.config['workers'][sid] = worker  # Add worker to workers dictionary

def wait_for_enter():
    input(f"Press Enter to shutdown server...\n\n")
    shutdown_server()

def shutdown_server():
    print("Shutting down server...")
    socketio.stop()
    print("Server shutdown complete.")
    os._exit(0)  # Use os._exit() to force exit without cleanup

if __name__ == "__main__":
    print(f"\nhttp://{HOST}:{PORT}\n")
    threading.Thread(target=wait_for_enter).start()
    socketio.run(app, host=HOST, port=PORT)  # Run the application with SocketIO
