import subprocess
from datetime import datetime
from rich.console import Console

console = Console()

def run_tool(cmd: list, tool_name: str, parse_func=None):
    start = datetime.now()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        output = result.stdout + result.stderr
        data = parse_func(output) if parse_func else {"raw": output[:2000]}
        
        return {
            "tool": tool_name,
            "timestamp": start.isoformat(),
            "command": " ".join(cmd),
            "status": "success" if result.returncode == 0 else "failed",
            "duration": str(datetime.now() - start),
            "data": data
        }
    except Exception as e:
        return {"tool": tool_name, "status": "error", "error": str(e)}