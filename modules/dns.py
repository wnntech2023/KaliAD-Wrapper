from config import CONFIG
from utils.runner import run_tool

def parse_dns(out: str):
    srv_count = out.count("_ldap._tcp") + out.count("SRV")
    summary = f"Найдено SRV-записей контроллеров домена: {srv_count}"
    return {
        "srv_records": srv_count,
        "summary": summary
    }

def run_dns_check():
    cmd = ["nslookup", "-type=SRV", f"_ldap._tcp.{CONFIG['domain']}", CONFIG['dc_ip']]
    return run_tool(cmd, "Поиск контроллеров домена", parse_dns)
