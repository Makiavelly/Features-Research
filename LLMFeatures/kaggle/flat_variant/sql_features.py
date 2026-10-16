"""Restricted SQL aggregates. The host owns tables, joins, time filtering and row order."""
import json
import re
import duckdb
import pandas as pd

ITEMS = ['product_code','product_type_no','graphical_appearance_no','colour_group_code',
         'perceived_colour_value_id','perceived_colour_master_id','department_no',
         'index_group_no','section_no','garment_group_no']
KEYS = {'customer_id','article_id',*ITEMS}
COLUMNS = KEYS | {'price','days_ago','sales_channel_id','customer_age'}
FUNCTIONS = {'count','sum','avg','min','max','stddev_pop','stddev_samp','variance','median',
             'quantile_cont','mode','coalesce','nullif','abs','sqrt','ln','log','log2','log10',
             'exp','pow','power','round','floor','ceil','cast','greatest','least','approx_count_distinct'}
WORDS = {'case','when','then','else','end','distinct','filter','where','and','or',
         'not','is','null','between','in','true','false','as','double','float','integer','bigint'}
TOKEN = re.compile(r'\s+|[A-Za-z][A-Za-z_0-9]*|\d+(?:\.\d+)?|<=|>=|<>|!=|[(),+*/%=<>-]')


RAW = {'raw_u_age','raw_u_fn','raw_u_active','raw_u_club_member_status','raw_u_fashion_news_frequency',
       *('raw_i_'+name for name in ITEMS)}


def validate_expression(sql,columns=None,aggregate=True):
    columns=COLUMNS if columns is None else columns
    if not isinstance(sql,str) or not sql or len(sql)>1000:
        raise ValueError('sql must be a nonempty numeric expression <=1000 characters')
    tokens=[]; offset=0
    while offset<len(sql):
        match=TOKEN.match(sql,offset)
        if not match:
            raise ValueError('Only numeric SQL expressions; no statements, strings, comments, or qualified names')
        offset=match.end()
        if not match.group().isspace():
            tokens.append(match.group().lower())
    for i,token in enumerate(tokens):
        if re.fullmatch('[a-z][a-z_0-9]*',token):
            if token not in columns|FUNCTIONS|WORDS:
                raise ValueError('Unknown or forbidden SQL identifier: '+token)
            if i+1<len(tokens) and tokens[i+1]=='(' and token not in FUNCTIONS|{'filter','in','and','or','not','where'}:
                raise ValueError('Function outside allowlist: '+token)
    # IDs can be counted, never averaged or used as numerical predictions.
    masked=re.sub(r'\b(?:count|approx_count_distinct)\s*\(\s*(?:distinct\s+)?(?:customer_id|article_id)\s*\)',
                  'count(*)',sql,flags=re.I) if aggregate else sql
    if re.search(r'\b(customer_id|article_id)\b',masked,re.I):
        raise ValueError('IDs only in grouping keys or count(DISTINCT id)')
    return ' '.join(tokens)


def validate_program(program,allow_empty=False):
    if not isinstance(program,dict) or set(program)-{'rationale','aggregates','derived'}:
        raise ValueError('Return JSON with aggregates, derived and optional rationale only')
    entries=program.get('aggregates',[]); derived=program.get('derived',[])
    if not isinstance(entries,list) or not isinstance(derived,list) or len(entries)>24 or len(derived)>12:
        raise ValueError('Maximum24 aggregates and12 derived features, as in local Qwen interface')
    if not entries and not derived and not allow_empty:
        raise ValueError('Provide at least one generated feature; raw control is host-only')
    names=set(); output=[]
    for entry in entries:
        if not isinstance(entry,dict) or set(entry)!={'name','keys','sql'}:
            raise ValueError('Each aggregate needs exactly name, keys, sql')
        name=entry['name']; keys=entry['keys']
        if not isinstance(name,str) or not re.fullmatch('f_[a-z][a-z0-9_]{0,45}',name) or name in names:
            raise ValueError('Use unique f_lowercase feature names')
        names.add(name)
        if not isinstance(keys,list) or not 1<=len(keys)<=2 or any(not isinstance(k,str) or k not in KEYS for k in keys) or len(set(keys))!=len(keys):
            raise ValueError('Invalid grouping keys')
        if len(keys)==2 and 'customer_id' not in keys:
            raise ValueError('Two keys must be customer_id + article_id or clothing category')
        output.append({'name':name,'keys':sorted(keys),'sql':validate_expression(entry['sql'])})
    formulas=[]; available=RAW|names
    for entry in derived:
        if not isinstance(entry,dict) or set(entry)!={'name','sql'}:
            raise ValueError('Each derived feature needs exactly name, sql')
        name=entry['name']
        if not isinstance(name,str) or not re.fullmatch('f_[a-z][a-z0-9_]{0,45}',name) or name in names:
            raise ValueError('Use unique f_lowercase feature names')
        formulas.append({'name':name,'sql':validate_expression(entry['sql'],columns=available,aggregate=False)})
        names.add(name);available.add(name)
    return {'aggregates':sorted(output,key=lambda e:e['name']),'derived':formulas}


def compile_sql(source):
    program=validate_program(json.loads(source),allow_empty=True)

    def modify_features(X,history):
        result=pd.DataFrame(index=X.index)
        if not program['aggregates'] and not program['derived']:
            return result
        connection=duckdb.connect(config={'enable_external_access':'false','threads':'1',
                                         'memory_limit':'512MB'})
        try:
            connection.register('history_input',history)
            groups={}
            for entry in program['aggregates']:
                groups.setdefault(tuple(entry['keys']),[]).append(entry)
            for keys,entries in groups.items():
                query='SELECT '+','.join(keys)+','+','.join(e['sql']+' AS '+e['name'] for e in entries)
                query+=' FROM history_input GROUP BY '+','.join(keys)
                aggregate=connection.execute(query).df()
                left=pd.DataFrame(index=X.index)
                for key in keys:
                    left[key]=X[key] if key in {'customer_id','article_id'} else X['raw_i_'+key]
                joined=left.merge(aggregate,on=list(keys),how='left',sort=False,validate='many_to_one')
                if len(joined)!=len(X):
                    raise ValueError('Host SQL join changed row count')
                for entry in entries:
                    result[entry['name']]=joined[entry['name']].to_numpy()
            # Derived expressions see ONLY raw fields and previously computed features.
            frame=pd.concat([X[[c for c in X if c.startswith('raw_')]],result],axis=1)
            for entry in program['derived']:
                connection.register('derived_input',frame.reset_index(drop=True))
                values=connection.execute('SELECT '+entry['sql']+' AS '+entry['name']+' FROM derived_input').df()
                connection.unregister('derived_input')
                if len(values)!=len(X):
                    raise ValueError('Derived SQL must produce one scalar per candidate row')
                frame[entry['name']]=values[entry['name']].to_numpy()
                result[entry['name']]=values[entry['name']].to_numpy()
        finally:
            connection.close()
        return result[[e['name'] for e in program['aggregates']+program['derived']]]
    modify_features._feature_source=source
    return modify_features
