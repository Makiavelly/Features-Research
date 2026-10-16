"""Recformer transfer to frozen small H&M: weekly multi-positive full softmax."""
import argparse
import gc
import hashlib
import importlib
import importlib.metadata
import json
import math
from pathlib import Path
import random
import sys
import time
import types
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'RelBenchGNN'))
from tracking import record
from relbench import load_dataset

# Import only inference modules: upstream __init__ also imports Lightning.
package = types.ModuleType('recformer')
package.__path__ = [str(ROOT/'Recformer/upstream/recformer')]
sys.modules['recformer'] = package
models = importlib.import_module('recformer.models')
tokenization = importlib.import_module('recformer.tokenization')
ASSETS = ROOT/'data/models/recformer'
DATA = ROOT/'data/rel-hm-small-v1'
OUT = ROOT/'Recformer/results/hm_small_seed42_v1'
RUN = 'hm_recformer_small_seed42_v1'

def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n',encoding='utf-8')

def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()

def seed():
    random.seed(42)
    np.random.seed(42)
    torch.manual_seed(42)
    torch.cuda.manual_seed_all(42)

def weekly_loss(logits, targets):
    logp=logits.log_softmax(-1)
    return torch.stack([-logp[j,torch.as_tensor(np.unique(true),device=logits.device)].mean() for j,true in enumerate(targets)]).mean()

