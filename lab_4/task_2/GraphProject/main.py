import copy
from WirthAdjacencyListGraph import WirthAdjacencyListGraph


def main():
    print("ДЕМОНСТРАЦИЯ НЕОРИЕНТИРОВАННОГО ГРАФА (МОДИФИЦИРОВАННАЯ СТРУКТУРА ВИРТА)")
    print("=" * 60)

    graph = WirthAdjacencyListGraph[int]()

    for i in range(1, 6):
        graph.add_vertex(i)
        print(f"Добавлена вершина: {i}")

    edges = [(1, 2, 1.5), (2, 3, 2.0), (3, 4, 1.0), (4, 5, 1.5), (5, 1, 0.5)]
    for from_v, to_v, weight in edges:
        graph.add_edge(from_v, to_v, weight)
        print(f"Добавлено ребро: {from_v} -- {to_v} (вес: {weight})")

    print("\nТекущее состояние графа:")
    print(graph)

    print("\nПеребор вершин:")
    for vertex in graph.vertices():
        print(f"  Вершина: {vertex.value}")

    print("\nПеребор ребер:")
    edge_count = 0
    for edge in graph.edges():
        print(f"  Ребро: {edge.from_vertex.value} -- {edge.to_vertex.value} (вес: {edge.weight})")
        edge_count += 1

    print(f"Всего ребер в итераторе: {edge_count}")

    print("\nСмежные вершины для вершины 2:")
    for vertex in graph.adjacent_vertices(2):
        print(f"  Смежная вершина: {vertex.value}")

    print("\nПроверка операций сравнения:")
    graph_copy = copy.deepcopy(graph)
    print(f"  Оригинал и копия равны: {graph == graph_copy}")

    print("\nУдаление ребра 1-2:")
    graph.remove_edge(1, 2)
    print(f"  Ребро 1-2 существует: {graph.has_edge(1, 2)}")
    print(f"  Ребро 2-1 существует: {graph.has_edge(2, 1)}")

    print("\nУдаление вершины 3:")
    graph.remove_vertex(3)
    print(f"  Вершина 3 существует: {graph.has_vertex(3)}")
    print(f"  Ребро 2-3 существует: {graph.has_edge(2, 3)}")

    print("\nОчистка графа:")
    try:
        graph.clear()
        print(f"  Граф пуст: {graph.empty()}")
        print(f"  Количество вершин: {graph.vertex_count()}")
        print(f"  Количество ребер: {graph.edge_count()}")
        print("   Очистка выполнена успешно")
    except Exception as e:
        print(f"  Ошибка при очистке: {e}")

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")


if __name__ == "__main__":
    main()