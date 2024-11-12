import socket
import threading

# Endereço e porta do servidor
SERVER_IP = '82.112.245.62'
SERVER_PORT = 6969

# Dicionário para armazenar clientes conectados {endereço: socket}
clients = {}
server_lock = threading.Lock()

def handle_client(client_socket, client_address):
    with server_lock:
        clients[client_address] = client_socket
    print(f"[LOG] Cliente conectado: {client_address}")

    try:
        client_socket.send("AGUARDANDO AUTORIZAÇÃO DO SERVIDOR...\n".encode('utf-8'))
        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg:
                print(f"[{client_address}] {msg}")
    except ConnectionResetError:
        print(f"[LOG] Cliente desconectado: {client_address}")
    finally:
        with server_lock:
            del clients[client_address]
        client_socket.close()

def list_clients():
    print("\nClientes conectados:")
    with server_lock:
        for i, (addr, _) in enumerate(clients.items(), start=1):
            print(f"{i}. {addr}")
    print()

def select_client():
    list_clients()
    try:
        choice = int(input("Selecione um cliente pelo número (ou 0 para voltar): "))
        with server_lock:
            if 0 < choice <= len(clients):
                addr, sock = list(clients.items())[choice - 1]
                return sock, addr  # Corrige ordem para start_chat.
    except ValueError:
        pass
    return None

def start_chat(client_socket, client_address):
    client_socket.send("CONEXÃO AUTORIZADA\n".encode('utf-8'))
    print(f"[CHAT INICIADO] Conversando com {client_address}")

    while True:
        msg = input(f"[SERVIDOR - {client_address}]: ")
        if msg.lower() == 'menu':
            client_socket.send("CHAT EM STANDBY. AGUARDE...\n".encode('utf-8'))
            break
        client_socket.send(f"[SERVIDOR]: {msg}\n".encode('utf-8'))

def main_menu():
    while True:
        print("\n--- MENU DO SERVIDOR ---")
        print("1. Listar clientes conectados")
        print("2. Iniciar chat com cliente")
        print("3. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            list_clients()
        elif choice == '2':
            selected = select_client()
            if selected:
                client_socket, client_address = selected  # Segue nova ordem de desempacotamento
                start_chat(client_socket, client_address)
        elif choice == '3':
            print("Encerrando servidor...")
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(5)
    print(f"[STARTING] Servidor iniciado em {SERVER_IP}:{SERVER_PORT}")

    threading.Thread(target=main_menu, daemon=True).start()

    while True:
        try:
            client_socket, client_address = server.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()
        except KeyboardInterrupt:
            print("\n[SERVER] Encerrando...")
            break

if __name__ == "__main__":
    main()
