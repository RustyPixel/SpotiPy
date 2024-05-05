import socket

def getIp():
    """
    Gets the IP address of the local device.

    Returns:
        str: The IP address of the local device.
    """
    try:
        # Get the hostname
        hostname = socket.gethostname()
        # Get the IP address corresponding to the hostname
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        print("Error:", e)
        return None
