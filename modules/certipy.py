from config import CONFIG
from utils.runner import run_tool
from pathlib import Path

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
        "summary": summary
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
    
    return run_tool(cmd, "Certipy-AD (certipy-ad)", parse_certipy)
