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
        "summary": summary,
        "raw_output": out
    }

def run_cme_check():
    base = ["nxc", "ldap", CONFIG['dc_ip'], "-u", CONFIG['username'], "-p", CONFIG['password']]
    cmds = [
        base + ["--users"],
        base + ["--groups"],
        base + ["--admin-count"],
        base + ["--pass-pol"],
        base + ["--shares"]
    ]
    
    subresults = []
    total_duration = 0.0
    
    for i, cmd in enumerate(cmds):
        res = run_tool(cmd, f"NetExec-{i+1}", parse_nxc)
        subresults.append(res)
        # Суммируем время выполнения подкоманд
        try:
            duration_str = res.get("duration", "0:00:00")
            h, m, s = map(float, duration_str.split(':'))
            total_duration += h*3600 + m*60 + s
        except:
            pass
    
    return {
        "tool": "NetExec (nxc) — полный скан",
        "status": "success",
        "duration": f"{total_duration//3600:02.0f}:{(total_duration%3600)//60:02.0f}:{total_duration%60:05.3f}",
        "data": {
            "subresults": subresults,
            "raw_output": "\n\n".join([s.get("data", {}).get("raw_output", "") for s in subresults]),
            "summary": f"Пользователей: {sum(s.get('data', {}).get('users_found', 0) for s in subresults)} | "
                       f"Групп: {sum(s.get('data', {}).get('groups_found', 0) for s in subresults)} | "
                       f"Администраторов: {sum(s.get('data', {}).get('admins_found', 0) for s in subresults)}"
        }
    }
