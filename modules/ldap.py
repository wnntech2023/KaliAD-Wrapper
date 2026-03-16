from config import CONFIG
from utils.runner import run_tool

def parse_ldap(out: str):
    entries = out.count("dn:")
    return {"entries": entries, "summary": f"Найдено объектов: {entries}"}

def run_ldap_check():
    base = f"DC={CONFIG['domain'].replace('.', ',DC=')}"
    cmd = ["ldapsearch", "-H", f"ldap://{CONFIG['dc_ip']}", "-x",
           "-D", f"{CONFIG['username']}@{CONFIG['domain']}",
           "-w", CONFIG['password'], "(objectClass=*)", "-b", base]
    return run_tool(cmd, "LDAP Enumeration", parse_ldap)