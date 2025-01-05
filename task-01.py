import networkx as nx
import pandas as pd

# Побудова графа
def build_graph():
    G = nx.DiGraph()
    edges = [
        ('Термінал 1', 'Склад 1', 25),
        ('Термінал 1', 'Склад 2', 20),
        ('Термінал 1', 'Склад 3', 15),
        ('Термінал 2', 'Склад 3', 15),
        ('Термінал 2', 'Склад 4', 30),
        ('Термінал 2', 'Склад 2', 10),
        ('Склад 1', 'Магазин 1', 15),
        ('Склад 1', 'Магазин 2', 10),
        ('Склад 1', 'Магазин 3', 20),
        ('Склад 2', 'Магазин 4', 15),
        ('Склад 2', 'Магазин 5', 10),
        ('Склад 2', 'Магазин 6', 25),
        ('Склад 3', 'Магазин 7', 20),
        ('Склад 3', 'Магазин 8', 15),
        ('Склад 3', 'Магазин 9', 10),
        ('Склад 4', 'Магазин 10', 20),
        ('Склад 4', 'Магазин 11', 10),
        ('Склад 4', 'Магазин 12', 15),
        ('Склад 4', 'Магазин 13', 5),
        ('Склад 4', 'Магазин 14', 10),
    ]
    for edge in edges:
        G.add_edge(edge[0], edge[1], capacity=edge[2])
    return G

# Додавання "суперджерела" і "суперстока"
def add_super_source_sink(graph, sources, sinks):
    graph.add_node('Суперджерело')
    graph.add_node('Суперстік')
    for source in sources:
        graph.add_edge('Суперджерело', source, capacity=float('inf'))
    for sink in sinks:
        graph.add_edge(sink, 'Суперстік', capacity=float('inf'))
    return 'Суперджерело', 'Суперстік'

# Алгоритм Едмондса-Карпа
def max_flow_analysis(graph, source, sink):
    flow_value, flow_dict = nx.maximum_flow(graph, source, sink, flow_func=nx.algorithms.flow.edmonds_karp)
    return flow_value, flow_dict

# Перетворення результатів у таблицю
def convert_results_to_table(flow_dict, sources, sinks, graph):
    rows = []
    for source in sources:
        for sink in sinks:
            flow = 0
            for intermediate in flow_dict[source]:
                if sink in flow_dict[intermediate]:
                    flow += flow_dict[intermediate][sink]
            # Перевірка на пропускну здатність
            if flow > graph[source][intermediate].get('capacity', 0):
                flow = graph[source][intermediate].get('capacity', 0)  # Обмежуємо потік пропускною здатністю
            rows.append([source, sink, flow])
    return pd.DataFrame(rows, columns=["Термінал", "Магазин", "Фактичний Потік (одиниць)"])

# Аналіз вузьких місць
def find_bottlenecks(graph, flow_dict):
    bottlenecks = []
    for u, v, data in graph.edges(data=True):
        потік = flow_dict[u].get(v, 0)
        пропускна_здатність = data['capacity']
        if потік == пропускна_здатність:
            bottlenecks.append((u, v, потік, пропускна_здатність))
    return bottlenecks

# Побудова графа
graph = build_graph()

# Визначення джерел і стоків
sources = ['Термінал 1', 'Термінал 2']
sinks = [
    'Магазин 1', 'Магазин 2', 'Магазин 3', 'Магазин 4', 'Магазин 5', 'Магазин 6',
    'Магазин 7', 'Магазин 8', 'Магазин 9', 'Магазин 10', 'Магазин 11', 'Магазин 12',
    'Магазин 13', 'Магазин 14'
]

# Додавання "суперджерела" і "суперстока"
super_source, super_sink = add_super_source_sink(graph, sources, sinks)

# Розрахунок максимального потоку
flow_value, flow_dict = max_flow_analysis(graph, super_source, super_sink)

# Конвертуємо результати в таблицю
result_table = convert_results_to_table(flow_dict, sources, sinks, graph)

# Визначення вузьких місць
bottlenecks = find_bottlenecks(graph, flow_dict)

# Аналіз терміналів
terminal_flows = result_table.groupby("Термінал")["Фактичний Потік (одиниць)"].sum()

# Аналіз магазинів
store_flows = result_table.groupby("Магазин")["Фактичний Потік (одиниць)"].sum().sort_values()

# Вивід результатів
print(f"Максимальний потік: {flow_value}\n")
print("Таблиця результатів:")
print(result_table.to_string(index=False))
print("\nВузькі місця (ребра, які повністю використовують пропускну здатність):")
for u, v, потік, пропускна_здатність in bottlenecks:
    print(f"{u} -> {v}: Потік = {потік}, Пропускна здатність = {пропускна_здатність}")

print("\nЗагальний потік по терміналах:")
print(terminal_flows)

print("\nМагазини з найменшим постачанням:")
print(store_flows)