def visible_items(dates,items,cutoff):
    n=np.searchsorted(dates,np.datetime64(cutoff),side='right')
    assert n==0 or dates[n-1]<=np.datetime64(cutoff)
    return items[:n][-50:],n

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--probe',action='store_true')
    parser.add_argument('--verify-only',action='store_true')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    seed()
    print('Preparing frozen small dataset and tokenizer',flush=True)
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False
    device=torch.device('cuda')
    task=load_dataset(DATA).load_task('user-item-purchase')
    tables={s:task.get_table(s,mask_input_cols=False) for s in ['train','val','test']}
    tx=pd.read_parquet(DATA/'db/transactions.parquet')
    tx['row_order']=np.arange(len(tx))
    tx=tx.sort_values(['customer_id','t_dat','row_order'],kind='stable')
    histories={int(u):(g.t_dat.to_numpy(),g.article_id.to_numpy()) for u,g in tx.groupby('customer_id',sort=False)}
    article=pd.read_parquet(DATA/'db/article.parquet').sort_values('article_id')
    assert np.array_equal(article.article_id,np.arange(5000))
    config=models.RecformerConfig.from_pretrained(ASSETS,local_files_only=True)
    config.max_attr_num=3
    config.max_attr_length=32
    config.max_item_embeddings=51
    config.attention_window=[64]*config.num_hidden_layers
    config.max_token_num=256
    config.item_num=5000
    config.finetune_negative_sample_size=0
    tokenizer=tokenization.RecformerTokenizer.from_pretrained(str(ASSETS),config)
    tokens={}
    texts=[]
    for row in article.fillna('').itertuples():
        attrs={'title':row.prod_name,
               'category':'; '.join([row.product_type_name,row.product_group_name,row.section_name]),
               'description':'; '.join([row.colour_group_name,row.graphical_appearance_name,row.detail_desc])}
        tokens[int(row.article_id)]=tokenizer.encode_item(attrs)
        texts.append(attrs)
        if len(tokens)%1000==0:
            print('Tokenized items',len(tokens),flush=True)
    encoded={}
    max_used={}
    for split,table in tables.items():
        encoded[split]=[]
        max_used[split]=None
        for row in table.df.itertuples():
            dates,items=histories.get(int(row.customer_id),(np.array([],dtype='datetime64[ns]'),np.array([],dtype=int)))
            used,n=visible_items(dates,items,row.timestamp)
            seq=[tokens[int(i)] for i in used]
            encoded[split].append(tokenizer.encode(seq,encode_item=False))
            if n:
                date=str(dates[n-1])
                max_used[split]=max(max_used[split] or date,date)
    # Behavioral invariants for cutoff and the multi-positive objective.
    d=np.array(['2020-01-01','2020-01-02','2020-01-03'],dtype='datetime64[ns]')
    assert np.array_equal(visible_items(d,np.array([1,2,3]),'2020-01-02')[0],np.array([1,2]))
    assert np.array_equal(visible_items(d[:2],np.array([1,2]),'2020-01-02')[0],visible_items(d,np.array([1,2,999]),'2020-01-02')[0])
    l=torch.zeros(2,5,requires_grad=True)
    loss=weekly_loss(l,[[1,2],[3]])
    assert abs(float(loss)-math.log(5))<1e-6
    loss.backward()
    assert l.grad[0,1]<0 and l.grad[0,2]<0 and l.grad[0,0]>0
    assert torch.allclose(weekly_loss(l,[[1,2],[3]]),weekly_loss(l,[[2,1,1],[3]]))
    dump(OUT/'data_checks.json',{'subset_sha256':sha(DATA/'subset_manifest.json'),
         'rows':{s:len(t.df) for s,t in tables.items()},'catalog':5000,
         'max_used_transaction':max_used,'cutoff_policy':'t_dat <= row.timestamp; future excluded before history truncation',
         'same_day_order':'source transaction row order, not known intraday chronology',
         'repeats_preserved':True,'cutoff_and_loss_behavior_checks':True,'text_example':texts[0],
         'unique_tokenized_items':len({json.dumps(t) for t in tokens.values()}),
         'input_sha256':hashlib.sha256(json.dumps(encoded,sort_keys=True).encode()).hexdigest()})
    def batch(seqs):
        # Upstream padding mutates lists, so supply copies of cached inputs.
        copy=[{k:list(v) for k,v in seq.items()} for seq in seqs]
        return {k:torch.tensor(v,device=device) for k,v in tokenizer.padding(copy,pad_to_max=False).items()}
    model=models.RecformerForSeqRec(config)
    weights=torch.load(ASSETS/'recformer_seqrec.bin',map_location='cpu',weights_only=True)
    missing,unexpected=model.load_state_dict(weights,strict=False)
    assert not missing, missing
    assert all(k.startswith('lm_head.') for k in unexpected),unexpected
    dump(OUT/'checkpoint_loading.json',{'missing':missing,'unexpected':unexpected,'sha256':sha(ASSETS/'recformer_seqrec.bin')})
    del weights
    model.to(device)
    def encode_items():
        model.eval()
        vectors=[]
        with torch.no_grad(),torch.autocast('cuda',dtype=torch.float16):
            for start in range(0,5000,32):
                seqs=[tokenizer.encode([tokens[i]],encode_item=False) for i in range(start,min(start+32,5000))]
                vectors.append(model.longformer(**batch(seqs)).pooler_output.float())
        return F.normalize(torch.cat(vectors),dim=-1).detach()
    def scores_for(seqs,item_vectors):
        with torch.autocast('cuda',dtype=torch.float16):
            output=model.longformer(**batch(seqs)).pooler_output
        # Matmul avoids broadcasting a batch x catalog x 768 cosine tensor.
        return F.normalize(output.float(),dim=-1)@item_vectors.T/config.temp
    def evaluate(split,item_vectors,folder=None):
        model.eval()
        start=time.perf_counter()
        scores=[]
        with torch.no_grad():
            for offset in range(0,len(encoded[split]),8):
                scores.append(scores_for(encoded[split][offset:offset+8],item_vectors).cpu().numpy())
        scores=np.concatenate(scores)
        assert np.isfinite(scores).all()
        pred=np.argsort(-scores,axis=1,kind='stable')[:,:12]
        metric=task.evaluate(pred,tables[split])
        # Independent AP calculation against actual weekly target sets.
        ap=[]
        for p,true in zip(pred,tables[split].df.article_id):
            hit=np.isin(p,true)
            ap.append(float((np.cumsum(hit)/np.arange(1,13)*hit).sum()/min(12,len(true))))
        assert abs(np.mean(ap)-metric['map'])<1e-12
        if folder:
            folder.mkdir(exist_ok=True)
            np.save(folder/f'{split}_scores.npy',scores)
            np.save(folder/f'{split}_predictions.npy',pred)
            np.save(folder/f'{split}_ap.npy',ap)
        return metric,time.perf_counter()-start,scores,pred
    if args.probe:
        started=time.perf_counter()
        vectors=encode_items()
        item_seconds=time.perf_counter()-started
        optimizer=torch.optim.AdamW(model.parameters(),lr=5e-5,foreach=False)
        scaler=torch.cuda.amp.GradScaler()
        model.train()
        times=[]
        for step in range(5):
            started=time.perf_counter()
            optimizer.zero_grad(set_to_none=True)
            logits=scores_for(encoded['train'][step*4:step*4+4],vectors)
            loss=weekly_loss(logits,tables['train'].df.iloc[step*4:step*4+4].article_id.tolist())
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            torch.cuda.synchronize()
            times.append(time.perf_counter()-started)
        result={'item_encode_seconds':item_seconds,'batch4_step_seconds':times,
                'peak_cuda_bytes':torch.cuda.max_memory_allocated(),
                'estimated_4epoch_training_seconds':np.median(times[1:])*math.ceil(4804/4)*4,
                'parameters':sum(p.numel() for p in model.parameters()),'scope':'smoke timing only; no scored experiment'}
        dump(OUT/'probe.json',result)
        print(json.dumps(result),flush=True)
        return
    cfg={'seed':42,'max_tokens':256,'max_items':50,'attributes':3,'max_attr_length':32,
         'batch':4,'gradient_accumulation':4,'epochs_per_stage':2,'stages':2,
         'lr':5e-5,'weight_decay':0.,'precision':'FP16 autocast; FP32 normalized cosine matmul',
         'objective':'mean per-user-time mean positive negative-log full softmax; catalog5000',
         'subset_sha256':sha(DATA/'subset_manifest.json'),'pretrained_sha256':sha(ASSETS/'recformer_seqrec.bin'),
         'source_commit':'26b00a58e7affe0c54a89c143ea7bce37f2e8e08',
         'runner_sha256':sha(Path(__file__)),
         'asset_manifest':json.loads((ASSETS/'download_manifest.json').read_text()),
         'runtime':{n:importlib.metadata.version(n) for n in ['torch','transformers','numpy','pandas']},
         'budget_policy':'4 full epochs; no test before checkpoint selection; no continuation under same run after changes'}
    if args.verify_only:
        checks={}
        for kind in ['zero_shot','finetuned']:
            folder=OUT/kind
            ckpt=torch.load(folder/'best.pt',map_location=device,weights_only=True)
            model.load_state_dict(ckpt['state'],strict=True)
            vectors=ckpt['item_vectors'].to(device)
            checks[kind]={}
            for split in ['val','test']:
                metric,seconds,scores,pred=evaluate(split,vectors)
                old=np.load(folder/f'{split}_scores.npy')
                identical=np.array_equal(pred,np.load(folder/f'{split}_predictions.npy'))
                close=np.allclose(old,scores,rtol=1e-4,atol=1e-4)
                checks[kind][split]={'passed':bool(close and identical),'predictions_identical':bool(identical),
                                     'scores_close':bool(close),'max_score_difference':float(np.abs(old-scores).max()),'map':metric['map'],'seconds':seconds}
            checks[kind]['checkpoint_sha256']=sha(folder/'best.pt')
        passed=all(checks[k][s]['passed'] for k in checks for s in ['val','test'])
        dump(OUT/'verification.json',{'passed':passed,'checks':checks})
        assert passed,checks
        record('recformer_verified','Recformer small: independent full val/test checkpoint and item-cache replay passed',RUN+'_inference',status='verified',checks=checks)
        return
    assert not (OUT/'finetuned/metrics.json').exists(),'Completed experiment already exists'
    dump(OUT/'config.json',cfg)
    record('recformer_start','Recformer small: zero-shot plus two-stage fine-tuning, frozen small subset',RUN,status='training',config=cfg)
    started=time.perf_counter()
    torch.cuda.reset_peak_memory_stats()
    vectors=encode_items()
    zero=OUT/'zero_shot'
    fine=OUT/'finetuned'
    zero.mkdir(exist_ok=True)
    fine.mkdir(exist_ok=True)
    def save(path,vectors,stage,epoch):
        torch.save({'state':model.state_dict(),'item_vectors':vectors.cpu(),'stage':stage,'epoch':epoch},path)
    save(zero/'best.pt',vectors,0,0)
    zero_metric,_,_,_=evaluate('val',vectors)
    dump(zero/'initial_val.json',zero_metric)
    history=[]
    best=-1.
    optimizer=torch.optim.AdamW(model.parameters(),lr=5e-5,weight_decay=0.,foreach=False)
    scaler=torch.cuda.amp.GradScaler()
    for stage in [1,2]:
        if stage==2:
            ckpt=torch.load(fine/'best.pt',map_location=device,weights_only=True)
            model.load_state_dict(ckpt['state'],strict=True)
            vectors=ckpt['item_vectors'].to(device)
            del ckpt
        for epoch in [1,2]:
            epoch_start=time.perf_counter()
            if stage==1:
                vectors=encode_items()
            model.train()
            order=np.random.default_rng(42+stage*10+epoch).permutation(len(encoded['train']))
            optimizer.zero_grad(set_to_none=True)
            losses=[]
            for step,offset in enumerate(range(0,len(order),4)):
                indices=order[offset:offset+4]
                logits=scores_for([encoded['train'][i] for i in indices],vectors)
                loss=weekly_loss(logits,[tables['train'].df.iloc[int(i)].article_id for i in indices])
                assert torch.isfinite(loss)
                # Four batches each accumulation group; last group is also scaled correctly.
                group_size=min(4,math.ceil(len(order)/4)-(step//4)*4)
                scaler.scale(loss/group_size).backward()
                if (step+1)%4==0 or offset+4>=len(order):
                    scaler.unscale_(optimizer)
                    torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                    scaler.step(optimizer)
                    scaler.update()
                    optimizer.zero_grad(set_to_none=True)
                losses.append(float(loss.detach()))
                if step%100==0:
                    print('progress',stage,epoch,step,len(order),float(loss.detach()),flush=True)
            metric,seconds,_,_=evaluate('val',vectors)
            row={'stage':stage,'epoch':epoch,'train_loss':float(np.mean(losses)),
                 'val_metrics':metric,'epoch_seconds':time.perf_counter()-epoch_start,'val_seconds':seconds,'rows':len(order)}
            history.append(row)
            if metric['map']>best:
                best=metric['map']
                save(fine/'best.pt',vectors,stage,epoch)
            dump(OUT/'history.json',history)
            record('recformer_epoch',f'Recformer stage {stage} epoch {epoch}: val MAP {metric["map"]*100:.5f}%',RUN,status='training',epoch=len(history),progress=row)
            print(json.dumps(row),flush=True)
    training_seconds=time.perf_counter()-started
    del optimizer,scaler
    gc.collect()
    torch.cuda.empty_cache()
    for kind in ['zero_shot','finetuned']:
        folder=OUT/kind
        ckpt=torch.load(folder/'best.pt',map_location=device,weights_only=True)
        model.load_state_dict(ckpt['state'],strict=True)
        vectors=ckpt['item_vectors'].to(device)
        result={'model':'Recformer '+kind,'config':cfg,'selected_stage':ckpt['stage'],'selected_epoch':ckpt['epoch'],
                'training_and_validation_seconds':training_seconds if kind=='finetuned' else 0.,
                'peak_cuda_bytes':torch.cuda.max_memory_allocated()}
        del ckpt
        for split in ['val','test']:
            metric,seconds,_,_=evaluate(split,vectors,folder)
            result[split+'_metrics']=metric
            result[split+'_inference_seconds']=seconds
        dump(folder/'metrics.json',result)
        record('recformer_measured',f'Recformer {kind}: metrics measured, independent replay pending',RUN+'_'+kind,status='measured_pending_verification',val_metrics=result['val_metrics'],test_metrics=result['test_metrics'],artifacts=str(folder.relative_to(ROOT)))
        print(kind,json.dumps(result),flush=True)

if __name__=='__main__':
    try:
        main()
    except Exception as error:
        record('recformer_error','Recformer small error: '+str(error),RUN,status='failed')
        raise
