from rich.table import Table
from rich.console import Console
from jinja2 import Template
from pathlib import Path
import json
from datetime import datetime

console = Console()

# Улучшенный HTML-шаблон с Bootstrap 5 accordion (collapsible-блоки)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>KaliAD-Wrapper — Полный отчёт по Active Directory (v1.3)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 30px; background: #f8f9fa; }
        .card { margin-bottom: 20px; }
        .accordion-button { font-weight: bold; }
        pre { background: #222; color: #0f0; padding: 15px; border-radius: 5px; overflow-x: auto; max-height: 600px; }
        .log-link { color: #0d6efd; text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center my-4">KaliAD-Wrapper v1.3 — Отчёт по аудиту Active Directory</h1>
        <p class="text-center text-muted">Дата генерации: {{ timestamp }} | Всего проверок: {{ results|length }}</p>
        
        {% for r in results %}
        <div class="card">
            <div class="card-header bg-dark text-white">
                <strong>{{ r.tool }}</strong> 
                <span class="badge {% if r.status == 'success' %}bg-success{% elif r.status == 'failed' %}bg-warning{% else %}bg-danger{% endif %} float-end">
                    {{ r.status.upper() }}
                </span>
                <span class="float-end me-3">{{ r.duration }}</span>
            </div>
            <div class="card-body">
                <p><strong>Краткий результат:</strong> {{ r.data.summary | default('—') }}</p>
                
                {% if r.log_file %}
                <p><a href="{{ r.log_file }}" class="log-link" target="_blank">Открыть полный лог-файл →</a></p>
                {% endif %}
                
                <!-- Collapsible блок с полным выводом -->
                <div class="accordion" id="accordion{{ loop.index }}">
                    <div class="accordion-item">
                        <h2 class="accordion-header">
                            <button class="accordion-button collapsed" type="button" 
                                    data-bs-toggle="collapse" data-bs-target="#collapse{{ loop.index }}">
                                Полный вывод утилиты (raw_output)
                            </button>
                        </h2>
                        <div id="collapse{{ loop.index }}" class="accordion-collapse collapse">
                            <div class="accordion-body">
                                <pre>{{ r.data.raw_output | default(r.data.raw | default('Вывод отсутствует')) }}</pre>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
        
        <h3 class="mt-5">Полные данные в формате JSON</h3>
        <pre>{{ json_data }}</pre>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

def print_results(results):
    """Улучшенный вывод результатов в терминал с подробной информацией."""
    console.print("\n[bold cyan]=== РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ KaliAD-Wrapper v1.3 ===[/bold cyan]")
    
    table = Table(title="Сводная таблица проверок", show_lines=True)
    table.add_column("Модуль", style="cyan", no_wrap=True)
    table.add_column("Статус", style="green")
    table.add_column("Время", style="yellow")
    table.add_column("Ключевые находки", style="white")
    
    for r in results:
        summary = r.get("data", {}).get("summary", "—")
        if len(summary) > 80:
            summary = summary[:77] + "..."
        table.add_row(
            r["tool"],
            "[bold green]SUCCESS[/bold green]" if r["status"] == "success" else "[bold red]ERROR[/bold red]",
            r.get("duration", "—"),
            summary
        )
    console.print(table)
    
    console.print(f"\n[green]Отчёты сохранены в директории reports/[/green]")
    console.print(f"[green]Подробные логи каждой утилиты — в reports/logs/[/green]")


def generate_html_report(results, filepath: Path):
    """Генерация подробного HTML-отчёта с collapsible-блоками и полным выводом."""
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    # Подготовка данных для шаблона
    html = Template(HTML_TEMPLATE).render(
        results=results,
        json_data=json.dumps(results, ensure_ascii=False, indent=2),
        timestamp=timestamp
    )
    
    filepath.write_text(html, encoding="utf-8")
    console.print(f"[green]HTML-отчёт успешно создан: {filepath}[/green]")


# Экспорт функций для использования в main.py
__all__ = ["print_results", "generate_html_report"]
