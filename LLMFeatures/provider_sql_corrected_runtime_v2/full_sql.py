"""Read-only full SELECT programs over a physically past-only history database."""
import hashlib
import json
import re
import threading
import duckdb
import numpy as np
import pandas as pd
import sqlglot
from sqlglot import exp
from base_features import FeatureEngine as BaseEngine, ITEM_COLUMNS, GROUP_COLUMNS

HISTORY = ['customer_id', 'article_id', 'price', 'sales_channel_id', 'days_ago', 'customer_age', *ITEM_COLUMNS]
MAX_QUERIES = 6
MAX_FEATURES = 36
FUNCTIONS = {'COUNT','SUM','AVG','MIN','MAX','STDDEV_POP','STDDEV_SAMP','VARIANCE','VAR_POP','VAR_SAMP',
             'MEDIAN','QUANTILE_CONT','PERCENTILE_CONT','APPROX_DISTINCT','APPROX_COUNT_DISTINCT','MODE',
             'COALESCE','NULLIF','ABS','SQRT','LN','LOG','LOG2','LOG10','EXP','POW','POWER','GREATEST',
             'LEAST','ROUND','FLOOR','CEIL','CEILING','CAST','TRY_CAST','CASE','IF','ROW_NUMBER','RANK',
             'DENSE_RANK','LAG','LEAD','FIRST_VALUE','LAST_VALUE','NTH_VALUE','NTILE'}
# SQLGlot models standard Boolean syntax as Func nodes. These are not external functions.
FUNCTIONS.update({'AND','OR','NOT','IN','BETWEEN','IS'})
NUMERIC_TYPE = re.compile(r'(BOOLEAN|TINYINT|SMALLINT|INTEGER|BIGINT|HUGEINT|UTINYINT|USMALLINT|UINTEGER|UBIGINT|UHUGEINT|FLOAT|DOUBLE|DECIMAL\(\d+,\s*\d+\))')


class SQLProgramError(ValueError):
    def __init__(self, issues):
        self.issues = issues
        super().__init__('Fix ALL listed queries; return the COMPLETE SQL script.\n' + '\n'.join(
            f"query{e['query']}: {e['reason'][:240]} | {e['hint'][:120]}" for e in issues))


def extract_sql(text):
    if not isinstance(text,str) or not text.strip():
        raise ValueError('Return a complete SELECT/WITH SQL script, not JSON/Python')
    if '```' in text:
        matches = list(re.finditer(r'```(?:sql|duckdb)?\s*\n(.*?)```',text,re.S|re.I))
        if not matches or re.sub(r'```(?:sql|duckdb)?\s*\n.*?```','',text,flags=re.S|re.I).strip():
            raise ValueError('Return only SQL, optionally in SQL code fences; no prose/JSON')
        text=';\n'.join(m.group(1).strip().rstrip(';') for m in matches)
    if len(text)>24000:
        raise ValueError('SQL script too long; use <=6 queries and <=36 total numeric features')
    return text.strip()


