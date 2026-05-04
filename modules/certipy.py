from config import CONFIG
from utils.runner import run_tool
from pathlib import Path
import re

def parse_certipy(out: str):
    total_match = re.search(r"Found\s+(\d+)\s+certificate templates", out)
    enabled_match = re.search(r"Found\s+(\d+)\s+enabled certificate templates", out)
    vulnerable = len(re.findall(r"Vulnerable|ESC\d+", out, re.IGNORECASE))

    total = int(total_match.group(1)) if total_match else 0
    enabled = int(enabled_match.group(1)) if enabled_match else 0

    summary = f"Всего шаблонов: {total} | Включённых шаблонов: {enabled} | Уязвимых шаблонов ESC: {vulnerable}"
    return {
        "vulnerable_templates": vulnerable,
        "enabled_templates": enabled,
        "total_templates": total,
        "summary": summary,
        "raw_output": out
    }

def run_certipy_check():
    out_dir = Path("reports/certipy")
    out_dir.mkdir(exist_ok=True)
    
    cmd = [
        "certipy-ad", "find",
        "-u", f"{CONFIG['username']}@{CONFIG['domain']}",
        "-p", CONFIG['password'],
        "-dc-ip", CONFIG['dc_ip']
    ]
    
    result = run_tool(cmd, "Certipy-AD (certipy-ad)", parse_certipy)
    
    # Читаем полный .txt отчёт
    txt_files = list(out_dir.glob("*Certipy.txt"))
    if txt_files:
        try:
            full_report = txt_files[0].read_text(encoding="utf-8", errors="ignore")
            result["data"]["full_report"] = full_report
        except:
            pass
    
    return result
