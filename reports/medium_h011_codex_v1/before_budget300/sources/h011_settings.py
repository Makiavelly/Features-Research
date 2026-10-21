"""User-authorized budget300 continuation; original session paths stay stable."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SESSION = 'h011_codex_seed42_v1'
RUN = 'hm_medium_h011_codex_seed42_budget300_v2'
REPORT = ROOT / 'reports/medium_h011_codex_budget300_v2'