def validate_ast(query):
    nodes=sqlglot.parse(query,read='duckdb')
    if len(nodes)!=1 or not isinstance(nodes[0],exp.Select):
        raise ValueError('Each statement must be SELECT or WITH ... SELECT; no DDL/DML/UNION/commands')
    tree=nodes[0]
    if any(isinstance(n,(exp.Insert,exp.Update,exp.Delete,exp.Create,exp.Drop,exp.Command,exp.Into)) for n in tree.walk()):
        raise ValueError('Only read-only SELECT queries are supported')
    if any(isinstance(n,exp.With) and n.args.get('recursive') for n in tree.walk()):
        raise ValueError('Recursive CTEs are not supported')
    if any(isinstance(n,exp.TableSample) for n in tree.walk()):
        raise ValueError('Random table sampling is not supported; use deterministic history statistics')
    ctes={n.alias_or_name.lower() for n in tree.find_all(exp.CTE)}
    if ctes.intersection({'history','tx','articles','customers','input_pairs'}):
        raise ValueError('CTE names must not shadow host tables; choose e.g. counts or recent')
    for table in tree.find_all(exp.Table):
        if not isinstance(table.this,exp.Identifier) or table.db or table.catalog:
            raise ValueError('No table functions, files, qualified databases, or external sources')
        if table.name.lower() not in {'history',*ctes}:
            raise ValueError('Unknown table '+table.name+'; only history and your own CTEs are available')
    if not any(t.name.lower()=='history' for t in tree.find_all(exp.Table)):
        raise ValueError('Each query must read past-only history, directly or through its CTEs')
    for function in tree.find_all(exp.Func):
        name=function.name.upper() if isinstance(function,exp.Anonymous) else function.sql_name().upper()
        if name not in FUNCTIONS:
            raise ValueError('Function outside supported numeric SQL operations: '+name)
    for alias in tree.find_all(exp.Alias):
        if alias.alias.lower() in GROUP_COLUMNS:
            if not isinstance(alias.this,exp.Column) or alias.this.name.lower()!=alias.alias.lower():
                raise ValueError('Join keys must retain original values/names; do not transform '+alias.alias)
    # IDs are valid keys/count inputs, never numeric predictors or arithmetic operands.
    for column in tree.find_all(exp.Column):
        if column.name.lower() not in {'customer_id','article_id'}:
            continue
        parent=column.parent
        if isinstance(parent,exp.Select) and column in parent.expressions: continue
        if isinstance(parent,exp.Alias) and parent.alias.lower()==column.name.lower(): continue
        if isinstance(parent,exp.Group): continue
        if column.find_ancestor(exp.Count,exp.ApproxDistinct) is not None: continue
        if isinstance(parent,exp.Window) and column in parent.args.get('partition_by',[]): continue
        if isinstance(parent,exp.EQ) and isinstance(parent.left,exp.Column) and isinstance(parent.right,exp.Column):
            if parent.left.name.lower()==parent.right.name.lower(): continue
        raise ValueError('IDs are join/group keys or count inputs, not feature values: '+column.sql())
    return tree


def schema(con,query):
    con.execute('EXPLAIN '+query)
    description=con.execute('DESCRIBE '+query).fetchall()
    names=[d[0] for d in description]
    if len(names)!=len(set(names)):
        raise ValueError('Duplicate output column names')
    keys=[n for n in names if n in GROUP_COLUMNS]
    features=[n for n in names if n not in keys]
    if not (1<=len(keys)<=2 and (len(keys)==1 or 'customer_id' in keys)):
        raise ValueError('Return one customer/article/category key or customer_id + article/category; no channel/age/price keys')
    if not features:
        raise ValueError('Return at least one numeric f_* feature in addition to keys')
    for name in features:
        if not re.fullmatch(r'f_[a-z][a-z0-9_]{0,45}',name):
            raise ValueError('Output feature names must be unique f_lowercase_names: '+name)
    for name,dtype,*_ in description:
        if not NUMERIC_TYPE.fullmatch(dtype):
            raise ValueError('Output must be numeric, including keys; '+name+' has type '+dtype)
    return keys,features


def validate_program(program):
    if not isinstance(program,dict) or set(program)!={'queries'} or not isinstance(program['queries'],list):
        raise ValueError('Host program must contain queries only')
    if len(program['queries'])>MAX_QUERIES:
        raise ValueError('At most6 complete SELECT queries')
    if not program['queries']: return program  # host-only raw control
    con=duckdb.connect(config={'enable_external_access':'false','threads':'1','memory_limit':'128MB'})
    con.execute('CREATE TABLE history ('+','.join(n+(' DOUBLE' if n in ['price','customer_age'] else ' BIGINT') for n in HISTORY)+')')
    names,issues=set(),[]
    try:
        for i,query in enumerate(program['queries'],1):
            try:
                if not isinstance(query,str) or len(query)>24000: raise ValueError('Query must be SQL text <=24000characters')
                validate_ast(query)
                keys,features=schema(con,query)
                overlap=names.intersection(features)
                if overlap: raise ValueError('Feature names repeated across queries: '+','.join(sorted(overlap)))
                names.update(features)
            except Exception as error:
                issues.append(dict(query=i,sql=query,reason=str(error)[:650],
                                   hint='Use the documented history columns; keys+numeric f_* outputs; full GROUP BY. Quantile: quantile_cont(price,0.5). CTEs may compute ratios before final SELECT.'))
        if len(names)>MAX_FEATURES:
            issues.append(dict(query=0,sql='',reason='More than36 output features',hint='Keep the complete set compact'))
        if issues: raise SQLProgramError(issues)
    finally:
        con.close()
    return program


