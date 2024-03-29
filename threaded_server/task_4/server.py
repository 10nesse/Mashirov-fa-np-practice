import socket
import threading
import os
import logging

HOST = 'localhost'
PORT = 8080
LOG_FILE = 'server.log'
IDENTIFICATION_FILE = 'identification.txt'

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

server_paused = False

def listen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)

        while True:
            if not server_paused:
                conn, addr = server_socket.accept()
                with conn:
                    logging.info('Connected by %s', addr)
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

def control_server():
    global server_paused

    while True:
        command = input("Введите команду: ").strip().lower()

        if command == 'exit':
            os._exit(0)
        elif command == 'pause':
            server_paused = True
            logging.info("Сервер приостановлен.")
            print("Сервер приостановлен.")
        elif command == 'resume':
            server_paused = False
            logging.info("Сервер возобновлен.")
            print("Сервер возобновлен.")
        elif command == 'show logs':
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'r') as log_file:
                    print(log_file.read())
            else:
                print("Лог файл не найден.")
        elif command == 'clear logs':
            if os.path.exists(LOG_FILE):
                open(LOG_FILE, 'w').close()
                logging.info("Логи очищены.")
                print("Логи очищены.")
            else:
                print("Лог файл не найден.")
        elif command == 'clear identification':
            if os.path.exists(IDENTIFICATION_FILE):
                open(IDENTIFICATION_FILE, 'w').close()
                logging.info("Файл идентификации очищен.")
                print("Файл идентификации очищен.")
            else:
                print("Файл идентификации не найден.")
        else:
            print("Неизвестная команда.")

if not os.path.exists(LOG_FILE):
    open(LOG_FILE, 'w').close()

if not os.path.exists(IDENTIFICATION_FILE):
    open(IDENTIFICATION_FILE, 'w').close()

with open(IDENTIFICATION_FILE, 'a') as identification_file:
    identification_file.write("Server started\n")

# Создание и запуск потоков
listen_thread = threading.Thread(target=listen)
control_thread = threading.Thread(target=control_server)

listen_thread.start()
control_thread.start()

# Ожидание завершения работы потоков
listen_thread.join()
control_thread.join()

print("Сервер завершил работу.")
