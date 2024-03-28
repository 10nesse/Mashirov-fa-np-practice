import socket
import threading
from colorama import init, Fore, Style
from itertools import cycle

init()

HOST_ADDR = "localhost"
HOST_PORT = 8080
clients = []
clients_names = []
color_cycle = cycle([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])

def send_receive_client_message(client_connection, client_ip_addr):
    client_name = client_connection.recv(4096).decode()
    clients_names.append(client_name)
    print(Fore.GREEN + f"{client_name} has joined the chat." + Style.RESET_ALL)

    # Генерируем бесконечную последовательность цветов для каждого пользователя
    user_colors = {}

    while True:
        user_colors.setdefault(client_name, next(color_cycle))
        data = client_connection.recv(4096).decode()
        if not data or data == "exit":
            break

        # Выводим сообщение с подсвеченным именем пользователя в его уникальном цвете
        print(user_colors[client_name] + f"{client_name}: " + Style.RESET_ALL + data)

    # Client is leaving
    print(Fore.RED + f"{client_name} has left the chat." + Style.RESET_ALL)
    idx = clients.index(client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.close()

def accept_clients(the_server):
    while True:
        client, addr = the_server.accept()
        clients.append(client)
        threading.Thread(target=send_receive_client_message, args=(client, addr)).start()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)
    print(f"Server started on port {HOST_PORT}...")
    accept_clients(server)

if __name__ == "__main__":
    start_server()
