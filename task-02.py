import timeit
import csv
from BTrees._OOBTree import OOBTree

# Функція для завантаження даних з CSV
def load_items(filename):
    items = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = {
                'ID': int(row['ID']),
                'Name': row['Name'],
                'Category': row['Category'],
                'Price': float(row['Price'])
            }
            items.append(item)
    return items

# Додавання товарів у OOBTree
def add_item_to_tree(tree, item):
    tree.insert(item['ID'], item)

# Додавання товарів у dict
def add_item_to_dict(dictionary, item):
    dictionary[item['ID']] = item

# Діапазонний запит для OOBTree
def range_query_tree(tree, min_price, max_price):
    result = []
    for item in tree.items(min_price, max_price):
        if min_price <= item[1]['Price'] <= max_price:
            result.append(item[1])
    return result

# Діапазонний запит для dict
def range_query_dict(dictionary, min_price, max_price):
    result = []
    for item in dictionary.values():
        if min_price <= item['Price'] <= max_price:
            result.append(item)
    return result

# Основна функція для порівняння продуктивності
def compare_performance(filename):
    items = load_items(filename)
    print(items[0])
    # Ініціалізація OOBTree та dict
    tree = OOBTree()
    dictionary = {}

    # Додавання товарів
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    # Визначаємо функцію для вимірювання часу
    def measure_time_query_tree():
        return range_query_tree(tree, 50, 150)

    def measure_time_query_dict():
        return range_query_dict(dictionary, 50, 150)

    # Вимірювання часу для OOBTree
    time_tree = timeit.timeit(measure_time_query_tree, number=100)

    # Вимірювання часу для dict
    time_dict = timeit.timeit(measure_time_query_dict, number=100)

    # Виведення результатів
    print(f"Total range_query time for OOBTree: {time_tree:.6f} seconds")
    print(f"Total range_query time for Dict: {time_dict:.6f} seconds")

# Виконати порівняння
compare_performance('generated_items_data.csv')
