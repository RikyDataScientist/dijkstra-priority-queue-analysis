"""
dijkstra.py — Algoritma Dijkstra dengan 3 Variasi Priority Queue
=================================================================
Implementasi algoritma Dijkstra (Single Source Shortest Path / SSSP)
menggunakan tiga variasi priority queue untuk perbandingan performa.

Setiap fungsi dijkstra_* menerima Graf dan node sumber, lalu
mengembalikan jarak terpendek ke semua node beserta path-nya.

Referensi artikel:
    Brodal, G. S. (2024). Priority queues with decreasing keys.
    Theoretical Computer Science, 1000, 114563.
    https://doi.org/10.1016/j.tcs.2024.114563
"""

import time
from src.graph_generator import Graph
from priority_queue.binary_heap import BinaryHeap
from priority_queue.fibonacci_heap import FibonacciHeap
from priority_queue.post_order_heap import PostOrderHeap


# ─── Konstanta ──────────────────────────────────────────────────────────────

INF = float('inf')

def dijkstra_basic(graph: Graph, source: int) -> tuple:
    """
    Dijkstra Basic (manual tanpa priority queue).

    Kompleksitas:
        O(V^2)

    Args:
        graph  : Graf berbobot (Graph object)
        source : Node asal (integer)

    Returns:
        (distances, predecessors, execution_time, num_operations)

        - distances[v]    : jarak terpendek dari source ke v
        - predecessors[v] : node sebelum v pada jalur terpendek
        - execution_time  : waktu eksekusi dalam detik
        - num_operations  : jumlah operasi utama algoritma
    """

    start_time = time.perf_counter()

    n = graph.num_nodes

    # Inisialisasi
    distances = [INF] * n
    predecessors = [None] * n
    visited = [False] * n

    distances[source] = 0

    num_operations = 0

    # ── Algoritma Utama ──────────────────────────────────────────────
    for _ in range(n):

        # Cari node dengan jarak minimum
        # yang belum dikunjungi
        min_distance = INF
        u = None

        for v in range(n):
            num_operations += 1

            if not visited[v] and distances[v] < min_distance:
                min_distance = distances[v]
                u = v

        # Tidak ada node yang dapat dijangkau
        if u is None:
            break

        # Tandai node sudah diproses
        visited[u] = True

        # Relaksasi semua tetangga
        for neighbor, weight in graph.neighbors(u):

            num_operations += 1

            if not visited[neighbor]:

                new_dist = distances[u] + weight

                # Jika ditemukan jalur lebih pendek
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = u

    execution_time = time.perf_counter() - start_time

    return (
        distances,
        predecessors,
        execution_time,
        num_operations
    )

def dijkstra_binary_heap(graph: Graph, source: int) -> tuple:
    """
    Dijkstra menggunakan Binary Heap.

    Kompleksitas: O((V + E) log V)

    Args:
        graph  : Graf berbobot (Graph object)
        source : Node asal (integer)

    Returns:
        (distances, predecessors, execution_time, num_operations)
        - distances[v]    : jarak terpendek dari source ke v
        - predecessors[v] : node sebelum v pada jalur terpendek
        - execution_time  : waktu eksekusi dalam detik
        - num_operations  : jumlah operasi heap yang dilakukan
    """
    start_time = time.perf_counter()

    n           = graph.num_nodes
    distances   = [INF] * n
    predecessors = [None] * n
    distances[source] = 0
    num_operations    = 0

    # Inisialisasi Priority Queue
    pq = BinaryHeap()

    # Masukkan semua node ke PQ dengan jarak awal
    for v in range(n):
        pq.insert(v, distances[v])

    # ── Algoritma Utama ──────────────────────────────────────────────────
    while not pq.is_empty():
        # Ambil node dengan jarak terkecil (Extract-Min)
        dist_u, u = pq.extract_min()
        num_operations += 1

        # Jika jarak yang diambil lebih besar dari yang tersimpan,
        # berarti node ini sudah diproses → lewati
        if dist_u > distances[u]:
            continue

        # Relaksasi: periksa semua tetangga node u
        for v, weight in graph.neighbors(u):
            new_dist = distances[u] + weight

            # Jika jalur lewat u lebih pendek → update!
            if new_dist < distances[v]:
                distances[v]    = new_dist
                predecessors[v] = u

                # Update priority di PQ (DecreaseKey)
                if pq.contains(v):
                    pq.decrease_key(v, new_dist)
                    num_operations += 1

    execution_time = time.perf_counter() - start_time
    return distances, predecessors, execution_time, num_operations


