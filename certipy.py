from config import CONFIG
from utils.runner import run_tool
from pathlib import Path

def parse_certipy(out: str):
    vulnerable = out.count("VULNERABLE") + out.count("ESC")
    templates = len([line for line in out.splitlines() if "Template:" in line])
    return {
        "vulnerable_templates": vulnerable,
        "templates_found": templates,
        "summary": f"Обнаружено уязвимых шаблонов AD CS: {vulnerable} (всего шаблонов: {templates})",
        "raw_output": out[:12000]
    }

def run_certipy_check():
    cmd = [
        "certipy", "find",
        "-u", f"{CONFIG['username']}@{CONFIG['domain']}",
        "-p", CONFIG['password'],
        "-dc-ip", CONFIG['dc_ip'],
        "--vulnerable", "--enabled", "--stdout"
    ]
    return run_tool(cmd, "Certipy-AD (ESC1–ESC16)", parse_certipy)
