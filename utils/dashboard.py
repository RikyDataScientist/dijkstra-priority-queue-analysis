import base64
from io import BytesIO
import os
import webbrowser
from pathlib import Path

def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string."""
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()

    return img_base64

def create_html_dashboard(figures, output_file="output/benchmark_dashboard.html"):
    """Gabungkan semua visualisasi ke satu dashboard HTML."""

    os.makedirs("output", exist_ok=True)

    images_html = ""

    for title, fig in figures:
        img = fig_to_base64(fig)

        images_html += f"""
        <div class="card">
            <h2>{title}</h2>
            <img src="data:image/png;base64,{img}" />
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dijkstra Benchmark Dashboard</title>

        <style>

            body {{
                font-family: Arial;
                background: #0f172a;
                color: white;
                padding: 30px;
                margin: 0;
            }}

            h1 {{
                text-align: center;
                margin-bottom: 50px;
                font-size: 40px;
            }}

            /* Container utama */
            .container {{
                max-width: 1100px;
                margin: auto;
            }}

            /* 1 kolom vertikal */
            .grid {{
                display: flex;
                flex-direction: column;
                gap: 30px;
            }}

            .card {{
                background: #1e293b;
                padding: 25px;
                border-radius: 18px;

                box-shadow:
                    0 8px 20px rgba(0,0,0,0.35);
            }}

            .card h2 {{
                margin-bottom: 20px;
                font-size: 28px;
            }}

            img {{
                width: 100%;
                border-radius: 14px;
                background: white;
            }}

        </style>
    </head>

    <body>

        <h1>
            Benchmark Dijkstra Priority Queue
        </h1>

        <div class="container">

            <div class="grid">
                {images_html}
            </div>

        </div>

    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] Dashboard disimpan ke: {output_file}")
    absolute_path = Path(output_file).resolve()

    webbrowser.open(f"file://{absolute_path}")
