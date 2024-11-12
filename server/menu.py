from server.client_manager import ClientManager

def main_menu():
    """
    Displays the server's main menu, allowing server-side operations like
    listing connected clients and starting a chat with a selected client.
    """
    client_manager = ClientManager()

    while True:
        print("\n--- SERVER MENU ---")
        print("1. List connected clients")
        print("2. Start chat with client")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            client_manager.list_clients()
        elif choice == '2':
            selected = client_manager.select_client()
            if selected:
                client_socket, client_address = selected
                client_manager.start_chat(client_socket, client_address)
        elif choice == '3':
            print("Shutting down server...")
            break
