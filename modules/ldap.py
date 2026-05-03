from config import CONFIG
from utils.runner import run_tool

def parse_ldap(out: str):
    entries = out.count("dn:")
    users = out.count("objectClass: user") + out.count("CN=Users")
    groups = out.count("objectClass: group") + out.count("CN=Groups")
    summary = f"Всего объектов: {entries} | Пользователей: {users} | Групп: {groups}"
    return {
        "entries": entries,
        "users_found": users,
        "groups_found": groups,
        "summary": summary
    }

def run_ldap_check():
    base = f"DC={CONFIG['domain'].replace('.', ',DC=')}"
    cmd = ["ldapsearch", "-H", f"ldap://{CONFIG['dc_ip']}", "-x",
           "-D", f"{CONFIG['username']}@{CONFIG['domain']}",
           "-w", CONFIG['password'], "(objectClass=*)", "-b", base]
    return run_tool(cmd, "LDAP Enumeration", parse_ldap)