def dijkstra_fibonacci_heap(graph: Graph, source: int) -> tuple:
    """
    Dijkstra menggunakan Fibonacci Heap.

    Kompleksitas teoritis terbaik: O(E + V log V)
    DecreaseKey amortized O(1) — unggul untuk graf sparse dan banyak relaksasi.

    Args:
        graph  : Graf berbobot (Graph object)
        source : Node asal (integer)

    Returns:
        (distances, predecessors, execution_time, num_operations)
    """
    start_time = time.perf_counter()

    n            = graph.num_nodes
    distances    = [INF] * n
    predecessors = [None] * n
    distances[source] = 0
    num_operations    = 0

    pq = FibonacciHeap()

    # Inisialisasi
    for v in range(n):
        pq.insert(v, distances[v])

    # ── Algoritma Utama ──────────────────────────────────────────────────
    while not pq.is_empty():
        dist_u, u = pq.extract_min()
        num_operations += 1

        if dist_u > distances[u]:
            continue

        for v, weight in graph.neighbors(u):
            new_dist = distances[u] + weight

            if new_dist < distances[v]:
                distances[v]    = new_dist
                predecessors[v] = u

                if pq.contains(v):
                    pq.decrease_key(v, new_dist)
                    num_operations += 1

    execution_time = time.perf_counter() - start_time
    return distances, predecessors, execution_time, num_operations


def dijkstra_postorder_heap(graph: Graph, source: int) -> tuple:
    """
    Dijkstra menggunakan Post-order Heap (Brodal, 2024).

    Modifikasi dari Binary Heap yang menggunakan post-order traversal
    untuk mendukung DecreaseKey lebih efisien dalam praktik.

    Referensi: Brodal (2024), "Priority queues with decreasing keys"

    Args:
        graph  : Graf berbobot (Graph object)
        source : Node asal (integer)

    Returns:
        (distances, predecessors, execution_time, num_operations)
    """
    start_time = time.perf_counter()

    n            = graph.num_nodes
    distances    = [INF] * n
    predecessors = [None] * n
    distances[source] = 0
    num_operations    = 0

    pq = PostOrderHeap()

    # Inisialisasi
    for v in range(n):
        pq.insert(v, distances[v])

    # ── Algoritma Utama ──────────────────────────────────────────────────
    while not pq.is_empty():
        dist_u, u = pq.extract_min()
        num_operations += 1

        if dist_u > distances[u]:
            continue

        for v, weight in graph.neighbors(u):
            new_dist = distances[u] + weight

            if new_dist < distances[v]:
                distances[v]    = new_dist
                predecessors[v] = u

                if pq.contains(v):
                    pq.decrease_key(v, new_dist)
                    num_operations += 1

    execution_time = time.perf_counter() - start_time
    return distances, predecessors, execution_time, num_operations


# ─── Utilitas ───────────────────────────────────────────────────────────────

def reconstruct_path(predecessors: list, source: int, target: int) -> list:
    """
    Rekonstruksi jalur terpendek dari source ke target.

    Args:
        predecessors : list hasil Dijkstra
        source       : node asal
        target       : node tujuan

    Returns:
        List node yang membentuk jalur terpendek, atau [] jika tidak ada jalur.
    """
    path = []
    current = target

    while current is not None:
        path.append(current)
        current = predecessors[current]

    path.reverse()

    # Validasi: jalur valid harus dimulai dari source
    if path and path[0] == source:
        return path
    return []  # tidak ada jalur


def verify_results(dist1: list, dist2: list, dist3: list, dist4: list) -> bool:
    """
    Verifikasi bahwa ketiga implementasi menghasilkan hasil yang sama.
    Jika hasilnya berbeda, ada bug dalam implementasi.

    Returns:
        True jika ketiga hasil identik (dalam toleransi floating point)
    """
    tolerance = 1e-9
    for i in range(len(dist1)):
        d1, d2, d3, d4 = dist1[i], dist2[i], dist3[i], dist4[i]

        # Tangani kasus INF
        both_inf = (d1 == INF and d2 == INF and d3 == INF and d4 == INF)
        if both_inf:
            continue

        if (abs(d1 - d2) > tolerance or abs(d1 - d3) > tolerance or abs(d1 - d4) > tolerance):
            return False
    return True
