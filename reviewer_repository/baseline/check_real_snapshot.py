import json
from manual_features import ManualFeatures, ROOT
import pandas as pd

engine = ManualFeatures(cache_dir=ROOT / "baseline/cache/real_smoke")
engine.prepare("2020-09-07", [0, 1])
frame = engine.frame(pd.DataFrame({"customer_id": [0, 1], "article_id": [0, 1]}))
maximum = engine.con.sql("SELECT max(t_dat) FROM hist").fetchone()[0]
assert len(frame) == 2 and len(engine.feature_names) == 126
assert maximum is None or pd.Timestamp(maximum) <= pd.Timestamp("2020-09-07")
result = {"passed": True, "feature_count": len(engine.feature_names), "pair_rows": len(frame),
          "cutoff": "2020-09-07", "max_used_transaction_date": str(maximum),
          "scope": "real-data SQL and memory check; not a trained baseline metric"}
engine.close()
destination = ROOT / "baseline/results/real_sql_check.json"
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text(json.dumps(result, indent=2))
print(json.dumps(result), flush=True)
