from config import CONFIG
from utils.runner import run_tool

def parse_enum(out: str):
    users = out.count("user(s)") + out.count("Found 15 user") + out.count("username:")
    groups = out.count("group(s)") + out.count("Found 55 group") + out.count("groupname:")
    shares = out.count("share(s)")
    summary = f"Пользователей: {users} | Групп: {groups} | Общих ресурсов (SMB): {shares}"
    return {
        "users_found": users,
        "groups_found": groups,
        "shares_found": shares,
        "summary": summary
    }

def run_enum4linux_check():
    cmd = ["enum4linux-ng", "-A", "-u", CONFIG['username'], "-p", CONFIG['password'], CONFIG['dc_ip']]
    return run_tool(cmd, "enum4linux-ng", parse_enum)
