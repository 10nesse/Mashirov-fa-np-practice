import socket
import threading
import logging
import sys

# Настройки сервера
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8888
LOG_FILE = 'server.log'
IDENTIFICATION_FILE = 'identification.txt'

# Флаг для остановки сервера
server_running = True

# Настройка логгирования
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Функция для обработки клиентских запросов
def handle_client(client_socket, address):
    logging.info(f'Соединение установлено с {address}')
    client_socket.send('Соединение установлено.\n'.encode())

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        # Ваша логика обработки запросов от клиента

    logging.info(f'Соединение с {address} закрыто')
    client_socket.close()

# Функция для прослушивания портов
def start_server():
    global server_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    logging.info(f'Сервер запущен на порту {SERVER_PORT}')

    while server_running:
        try:
            client_socket, address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
            client_handler.start()
        except KeyboardInterrupt:
            logging.info('Получен сигнал остановки сервера.')
            break

    server_socket.close()

# Функция для очистки файла идентификации
def clear_identification_file():
    open(IDENTIFICATION_FILE, 'w').close()
    print('Файл идентификации очищен.')

# Главная функция программы
def main():
    global server_running
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    print("Для просмотра списка команд введите 'help'.")

    while True:
        command = input('Введите команду: ')
        if command == 'stop':
            logging.info('Остановка сервера...')
            server_running = False
            sys.exit(0)
        elif command == 'pause':
            logging.info('Приостановка прослушивания порта...')
            # Добавьте вашу логику для приостановки прослушивания порта
        elif command == 'resume':
            logging.info('Возобновление прослушивания порта...')
            # Добавьте вашу логику для возобновления прослушивания порта
        elif command == 'show_logs':
            with open(LOG_FILE, 'r') as f:
                print(f.read())
        elif command == 'clear_logs':
            open(LOG_FILE, 'w').close()
            print('Логи очищены.')
        elif command == 'clear_identification_file':
            clear_identification_file()
        elif command == 'help':
            print("Список команд:")
            print("stop - остановить сервер")
            print("pause - приостановить прослушивание порта")
            print("resume - возобновить прослушивание порта")
            print("show_logs - показать логи")
            print("clear_logs - очистить логи")
            print("clear_identification_file - очистить файл идентификации")
            print("help - показать это сообщение")
        else:
            print('Неверная команда.')

    server_thread.join()
    logging.info('Сервер остановлен.')

if __name__ == "__main__":
    main()
