"""Record validation-only epoch0/trained choices as soon as training finishes."""
from pathlib import Path
import json
import subprocess
import sys
import time

root=Path(__file__).resolve().parents[1]
pending={'low_lr_warmup','freeze_lower6'}
deadline=time.monotonic()+3600
while pending:
    assert time.monotonic()<deadline,'Pretest selection watcher timed out'
    failed=root/'Recformer/logs/ablations_v1/pipeline.exitcode'
    assert not failed.exists() or failed.read_text().strip()=='0','Training pipeline failed'
    for variant in list(pending):
        base=root/'Recformer/results'/f'hm_small_{variant}_seed42_v1'
        try:
            history=json.loads((base/'history.json').read_text())
        except (FileNotFoundError,json.JSONDecodeError):
            continue
        if len(history)==4:
            subprocess.run([sys.executable,str(root/'Recformer/select_pretest.py'),variant],check=True,cwd=root)
            pending.remove(variant)
    if pending:
        time.sleep(2)
