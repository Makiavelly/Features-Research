"""Create a separate Codex home/config/workspace without changing user settings."""
import argparse
import ast
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent


def wsl(path):
    path = Path(path).resolve()
    return '/mnt/' + path.drive[0].lower() + path.as_posix()[2:]


def setup(fold, session, island=None, gateway=None):
    if fold not in range(3) or not session.replace('_', '').replace('-', '').isalnum():
        raise ValueError('Invalid fold/session')
    folder = BASE / 'sessions' / session / f'fold_{fold}'
    if island is not None:
        folder = folder / f'island_{island}'
    work, home = folder / 'work', folder / 'codex_home'
    work.mkdir(parents=True, exist_ok=True)
    home.mkdir(exist_ok=True)
    original = json.loads((ROOT / f'CVBenchmark/results/medium_v2/fold_{fold}/h009/run_config.json').read_text(encoding='utf-8'))
    q = lambda x: json.dumps(x, ensure_ascii=False)
    lines = [f'model = {q(original["model_id"])}', 'model_provider = "hm_fold_api"',
             'model_reasoning_effort = "low"', 'approval_policy = "never"',
             'sandbox_mode = "read-only"', '', '[features]', 'shell_tool = false', 'shell_snapshot = false', '',
             'apps = false', 'browser_use = false', 'view_image = false', '',
             '[model_providers.hm_fold_api]', 'name = "H&M isolated GPT-6.1 Sol"',
             f'base_url = {q(gateway or original["base_url"])}', 'env_key = "HM_AGENT_ACCESS_TOKEN"',
             'wire_api = "responses"', 'request_max_retries = 0', 'stream_max_retries = 0',
             'supports_websockets = false', '', '[mcp_servers.fold]',
             f'command = {q(str(Path("C:/Windows/System32/wsl.exe")))}',
             'args = ' + q(['--exec', wsl(ROOT / 'RelBenchGNN/.venv-wsl/bin/python'),
                         '-u', wsl(BASE / 'mcp_server.py'), '--fold', str(fold), '--session', session] +
                         (['--island', str(island)] if island is not None else [])),
             'startup_timeout_sec = 30', 'tool_timeout_sec = 3600', 'required = true',
             'default_tools_approval_mode = "approve"', 'env_vars = []', '']
    configpath = home / 'config.toml'
    if gateway:
        lines.insert(0, 'web_search = "disabled"')
        lines.insert(lines.index('[features]') + 1, 'unbounded_connection_retries = false')
    text = '\n'.join(lines)
    if gateway:
        text += '\n[model_providers.hm_fold_api.http_headers]\nX-HM-Fold = ' + q(str(fold)) + '\nX-HM-Island = ' + q(str(island)) + '\n'
    if configpath.exists():
        assert configpath.read_text(encoding='utf-8') == text, 'Do not change an existing agent profile silently'
    else:
        configpath.write_text(text, encoding='utf-8')
    agents = '''# Standalone H&M research agent

This is a separate train-only agent workspace. Read CONTEXT.md and
FEATURE_INTERFACE.md here, then use the fold MCP tools. The original repository's
history instructions are satisfied through these local context files; do not
look for files outside this workspace or other folds.

Native host shell is disabled. Use fold.terminal for commands: it runs inside
an OS-isolated Linux environment with /work writable and a read-only
/data/research.duckdb. pandas/NumPy/DuckDB are available. No host project,
validation/test data, API credentials or network are visible inside that terminal.
Use fold.write_file/read_file for files. Never use native file/image tools to
look outside this working folder. Keep hypotheses and observed statistics in
WORK_LOG.md. Do not train predictive models in terminal. Submit feature programs
only through fold.evaluate_features; it enforces20 accepted distinct checks
outside your writable workspace. Invalid/duplicate submissions do not earn
extra search feedback. Train labels may be researched; search labels stay hidden.
No confirmation, heldout or outer-test selection is available to this agent.

Before writing features, ask statistical questions of your own and inspect
training data. Join train_history.cutoff=train_pairs.timestamp for label-related
analyses. history is only the last train snapshot. Sampled negative pairs bias
label rates. Respect cutoff boundaries and never hardcode train labels/IDs.
Do not change the evaluator, data, environment, budgets, or previous results.
When20 checks are used, stop and report evidence; the parent controller performs
confirmation/freeze/final evaluation separately. This session is not itself a
completed benchmark or a matched replication of H009's three-population search.
'''
    for name, content in [('AGENTS.md', agents), ('CONTEXT.md', f'# Train fold{fold}\n\nUse fold.status to inspect schemas, six training cutoffs and remaining budget.\nNo test or validation targets are available.\n')]:
        path = work / name
        if not path.exists():
            path.write_text(content, encoding='utf-8')
    # Extract the existing final feature contract without executing repository code.
    tree = ast.parse((ROOT / f'CVBenchmark/results/medium_v2/fold_{fold}/runtime/api/prompting.py').read_text(encoding='utf-8'))
    node = next(n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'INSTRUCTION' for t in n.targets))
    contract = ast.literal_eval(node.value.func.value)
    manifest = json.loads((ROOT / f'LLMResearch/results/v2/fold_{fold}/research_manifest.json').read_text(encoding='utf-8'))
    historycols = [c[0] for c in manifest['tables']['history']]
    contract = contract.replace('COLUMNS', ', '.join(historycols))
    path = work / 'FEATURE_INTERFACE.md'
    if not path.exists():
        path.write_text('# Feature function contract\n\nThe following applies to submitted .py files, not your conversational/tool replies.\n\n' + contract, encoding='utf-8')
    paths = BASE / 'tool_paths.json'
    if not paths.exists():
        paths.write_text(json.dumps({'codex': shutil.which('codex')}, ensure_ascii=False), encoding='utf-8')
    return folder, work, home


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fold', type=int, default=0)
    parser.add_argument('--session', default='standalone_v2')
    args = parser.parse_args()
    folder, work, home = setup(args.fold, args.session)
    print(json.dumps({'folder': str(folder), 'workspace': str(work), 'codex_home': str(home)}, ensure_ascii=False, indent=2))
