"""Stop only this workspace's training pipeline when changing its seed plan."""
from pathlib import Path
import psutil
import signal
import time

ROOT = Path(__file__).resolve().parents[1]
matches = []
for process in psutil.process_iter(["pid", "cmdline", "cwd"]):
    try:
        command = process.info["cmdline"] or []
        if Path(process.info["cwd"] or "/").resolve() != ROOT:
            continue
        if any(value.endswith(("background_pipeline.sh", "run_experiment.sh", "run_idgnn.py")) for value in command):
            matches.append(process)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
for process in matches:
    if any(value.endswith("background_pipeline.sh") for value in process.cmdline()):
        process.send_signal(signal.SIGSTOP)
for process in matches:
    try:
        print("Stopping", process.pid, process.cmdline(), flush=True)
        process.terminate()
        process.send_signal(signal.SIGCONT)
    except psutil.NoSuchProcess:
        pass
for _ in range(100):
    alive = [process for process in matches if process.is_running() and process.status() != psutil.STATUS_ZOMBIE]
    if not alive:
        break
    time.sleep(.1)
for process in alive:
    try:
        process.kill()
    except psutil.NoSuchProcess:
        pass
print("Training queue stopped", flush=True)