def parse(text):
    source=extract_sql(text)
    # DuckDB preserves original SQL, including CTEs/window syntax. SQLGlot only
    # validates and fingerprints; it never rewrites the executed program.
    con=duckdb.connect()
    try:
        statements=con.extract_statements(source)
        queries=[statement.query.strip().rstrip(';') for statement in statements]
    except duckdb.Error as error:
        raise ValueError(str(error)) from None
    finally: con.close()
    if not queries: raise ValueError('Raw control is host-only: propose at least one feature SELECT')
    return validate_program({'queries':queries})


def render(program):
    return ';\n\n'.join(program['queries'])+';' if program['queries'] else '-- Raw15 control: no engineered feature query'


def program_key(program):
    canonical=[]
    for query in program['queries']:
        tree=sqlglot.parse_one(query,read='duckdb')
        names={}
        for n in tree.find_all(exp.Identifier):
            value=n.name.lower()
            if value.startswith('f_'):
                if value not in names: names[value]='f_normalized_'+str(len(names))
                n.set('this',names[value])
        # Conservative AST dedup: not general SQL/algebraic equivalence.
        canonical.append(tree.sql(dialect='duckdb',normalize=True,pretty=False,comments=False))
    return hashlib.sha256(json.dumps(sorted(canonical)).encode()).hexdigest()


def signature(text):
    try: return program_key(parse(text))
    except Exception: return re.sub(r'\s+',' ',text.strip()).lower()


class FeatureEngine(BaseEngine):
    def __init__(self,scratch,data_dir=None):
        super().__init__(scratch,data_dir)
        self.query_con=None

    def prepare(self,timestamp,users,program):
        validate_program(program)
        super().prepare(timestamp,users,{'aggregates':[],'derived':[]})
        if self.query_con is not None: self.query_con.close()
        # The LLM connection contains PHYSICALLY PAST-ONLY history. No tx,
        # labels, candidate rows, targets, or future transactions are registered.
        past=self.con.execute('SELECT * FROM history').fetch_arrow_table()
        self.query_con=duckdb.connect(config={'enable_external_access':'false','threads':'2','memory_limit':'768MB'})
        self.query_con.register('history',past)
        all_names=[]
        for index,query in enumerate(program['queries']):
            timer=threading.Timer(60,self.query_con.interrupt)
            timer.daemon=True
            timer.start()
            try:
                keys,names=schema(self.query_con,query)
                # Bound materialization; reject oversize results, never accept a
                # silently truncated feature table.
                result=self.query_con.execute('SELECT * FROM (\n'+query+'\n) LIMIT 250001').fetch_df()
            except Exception as error:
                raise ValueError(f'query{index+1}: {error}') from None
            finally: timer.cancel()
            if len(result)>250000:
                raise ValueError(f'query{index+1}: too many output rows; aggregate by your join keys')
            if result.duplicated(subset=keys).any():
                raise ValueError(f'query{index+1}: duplicate key rows would multiply candidate pairs; return exactly one row per '+str(keys))
            for key in keys:
                allowed=np.asarray(past.column(key).to_pandas().dropna().unique())
                values=result[key].dropna().to_numpy()
                if not np.isin(values,allowed).all():
                    raise ValueError(f'query{index+1}: invented/transformed join key values in '+key)
            table='full_sql_group_'+str(index)
            self.con.register('full_sql_result',result)
            self.con.execute(f'CREATE OR REPLACE TEMP TABLE {table} AS SELECT * FROM full_sql_result')
            self.con.unregister('full_sql_result')
            entries=[{'name':n} for n in names]
            self.groups.append((table,keys,entries))
            all_names.extend(names)
        # Reuse the frozen host join/matrix implementation, with no derived SQL
        # stage: all formulas were already computed by the LLM's complete SELECTs.
        self.program={'aggregates':[{'name':n} for n in all_names],'derived':[]}

    def close(self):
        if self.query_con is not None: self.query_con.close()
        super().close()
