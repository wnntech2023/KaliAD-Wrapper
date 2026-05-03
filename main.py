from rich.table import Table
from rich.console import Console
from jinja2 import Template
from pathlib import Path
import json
from datetime import datetime

from config import CONFIG

console = Console()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>KaliAD-Wrapper v1.4 — Отчёт по аудиту Active Directory</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 30px; background:#f8f9fa; font-family: 'Segoe UI', sans-serif; }
        .table th { background: #0d6efd; color: white; }
        .badge-success { background: #198754; }
        .badge-danger { background: #dc3545; }
        .card { margin-bottom: 25px; }
        .result-card { border-left: 5px solid #0d6efd; }
        pre { background: #f4f4f4; padding: 15px; border-radius: 8px; font-size: 0.95em; max-height: 800px; overflow-y: auto; }
        .summary { font-weight: 600; color: #0d6efd; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center my-4 text-primary">KaliAD-Wrapper v1.4 — Отчёт по аудиту Active Directory</h1>
        <p class="text-center text-muted">
            <strong>Домен:</strong> {{ domain }} | 
            <strong>Дата:</strong> {{ timestamp }}
        </p>

        <!-- Сводная таблица -->
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">Сводная таблица результатов</h5>
            </div>
            <div class="card-body">
                <table class="table table-hover table-bordered align-middle">
                    <thead>
                        <tr>
                            <th>Модуль</th>
                            <th>Статус</th>
                            <th>Время</th>
                            <th>Ключевые находки</th>
                        </tr>
                    </thead>
                    <tbody>
                    {% for r in results %}
                    <tr>
                        <td><strong>{{ r.tool }}</strong></td>
                        <td><span class="badge {% if r.status == 'success' %}bg-success{% else %}bg-danger{% endif %}">{{ r.status|upper }}</span></td>
                        <td>{{ r.duration|default('—') }}</td>
                        <td>{{ r.findings|default('—') }}</td>
                    </tr>
                    {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Подробные результаты -->
        <h3 class="mt-5 mb-3">Подробные результаты по модулям</h3>
        {% for r in results %}
        <div class="card result-card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <strong>{{ r.tool }}</strong>
                <span class="badge {% if r.status == 'success' %}bg-success{% else %}bg-danger{% endif %}">{{ r.status|upper }}</span>
            </div>
            <div class="card-body">
                <p class="summary">{{ r.findings|default('—') }}</p>

                {% if r.data and r.data.summary %}
                <p><strong>Summary:</strong> {{ r.data.summary }}</p>
                {% endif %}

                <!-- Полный отчёт Certipy-AD (все шаблоны + CA) -->
                {% if r.tool.startswith('Certipy-AD') and r.data and r.data.full_report %}
                <p><strong>Полный отчёт Certipy-AD (все шаблоны сертификатов + описание CA):</strong></p>
                <pre>{{ r.data.full_report }}</pre>
                {% elif r.data and r.data.raw_output %}
                <details>
                    <summary>Полный вывод инструмента</summary>
                    <pre>{{ r.data.raw_output[:5000] }}{% if r.data.raw_output|length > 5000 %}... (вывод обрезан){% endif %}</pre>
                </details>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

def get_readable_findings(result):
    if result.get("status") in ["error", "failed"]:
        return f"ОШИБКА: {result.get('error', 'Неизвестная ошибка')[:150]}"

    data = result.get("data", {})
    summary = data.get("summary", "")

    if summary:
        return summary

    if "subresults" in data:
        total_users = sum(s.get("data", {}).get("users_found", 0) for s in data["subresults"])
        total_groups = sum(s.get("data", {}).get("groups_found", 0) for s in data["subresults"])
        total_admins = sum(s.get("data", {}).get("admins_found", 0) for s in data["subresults"])
        return f"Пользователей: {total_users} | Групп: {total_groups} | Администраторов: {total_admins}"

    if "entries" in data:
        return f"Объектов LDAP: {data.get('entries', 0)} | Пользователей: {data.get('users_found', 0)} | Групп: {data.get('groups_found', 0)}"
    if "users_found" in data or "groups_found" in data:
        return f"Пользователей: {data.get('users_found', 0)} | Групп: {data.get('groups_found', 0)} | Администраторов: {data.get('admins_found', 0)}"
    if "srv_records" in data:
        return data.get("summary", "SRV-записи контроллеров домена собраны")
    if "spns_found" in data:
        return f"SPN-хэшей: {data.get('spns_found', 0)} (хэши сохранены)"
    if "vulnerable_templates" in data:
        return f"Уязвимых шаблонов ESC: {data.get('vulnerable_templates', 0)} | Всего шаблонов: {data.get('total_templates', 0)}"

    return "Данные успешно собраны"


def print_results(results):
    table = Table(title="=== РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ KaliAD-Wrapper v1.4 ===", title_style="bold cyan")
    table.add_column("Модуль", style="cyan", width=42)
    table.add_column("Статус", style="bold")
    table.add_column("Время", style="dim")
    table.add_column("Ключевые находки", style="yellow", width=85)

    for r in results:
        findings = get_readable_findings(r)
        status_style = "green" if r.get("status") == "success" else "red"
        table.add_row(
            r.get("tool", "—"),
            f"[{status_style}]{r.get('status', '—').upper()}[/{status_style}]",
            r.get("duration", "—"),
            findings
        )
    console.print(table)


def generate_html_report(results, filepath: Path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    domain = CONFIG.get("domain", "—")

    for r in results:
        if "findings" not in r:
            r["findings"] = get_readable_findings(r)

    template = Template(HTML_TEMPLATE)
    html = template.render(
        results=results,
        timestamp=timestamp,
        domain=domain
    )
    filepath.write_text(html, encoding="utf-8")
    console.print(f"[green]✅ Подробный HTML-отчёт сохранён: {filepath}[/green]")
