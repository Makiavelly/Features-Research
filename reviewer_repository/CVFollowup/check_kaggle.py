"""Verify notebook syntax and that portability edits preserve training computation."""
import ast
import copy
from common import ROOT,OUT,REPORT,read,write,sha,record

class Normalize(ast.NodeTransformer):
    def visit_Import(self,node):
        return None if len(node.names)==1 and node.names[0].name=='os' else node
    def visit_Assign(self,node):
        if len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ['ROOT','DATA','OUT','RUN']:
            node.value=ast.Constant(value='<portable location or run id>')
        return self.generic_visit(node)
    def visit_Assert(self,node):
        if isinstance(node.msg,ast.Constant) and node.msg.value=='Kaggle runner is train-only':return None
        return self.generic_visit(node)

def main():
    base=ROOT/'CVFollowup/cache/kaggle_recformer_v1';checks=[]
    manifest=read(base/'input_manifest.json')
    for fold in range(3):
        for label in ['lr3e6_w100','lr1e5_w300']:
            local=OUT/f'fold_{fold}/runtime/recformer_{label}.py'
            portable=base/f'runtime/fold_{fold}/recformer_{label}.py'
            a=Normalize().visit(ast.parse(local.read_text(encoding='utf-8')))
            b=Normalize().visit(ast.parse(portable.read_text(encoding='utf-8')))
            assert ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False),'Training computation changed'
            checks.append({'fold':fold,'label':label,'training_AST_matches':True,'portable_sha256':sha(portable),'source_sha256':sha(local)})
    for file in (ROOT/'CVFollowup/kaggle').glob('*.ipynb'):
        nb=read(file);assert nb['nbformat']==4
        ids=[]
        for cell in nb['cells']:
            ids.append(cell['id'])
            if cell['cell_type']=='code':ast.parse(''.join(cell['source']));assert not cell['outputs']
        assert len(ids)==len(set(ids))
    write(REPORT/'kaggle_portability_verification.json',{'passed':True,'checks':checks,
        'notebooks':'code parsed; cells have unique IDs and no outputs','scope':'CPU/data/static checks only; actual T4 execution has not been run locally'})
    record('recformer_kaggle_portability_verified','All six portable training sources have identical computation AST to frozen local sources after normalizing paths/run IDs and train-only guard. Both notebooks syntax checked; T4 execution remains user-run.',
        'hm_medium_recformer_kaggle_split_v1',status='prepared_verified',artifacts='CVFollowup/kaggle')
    print('PORTABILITY: six training AST comparisons passed, two notebooks parsed',flush=True)

if __name__=='__main__':main()
