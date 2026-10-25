# H010: train-data research tools added to H009

Authorized 2026-10-18 by the user. Run: `hm_medium_h010_research_seed42_v1`.
This is a new independent stochastic search, compared primarily with the
original H009 budget20 on the same three medium-v2 folds. Existing results and
frozen runtimes are immutable. No claims of an untouched outer test: these
weeks have already been inspected in previous experiments.

Keep H009's model/provider, temperature/reasoning, output tokens, seed42,
three isolated round-robin populations, full own-population conversations,
up to3 repairs, generated-only features (max36), unchanged training pairs,
150-round/31-leaf/4CPU LightGBM, search256 and top3+constant confirmation.
Target20 accepted AST-distinct programs PER FOLD, not20 API messages.
Numerical feature duplicates remain a separate audit, not assumed distinct.
Do not add incumbent retention or additional model-selection diagnostics.

The treatment is an optional `query_train` research tool. The text API protocol
uses a JSON command {"action":"query_train","sql":"SELECT ..."}; otherwise
the model returns its complete Python program. Native tool-call support is not
assumed for the configured third-party provider. Model sees tool instructions
and table schemas; it chooses statistics and hypotheses itself. A Python source
comment can record its hypothesis. No manually selected predictive statistics
are supplied. The original feature validator and evaluator remain unchanged.

Research database tables:
- `train_pairs`: the unchanged sampled training pairs, timestamp, label and
  encoded raw15 attributes; train labels are deliberately available for research.
- `train_history`: visible transaction history independently constructed at
  EACH training timestamp, with `cutoff` and `days_ago`, using the original host
  encodings. Join to pairs by timestamp=cutoff for time-consistent analysis.
- `history`: the snapshot at the LAST training cutoff, for descriptive research.
  Do not join this snapshot to earlier labels as if it were their past.

No validation/test targets, IDs sampled from validation, predictions, metrics,
source filenames, or other-fold tables are provided to the research database.
Training labels end no later than the inner-validation prediction cutoff.
Research can inspect all train data, as ordinary training does; the eventual
feature function still receives only history at its actual prediction cutoff,
without labels or a route to the research tool. No model fitting is exposed by
SQL; every accepted candidate is trained and scored through the existing loop.

Budget:40 tool requests/fold (islands0/1/2:14/13/13), including invalid requests;
max4 tool requests in a single generation, then request program submission.
Global300 actual HTTP POSTs/fold, including research, repairs and failures.
Maximum20seconds/query,512MB DuckDB memory,2CPU, read-only database,
external access disabled, one SELECT/WITH statement, max40rows/24columns,
max12000 result characters. Stop on provider/transport failure and preserve
responses. Resume uses saved API responses and tool outputs without repaying.
Queries/results and all reasoning/code returned by API remain in their own
population, never shared across folds or populations. No silent history trimming.

Freeze runtime/config/data hashes before requests. Before paid calls verify
unchanged evaluator/validator hashes, existing validator regressions, SQL
external-access denial, SELECT-only execution, limits, time boundaries,
population isolation, caching and resume with mocked transport, and a separately
labelled scripted CPU smoke. All three folds must finish selection before ANY
new outer evaluation. Freeze selected program/model hashes, reload and replay
all validation/test predictions; independently recompute AP retaining all
original positives including unavailable items. Report search/confirmation,
fold and pooled test MAP, paired customer bootstrap5000/seed42 against H009-20,
query/API/token usage, feature counts and matrix-diversity diagnostics.

Equal candidate budgets do not imply equal API tokens, research compute or
amount of information. Same-fold results are exploratory because test weeks
were previously viewed. Any confirmation on new weeks is a separate protocol.
