import ast
import re
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

