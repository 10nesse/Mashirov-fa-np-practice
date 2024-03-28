import socket
import threading

def client_handler(connection, address):
    current_thread = threading.current_thread()
    print(f"[{current_thread.name}] Подключен клиент: {address}")
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            connection.sendall(data)
            print(f"[{current_thread.name}] Эхо-отправлено сообщение клиенту {address}")
    except Exception as e:
        print(f"[{current_thread.name}] Ошибка при обработке клиента {address}: {e}")
    finally:
        connection.close()
        print(f"[{current_thread.name}] Клиент {address} отключен")

def echo_server(host='', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Сервер запущен и слушает порт {port}")
        while True:
            conn, addr = server_socket.accept()
            # Здесь мы используем имя потока, созданного для каждого подключения клиента
            client_thread = threading.Thread(target=client_handler, args=(conn, addr), name=f"ClientThread-{addr[0]}:{addr[1]}")
            client_thread.start()

if __name__ == "__main__":
    echo_server()
