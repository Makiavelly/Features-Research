from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ContextGNN/upstream"))
from contextgnn.nn.models import ContextGNN, IDGNN
print("CONTEXT_IMPORT_OK", flush=True)
from relbench import load_dataset
dataset = load_dataset(ROOT / "data/rel-hm-small-v1")
db = dataset.get_db()
task = dataset.load_task("user-item-purchase")
print({name: len(table.df) for name, table in db.table_dict.items()}, flush=True)
print({split: len(task.get_table(split).df) for split in ["train", "val", "test"]}, flush=True)
