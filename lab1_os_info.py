import json
import os
import platform
import sys
from datetime import datetime
from typing import Any, Dict, Optional

def get_basic_info() -> Dict[str, Any]:
    return {
        "os_name": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor() or "Unknown",
        "hostname": platform.node(),
        "python_version": sys.version,
        "cwd": os.getcwd(),
        "home_dir": os.path.expanduser("~"),
        "path_sep": os.path.sep,
        "timestamp": datetime.now().isoformat()
    }

def get_extended_info() -> Optional[Dict[str, Any]]:
    try:
        import psutil
        root = "/" if os.name != "nt" else "C:\\"
        du = psutil.disk_usage(root)
        return {
            "cpu_logical": psutil.cpu_count(logical=True),
            "cpu_physical": psutil.cpu_count(logical=False),
            "ram_total_gb": round(du.total / (1024**3), 2),
            "ram_used_gb": round(du.used / (1024**3), 2),
            "disk_total_gb": round(du.total / (1024**3), 2),
            "disk_used_gb": round(du.used / (1024**3), 2),
            "uptime_sec": int(datetime.now().timestamp() - psutil.boot_time()),
            "interfaces": list(psutil.net_if_addrs().keys())
        }
    except ImportError:
        return None

def save_json(data: Dict[str, Any], filename: str = "os_info.json") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    basic = get_basic_info()
    extended = get_extended_info()
    result = {
        "basic_info": basic,
        "extended_info": extended if extended else {"status": "unavailable", "reason": "psutil not installed"}
    }
    save_json(result)
    print("OK: os_info.json saved.")
