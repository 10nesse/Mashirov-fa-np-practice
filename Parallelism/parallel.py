from multiprocessing import Pool, cpu_count, Event
import numpy as np
import time
import random

# Функция для перемножения одного элемента матрицы
def element(args):
    i, j, N, matrix1, matrix2 = args
    res = 0
    
    for k in range(N):
        res += matrix1[i][k] * matrix2[k][j]
    return res

# Функция для параллельного перемножения матриц
def multiply_matrices_parallel(event, min_matrix_size, max_matrix_size):
    while not event.is_set():  # Проверяем событие на установку
        matrix_size = random.randint(min_matrix_size, max_matrix_size)
        matrix1 = np.random.randint(0, 10, size=(matrix_size, matrix_size))
        matrix2 = np.random.randint(0, 10, size=(matrix_size, matrix_size))

        N = len(matrix1[0])
        M = len(matrix1)

        # Определяем количество процессов пропорционально квадратному корню от общего числа элементов в матрицах
        num_processes = int(np.sqrt(N * M))

        # Ограничиваем количество процессов минимальным значением 1
        num_processes = max(num_processes, 1)

        print("Matrix size:", matrix_size)
        print("Number of processes:", num_processes)

        # Создаем пул процессов
        with Pool(processes=num_processes) as pool:
            # Создаем список аргументов для каждого элемента матрицы
            args_list = [(i, j, N, matrix1, matrix2) for i in range(M) for j in range(N)]
            # Выполняем перемножение матриц параллельно
            results = pool.map(element, args_list)

        # Преобразуем результат в матрицу
        result_matrix = np.array(results).reshape((M, N))
        print("Matrix 1:")
        print(matrix1)
        print("Matrix 2:")
        print(matrix2)
        print("Result:")
        print(result_matrix)
        print()

        # Ждем некоторое время перед генерацией следующей пары матриц
        time.sleep(2)

if __name__ == '__main__':
    min_matrix_size = 2
    max_matrix_size = 5
    stop_event = Event()

    try:
        multiply_matrices_parallel(stop_event, min_matrix_size, max_matrix_size)
    except KeyboardInterrupt:
        print("Process stopped.")
        stop_event.set()
