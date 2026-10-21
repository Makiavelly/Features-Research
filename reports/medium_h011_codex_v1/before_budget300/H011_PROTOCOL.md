# H011: autonomous Codex GPT-6.1 Sol agent with train-only terminal

Authorized2026-10-18: user chose an autonomous agent that investigates folds and
conducts the experiment. ID `hm_medium_h011_codex_seed42_v1`; session
`h011_codex_seed42_v1`; reports `reports/medium_h011_codex_v1/`.
H010 remains separate and unchanged. No programs, search feedback or workspace
history from H010 or the standalone environment smokes enter H011.

Same medium-v2 three folds, cohort/catalog, original train pairs, generated-only
feature contract, evaluator/validator, LightGBM150rounds/31leaves/4CPU, search256,
top3+constant disjoint confirmation, full original targets and metric as H009.
Model/provider `gpt-6.1-sol`, low reasoning, temperature.8, max2048output tokens
are enforced by a local recording API gateway. Codex does not expose the old
per-proposal sampling seed: model randomness/provider implementation is not
guaranteed. Data/model evaluator seeds remain42. Three isolated Codex homes,
workspaces, conversations and tools per fold; no cross-fold/population feedback.
Round-robin turns across populations; each turn may submit one accepted program
or up to4 programs (proposal+3repairs). Shared budget20 accepted AST-distinct
feature programs PER FOLD, enforced outside writable workspaces. Duplicate and
invalid submissions consume the turn's submission allowance but not accepted
checks. Global maximum100 submitted programs/fold and300 actual Responses POSTs
including failures. Gateway records every actual POST, token usage and SSE;
frontend HTTP/stream retries are disabled and gateway cap cannot be reset by
the agent. Before the first paid request, the user authorized launch and asked
for provider-timeout handling. The gateway retries transient connection errors
and HTTP429/500/502/503/504 at most3 times, waiting5/15/30 seconds, ONLY before
response headers are received/forwarded. Each retry is a separately recorded
actual POST under the same300 cap; failed attempts and recovery links persist.
No model tool can have executed from these unforwarded responses. Interrupted
streams, non-transient errors or exhausted retries stop the controller with
history saved for inspection; completed responses/tools are never auto-replayed.

Train-only research: bubblewrap terminal sees /work (own writable files),
/data/research.duckdb (read-only) and existing runtime libraries. Host project,
other populations/folds, labels from validation/test, API secrets, network and
GPU are unavailable to terminal commands. pandas/NumPy/DuckDB statistics and
notes/code are allowed. Do not fit predictive models in terminal; all candidate
training/search scoring goes through evaluate_features. Terminal requests count
as research:40/fold (14/13/13),60seconds/request, max24000output bytes, CPU affinity2.
MCP file read/write stay under /work and do not provide statistics or model scores.
One successful initial research command per population is required before its
first submission; agent chooses statistical questions and hypotheses itself.
Native frontend shell/apps/browser/image tools disabled; host native filesystem
sandbox read-only. The API frontend runs on Windows outside the isolated Linux
terminal. This is not a claim that the entire Codex frontend is OS-containerized.

This is a distinct agentic protocol, not the sole-variable H010 tool experiment:
Codex instructions, native tools, token/context overhead, turn orchestration and
sampling controls differ from H009. Equal20 checks do not imply equal token or
compute cost. Compare primarily with original H009-20; include H010 separately
if complete. One seed and already-viewed outer weeks permit only exploratory
same-week conclusions. Do not tune based on outer results or overwrite old runs.

Before paid work: verify gateway field enforcement/count cap with mocked upstream,
MCP own-population status, OS isolation, time boundaries, byte-identical original
evaluator hashes and externally held budgets; scripted CPU smoke is separate.
Freeze protocol/source/config hashes. All3 fold selections must finish and be
hashed before new outer scoring. Parent controller handles confirmation, selection
barrier, heldout/val/test scoring, independent AP and full frozen-model replays.
Report all fold and pooled metrics, paired customer bootstrap5000/seed42 versus
H009-20, per-user AP, API/research usage, selected hypotheses/programs and limitations.
No success claim until final metrics/replays and figure verification exist.
