"""Reuse the tested TDM implementation, only fixed-tree beam64."""
import argparse
import os
import sys
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')
import numpy as np
import torch
from common import paths,write,read,sha,save_predictions
from build_runtime import build

def run(fold,stage):
    data,out=paths(fold);runtime=build(fold);sys.path.insert(0,str(runtime))
    import tdm_common as c
    import tdm_train as trainer
    c.seed();dataset=c.Dataset();device=torch.device('cuda')
    c.OUT.mkdir(exist_ok=True)
    if stage=='train':
        if (c.OUT/'fixed/training_summary.json').exists():return
        tree=c.build_tree(10000,categories=dataset.article.product_type_no.to_numpy())
        trainer.train('fixed',tree,dataset,device,{'tree':'fixed categories; no clustering'})
        write(c.OUT/'selection_pretest.json',{'checkpoint_sha256':sha(c.OUT/'fixed/best.pt'),'dataset_sha256':dataset.fingerprint})
    else:
        selected=read(c.OUT/'selection_pretest.json');assert sha(c.OUT/'fixed/best.pt')==selected['checkpoint_sha256']
        folder=c.OUT/'fixed/beam';folder.mkdir(parents=True,exist_ok=True)
        model,tree,checkpoint=trainer.load('fixed',device)
        for split in ['val','test']:
            result,arrays=c.evaluate(model,tree,dataset,split,'beam',device)
            pred=arrays['predictions']
            if stage=='verify':
                np.testing.assert_array_equal(pred,np.load(folder/f'{split}_predictions.npy'))
            else:
                metric=save_predictions(folder,split,pred,dataset.tables[split].df)
                assert abs(metric['map']-result['map'])<1e-12
                write(folder/f'{split}_timing.json',result)
        if stage=='verify':write(folder/'verification.json',{'passed':True,'full_replay':True})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('fold',type=int);p.add_argument('stage',choices=['train','evaluate','verify'])
    a=p.parse_args();run(a.fold,a.stage)
