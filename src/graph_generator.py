import random
import pandas as pd


class Graph:

    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.adjacency_list = {i: [] for i in range(num_nodes)}

    def add_edge(self, u, v, weight, directed=False):
        if weight < 0:
            raise ValueError("Dijkstra membutuhkan bobot non-negatif!")

        self.adjacency_list[u].append((v, weight))
        if not directed:
            self.adjacency_list[v].append((u, weight))

    def neighbors(self, node):
        return self.adjacency_list[node]

    def __repr__(self):
        lines = [f"Graf dengan {self.num_nodes} node:"]
        for u, edges in self.adjacency_list.items():
            for v, w in edges:
                lines.append(f"  {u} --{w}--> {v}")
        return "\n".join(lines)

def generate_random_edges(num_nodes, num_edges, max_weight=20, directed=False):
    graph = Graph(num_nodes)

    possible_edges = []

    for u in range(num_nodes):
        for v in range(num_nodes):
            if u != v:
                possible_edges.append((u, v))

    random.shuffle(possible_edges)

    selected_edges = possible_edges[:num_edges]

    for u, v in selected_edges:
        w = random.randint(1, max_weight)
        graph.add_edge(u, v, w, directed)

    return graph

def data_from_file(path):
    df = pd.read_csv(path)
    max_node = max(df['id1'].max(), df['id2'].max())
    graph = Graph(max_node + 1)
    for _, row in df.iterrows():
        graph.add_edge(row['id1'], row['id2'], row['dist'], True)
    return graph

def create_sample_graph():
    graph = Graph(7)
    graph.add_edge(0, 1, 7)
    graph.add_edge(0, 2, 9)
    graph.add_edge(0, 5, 14)
    graph.add_edge(1, 2, 10)
    graph.add_edge(1, 3, 15)
    graph.add_edge(1, 6, 17)
    graph.add_edge(2, 3, 11)
    graph.add_edge(2, 5, 2)
    graph.add_edge(3, 4, 6)
    graph.add_edge(3, 5, 7)
    graph.add_edge(4, 5, 9)
    graph.add_edge(4, 6, 12)
    graph.add_edge(5, 6, 4)
    return graph

def create_dense_graph(num_nodes: int, max_weight: int = 50) -> Graph:
    g = Graph(num_nodes)
    for u in range(num_nodes):
        for v in range(u + 1, num_nodes):
            w = random.randint(1, max_weight)
            g.add_edge(u, v, w)
    return g

def save_graph_to_csv(graph: Graph, filename: str):
    edges = []
    for u, neighbors in graph.adjacency_list.items():
        for v, w in neighbors:
            if u < v:  # Hindari duplikasi untuk graf tidak berarah
                edges.append({'id1': u, 'id2': v, 'dist': w})
    df = pd.DataFrame(edges)
    df.to_csv(f'data/{filename}.csv', index=False)
