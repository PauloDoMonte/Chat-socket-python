import socket
import threading
from utils.constants import SERVER_IP, SERVER_PORT

def receive_messages(client):
    """
    Handles receiving messages from the server.
    """
    while True:
        msg = client.recv(1024).decode('utf-8')
        print(msg)
        if "CONEXÃO AUTORIZADA" in msg:
            break

def send_messages(client):
    """
    Handles sending messages to the server.
    """
    while True:
        msg = input("[CLIENTE]: ")
        client.send(msg.encode('utf-8'))

def main():
    """
    Client program that connects to the server and sends/receives messages.
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    print("[CLIENTE] Conectado ao servidor.")

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
    threading.Thread(target=send_messages, args=(client,), daemon=True).start()
