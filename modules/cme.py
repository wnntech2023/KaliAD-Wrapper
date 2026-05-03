from config import CONFIG
from utils.runner import run_tool

def parse_nxc(out: str):
    users = out.count("Enumerated") + out.count("Username") + out.count("domain users")
    groups = out.count("Group") + out.count("group")
    admins = out.count("adminCount=1") + out.count("Domain Admins") + out.count("Enterprise Admins")
    summary = f"Пользователей: {users} | Групп: {groups} | Администраторов: {admins}"
    return {
        "users_found": users,
        "groups_found": groups,
        "admins_found": admins,
        "summary": summary
    }

def run_cme_check():
    base = ["nxc", "ldap", CONFIG['dc_ip'], "-u", CONFIG['username'], "-p", CONFIG['password']]
    cmds = [
        base + ["--users"],
        base + ["--groups"],
        base + ["--admin-count"]
    ]
    subresults = [run_tool(cmd, f"NetExec-{i+1}", parse_nxc) for i, cmd in enumerate(cmds)]
    
    return {
        "tool": "NetExec (nxc) — полный скан",
        "status": "success",
        "data": {"subresults": subresults}
    }
