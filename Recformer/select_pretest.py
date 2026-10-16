"""Freeze epoch0 vs trained choice from completed validation history before tests."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse
import json

parser=argparse.ArgumentParser()
parser.add_argument('variant',choices=['low_lr_warmup','freeze_lower6'])
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
base=root/'Recformer/results'/f'hm_small_{args.variant}_seed42_v1'
history=json.loads((base/'history.json').read_text())
assert len(history)==4
assert not (base/'finetuned/test_predictions.npy').exists()
assert not (base/'zero_shot/test_predictions.npy').exists()
zero=json.loads((base/'zero_shot/initial_val.json').read_text())['map']
best=max(history,key=lambda row:row['val_metrics']['map'])
selected='finetuned' if best['val_metrics']['map']>zero else 'zero_shot'
result={'time_moscow':datetime.now(ZoneInfo('Europe/Moscow')).isoformat(),
        'selected_kind':selected,'zero_shot_val_map':zero,'best_trained_val_map':best['val_metrics']['map'],
        'best_stage':best['stage'],'best_epoch':best['epoch'],'test_predictions_absent':True,
        'criterion':'validation MAP only; epoch0 eligible'}
(base/'selection_pretest.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
