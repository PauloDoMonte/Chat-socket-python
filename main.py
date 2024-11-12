# main.py

import socket
import sys
from settings import SERVER_IP
from server.server import main as start_server
from client.client import main as start_client

def get_local_ip():
    """
    Returns the local IP address of the machine.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))  # An IP address that will likely always be reachable
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'  # If there's an error, fall back to localhost
    finally:
        s.close()
    return local_ip

def main():
    """
    Main entry point of the program. Checks the local machine's IP
    and starts the server or client accordingly.
    """
    local_ip = get_local_ip()
    print(f"Local IP Address: {local_ip}")
    
    if local_ip == SERVER_IP:
        print("[INFO] Starting as Server...")
        start_server()  # Inicia o servidor
    else:
        print("[INFO] Starting as Client...")
        start_client()  # Inicia o cliente

if __name__ == "__main__":
    main()
