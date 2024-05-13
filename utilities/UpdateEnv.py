import os
import dotenv

def update_env_var(var_name, new_value):
    """
    Updates an environment variable.

    Args:
        var_name (str): The name of the variable.
        new_value (str): The value of the variable.

    Returns:
        bool: True if successful.
    """
    # Finds and loads .env file
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    # Updates environment variable
    os.environ[var_name] = new_value

    # Adds or updates a key/value
    dotenv.set_key(dotenv_file, var_name, os.environ[var_name])

    return True
