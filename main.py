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
    "1": ("Certipy-AD (certipy-ad)", run_certipy_check),
    "2": ("LDAP Enumeration (ldapsearch)", run_ldap_check),
    "3": ("DNS Enumeration (nslookup)", run_dns_check),
    "4": ("NetExec (nxc) — полный скан", run_cme_check),
    "5": ("enum4linux-ng", run_enum4linux_check),
    "6": ("BloodHound Collector (rusthound-ce)", run_bloodhound_check),
    "7": ("AS-REP Roasting (GetNPUsers.py)", run_impacket_check),
    "8": ("Kerberoasting (GetUserSPNs.py)", run_kerberoasting_check),
}

def main():
    parser = argparse.ArgumentParser(description="KaliAD-Wrapper v1.4 — оркестратор аудита Active Directory")
    parser.add_argument("--all", action="store_true", help="Запустить все проверки")
    parser.add_argument("--html", action="store_true", help="Сразу экспортировать HTML-отчёт")
    args = parser.parse_args()

    if not all(CONFIG.values()):
        console.print("[red]Ошибка: заполните файл .env перед запуском![/red]")
        exit(1)

    if args.all:
        results = [func() for func in [v[1] for v in MODULES.values()]]
    else:
        console.clear()
        console.print(Panel("KaliAD-Wrapper v1.4 — AD Pentest Suite", style="bold cyan"))
        
        choices = [f"{k}. {v[0]}" for k, v in MODULES.items()] + ["0. Выход", "A. Запустить ВСЁ"]
        choice = select("Выберите проверку:", choices=choices).ask()
        
        if choice.startswith("0.") or choice == "0":
            return
        elif choice.startswith("A.") or "Запустить ВСЁ" in choice:
            results = [func() for func in [v[1] for v in MODULES.values()]]
        else:
            mod_key = choice.split('.')[0].strip()
            results = [MODULES[mod_key][1]()]

    print_results(results)
    
    report_file = Path(f"reports/report_{datetime.now():%Y%m%d_%H%M%S}.json")
    report_file.parent.mkdir(exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    html_file = report_file.with_suffix(".html")
    generate_html_report(results, html_file)
    
    console.print(f"[green]✅ JSON-отчёт сохранён: {report_file}[/green]")
    console.print(f"[green]✅ HTML-отчёт сохранён: {html_file}[/green]")

if __name__ == "__main__":
    main()
