"""Complete Python feature programs, with input/output and execution checks.

Static restrictions reduce accidental I/O. This is not a hostile-code sandbox.
No SQL AST function allowlist: ordinary pandas/NumPy computations are supported.
"""
import ast
import builtins
import hashlib
import json
import re
import signal
import numpy as np
import pandas as pd
from base_features import FeatureEngine as RawEngine

RAW = 'def modify_features(X, history):\n    return pd.DataFrame({"f_control": np.ones(len(X))}, index=X.index)\n'
HISTORY = ['customer_id', 'article_id', 'price', 'sales_channel_id', 'days_ago',
           'product_code', 'product_type_no', 'graphical_appearance_no', 'colour_group_code',
           'perceived_colour_value_id', 'perceived_colour_master_id', 'department_no',
           'index_group_no', 'section_no', 'garment_group_no', 'customer_age']
BLOCKED_NAMES = {'open','exec','eval','compile','globals','locals','vars','getattr','setattr',
                 'delattr','input','breakpoint','help','exit','quit','memoryview','__import__'}
BLOCKED_ATTRS = {'eval','query','io','os','sys','ctypes','random','lib','testing',
                 'load','loads','save','savez','savez_compressed','memmap','fromfile','tofile',
                 'frombuffer','ctypeslib','get_handle','ExcelFile','ExcelWriter','HDFStore'}


class PythonProgramError(ValueError):
    def __init__(self, issues):
        self.issues = issues
        super().__init__('\n'.join(issues))


def validate_program(program):
    if not isinstance(program, dict) or set(program) != {'code'} or not isinstance(program['code'], str):
        raise PythonProgramError(['Expected a complete Python source string under code'])
    code = program['code']
    if len(code) > 24000:
        raise PythonProgramError(['Python source exceeds 24000 characters'])
    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        raise PythonProgramError([f'SyntaxError at line {error.lineno}: {error.msg}']) from None
    errors = []
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'modify_features']
    if len(functions) != 1 or [a.arg for a in functions[0].args.args] != ['X','history']:
        errors.append('Define exactly one def modify_features(X, history)')
    for statement in tree.body:
        if isinstance(statement,(ast.Assign,ast.AnnAssign)):
            try: ast.literal_eval(statement.value)
            except (ValueError,TypeError): errors.append(f'line {statement.lineno}: module constants must be literal values')
        elif not isinstance(statement, (ast.FunctionDef, ast.Import, ast.Expr)):
            errors.append(f'line {statement.lineno}: module scope allows functions, literal constants, pandas/numpy imports and docstrings only')
        elif isinstance(statement, ast.Expr) and not isinstance(statement.value, ast.Constant):
            errors.append(f'line {statement.lineno}: no executable module-level expressions')
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(a.name not in {'pandas','numpy'} or a.asname not in {'pd','np',None} for a in node.names):
                errors.append(f'line {node.lineno}: only import pandas as pd / numpy as np supported')
        if isinstance(node, (ast.ImportFrom,ast.ClassDef,ast.Global,ast.Nonlocal,ast.AsyncFunctionDef)):
            errors.append(f'line {node.lineno}: unsupported execution construct {type(node).__name__}')
        if isinstance(node, ast.Name) and (node.id.startswith('__') or node.id in BLOCKED_NAMES):
            errors.append(f'line {node.lineno}: unavailable name {node.id}')
        if isinstance(node, ast.Attribute):
            attr = node.attr
            if attr.startswith('_') or attr.startswith(('read_','to_')) and attr not in {'to_numpy','to_frame','to_dict','to_list','to_numeric','to_datetime'} or attr in BLOCKED_ATTRS:
                errors.append(f'line {node.lineno}: I/O, randomness or private attribute unavailable: {attr}')
        if isinstance(node, ast.FunctionDef) and (node.decorator_list or node.name.startswith('__')):
            errors.append(f'line {node.lineno}: no decorators/private functions')
    if errors:
        raise PythonProgramError(list(dict.fromkeys(errors)))
    # Compilation is a separate check; syntax-valid AST can still be invalid code.
    try:
        compile(tree, '<llm-features>', 'exec')
    except (SyntaxError,ValueError) as error:
        raise PythonProgramError([str(error)]) from None
    return {'code': code}


