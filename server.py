import socket
import threading

# Endereço e porta do servidor
SERVER_IP = '82.112.245.62'
SERVER_PORT = 6969

# Lista para armazenar clientes conectados
clients = []
server_ready = threading.Event()

def handle_client(client_socket, client_address):
    print(f"[LOG] Cliente conectado: {client_address}")
    clients.append(client_socket)

    # Espera até que o servidor "entre no chat"
    server_ready.wait()

    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break
            print(f"[{client_address}] {msg}")
            broadcast(f"[{client_address}] {msg}", client_socket)
        except ConnectionResetError:
            break

    print(f"[LOG] Cliente desconectado: {client_address}")
    clients.remove(client_socket)
    client_socket.close()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message.encode('utf-8'))

def server_chat():
    server_ready.set()
    print("[SERVIDOR] Você entrou no chat!")
    while True:
        msg = input("[SERVIDOR]: ")
        broadcast(f"[SERVIDOR]: {msg}", None)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(5)
    print(f"[STARTING] Servidor iniciado em {SERVER_IP}:{SERVER_PORT}")

    threading.Thread(target=server_chat, daemon=True).start()

    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    main()
