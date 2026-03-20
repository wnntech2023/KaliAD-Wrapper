import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from questionary import select
import json
from datetime import datetime
from pathlib import Path

from config import CONFIG
from utils.runner import run_tool
from utils.output import print_results, generate_html_report

from modules.certipy import run_certipy_check
from modules.ldap import run_ldap_check
from modules.dns import run_dns_check
from modules.cme import run_cme_check
from modules.enum4linux import run_enum4linux_check
from modules.bloodhound import run_bloodhound_check
from modules.impacket import run_impacket_check
from modules.kerberoasting import run_kerberoasting_check

console = Console()


MODULES = {
    "1": ("Уязвимости шаблонов сертификатов AD CS (ESC1–ESC16) — Certipy-AD",
          run_certipy_check),
    "2": ("Конфигурационные ошибки ACL и избыточные права в объектах AD — ldapsearch",
          run_ldap_check),
    "3": ("Поиск контроллеров домена (Primary DC + все DC + GC) — nslookup SRV-запросы",
          run_dns_check),                    # ← обновлено по Вашему запросу
    "4": ("Полная энумерация пользователей, групп, AdminCount, RID-brute — NetExec (nxc)",
          run_cme_check),
    "5": ("Перечисление пользователей, групп и SMB-ресурсов — enum4linux-ng",
          run_enum4linux_check),
    "6": ("Граф путей повышения привилегий (BloodHound All) — bloodhound.py",
          run_bloodhound_check),
    "7": ("Дамп хэшей NTDS + AS-REP Roasting — Impacket (secretsdump + GetNPUsers)",
          run_impacket_check),
    "8": ("Kerberoasting (T1558.003) — извлечение TGS-хэшей SPN-учёток — GetUserSPNs.py",
          run_kerberoasting_check),
}

def main():
    parser = argparse.ArgumentParser(description="KaliAD-Wrapper v1.3 — AD Pentest Suite")
    parser.add_argument("--all", action="store_true", help="Запустить все проверки")
    parser.add_argument("--html", action="store_true", help="Сразу сформировать HTML-отчёт")
    args = parser.parse_args()

    if not all(CONFIG.values()):
        console.print("[red]Ошибка: заполните файл .env ![/red]")
        exit(1)

    if args.all:
        results = [func() for _, func in MODULES.values()]
    else:
        console.clear()
        console.print(Panel("🔥 KaliAD-Wrapper v1.3 — Поиск уязвимостей Active Directory", 
                           style="bold cyan", subtitle="выберите проверку"))

        choices = [f"{k}. {v[0]}" for k, v in MODULES.items()] + ["A. Запустить ВСЕ проверки", "0. Выход"]
        choice = select("Выберите проверку:", choices=choices).ask()

        if choice == "0":
            return
        elif choice == "A":
            results = [func() for _, func in MODULES.values()]
        else:
            mod_key = choice.split('.')[0]
            results = [MODULES[mod_key][1]()]

    print_results(results)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = Path(f"reports/report_{timestamp}.json")
    report_file.parent.mkdir(exist_ok=True)

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    if args.html or True:  # всегда генерируем HTML в v1.3
        html_file = report_file.with_suffix(".html")
        generate_html_report(results, html_file)
        console.print(f"[green]✅ HTML-отчёт сохранён: {html_file}[/green]")

    console.print(f"[green]✅ JSON сохранён: {report_file}[/green]")
    console.print("[bold green]Готово! Инструмент успешно отработал.[/bold green]")

if __name__ == "__main__":
    main()
