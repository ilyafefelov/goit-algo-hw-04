import timeit
import random
import json
import os

RESULTS_FILE = 'sorting_results.json'

# Алгоритми сортування

# Реалізація сортування злиттям
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

# Реалізація сортування вставками
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# Використання вбудованого сортування Timsort
def timsort(arr):
    return sorted(arr)

# Функція для вимірювання часу виконання
def measure_time(sort_func, arr):
    start_time = timeit.default_timer()
    sort_func(arr.copy())
    end_time = timeit.default_timer()
    return end_time - start_time

# Генерація даних
random.seed(0)
small_data = [random.randint(0, 100) for _ in range(10)]
medium_data = [random.randint(0, 1000) for _ in range(1000)]
large_data = [random.randint(0, 10000) for _ in range(10000)]

# Вимірювання часу виконання
algorithms = {
    "Merge Sort": merge_sort,
    "Insertion Sort": insertion_sort,
    "Timsort": timsort
}

datasets = {
    "Small Data": small_data,
    "Medium Data": medium_data,
    "Large Data": large_data
}

results = {algorithm: {dataset: 0 for dataset in datasets} for algorithm in algorithms}

for algo_name, algo_func in algorithms.items():
    for data_name, data in datasets.items():
        results[algo_name][data_name] = measure_time(algo_func, data)

# Завантаження попередніх результатів
if os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, 'r') as file:
        previous_results = json.load(file)
else:
    previous_results = {}

# Оновлення результатів
for algo_name, algo_results in results.items():
    if algo_name not in previous_results:
        previous_results[algo_name] = {}
    for data_name, time_taken in algo_results.items():
        if data_name not in previous_results[algo_name]:
            previous_results[algo_name][data_name] = []
        previous_results[algo_name][data_name].append(time_taken)

# Збереження оновлених результатів
with open(RESULTS_FILE, 'w') as file:
    json.dump(previous_results, file, indent=4)

# Виведення результатів
for algo_name, algo_results in previous_results.items():
    print(f"{algo_name}:")
    for data_name, times in algo_results.items():
        avg_time = sum(times) / len(times)
        print(f"  {data_name}: {avg_time:.6f} seconds (average over {len(times)} runs)")

# Збереження результатів в файл README.md
with open('README.md', 'w') as f:
    f.write("# Порівняльний аналіз алгоритмів сортування\n\n")
    f.write("### Результати вимірювань часу виконання:\n")
    for algo_name, algo_results in previous_results.items():
        f.write(f"**{algo_name}**:\n")
        for data_name, times in algo_results.items():
            avg_time = sum(times) / len(times)
            f.write(f"- {data_name}: {avg_time:.6f} seconds (average over {len(times)} runs)\n")
