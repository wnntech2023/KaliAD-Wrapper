from config import CONFIG
from utils.runner import run_tool

def parse_nxc(out: str):
    users = out.count("user:") + out.count("User:")
    return {"users_found": users, "summary": f"Найдено пользователей/групп: {users}"}

def run_cme_check():
    base = ["nxc", "ldap", CONFIG['dc_ip'], "-u", CONFIG['username'], "-p", CONFIG['password']]
    cmds = [
        base + ["--users"],
        base + ["--groups"],
        base + ["--admin-count"],
        base + ["--rid-brute"]
    ]
    subresults = []
    for i, cmd in enumerate(cmds):
        res = run_tool(cmd, f"NetExec-{i+1}", parse_nxc)
        subresults.append(res)
    
    return {
        "tool": "NetExec (nxc) — полный скан",
        "status": "success",
        "data": {"subresults": subresults}
    }