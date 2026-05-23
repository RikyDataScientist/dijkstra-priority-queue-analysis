import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import networkx as nx
from src.dijkstra import reconstruct_path, dijkstra_basic, dijkstra_binary_heap, dijkstra_fibonacci_heap, dijkstra_postorder_heap


# Warna Tema

COLOR = {
    "basic" : "#D96C06",   # oranye
    "binary"    : "#1D9E75",   # hijau teal
    "fibonacci" : "#534AB7",   # ungu
    "postorder" : "#185FA5",   # biru
    "node_default" : "#E1F5EE",
    "node_source"  : "#1D9E75",
    "node_target"  : "#534AB7",
    "node_path"    : "#EF9F27",
    "edge_default" : "#B4B2A9",
    "edge_path"    : "#EF9F27",
    "bg"        : "#FAFAF8",
}


# Visualisasi Graf

def visualize_graph_with_path(graph, distances: list, predecessors: list,
                               source: int, target: int,
                               heap_name: str = "Binary Heap",
                               title: str = None):
    """
    Visualisasikan graf dan tandai jalur terpendek dari source ke target.

    Args:
        graph       : Graph object
        distances   : hasil jarak dari Dijkstra
        predecessors: hasil predecessor dari Dijkstra
        source      : node asal
        target      : node tujuan
        heap_name   : nama heap yang digunakan (untuk judul)
        title       : judul custom (opsional)
    """
    # Rekonstruksi jalur
    path = reconstruct_path(predecessors, source, target)

    # Buat graph networkx
    G = nx.DiGraph()
    G.add_nodes_from(range(graph.num_nodes))

    edge_labels = {}
    for u in range(graph.num_nodes):
        for v, w in graph.neighbors(u):
            G.add_edge(u, v, weight=w)
            edge_labels[(u, v)] = str(w)

    # Layout posisi node
    pos = nx.spring_layout(G, seed=42, k=2.0)

    # Tentukan warna node
    node_colors = []
    for node in G.nodes():
        if node == source:
            node_colors.append(COLOR["node_source"])
        elif node == target:
            node_colors.append(COLOR["node_target"])
        elif node in path:
            node_colors.append(COLOR["node_path"])
        else:
            node_colors.append(COLOR["node_default"])

    # Tentukan warna edge
    path_edges = set()
    for i in range(len(path) - 1):
        path_edges.add((path[i], path[i+1]))

    edge_colors = [COLOR["edge_path"] if (u, v) in path_edges
                   else COLOR["edge_default"] for u, v in G.edges()]
    edge_widths = [3.0 if (u, v) in path_edges else 1.0 for u, v in G.edges()]

    # Label node: tampilkan nomor + jarak
    INF = float('inf')
    node_labels = {}
    for node in G.nodes():
        d = distances[node]
        d_str = "∞" if d == INF else str(int(d)) if d == int(d) else f"{d:.1f}"
        node_labels[node] = f"{node}\n(d={d_str})"

    # Gambar
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor(COLOR["bg"])
    ax.set_facecolor(COLOR["bg"])

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors,
                           width=edge_widths, alpha=0.8,
                           arrows=True, arrowsize=20,
                           connectionstyle="arc3,rad=0.1")
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                           node_size=800, linewidths=1.5,
                           edgecolors="#5F5E5A")
    nx.draw_networkx_labels(G, pos, labels=node_labels, ax=ax,
                            font_size=8, font_weight="500")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax,
                                 font_size=8, label_pos=0.3)

    # Judul dan legenda
    if title is None:
        path_str  = " → ".join(map(str, path)) if path else "tidak ada"
        dist_str  = distances[target]
        dist_str  = "∞" if dist_str == INF else str(dist_str)
        title = (f"Dijkstra + {heap_name}\n"
                 f"Jalur terpendek {source}→{target}: {path_str}  (jarak = {dist_str})")

    ax.set_title(title, fontsize=13, fontweight="500", pad=15)
    ax.axis("off")

    # Legenda
    legend_elements = [
        mpatches.Patch(color=COLOR["node_source"],   label=f"Node asal ({source})"),
        mpatches.Patch(color=COLOR["node_target"],   label=f"Node tujuan ({target})"),
        mpatches.Patch(color=COLOR["node_path"],     label="Node pada jalur"),
        mpatches.Patch(color=COLOR["node_default"],  label="Node lainnya"),
        mpatches.Patch(color=COLOR["edge_path"],     label="Edge jalur terpendek"),
    ]
    ax.legend(handles=legend_elements, loc="lower left", fontsize=8,
              framealpha=0.9, facecolor=COLOR["bg"])

    plt.tight_layout()
    return fig


