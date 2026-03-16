from config import CONFIG
from utils.runner import run_tool

def parse_enum(out: str):
    users = out.count("user:")
    return {"summary": f"Найдено пользователей: {users}"}

def run_enum4linux_check():
    cmd = ["enum4linux-ng", "-A", "-u", CONFIG['username'], "-p", CONFIG['password'], CONFIG['dc_ip']]
    return run_tool(cmd, "enum4linux-ng", parse_enum)