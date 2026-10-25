"""Stop only this workspace's context monitor; never stop model training."""
from pathlib import Path
import psutil

ROOT = Path(__file__).resolve().parents[1]
for process in psutil.process_iter(["pid", "cmdline", "cwd"]):
    try:
        command = process.info["cmdline"] or []
        if "RelBenchGNN/monitor.py" in command and process.info["cwd"] == str(ROOT):
            process.terminate()
            process.wait(timeout=10)
            print(f"Stopped context monitor PID {process.pid}")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
