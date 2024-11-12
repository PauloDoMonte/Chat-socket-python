import socket

# Endereço e porta do servidor
SERVER_IP = '82.112.245.62'
SERVER_PORT = 6969

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    print("[CLIENTE] Conectado ao servidor. Aguardando servidor entrar no chat...")

    while True:
        msg = client.recv(1024).decode('utf-8')
        if msg:
            print(msg)

if __name__ == "__main__":
    main()
