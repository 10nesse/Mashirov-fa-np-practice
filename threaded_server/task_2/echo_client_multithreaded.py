import socket

def echo_client(server_host='localhost', server_port=12345):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_host, server_port))
            print("Подключен к серверу. Введите 'exit' для выхода.")
            while True:
                message = input("Сообщение: ")
                if message.lower() == 'exit':
                    break
                client_socket.sendall(message.encode('utf-8'))
                data = client_socket.recv(1024)
                print(f"Эхо: {data.decode('utf-8')}")
    except ConnectionRefusedError:
        print("Не удается подключиться к серверу. Проверьте, запущен ли сервер.")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 12345
    echo_client(HOST, PORT)
