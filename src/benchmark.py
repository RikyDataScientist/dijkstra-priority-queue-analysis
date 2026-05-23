"""
benchmark.py — Pengukuran dan Perbandingan Performa
=====================================================
Modul ini menjalankan eksperimen benchmark untuk membandingkan
performa keempat implementasi Dijkstra pada berbagai ukuran graf.

Metrik yang diukur:
    - Waktu eksekusi (detik)
    - Jumlah operasi heap
    - Throughput (node diproses per detik)

Referensi artikel:
    Brodal (2024), Section 7 — Experimental evaluation
"""

import statistics
from src.graph_generator import Graph, generate_random_edges, create_dense_graph
from src.dijkstra import dijkstra_basic, dijkstra_binary_heap, dijkstra_fibonacci_heap, dijkstra_postorder_heap, verify_results


def run_single_benchmark(graph: Graph, source: int = 0,
                          runs: int = 4) -> dict:
    """
    Jalankan benchmark pada satu graf dengan beberapa kali percobaan.

    Args:
        graph  : Graf yang diuji
        source : Node asal
        runs   : Jumlah percobaan (rata-rata diambil)

    Returns:
        dict berisi hasil benchmark untuk keempat heap
    """
    results = {
        "Basic Dijkstra": {"times": [], "operations": []},
        "Binary Heap"   : {"times": [], "operations": []},
        "Fibonacci Heap": {"times": [], "operations": []},
        "Post-order Heap": {"times": [], "operations": []},
    }

    for _ in range(runs):
        d0, p0, t0, ops0 = dijkstra_basic(graph, source)
        results["Basic Dijkstra"]["times"].append(t0)
        results["Basic Dijkstra"]["operations"].append(ops0)
        # Binary Heap
        d1, p1, t1, ops1 = dijkstra_binary_heap(graph, source)
        results["Binary Heap"]["times"].append(t1)
        results["Binary Heap"]["operations"].append(ops1)

        # Fibonacci Heap
        d2, p2, t2, ops2 = dijkstra_fibonacci_heap(graph, source)
        results["Fibonacci Heap"]["times"].append(t2)
        results["Fibonacci Heap"]["operations"].append(ops2)

        # Post-order Heap
        d3, p3, t3, ops3 = dijkstra_postorder_heap(graph, source)
        results["Post-order Heap"]["times"].append(t3)
        results["Post-order Heap"]["operations"].append(ops3)

    # Verifikasi kebenaran hasil
    is_correct = verify_results(d0, d1, d2, d3)

    # Hitung rata-rata
    summary = {"correct": is_correct, "num_nodes": graph.num_nodes}
    for heap_name, data in results.items():
        avg_time = statistics.mean(data["times"])
        avg_ops  = statistics.mean(data["operations"])
        throughput = graph.num_nodes / avg_time if avg_time > 0 else 0

        summary[heap_name] = {
            "avg_time_ms"  : avg_time * 1000,  # konversi ke milidetik
            "avg_operations": int(avg_ops),
            "throughput"   : throughput,
        }

    return summary


def run_scalability_benchmark(node_sizes: list = None,
                               edge_multiplier: int = 4) -> list:
    """
    Uji skalabilitas - bagaimana performa berubah seiring bertambahnya node.
    """

    if node_sizes is None:
        node_sizes = [50, 100, 200, 500, 1000]

    print("\n" + "="*90)
    print("  BENCHMARK SKALABILITAS - Dijkstra dengan 4 Variasi")
    print("="*90)

    print(
        f"  {'Nodes':>6} | "
        f"{'Basic (ms)':>12} | "
        f"{'Binary (ms)':>12} | "
        f"{'Fibonacci (ms)':>14} | "
        f"{'Post-order (ms)':>15} | OK?"
    )

    print("-"*90)

    all_results = []
    gr = None

    for n in node_sizes:
        num_edges = n * edge_multiplier
        graph     = generate_random_edges(n, num_edges)
        if n == node_sizes[-1]:
            gr = graph  # Simpan graf terbesar untuk analisis lebih lanjut

        result = run_single_benchmark(graph, source=0, runs=4)

        all_results.append({"nodes": n, **result})

        t_basic = result["Basic Dijkstra"]["avg_time_ms"]
        t_bin   = result["Binary Heap"]["avg_time_ms"]
        t_fib   = result["Fibonacci Heap"]["avg_time_ms"]
        t_post  = result["Post-order Heap"]["avg_time_ms"]

        ok = "[OK]" if result["correct"] else "BUG!"

        print(
            f"  {n:>6} | "
            f"{t_basic:>12.3f} | "
            f"{t_bin:>12.3f} | "
            f"{t_fib:>14.3f} | "
            f"{t_post:>15.3f} | "
            f"{ok}"
        )

    print("="*90)

    return all_results, gr


def run_density_benchmark() -> list:
    """
    Uji pengaruh kepadatan graf terhadap performa.
    """

    configs = [
        {"type": "sparse",   "nodes": 200, "edges": 400},
        {"type": "medium",   "nodes": 200, "edges": 1000},
        {"type": "dense",    "nodes": 200, "edges": 3000},
        {"type": "complete", "nodes": 50,  "edges": None},
    ]

    print("\n" + "="*90)
    print("  BENCHMARK KEPADATAN GRAF")
    print("="*90)

    print(
        f"  {'Tipe':>10} | "
        f"{'Basic (ms)':>12} | "
        f"{'Binary (ms)':>12} | "
        f"{'Fibonacci (ms)':>14} | "
        f"{'Post-order (ms)':>15}"
    )

    print("-"*90)

    results = []

    for cfg in configs:

        if cfg["type"] == "complete":
            graph = create_dense_graph(cfg["nodes"])
        else:
            graph = generate_random_edges(cfg["nodes"], cfg["edges"])

        result = run_single_benchmark(graph, source=0, runs=3)

        results.append({"config": cfg, **result})

        t_basic = result["Basic Dijkstra"]["avg_time_ms"]
        t_bin   = result["Binary Heap"]["avg_time_ms"]
        t_fib   = result["Fibonacci Heap"]["avg_time_ms"]
        t_post  = result["Post-order Heap"]["avg_time_ms"]

        print(
            f"  {cfg['type']:>10} | "
            f"{t_basic:>12.3f} | "
            f"{t_bin:>12.3f} | "
            f"{t_fib:>14.3f} | "
            f"{t_post:>15.3f}"
        )

    print("="*90)

    return results


def print_detailed_result(result: dict, title: str = "Hasil Benchmark"):
    """Cetak hasil benchmark secara detail."""
    print(f"\n{'-'*50}")
    print(f"  {title}")
    print(f"  Graf: {result['num_nodes']} node | Hasil benar: {result['correct']}")
    print(f"{'-'*50}")

    for heap_name in ["Basic Dijkstra", "Binary Heap", "Fibonacci Heap", "Post-order Heap"]:
        data = result[heap_name]
        print(f"\n  [{heap_name}]")
        print(f"    Waktu rata-rata : {data['avg_time_ms']:.4f} ms")
        print(f"    Operasi heap    : {data['avg_operations']:,}")
        print(f"    Throughput      : {data['throughput']:.0f} node/detik")

    print(f"{'-'*50}")
