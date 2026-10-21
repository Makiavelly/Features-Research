"""Record visual review of the combined existing-result plots."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/medium_all_methods_h011_v1'
path = OUT / 'comparison.json'
result = json.loads(path.read_text(encoding='utf-8'))
assert len(result['methods']) == 16
result.update(status='complete', visual_review_passed=True)
path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record
record('h011_all_methods_plot_verified',
       'Comparison of16 existing verified methods with H010/H011 completed. Overall and budget20 PNG/SVG plots visually reviewed; weighted fold aggregation checked for every method; source hashes and CSV retained. No training/API or selection changes.',
       'hm_medium_all_methods_h011_plot_v1', status='complete', artifacts=str(OUT.relative_to(ROOT)))
