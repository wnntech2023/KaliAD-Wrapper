from config import CONFIG
from utils.runner import run_tool

def parse_dns(out: str):
    return {"summary": f"Найдено SRV-записей: {out.count('_ldap')}"}

def run_dns_check():
    cmd = ["nslookup", "-type=SRV", f"_ldap._tcp.{CONFIG['domain']}", CONFIG['dc_ip']]
    return run_tool(cmd, "DNS Enumeration", parse_dns)