import threading
from utils.constants import AUTHORIZED_MSG

class ClientManager:
    """
    Manages connected clients, including adding, listing, selecting,
    and handling chats.
    """
    def __init__(self):
        self.clients = {}
        self.server_lock = threading.Lock()

    def handle_client(self, client_socket, client_address):
        """
        Handles communication with a client, including receiving and sending messages.
        """
        handle_client(client_socket, client_address, self.clients, self.server_lock)

    def list_clients(self):
        """
        Lists all currently connected clients.
        """
        print("\nConnected clients:")
        with self.server_lock:
            for i, (addr, _) in enumerate(self.clients.items(), start=1):
                print(f"{i}. {addr}")
        print()

    def select_client(self):
        """
        Prompts the server to select a client for chat.
        """
        self.list_clients()
        try:
            choice = int(input("Select a client by number (or 0 to go back): "))
            with self.server_lock:
                if 0 < choice <= len(self.clients):
                    addr, sock = list(self.clients.items())[choice - 1]
                    return sock, addr
        except ValueError:
            pass
        return None

    def start_chat(self, client_socket, client_address):
        """
        Starts a chat session with a selected client.
        """
        client_socket.send(AUTHORIZED_MSG.encode('utf-8'))
        print(f"[CHAT STARTED] Chatting with {client_address}")

        def receive_messages():
            """
            Handles receiving messages from the client during the chat.
            """
            while True:
                try:
                    msg = client_socket.recv(1024).decode('utf-8')
                    if msg:
                        print(f"[{client_address}] {msg}")
                except Exception as e:
                    print(f"[ERROR] Failed to receive message from {client_address}: {e}")
                    break

        def send_messages():
            """
            Handles sending messages to the client during the chat.
            """
            while True:
                msg = input(f"[SERVER - {client_address}]: ")
                if msg.lower() == 'menu':
                    client_socket.send("CHAT ON STANDBY. PLEASE WAIT...\n".encode('utf-8'))
                    break
                client_socket.send(f"[SERVER]: {msg}\n".encode('utf-8'))

        # Start receiving and sending messages in separate threads
        threading.Thread(target=receive_messages, daemon=True).start()
        threading.Thread(target=send_messages, daemon=True).start()
