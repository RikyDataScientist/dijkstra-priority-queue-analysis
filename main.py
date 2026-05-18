"""
main.py — Entry Point Utama Proyek
====================================
Jalankan file ini untuk:
1. Demo sederhana pada graf contoh (cocok untuk video demo)
2. Benchmark performa ketiga heap
3. Visualisasi graf dan grafik perbandingan

Cara menjalankan:
    python main.py             # demo + benchmark + visualisasi
    python main.py --demo      # hanya demo sederhana
    python main.py --bench     # hanya benchmark
    python main.py --no-plot   # tanpa visualisasi (hanya teks)

Referensi artikel:
    Brodal, G. S. (2024). Priority queues with decreasing keys.
    Theoretical Computer Science, 1000, 114563.
    https://doi.org/10.1016/j.tcs.2024.114563
"""

import sys
import os

# Tambahkan direktori proyek ke path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from src.graph_generator import create_sample_graph, generate_random_edges
from src.djikstra import (
    dijkstra_basic,
    dijkstra_binary_heap,
    dijkstra_fibonacci_heap,
    dijkstra_postorder_heap,
    reconstruct_path,
)
from src.benchmark import (
    run_single_benchmark,
    run_scalability_benchmark,
    run_density_benchmark,
    print_detailed_result,
)


def demo_simple():
    """
    Demo sederhana pada graf kecil 6 node.
    Cocok ditampilkan saat video demo.
    """
    print("\n" + "=" * 55)
    print("  DEMO: Dijkstra pada Graf Kecil (6 Node)")
    print("  Artikel: Brodal (2024), TCS Vol. 1000")
    print("=" * 55)

    graph = create_sample_graph()
    source = 0
    target = 4

    print(f"\n{graph}")
    print(f"\nMencari jalur terpendek dari Node {source} ke Node {target}...")

    heaps = [
        ("Basic Dijkstra", dijkstra_basic),
        ("Binary Heap", dijkstra_binary_heap),
        ("Fibonacci Heap", dijkstra_fibonacci_heap),
        ("Post-order Heap", dijkstra_postorder_heap),
    ]

    for name, func in heaps:
        distances, predecessors, exec_time, ops = func(graph, source)
        path = reconstruct_path(predecessors, source, target)
        path_str = " -> ".join(map(str, path)) if path else "tidak ada jalur"

        print(f"\n  [{name}]")
        print(f"    Jalur     : {path_str}")
        print(f"    Jarak     : {distances[target]}")
        print(f"    Waktu     : {exec_time*1000:.4f} ms")
        print(f"    Operasi   : {ops}")
        print(
            f"    Jarak semua node: {[d if d < float('inf') else 'INF' for d in distances]}"
        )


def demo_benchmark():
    """Jalankan benchmark lengkap."""
    # Benchmark satu graf medium
    print("\n  Menjalankan benchmark pada graf 300 node...")
    graph = generate_random_edges(300, 900)
    result = run_single_benchmark(graph, source=0, runs=5)
    print_detailed_result(result, "Benchmark Graf 300 Node (rata-rata 5 percobaan)")

    # Benchmark skalabilitas
    scalability = run_scalability_benchmark(
        node_sizes=[50, 100, 200, 500], edge_multiplier=3
    )

    # Benchmark kepadatan
    run_density_benchmark()

    return scalability


def show_visualizations(scalability_data: list = None):
    """Tampilkan semua visualisasi."""
    try:
        import matplotlib.pyplot as plt
        from src.visualization import (
            visualize_graph_with_path,
            compare_all_heaps_on_graph,
            plot_benchmark_results,
            plot_bar_comparison,
        )

        print("\n  Membuat visualisasi...")

        # 1. Visualisasi graf contoh dengan satu heap
        # 1. Visualisasi graf contoh dengan Basic Dijkstra
        graph = create_sample_graph()

        d, p, _, _ = dijkstra_basic(graph, 0)

        fig1 = visualize_graph_with_path(
            graph, d, p, source=0, target=4, heap_name="Basic Dijkstra"
        )
        fig1.savefig("asset/output_graf_basic.png", dpi=150, bbox_inches="tight")

        # 2. Perbandingan ketiga heap pada satu graf
        fig2 = compare_all_heaps_on_graph(graph, source=0, target=4)
        fig2.savefig("asset/output_komparasi_heap.png", dpi=150, bbox_inches="tight")

        # 3. Grafik benchmark (jika data tersedia)
        if scalability_data:
            fig3 = plot_benchmark_results(scalability_data, metric="avg_time_ms")
            fig3.savefig("asset/output_benchmark_waktu.png", dpi=150, bbox_inches="tight")

            fig4 = plot_benchmark_results(scalability_data, metric="avg_operations")
            fig4.savefig("asset/output_benchmark_operasi.png", dpi=150, bbox_inches="tight")

            # Bar chart untuk satu ukuran
            idx_mid = len(scalability_data) // 2
            fig5 = plot_bar_comparison(scalability_data[idx_mid])
            fig5.savefig("asset/output_bar_comparison.png", dpi=150, bbox_inches="tight")

        print("Gambar disimpan: asset/output_*.png")
        plt.show()

    except ImportError:
        print("  [INFO] matplotlib/networkx tidak terinstall.")
        print("  Jalankan: pip install matplotlib networkx")


def main():
    """Fungsi utama — jalankan semua komponen proyek."""
    args = sys.argv[1:]

    print("\n" + "*" * 55)
    print("  Re-Implementasi Analisis Performa Priority Queue")
    print("  untuk Algoritma Dijkstra (Brodal, 2024)")
    print("*" * 55)

    run_demo = "--demo" in args or len(args) == 0
    run_bench = "--bench" in args or len(args) == 0
    no_plot = "--no-plot" in args

    scalability_data = None

    if run_demo:
        demo_simple()

    if run_bench:
        scalability_data = demo_benchmark()

    if not no_plot:
        show_visualizations(scalability_data)
    else:
        print("\n  Lewati visualisasi (--no-plot).")

    print("\n" + "=" * 55)
    print("  Selesai! Lihat output_*.png untuk visualisasi.")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
