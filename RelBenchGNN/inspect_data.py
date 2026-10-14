"""Record dimensions, time ranges and schema of the reusable local snapshot."""
import json
from pathlib import Path

import pyarrow.parquet as pq
from relbench import load_dataset

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/rel-hm"


def main():
    stats = {"tables": {}, "tasks": {}}
    for file in sorted((DATA / "db").glob("*.parquet")):
        parquet = pq.ParquetFile(file)
        stats["tables"][file.stem] = {"rows": parquet.metadata.num_rows, "bytes": file.stat().st_size,
                                       "schema": str(parquet.schema_arrow)}
    ds = load_dataset(DATA)
    stats["val_timestamp"] = str(ds.val_timestamp)
    stats["test_timestamp"] = str(ds.test_timestamp)
    for name in ds.get_task_names():
        task = ds.load_task(name)
        task_info = {"task_type": task.task_type.value, "splits": {}}
        for split in ["train", "val", "test"]:
            table = task.get_table(split, mask_input_cols=False)
            task_info["splits"][split] = {"rows": len(table), "min_timestamp": str(table.df.timestamp.min()),
                                         "max_timestamp": str(table.df.timestamp.max())}
        stats["tasks"][name] = task_info
    (ROOT / "data/dataset_summary.json").write_text(json.dumps(stats, indent=2))
    print(json.dumps(stats, indent=2), flush=True)


if __name__ == "__main__":
    main()
