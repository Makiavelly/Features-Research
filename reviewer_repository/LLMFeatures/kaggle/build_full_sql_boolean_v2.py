"""Preserve v1; publish the same Boolean validation correction for Kaggle Qwen."""
import ast
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def main():
    parent=HERE/'hm_small_qwen7b_full_sql_kaggle_t4.ipynb'
    notebook=json.loads(parent.read_text(encoding='utf-8'))
    cells=copy.deepcopy(notebook['cells'])
    cell=next(c for c in cells if 'MODULES = ' in ''.join(c['source']))
    source=''.join(cell['source'])
    modules=next(ast.literal_eval(n.value) for n in ast.parse(source).body if isinstance(n,ast.Assign)
                 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='MODULES')
    modules['full_sql.py']=modules['full_sql.py'].replace('\nNUMERIC_TYPE = ',
        "\n# SQLGlot models standard Boolean syntax as Func nodes. These are not external functions.\nFUNCTIONS.update({'AND','OR','NOT','IN','BETWEEN','IS'})\nNUMERIC_TYPE = ",1)
    hashes={n:hashlib.sha256(s.encode()).hexdigest() for n,s in modules.items()}
    folder=HERE/'full_sql_small_v2'
    folder.mkdir(exist_ok=True)
    for name,body in modules.items():(folder/name).write_text(body,encoding='utf-8')
    for index,c in enumerate(cells):
        text=''.join(c['source'])
        if 'MODULES = ' in text:
            start,end=text.index('MODULES = '),text.index('EXPECTED_MANIFEST = ')
            text=text[:start]+'MODULES = '+repr(modules)+'\nMODULE_SHA = '+repr(hashes)+'\n'+text[end:]
            text=text.replace("WORK / 'hm_small_full_sql_runtime'","WORK / 'hm_small_full_sql_runtime_v2'")
        else:
            text=text.replace('hm_small_qwen7b_full_sql_v1','hm_small_qwen7b_full_sql_v2')
        if index==0:
            text+='\nВерсия2: исправлен ложный отказ логических AND/OR/NOT/IN/BETWEEN/IS.\nВсе остальные данные/параметры/prompt сохранены, старый v1 не изменён.\n'
        if c['cell_type']=='code':ast.parse(text);c.update(outputs=[],execution_count=None)
        c['source']=text.splitlines(keepends=True)
        c['id']=hashlib.sha256(text.encode()).hexdigest()[:12]
    notebook['cells']=cells
    output=HERE/'hm_small_qwen7b_full_sql_v2_kaggle_t4.ipynb'
    output.write_text(json.dumps(notebook,ensure_ascii=False,indent=1),encoding='utf-8')
    delivery=json.loads((HERE/'full_sql_small/delivery_manifest.json').read_text())
    delivery.update(protocol='hm_small_qwen7b_full_sql_v2',notebook=output.name,
                    notebook_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),modules=hashes,
                    parent_notebook_sha256=hashlib.sha256(parent.read_bytes()).hexdigest(),
                    validator_patch='Standard Boolean AST syntax',llm_inference_executed_locally=False)
    (folder/'delivery_manifest.json').write_text(json.dumps(delivery,indent=2),encoding='utf-8')
    print(output)


if __name__=='__main__':main()