def compare_all_heaps_on_graph(graph, source: int = 0, target: int = None):
    """
    Tampilkan 4 visualisasi (satu per heap) secara berdampingan.
    """

    if target is None:
        target = graph.num_nodes - 1

    # Jalankan ketiga Dijkstra
    d0, p0, t0, _ = dijkstra_basic(graph, source)
    d1, p1, t1, _ = dijkstra_binary_heap(graph, source)
    d2, p2, t2, _ = dijkstra_fibonacci_heap(graph, source)
    d3, p3, t3, _ = dijkstra_postorder_heap(graph, source)

    fig, axes = plt.subplots(1, 4, figsize=(24, 6))
    fig.patch.set_facecolor(COLOR["bg"])

    configs = [
        (d0, p0, t0, "Basic Dijkstra", COLOR["basic"], axes[0]),
        (d1, p1, t1, "Binary Heap",    COLOR["binary"],    axes[1]),
        (d2, p2, t2, "Fibonacci Heap", COLOR["fibonacci"], axes[2]),
        (d3, p3, t3, "Post-order Heap", COLOR["postorder"], axes[3]),
    ]

    G = nx.DiGraph()
    G.add_nodes_from(range(graph.num_nodes))
    edge_labels = {}
    for u in range(graph.num_nodes):
        for v, w in graph.neighbors(u):
            G.add_edge(u, v, weight=w)
            edge_labels[(u, v)] = str(w)
    pos = nx.spring_layout(G, seed=42, k=2.0)

    for d, p, t, name, color, ax in configs:
        path = reconstruct_path(p, source, target)
        path_edges = set(zip(path, path[1:]))

        node_colors = [color if n in path else "#E5E3DB" for n in G.nodes()]
        if path:
            node_colors[source] = "#1D9E75"
            node_colors[target] = "#534AB7"

        edge_colors = [color if e in path_edges else "#C4C2BA"
                       for e in G.edges()]
        edge_widths = [2.5 if e in path_edges else 0.8 for e in G.edges()]

        ax.set_facecolor(COLOR["bg"])
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors,
                               width=edge_widths, arrows=True, arrowsize=15,
                               connectionstyle="arc3,rad=0.1")
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                               node_size=500, linewidths=1.2,
                               edgecolors="#5F5E5A")
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)

        INF = float('inf')
        dist_str = "∞" if d[target] == INF else str(d[target])
        ax.set_title(f"{name}\nWaktu: {t*1000:.3f} ms | Jarak: {dist_str}",
                     fontsize=10, fontweight="500")
        ax.axis("off")

    plt.suptitle(f"Perbandingan Dijkstra: Jalur Terpendek Node {source} → {target}",
                 fontsize=13, fontweight="500", y=1.02)
    plt.tight_layout()
    return fig


# Visualisasi Benchmark

