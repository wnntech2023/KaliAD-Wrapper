from config import CONFIG
from utils.runner import run_tool
from pathlib import Path

def run_bloodhound_check():
    out_dir = Path("reports/bloodhound")
    out_dir.mkdir(exist_ok=True)
    cmd = ["bloodhound.py", "-u", CONFIG['username'], "-p", CONFIG['password'],
           "-d", CONFIG['domain'], "-dc", CONFIG['dc_ip'], "--collectionmethod", "All", "-o", str(out_dir)]
    return run_tool(cmd, "BloodHound Collector", lambda x: {"summary": "JSON-файлы сохранены в reports/bloodhound"})