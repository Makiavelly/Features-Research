"""Read-only resource/schema check; never reads the API secret."""
import json
import os
from pathlib import Path
import sys
import importlib.metadata
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]
print('python', sys.executable, flush=True)
print('versions', {n: importlib.metadata.version(n) for n in ['torch','numpy','pandas','pyarrow','duckdb','transformers']}, flush=True)
print('cuda', torch.cuda.is_available(), torch.cuda.get_device_name() if torch.cuda.is_available() else None, flush=True)
for split in ['train','val','test']:
    f = pd.read_parquet(ROOT/f'data/rel-hm/tasks/user-item-purchase/{split}.parquet', columns=['timestamp'])
    print(split, len(f), sorted(map(str, f.timestamp.unique()))[-16:], flush=True)
print('old_cohort', pd.read_csv(ROOT/'data/rel-hm-small-v1/customer_id_map.csv').shape, flush=True)
print('processes', flush=True)
os.system('ps -eo pid,etime,args')
