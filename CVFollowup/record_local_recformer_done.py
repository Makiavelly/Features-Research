from common import ROOT,OUT,REPORT,read,write,sha,record

rows=[]
for label in ['lr1e6_w100','lr3e6_w300']:
    for fold in range(3):
        folder=OUT/f'fold_{fold}/recformer_grid'/label
        summary=read(folder/'training_summary.json')
        assert summary['epochs']==4 and read(folder/'frozen_verification.json')['passed']
        rows.append({'label':label,'fold':fold,'summary':summary,
            'checkpoint_sha256':sha(folder/'finetuned/best.pt')})
write(REPORT/'recformer_local_training_complete.json',{'local_fits_complete':6,'rows':rows,
    'selection_performed':False,'next':'Wait for two Kaggle result archives; import before global validation selection'})
record('recformer_local_assignments_complete','All six assigned local Recformer fits complete (two LR/warmup settings x three folds, four epochs each). GPU idle while awaiting two Kaggle result archives. Global selection and outer scoring not performed.',
    'hm_medium_recformer_distributed_v1',status='waiting_kaggle_imports',artifacts='reports/medium_followup_v1/recformer_local_training_complete.json')
