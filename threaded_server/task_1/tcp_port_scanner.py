import socket
import threading
from tqdm import tqdm
from queue import Queue

def scan_port(hostname, port, result_dict, queue):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((hostname, port)) == 0:
                result_dict[port] = True
    except Exception as e:
        pass
    finally:
        queue.put(port)  # Сигнализируем о завершении обработки порта

def main():
    hostname = input("Введите имя хоста или IP-адрес: ")
    port_range = range(1, 65536)
    open_ports = {}
    threads = []
    queue = Queue()  # Для отслеживания обработанных портов

    print("Начало сканирования портов...")
    progress_bar = tqdm(total=len(port_range), desc="Сканирование", unit="порт")

    for port in port_range:
        thread = threading.Thread(target=scan_port, args=(hostname, port, open_ports, queue))
        threads.append(thread)
        thread.start()

        if len(threads) >= 100:  # Ограничение на максимальное количество одновременно работающих потоков
            while not queue.empty():
                queue.get()
                progress_bar.update(1)

            # Ждем завершения всех потоков в текущей группе, прежде чем продолжить
            for t in threads:
                t.join()
            threads = []

    # Дождаться завершения оставшихся потоков и обработать оставшуюся очередь
    for thread in threads:
        thread.join()
    while not queue.empty():
        queue.get()
        progress_bar.update(1)

    progress_bar.close()

    print("\nСканирование завершено. Открытые порты:")
    for port in sorted(open_ports):
        print(f"Порт {port} открыт")

if __name__ == "__main__":
    main()
