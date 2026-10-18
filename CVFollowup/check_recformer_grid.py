"""Validate generated schedules and frozen hyperparameters without model fitting."""
import ast
import math
from common import ROOT,REPORT,write,sha
from recformer_grid import GRID,build

checks=[]
for fold in range(3):
    for label,(lr,warmup) in GRID.items():
        folder,runtime=build(fold,label)
        tree=ast.parse(runtime.read_text(encoding='utf-8'))
        function=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='lr_multiplier')
        scope={};exec(compile(ast.Module(body=[function],type_ignores=[]),'<scheduler>','exec'),scope)
        schedule=scope['lr_multiplier'];total=3000
        assert schedule(0,total)==1/warmup and schedule(warmup-1,total)==1
        assert schedule(warmup,total)==1 and schedule(total,total)==0 and schedule(total+10,total)==0
        assert all(schedule(step,total)>=schedule(step+1,total) for step in range(warmup,total))
        assert str(folder) in runtime.read_text(encoding='utf-8')
        checks.append({'fold':fold,'label':label,'peak_lr':lr,'warmup':warmup,'runtime_sha256':sha(runtime)})
write(REPORT/'recformer_grid_verification.json',{'passed':True,'settings':checks,'model_fits':0,'api_calls':0})
print('Recformer schedules/source checks:12 settings passed; no model fitting.')
