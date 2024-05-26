import subprocess
import socket

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

def telnet(host: str, port: int, timeout=5):
    """
    Check if a specific port on a host is open.
    Returns True if the port is open, False otherwise.
    """
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        # Try to connect to the host and port
        sock.connect((host, port))
    except socket.error:
        return False
    finally:
        sock.close()
    return True

def read_file(source):
    with open(f'static/{source}', 'r', encoding="utf-8") as file:
        # Read the entire contents of the file
        content = file.read()
        return content

def write_to_file(source, value):
    with open(f'static/{source}', 'w', encoding="utf-8") as file:
    # Write new content to the file
        file.write(value)
