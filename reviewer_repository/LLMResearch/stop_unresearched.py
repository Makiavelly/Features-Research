"""Stop optional-tool pilot only at an evaluator boundary, preserving paid text."""
import os
from pathlib import Path
import signal
import time
from common import REPORT

controller = int((REPORT / 'pipeline.pid').read_text())
assert b'LLMResearch/pipeline.py' in Path(f'/proc/{controller}/cmdline').read_bytes()
deadline = time.monotonic() + 240
while time.monotonic() < deadline:
    children_file = Path(f'/proc/{controller}/task/{controller}/children')
    if not children_file.exists():
        raise RuntimeError('Controller already stopped; inspect status')
    for value in children_file.read_text().split():
        pid = int(value)
        command = Path(f'/proc/{pid}/cmdline').read_bytes()
        if b'LLMResearch/run.py' not in command:
            continue
        grandchildren = Path(f'/proc/{pid}/task/{pid}/children').read_text().split()
        for child in grandchildren:
            childcmd = Path(f'/proc/{child}/cmdline').read_bytes()
            if b'/worker.py' in childcmd:
                # Search evaluator starts only after final paid text is durable.
                os.kill(pid, signal.SIGTERM)
                print('Stopped optional-tool search PID', pid, 'at saved-response evaluator boundary; worker', child, 'can finish.', flush=True)
                raise SystemExit(0)
    time.sleep(.2)
raise RuntimeError('No safe evaluator boundary reached; no process terminated')
