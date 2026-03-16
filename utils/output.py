from rich.table import Table
from rich.console import Console
from jinja2 import Template
from pathlib import Path
import json

console = Console()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>KaliAD-Wrapper Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>body { padding: 20px; background:#111; color:#ddd; } .collapsible { cursor: pointer; }</style>
</head>
<body>
    <div class="container">
        <h1 class="text-center my-4">KaliAD-Wrapper — Отчёт по AD (v1.2)</h1>
        <table class="table table-dark table-striped">
            <thead><tr><th>Tool</th><th>Status</th><th>Duration</th><th>Findings</th></tr></thead>
            <tbody>
            {% for r in results %}
            <tr>
                <td><strong>{{ r.tool }}</strong></td>
                <td><span class="badge {% if r.status == 'success' %}bg-success{% else %}bg-danger{% endif %}">{{ r.status }}</span></td>
                <td>{{ r.duration }}</td>
                <td>{{ r.data.get('summary', r.data.get('raw', '—')[:100]) }}</td>
            </tr>
            {% endfor %}
            </tbody>
        </table>
        <h3>Полные данные (JSON)</h3>
        <pre>{{ json_data }}</pre>
    </div>
</body>
</html>
"""

def print_results(results):
    table = Table(title="Результаты сканирования")
    table.add_column("Tool", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Duration")
    for r in results:
        table.add_row(r["tool"], r["status"], r.get("duration", "—"))
    console.print(table)

def generate_html_report(results, filepath: Path):
    template = Template(HTML_TEMPLATE)
    html = template.render(
        results=results,
        json_data=json.dumps(results, ensure_ascii=False, indent=2)
    )
    filepath.write_text(html, encoding="utf-8")