from utils.constants import CLIENT_WAIT_MSG

def handle_client(client_socket, client_address, clients, server_lock):
    """
    Handles incoming client connections, receiving and sending messages.
    """
    with server_lock:
        clients[client_address] = client_socket
    print(f"[LOG] Client connected: {client_address}")

    try:
        client_socket.send(CLIENT_WAIT_MSG.encode('utf-8'))
        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg:
                print(f"[{client_address}] {msg}")
    except ConnectionResetError:
        print(f"[LOG] Client disconnected: {client_address}")
    finally:
        with server_lock:
            del clients[client_address]
        client_socket.close()
