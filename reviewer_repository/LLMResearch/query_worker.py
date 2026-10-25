"""Single read-only query against a database containing only training data."""
import argparse
import json
from pathlib import Path
import re
import threading
import duckdb


def execute(database, sql):
    if not isinstance(sql, str) or len(sql) > 8000:
        raise ValueError('sql must be a string of at most8000 characters')
    # DuckDB rewrites some PRAGMA forms as SELECT during parsing.
    if not re.match(r'\s*(SELECT|WITH)\b', sql, re.I):
        raise ValueError('Query must start with SELECT or WITH')
    con = duckdb.connect(str(database), read_only=True,
                         config={'enable_external_access': False, 'threads': 2,
                                 'memory_limit': '512MB'})
    timer = threading.Timer(15, con.interrupt)
    try:
        statements = con.extract_statements(sql)
        if len(statements) != 1 or statements[0].type != duckdb.StatementType.SELECT:
            raise ValueError('Exactly one SELECT/WITH statement is allowed')
        timer.start()
        cursor = con.execute(sql)
        columns = [d[0] for d in cursor.description]
        if len(columns) > 24:
            raise ValueError('Maximum24 result columns; aggregate or narrow your query')
        rows = cursor.fetchmany(41)
        # JSON conversion also normalizes dates and finite/nonfinite scalars.
        clean = []
        for row in rows[:40]:
            clean.append([None if isinstance(v, float) and not __import__('math').isfinite(v)
                          else (str(v)[:160] if not isinstance(v, (int, float, bool, type(None))) else v)
                          for v in row])
        result = {'columns': columns, 'rows': clean, 'truncated_rows': len(rows) > 40}
        while len(json.dumps(result, ensure_ascii=False)) > 12000 and result['rows']:
            result['rows'].pop()
            result['truncated_rows'] = True
        return result
    finally:
        timer.cancel()
        con.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        value = execute(args.database, json.loads(Path(args.input).read_text())['sql'])
        result = {'ok': True, 'result': value}
    except Exception as error:
        result = {'ok': False, 'error': str(error)[:1200]}
    path = Path(args.output)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(result, ensure_ascii=False))
    temporary.replace(path)


if __name__ == '__main__':
    main()
