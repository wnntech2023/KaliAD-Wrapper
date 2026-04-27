import subprocess
from datetime import datetime
from pathlib import Path
from rich.console import Console

console = Console()

def run_tool(cmd: list, tool_name: str, parse_func=None):
    start = datetime.now()
    log_dir = Path("reports/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = start.strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"{tool_name.replace(' ', '_').lower()}_{timestamp}.log"
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        full_output = result.stdout + result.stderr
        
        # Сохраняем полный вывод в отдельный лог-файл
        log_file.write_text(full_output, encoding="utf-8")
        
        data = parse_func(full_output) if parse_func else {"raw": full_output[:3000]}
        # Гарантированно добавляем полный raw_output
        data["raw_output"] = full_output[:15000]
        
        return {
            "tool": tool_name,
            "timestamp": start.isoformat(),
            "command": " ".join(cmd),
            "status": "success" if result.returncode == 0 else "failed",
            "returncode": result.returncode,
            "duration": str(datetime.now() - start),
            "log_file": str(log_file),
            "data": data
        }
    except subprocess.TimeoutExpired:
        return {"tool": tool_name, "status": "timeout", "error": "Превышено время выполнения (300 с)"}
    except Exception as e:
        return {"tool": tool_name, "status": "error", "error": str(e)}
