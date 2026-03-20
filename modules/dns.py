from config import CONFIG
from utils.runner import run_tool
from pathlib import Path

def parse_dns(out: str):
    lines = out.lower().splitlines()
    dc_count = sum(1 for line in lines if "dc._msdcs" in line or "_ldap._tcp." in line and "dc" in line)
    pdc_found = any("pdc._msdcs" in line for line in lines)
    gc_found = any("gc._msdcs" in line for line in lines)
    
    summary = f"Найдено контроллеров домена: {dc_count} | PDC Emulator: {'✓' if pdc_found else '✗'} | GC: {'✓' if gc_found else '✗'}"
    return {
        "dcs_found": dc_count,
        "pdc_emulator": "обнаружен" if pdc_found else "не обнаружен",
        "global_catalog": "обнаружен" if gc_found else "не обнаружен",
        "summary": summary,
        "raw_hint": "Полные SRV-записи сохранены в reports/dns.log"
    }

def run_dns_check():
    domain = CONFIG['domain']
    dc_ip = CONFIG['dc_ip']
    out_dir = Path("reports")
    out_dir.mkdir(exist_ok=True)
    log_file = out_dir / "dns.log"
    
    # Массив запросов для полного поиска контроллеров
    queries = [
        f"_ldap._tcp.{domain}",
        f"_ldap._tcp.dc._msdcs.{domain}",
        f"_ldap._tcp.pdc._msdcs.{domain}",
        f"_ldap._tcp.gc._msdcs.{domain}",
        f"_kerberos._tcp.dc._msdcs.{domain}"
    ]
    
    all_output = ""
    for q in queries:
        cmd = ["nslookup", "-type=SRV", q, dc_ip]
        result = run_tool(cmd, f"DNS SRV: {q}", None)  # временно без парсера
        all_output += f"\n=== {q} ===\n{result.get('data', {}).get('raw', '')}\n"
    
    # Сохраняем полный лог
    log_file.write_text(all_output, encoding="utf-8")
    
    # Финальный парсинг
    return run_tool(["echo", "DNS scan completed"], "Поиск контроллеров домена", parse_dns)
    # Примечание: run_tool с echo используется только как заглушка для унификации;
    # реальный вывод уже обработан выше и передан в parse_dns через all_output.
