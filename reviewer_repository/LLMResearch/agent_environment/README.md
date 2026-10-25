# Separate GPT-6.1 Sol agent environment

## Active research-budget revision

The user increased research terminal calls to300 per fold,100 per population.
Run `hm_medium_h011_codex_seed42_budget300_v2` continues the same conversations,
14 already accepted fold0 programs,22 research calls and99 API attempts; no counts
are reset. Reports: `reports/medium_h011_codex_budget300_v2/`. The old state and
sources are preserved in `reports/medium_h011_codex_v1/before_budget300/`.
20 accepted feature checks and300 actual API POSTs per fold are unchanged.
The historical preparation below describes the original40-call protocol.

## Autonomous H011 experiment: launch authorized

On2026-10-18, after H010 completed, the user explicitly authorized H011 launch
and requested provider-timeout handling. This supersedes the earlier deferral.
Before-response connection failures and HTTP429/5xx are retried at most3 times
with5/15/30-second backoff; all failed/retried POSTs remain in the300/fold cap.
Partial stream failures stop for inspection. Native retries remain disabled;
the launch command overrides the stream idle timeout to1200000ms to allow
the bounded gateway recovery. Completed tool actions are never auto-replayed.

The user initially deferred H011 on2026-10-18 to avoid interfering with
current runs; the following preparation record describes that earlier state.
The earlier standalone environment smoke is a separate diagnostic.

Protocol: [H011_PROTOCOL.md](H011_PROTOCOL.md). Nine private Codex profiles
(three populations for each of three folds), shared20 accepted checks/fold,
40 terminal research requests/fold and a recording gateway enforcing300 actual
model POSTs/fold. Native conversations resume separately per population.
The parent controller rotates populations, selects top3+constant on confirmation,
freezes all three folds, then evaluates/replays and builds the comparison.

Preparation checks: `h011_verification.json` and
`h011_tools_verification.json`; mocked API/SSE, model parameter/call cap,
population isolation, protected budgets, original evaluator hashes and real
terminal CPU/OS isolation. These checks used0 real H011 API calls and0 trainings.
The start-admission check was actually tested against the live H010 and refused
to start H011 while H010 was alive. There is no automatic waiting/launch watcher.

Later, from Windows PowerShell at the project root:

```powershell
# Inspect readiness only; does not launch anything.
python LLMResearch/agent_environment/launch_h011_windows.py

# Start only when you decide to do so, after current experiments finish.
python LLMResearch/agent_environment/launch_h011_windows.py --start
```

The second command still refuses admission if another project controller is
alive. Status/logs will be in `reports/medium_h011_codex_v1/`; until actual
launch, `prepared.json` records `prepared_not_started`. This complete controller
has not been exercised end-to-end on real model search yet; that is the deferred
experiment. It preserves frozen configs/sources and stops on a provider failure
for explicit inspection. Final figures require visual review.

## Standalone interactive or smoke use

This is an actual separate **Codex CLI** session using the configured
`gpt-6.1-sol` API provider. It has a private Codex home, persistent conversation,
working directory, notes, and local MCP tools. It does not alter the normal
Codex configuration or the `unsloth`/existing Python environments.

The native agent smoke succeeded on2026-10-18: GPT called `fold.status`, then
`fold.terminal`, imported pandas/NumPy/DuckDB, read190260 training pairs from
fold0, and observed that `/mnt/c` was absent. No model training/evaluation
occurred; all20 checks remained available. Logs are in
`sessions/standalone_v2/fold_0/`; OS/MCP verification is `verification.json`.

From **Windows PowerShell**, in the project root:

```powershell
# Interactive conversation with the separate agent.
python LLMResearch/agent_environment/launch_windows.py --fold 0 --interactive

# Autonomous task from a UTF-8 prompt file, with persistent logs.
python LLMResearch/agent_environment/launch_windows.py --fold 0 --prompt-file task.txt

# Environment check only; no model training.
python LLMResearch/agent_environment/launch_windows.py --fold 0 --smoke
```

Use `--fold 1` or `--fold 2` for another fold; each has separate work/history.
Use `--session another_name` for an independent experiment. Starting a command
creates a new Codex thread; the work files and evaluation budget persist in
that session/fold. Thread IDs/events remain in its separate Codex home.

Available tools:
- `fold.status`: schema, training cutoffs, remaining checks.
- `fold.terminal`: bash/Python commands inside a bubblewrap OS sandbox.
- `fold.read_file` / `fold.write_file`: files inside the agent's own `/work`.
- `fold.evaluate_features`: original H009 feature validator, train pairs,
  LightGBM and search feedback. At most20 accepted AST-distinct programs;
  budget state is outside the agent's writable folder. At most100 submitted
  invalid/valid programs. No test/confirmation tool is exposed.

Terminal filesystem: `/work` writable; the train-only research database at
`/data/research.duckdb` and existing runtime read-only. Host project files and
network are absent inside this terminal. The Codex frontend runs on Windows;
its native command tools/apps/browser/image tool are disabled, and its native
filesystem sandbox is read-only. Agent commands go through the isolated MCP
terminal. The model's API transport remains outside that terminal. The API
credential is supplied to the frontend only in its child-process environment.

The standalone environment is **separate from the H010 v2 experiment**. Its
current task was only a smoke test. A full Codex-driven experiment changes
the agent instructions and tool interface and needs its own protocol/run ID;
it must not silently replace H010 or claim H009's three-island controls.
It does not automatically perform final confirmation, test scoring, replay or
comparison. Those remain the parent controller's job after selections freeze.
Codex has additional system/context overhead;20 checks do not mean20 API
requests or equal token costs. Explicit HTTP/stream retries are disabled in
this profile. Keep the API/provider's unknown model-identity caveat.