def plot_benchmark_results(benchmark_data: list, metric: str = "avg_time_ms", separate: bool = False):
    """
    Buat grafik perbandingan performa basic dijkstra dan ketiga heap.
    """
    metric_labels = {
        "avg_time_ms"    : ("Waktu Rata-rata (ms)", "Perbandingan Waktu Eksekusi"),
        "avg_operations" : ("Jumlah Operasi Heap", "Perbandingan Jumlah Operasi"),
        "throughput"     : ("Throughput (node/detik)", "Perbandingan Throughput"),
    }
    y_label, chart_title = metric_labels.get(metric, (metric, metric))

    node_sizes = [d["nodes"] for d in benchmark_data]
    vals_basic = [d["Basic Dijkstra"][metric] for d in benchmark_data]
    vals_bin   = [d["Binary Heap"][metric]    for d in benchmark_data]
    vals_fib   = [d["Fibonacci Heap"][metric] for d in benchmark_data]
    vals_post  = [d["Post-order Heap"][metric] for d in benchmark_data]

    if not separate:
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(COLOR["bg"])
        ax.set_facecolor(COLOR["bg"])
        
        ax.plot(node_sizes, vals_basic, "D-", color=COLOR["basic"],
                linewidth=2, markersize=7, label="Basic Dijkstra", zorder=3)
        ax.plot(node_sizes, vals_bin,  "o-", color=COLOR["binary"],
                linewidth=2, markersize=7, label="Binary Heap",     zorder=3)
        ax.plot(node_sizes, vals_fib,  "s-", color=COLOR["fibonacci"],
                linewidth=2, markersize=7, label="Fibonacci Heap",  zorder=3)
        ax.plot(node_sizes, vals_post, "^-", color=COLOR["postorder"],
                linewidth=2.5, markersize=8, label="Post-order Heap (Brodal 2024)",
                zorder=4, linestyle="--")

        ax.set_xlabel("Jumlah Node", fontsize=11)
        ax.set_ylabel(y_label, fontsize=11)
        ax.set_title(chart_title, fontsize=13, fontweight="500", pad=15)
        ax.legend(fontsize=10, framealpha=0.9, facecolor=COLOR["bg"])
        ax.grid(True, alpha=0.3, color="#B4B2A9")
        ax.spines[["top", "right"]].set_visible(False)

        plt.tight_layout()
        return fig
    else:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.patch.set_facecolor(COLOR["bg"])

        fig.suptitle(chart_title, fontsize=13, fontweight="500", y=0.98)

        ax1.plot(
            node_sizes, vals_basic, "D-", color=COLOR["basic"],
            linewidth=2, markersize=7, label="Basic Dijkstra", zorder=3
        )

        ax1.set_xticks(node_sizes)

        ax1.set_xlabel("Jumlah Node", fontsize=11)
        ax1.set_ylabel(y_label, fontsize=11)
        ax1.set_title('Basic Dijkstra', fontsize=13, fontweight="500", pad=15)
        ax1.legend(fontsize=10, framealpha=0.9, facecolor=COLOR["bg"])
        ax1.grid(True, alpha=0.3, color="#B4B2A9")

        ax1.spines[["top", "right"]].set_visible(False)

        ax2.set_facecolor(COLOR["bg"])

        x = np.arange(len(node_sizes))

        width = 0.25

        bars1 = ax2.bar(
            x - width,
            vals_bin,
            width,
            color=COLOR["binary"],
            label="Binary Heap",
        )

        bars2 = ax2.bar(
            x,
            vals_fib,
            width,
            color=COLOR["fibonacci"],
            label="Fibonacci Heap",
        )

        bars3 = ax2.bar(
            x + width,
            vals_post,
            width,
            color=COLOR["postorder"],
            label="Post-order Heap",
        )

        ax2.set_xticks(x)
        ax2.set_xticklabels(node_sizes)

        ax2.set_xlabel("Jumlah Node", fontsize=12)
        ax2.set_ylabel("Jumlah Operasi", fontsize=12)

        ax2.set_title(
            "Priority Queues",
            fontsize=13,
            fontweight="500",
            pad=15,
        )

        ax2.grid(True, axis="y", alpha=0.3)

        ax2.legend()

        ax2.spines[["top", "right"]].set_visible(False)

        for bars in [bars1, bars2, bars3]:

            for bar in bars:

                height = bar.get_height()

                ax2.annotate(
                    f"{int(height)}",
                    xy=(
                        bar.get_x() + bar.get_width()/2,
                        height
                    ),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha="center",
                    fontsize=8,
                )

        return fig


def plot_bar_comparison(single_result: dict):
    """
    Grafik bar untuk membandingkan hasil pada satu graf tertentu.
    """
    heap_names = ["Basic Dijkstra", "Binary Heap", "Fibonacci Heap", "Post-order Heap"]
    times = [single_result[h]["avg_time_ms"] for h in heap_names]
    ops   = [single_result[h]["avg_operations"] for h in heap_names]
    colors = [COLOR["basic"], COLOR["binary"], COLOR["fibonacci"], COLOR["postorder"]]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor(COLOR["bg"])

    # Grafik waktu
    bars1 = ax1.bar(["Basic\nDijkstra", "Binary\nHeap", "Fibonacci\nHeap", "Post-order\nHeap"],
                    times, color=colors, edgecolor="white", linewidth=1.5)
    ax1.set_ylabel("Waktu (ms)", fontsize=11)
    ax1.set_title("Perbandingan Waktu Eksekusi", fontsize=12, fontweight="500")
    ax1.set_facecolor(COLOR["bg"])
    ax1.spines[["top", "right"]].set_visible(False)
    ax1.grid(axis="y", alpha=0.3)
    for bar, val in zip(bars1, times):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                 f"{val:.3f} ms", ha="center", va="bottom", fontsize=9)

    # Grafik operasi
    bars2 = ax2.bar(["Basic\nDijkstra", "Binary\nHeap", "Fibonacci\nHeap", "Post-order\nHeap"],
                    ops, color=colors, edgecolor="white", linewidth=1.5)
    ax2.set_ylabel("Jumlah Operasi", fontsize=11)
    ax2.set_title("Perbandingan Jumlah Operasi", fontsize=12, fontweight="500")
    ax2.set_facecolor(COLOR["bg"])
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.grid(axis="y", alpha=0.3)
    for bar, val in zip(bars2, ops):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f"{val:,}", ha="center", va="bottom", fontsize=9)

    plt.suptitle(f"Hasil Benchmark — Graf {single_result['num_nodes']} Node",
                 fontsize=13, fontweight="500")
    plt.tight_layout()
    return fig
