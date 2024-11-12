# server/server.py

import socket
import threading
from server.menu import main_menu
from server.client_manager import ClientManager
from utils.constants import SERVER_IP, SERVER_PORT

def main():
    """
    Server program that listens for incoming client connections
    and manages client interactions.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((SERVER_IP, SERVER_PORT))
        server.listen(5)
        print(f"[STARTING] Server started on {SERVER_IP}:{SERVER_PORT}")

        threading.Thread(target=main_menu, daemon=True).start()

        client_manager = ClientManager()

        while True:
            try:
                client_socket, client_address = server.accept()
                threading.Thread(target=client_manager.handle_client, args=(client_socket, client_address), daemon=True).start()
            except KeyboardInterrupt:
                print("\n[SERVER] Shutting down...")
                break
    finally:
        server.close()