def parse(text):
    text = text.strip()
    if text.startswith('```'):
        match = re.fullmatch(r'```(?:python)?\s*\n(.*?)\n```', text, re.S)
        if not match:
            raise PythonProgramError(['Return one complete Python program, without prose'])
        text = match[1]
    return validate_program({'code': text + '\n'})


def render(program):
    return program['code']


def program_key(program):
    # Conservative structural dedup; does not claim algebraic/matrix uniqueness.
    tree = ast.parse(program['code'])
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef,ast.Module)) and node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):
            node.body.pop(0)
    return hashlib.sha256(ast.dump(tree, include_attributes=False).encode()).hexdigest()


def signature(text):
    try:
        return program_key(parse(text))
    except Exception:
        return hashlib.sha256(text.strip().encode()).hexdigest()


def compile_function(program):
    program = validate_program(program)
    permitted = ['abs','all','any','bool','dict','enumerate','filter','float','int','isinstance',
                 'len','list','map','max','min','range','reversed','round','set','slice','sorted',
                 'str','hasattr','sum','tuple','zip','ValueError','TypeError','Exception']
    safe = {name: getattr(builtins,name) for name in permitted}
    def restricted_import(name, *args, **kwargs):
        if name == 'pandas': return pd
        if name == 'numpy': return np
        raise ImportError('Only pandas/numpy available')
    safe['__import__'] = restricted_import
    scope = {'__builtins__':safe, 'pd':pd, 'np':np}
    exec(compile(program['code'],'<llm-features>','exec'),scope)
    return scope['modify_features']


def construct(function, X, history, expected=None):
    def timeout(*args):
        raise TimeoutError('Python feature function exceeded 60 seconds')
    previous = signal.signal(signal.SIGALRM, timeout)
    signal.alarm(60)
    try:
        result = function(X.copy(deep=True), history.copy(deep=True))
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)
    if not isinstance(result,pd.DataFrame): raise ValueError('Return a pandas DataFrame')
    if len(result)!=len(X) or not result.index.equals(X.index):
        raise ValueError('Output must have exactly X rows and unchanged X.index in the same order')
    columns = list(result)
    if not 1 <= len(columns) <= 36 or len(set(columns))!=len(columns) or any(not isinstance(n,str) or not re.fullmatch(r'f_[a-z][a-z0-9_]{0,63}',n) for n in columns):
        raise ValueError('Return 1..36 unique numeric f_lowercase features, no raw fields or IDs')
    if expected is not None:
        if set(columns) != set(expected): raise ValueError('Feature schema differs across cutoffs/batches')
        # Column names define identity. A different return order is harmless if
        # aligned before conversion to arrays; never align or reorder rows here.
        result = result.loc[:,expected]
    bad = [n for n in columns if not pd.api.types.is_numeric_dtype(result[n])]
    if bad: raise ValueError('Non-numeric output columns: '+str(bad))
    return result


class FeatureEngine(RawEngine):
    def __init__(self, scratch, data_dir=None):
        super().__init__(scratch,data_dir)
        self.names = None

    def prepare(self,timestamp,users,program):
        if getattr(self,'python_program',None) != program:
            self.names = None
        self.python_program = validate_program(program)
        self.function = compile_function(program)
        # Time filtering and all static encodings remain owned by the existing host.
        super().prepare(timestamp,users,{'aggregates':[]})
        self.history = self.con.sql('SELECT * FROM history').df()[HISTORY]

    @property
    def feature_names(self):
        return self.raw_names if getattr(self, '_building_raw', False) else (self.names or [])

    def frame(self, pairs):
        self._building_raw = True
        try:
            raw = RawEngine.frame(self, pairs)
        finally:
            self._building_raw = False
        X = pd.concat([pairs[['customer_id','article_id']].reset_index(drop=True), raw], axis=1)
        out = construct(self.function, X, self.history, expected=self.names)
        self.names = list(out)
        assert all(n.startswith('f_') for n in self.names)
        return out
