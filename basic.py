import os
import socket
from datetime import datetime
import pytz

async def crontask():
    now = datetime.now(pytz.timezone('Europe/Kyiv'))
    timestamp = now.strftime("%d/%m %H:%M:%S")

    known_status = await read_file("status")

    power = await telnet()

    if known_status == power:
        pass
    else:
        await write_to_file(source="status", value=power)

    if known_status == power:
        pass
    else:
        await write_to_file(source="last-change", value=timestamp)

    await write_to_file(source="updated", value=timestamp)

async def telnet():
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

async def read_file(source):
    with open(f'static/{source}', 'r', encoding="utf-8") as file:
        # Read the entire contents of the file
        content = file.read()
        return content

async def write_to_file(source, value):
    with open(f'static/{source}', 'w', encoding="utf-8") as file:
    # Write new content to the file
        file.write(value)
