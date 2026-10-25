"""CPU-only balance-scale feature compliance and four-fold CV diagnostic."""
import os
if __name__=='__main__':
    os.environ['CUDA_VISIBLE_DEVICES']=''
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:
        os.environ[key]='1'
import ast
import argparse
import json
from pathlib import Path
import re
import resource
import signal
import traceback
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
import xgboost

FORBIDDEN={'open','eval','exec','compile','getattr','setattr','globals','locals','vars','__import__',
           'input','breakpoint','help','dir','type','super'}


def extract(text):
    blocks=re.findall(r'```(?:python)?\s*\n(.*?)```',text,re.S|re.I)
    source=next((b for b in blocks if 'def modify_features' in b),text).strip()
    if not re.search(r'def modify_features(?:_v\d+)?\s*\(',source):
        # Authors sample a continuation after a prefilled function header.
        source='def modify_features(df_input):\n'+ '\n'.join('    '+line for line in source.splitlines())
    tree=ast.parse(source)
    functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and re.fullmatch(r'modify_features(?:_v\d+)?',n.name)]
    if not functions:raise ValueError('No modify_features function')
    function=functions[-1]
    if len(function.args.args)!=1 or function.decorator_list:
        raise ValueError('One dataframe argument, no decorators')
    function.name='modify_features'
    for node in ast.walk(function):
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            permitted=isinstance(node,ast.Import) and all(a.name in {'pandas','numpy'} and a.asname=={'pandas':'pd','numpy':'np'}[a.name] for a in node.names)
            if not permitted:raise ValueError('Only imports pandas as pd / numpy as np are supported')
        if isinstance(node,(ast.Global,ast.Nonlocal,ast.ClassDef,ast.With)):
            raise ValueError('No global state, classes or context managers')
        if isinstance(node,ast.Name) and (node.id.startswith('_') or node.id in FORBIDDEN):raise ValueError('Forbidden name '+node.id)
        if isinstance(node,ast.Attribute) and (node.attr.startswith('_') or node.attr.startswith(('read_','to_')) and node.attr not in {'to_numpy','to_frame','to_list','to_dict'} or node.attr in {'eval','query','ctypes','save','load','loadtxt','savetxt','fromfile','memmap'}):
            raise ValueError('Forbidden attribute '+node.attr)
    # Only the selected function is compiled. Permit pd/np imports by removing them from its body.
    class RemoveImports(ast.NodeTransformer):
        def visit_Import(self,node):return None
    function=RemoveImports().visit(function)
    tree=ast.fix_missing_locations(ast.Module(body=[function],type_ignores=[]))
    return ast.unparse(tree)+'\n'


def transform(source,X):
    import builtins
    names=['abs','min','max','sum','len','range','enumerate','zip','list','tuple','dict','set',
           'float','int','str','bool','round','isinstance','any','all','ValueError','Exception']
    scope={'pd':pd,'np':np,'__builtins__':{n:getattr(builtins,n) for n in names}}
    exec(compile(source,'<balance-features>','exec'),scope)
    before=X.copy(deep=True)
    output=scope['modify_features'](X.copy(deep=True))
    if not isinstance(output,pd.DataFrame) or not output.index.equals(before.index):
        raise ValueError('Return dataframe preserving rows and index')
    if not 1<=len(output.columns)<=64 or output.columns.duplicated().any():
        raise ValueError('Require1-64 unique columns')
    if any(not pd.api.types.is_numeric_dtype(output[c]) for c in output):raise ValueError('Numeric features required')
    output=output.astype(float).replace([np.inf,-np.inf],np.nan)
    if output.isna().all(axis=None):raise ValueError('All features are missing')
    return output


def run(data,directory):
    directory=Path(directory);phase='parse'
    try:
        build=xgboost.build_info()
        if build.get('USE_CUDA') is not False:
            raise RuntimeError('Expected xgboost-cpu with USE_CUDA=false; got '+str(build))
        source=extract((directory/'response.txt').read_text())
        (directory/'program.py').write_text(source)
        frame=pd.read_csv(data)
        X=frame.iloc[:,:-1];y=LabelEncoder().fit_transform(frame.iloc[:,-1])
        # Exactly the first outer fold, as in authors' five-fold setup; heldout is never evaluated.
        train,heldout=next(StratifiedKFold(n_splits=5,shuffle=True,random_state=42).split(X,y))
        X=X.iloc[train].reset_index(drop=True);y=y[train]
        phase='feature_runtime'
        output=transform(source,X)
        extra=[c for c in output if c not in X or not np.array_equal(output[c],X[c],equal_nan=True)]
        removed=[c for c in X if c not in output]
        phase='cv_training'
        scores=[]
        for a,b in StratifiedKFold(n_splits=4,shuffle=True,random_state=42).split(output,y):
            model=XGBClassifier(random_state=42,n_jobs=4,tree_method='hist',device='cpu')
            model.fit(output.iloc[a],y[a])
            scores.append(float((model.predict(output.iloc[b])==y[b]).mean()))
        result={'status':'valid','cv_accuracy':float(np.mean(scores)),'cv_folds':scores,
                'columns':list(output),'changed_or_added_columns':extra,'removed_columns':removed,
                'has_feature_change':bool(extra or removed),
                'train_rows':len(X),'heldout_rows_not_evaluated':len(heldout),'paper_reproduction':False,
                'xgboost_version':xgboost.__version__,'xgboost_build_info':build}
    except Exception as error:
        result={'status':'rejected','phase':phase,'error':str(error),'traceback':traceback.format_exc()}
    (directory/'result.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--data');parser.add_argument('--directory')
    args=parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('Diagnostic worker exceeded60s')))
    signal.alarm(60)
    run(args.data,args.directory)
