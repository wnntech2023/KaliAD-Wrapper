from config import CONFIG
from utils.runner import run_tool
from pathlib import Path

def run_bloodhound_check():
    out_dir = Path("reports/bloodhound")
    out_dir.mkdir(exist_ok=True)
    
    cmd = [
        "rusthound-ce",                                      # основная команда
        "-u", f"{CONFIG['username']}@{CONFIG['domain']}",
        "-p", CONFIG['password'],
        "-d", CONFIG['domain'],
        "-i", CONFIG['dc_ip'],
        "--collectionmethod", "All",
        "-o", str(out_dir),
        "--zip"
    ]
    
    return run_tool(
        cmd,
        "BloodHound Collector (rusthound-ce)",
        lambda x: {"summary": "JSON-файлы и архив .zip сохранены в reports/bloodhound/"}
    )
