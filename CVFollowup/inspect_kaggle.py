"""Inspect report JSON directly in an archive without loading checkpoint files."""
import argparse
import json
import zipfile

def main():
    parser=argparse.ArgumentParser();parser.add_argument('archive');args=parser.parse_args()
    with zipfile.ZipFile(args.archive) as z:
        def read(name):return json.loads(z.read(name))
        run=read('run_manifest.json');export=read('export_manifest.json');label=run['label']
        print('LABEL',label,'GPU',run.get('gpu'),'COMPLETED',export['completed_folds'],flush=True)
        for fold in range(3):
            base=f'fold_{fold}/recformer_grid/{label}'
            summary=read(base+'/training_summary.json');history=read(base+'/history.json')
            print(json.dumps({'fold':fold,'best_validation_MAP_percent':100*summary['best_trained_val_map'],
                'epochs':summary['epochs'],'seconds':summary['training_and_validation_seconds'],
                'optimizer_updates':summary['optimizer_updates'],'amp_skipped_updates':summary['amp_skipped_updates'],
                'epoch_validation_MAP_percent':[100*h['val_metrics']['map'] for h in history]},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
