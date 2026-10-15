"""Compile bounded feature descriptions into host-owned SQL; never execute model code."""
import json
import math
import re
from decimal import Decimal
from sql_features import KEYS,RAW,compile_sql

AGGREGATIONS={'count','count_distinct','sum','avg','min','max','stddev_pop','median'}
NUMERIC={'price','days_ago','customer_age'}
COUNTABLE=KEYS|{'sales_channel_id'}|NUMERIC
UNARY={'abs','log1p','sqrt','negate'}
BINARY={'add','subtract','multiply','divide','min','max','coalesce'}


def expression(node,available,depth=0,budget=None):
    budget=[0] if budget is None else budget
    budget[0]+=1
    if depth>6 or budget[0]>64:
        raise ValueError('Expression limit: depth6,64 nodes')
    if isinstance(node,(int,float)) and not isinstance(node,bool):
        if not math.isfinite(node) or abs(node)>1e6:
            raise ValueError('Constants must be finite and within +/-1000000')
        return format(Decimal(str(node)),'f')
    if not isinstance(node,dict):
        raise ValueError('Expression: number, {"ref":"existing_feature"}, or {"op":...,"args":[...]}')
    if set(node)=={'ref'}:
        if not isinstance(node['ref'],str) or node['ref'] not in available:
            raise ValueError('Unknown reference '+str(node['ref'])+'; available: '+','.join(sorted(available)))
        return node['ref']
    if set(node)!={'op','args'} or not isinstance(node['op'],str) or not isinstance(node['args'],list):
        raise ValueError('Operation needs exactly op and args')
    op=node['op'];args=node['args']
    if op not in UNARY|BINARY or len(args)!=(1 if op in UNARY else 2):
        raise ValueError('Unary ops: '+','.join(sorted(UNARY))+'; binary ops: '+','.join(sorted(BINARY)))
    sql=[expression(arg,available,depth+1,budget) for arg in args]
    a='('+sql[0]+')'
    if op=='abs':return 'ABS('+a+')'
    if op=='log1p':return 'LN(1 + GREATEST('+a+', 0))'
    if op=='sqrt':return 'SQRT(GREATEST('+a+', 0))'
    if op=='negate':return '-'+a
    b='('+sql[1]+')'
    if op=='divide':return a+' / NULLIF('+b+', 0)'
    if op in {'add','subtract','multiply'}:return a+{'add':'+','subtract':'-','multiply':'*'}[op]+b
    return {'min':'LEAST','max':'GREATEST','coalesce':'COALESCE'}[op]+'('+a+','+b+')'


def validate_program(program,allow_empty=False):
    if not isinstance(program,dict) or set(program)-{'aggregates','derived','rationale'}:
        raise ValueError('JSON object with aggregates and derived only (optional rationale)')
    aggs=program.get('aggregates',[]);derived=program.get('derived',[])
    if not isinstance(aggs,list) or not isinstance(derived,list) or len(aggs)>24 or len(derived)>12:
        raise ValueError('Maximum24 aggregates and12 derived formulas')
    if not aggs and not derived and not allow_empty:
        raise ValueError('At least one generated feature required')
    errors=[]; names=set(); normalized=[]; formulas=[]
    def name_check(name):
        if not isinstance(name,str) or not re.fullmatch('f_[a-z][a-z0-9_]{0,45}',name) or name in names:
            raise ValueError('name must be unique f_lowercase (<=48 characters)')
    for i,entry in enumerate(aggs):
        try:
            if not isinstance(entry,dict) or set(entry)-{'name','keys','op','column','window'} or not {'name','keys','op'}<=set(entry):
                raise ValueError('Use name, keys, op; optional column and window. No sql field.')
            name=entry['name'];name_check(name)
            keys=entry['keys'];op=entry['op'];column=entry.get('column','*');window=entry.get('window',180)
            if not isinstance(keys,list) or not 1<=len(keys)<=2 or any(not isinstance(k,str) or k not in KEYS for k in keys) or len(set(keys))!=len(keys) or len(keys)==2 and 'customer_id' not in keys:
                raise ValueError('keys: one customer_id/article_id/clothing category, or customer_id + article/category')
            if not isinstance(op,str) or op not in AGGREGATIONS:
                raise ValueError('op must be '+','.join(sorted(AGGREGATIONS)))
            if not isinstance(column,str) or (op=='count' and column!='*') or (op=='count_distinct' and column not in COUNTABLE) or (op not in {'count','count_distinct'} and column not in NUMERIC):
                raise ValueError('count uses column="*"; count_distinct uses a history column; numeric aggregates use price/days_ago/customer_age only. No raw_* fields.')
            if not isinstance(window,int) or isinstance(window,bool) or not 1<=window<=180:
                raise ValueError('window must be integer days1..180')
            normalized.append({'name':name,'keys':sorted(keys),'op':op,'column':column,'window':window})
            names.add(name)
        except ValueError as error:
            errors.append(f'aggregates[{i}]: {error}')
    available=RAW|names
    for i,entry in enumerate(derived):
        try:
            if not isinstance(entry,dict) or set(entry)!={'name','expr'}:
                raise ValueError('Use exactly name and expr (expression tree), no SQL')
            name=entry['name'];name_check(name)
            expression(entry['expr'],available)
            formulas.append(entry);names.add(name);available.add(name)
        except ValueError as error:
            errors.append(f'derived[{i}]: {error}')
    if errors:
        raise ValueError('Fix ALL listed schema errors:\n'+'\n'.join(errors))
    return {'aggregates':sorted(normalized,key=lambda e:e['name']),'derived':formulas}


def to_sql(program,allow_empty=False):
    program=validate_program(program,allow_empty=allow_empty)
    aggs=[]
    for entry in program['aggregates']:
        operation=entry['op'];column=entry['column']
        sql='COUNT(DISTINCT '+column+')' if operation=='count_distinct' else operation.upper()+'('+column+')'
        sql+=' FILTER (WHERE days_ago <= '+str(entry['window'])+')'
        aggs.append({'name':entry['name'],'keys':entry['keys'],'sql':sql})
    available=RAW|{entry['name'] for entry in aggs};derived=[]
    for entry in program['derived']:
        derived.append({'name':entry['name'],'sql':expression(entry['expr'],available)})
        available.add(entry['name'])
    return {'aggregates':aggs,'derived':derived}


def compile_structured(source):
    return compile_sql(json.dumps(to_sql(json.loads(source),allow_empty=True)))
