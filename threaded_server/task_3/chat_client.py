import socket
import threading

HOST_ADDR = "localhost"
HOST_PORT = 8080


def receive_message_from_server(sck):
    while True:
        from_server = sck.recv(4096).decode()
        if not from_server:
            break
        print("\n" + from_server)


def send_message_to_server(sck):
    while True:
        msg = input("Введите сообщение (или 'exit' для выхода): ")
        sck.send(msg.encode())
        if msg == "exit":
            break


def connect_to_server(name):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST_ADDR, HOST_PORT))
    client.send(name.encode())  # Отправляем имя на сервер

    # Поток для приема сообщений от сервера
    threading.Thread(target=receive_message_from_server, args=(client,)).start()

    # Поток для отправки сообщений на сервер
    threading.Thread(target=send_message_to_server, args=(client,)).start()

    # Ожидаем завершения потоков перед закрытием соединения
    client.recv(4096)
    client.close()


if __name__ == "__main__":
    username = input("Введите ваше имя пользователя: ")
    connect_to_server(username)
