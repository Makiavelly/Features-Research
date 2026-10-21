"""Record observed live startup without changing experiment sources or budgets."""
import sys
from toolbox import ROOT

sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record
record('h011_live_start_verified',
       'H011 real launch verified: controller23016 and native Codex21700 alive, fold0/population0 received actual provider response and successfully researched train-only DuckDB through isolated MCP terminal. First sandboxed launcher stopped before API with WSL E_ACCESSDENIED; relaunched with WSL access, original failure log preserved. Bounded pre-response transport retries active; no feature checks accepted at startup verification.',
       'hm_medium_h011_codex_seed42_v1', status='searching', fold=0, island=0,
       startup_verified=True, initial_successful_research_requests=1,
       artifacts='reports/medium_h011_codex_v1')
