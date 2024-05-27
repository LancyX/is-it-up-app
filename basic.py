import os
import subprocess
import socket
from datetime import datetime
import pytz

def ping(host):
    """
    Ping a host and return True if the host responds, False otherwise.
    """
    command = ['ping', '-c', '1', '-W', '2', host]
    try:
        subprocess.check_output(command)
        return True
    except subprocess.CalledProcessError:
        return False

async def crontask():
    now = datetime.now(pytz.timezone('Europe/Kyiv'))
    timestamp = now.strftime("%d/%m %H:%M:%S")

    known_status = read_file("status")

    power = telnet()

    if known_status == power:
        pass
    else:
        write_to_file(source="status", value=power)

    if known_status == power:
        pass
    else:
        write_to_file(source="last-change", value=timestamp)

    write_to_file(source="updated", value=timestamp)

def telnet():
    """
    Check if a specific port on a host is open.
    Returns True if the port is open, False otherwise.
    """
    host = os.getenv("HOME_HOST")
    port = int(os.getenv("HOME_PORT"))
    timeout = 5

    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        # Try to connect to the host and port
        sock.connect((host, port))
        return "1"
    except socket.error:
        return "0"
    finally:
        sock.close()

def read_file(source):
    with open(f'static/{source}', 'r', encoding="utf-8") as file:
        # Read the entire contents of the file
        content = file.read()
        return content

def write_to_file(source, value):
    with open(f'static/{source}', 'w', encoding="utf-8") as file:
    # Write new content to the file
        file.write(value)
