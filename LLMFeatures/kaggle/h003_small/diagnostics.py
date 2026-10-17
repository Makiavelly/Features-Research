"""Address every invalid feature; bind empty schemas without repairing LLM output."""
import json
import re
import duckdb
from features import GROUP_COLUMNS, ITEM_COLUMNS, USER_COLUMNS, validate_program, validate_expression

HISTORY = ['customer_id', 'article_id', 'price', 'sales_channel_id', 'days_ago', 'customer_age', *ITEM_COLUMNS]
RAW = ['raw_u_' + c.lower() for c in USER_COLUMNS] + ['raw_i_' + c for c in ITEM_COLUMNS]
KEY_HELP = 'keys=[customer_id], [article_id], [one clothing category], or [customer_id,article/category]; no price/days_ago/channel/raw keys'


def signature(text):
    try:
        p = decode(text)
        return json.dumps({k: v for k, v in p.items() if k != 'rationale'}, sort_keys=True)
    except (ValueError, TypeError, AttributeError):
        return None


def decode(text):
    blocks = re.findall(r'```(?:json)?\s*\n(.*?)```', text, re.S | re.I)
    return json.loads(blocks[0] if blocks else text)


def diagnose(program):
    issues = []
    if not isinstance(program, dict):
        return [{'path': '$', 'name': '', 'sql': '', 'reason': 'Return a JSON object', 'hint': 'aggregates and derived must be arrays'}]
    aggs, derived = program.get('aggregates', []), program.get('derived', [])
    if not isinstance(aggs, list) or not isinstance(derived, list):
        return [{'path': '$', 'name': '', 'sql': '', 'reason': 'aggregates/derived must be arrays', 'hint': 'Use the documented JSON shape'}]
    con = duckdb.connect(config={'enable_external_access': 'false', 'threads': '1', 'memory_limit': '128MB'})
    con.execute('CREATE TABLE history (' + ','.join(c + (' DOUBLE' if c in ['price', 'customer_age'] else ' BIGINT') for c in HISTORY) + ')')
    con.execute('CREATE TABLE candidate_features (' + ','.join(c + ' DOUBLE' for c in RAW) + ')')
    names = set(RAW)
    try:
        if len(aggs) > 24 or len(derived) > 12:
            issues.append(dict(path='$', name='', sql='', reason='Maximum24 aggregates/12 derived', hint='Remove excess features and dependent formulas'))
        for kind, entries in [('aggregates', aggs), ('derived', derived)]:
            for i, entry in enumerate(entries):
                path, reasons, hints = f'{kind}[{i}]', [], []
                if not isinstance(entry, dict):
                    issues.append(dict(path=path, name='', sql='', reason='Feature must be an object', hint='Use name/sql and aggregate keys'))
                    continue
                name, sql = entry.get('name'), entry.get('sql')
                safe_name = isinstance(name, str) and re.fullmatch(r'f_[a-z][a-z0-9_]{0,45}', name) and name not in names
                if not safe_name:
                    reasons.append('Invalid/duplicate feature name')
                    hints.append('Unique f_lowercase_name, <=48 characters')
                if set(entry) - {'name', 'keys', 'sql'}:
                    reasons.append('Unknown feature JSON keys')
                keys = entry.get('keys')
                safe_keys = (isinstance(keys, list) and 1 <= len(keys) <= 2
                             and all(isinstance(k, str) and k in GROUP_COLUMNS for k in keys)
                             and len(set(keys)) == len(keys) and (len(keys) == 1 or 'customer_id' in keys))
                if kind == 'aggregates' and not safe_keys:
                    reasons.append('Invalid grouping keys: ' + repr(keys))
                    hints.append(KEY_HELP + '; channel counts use count(*) FILTER(WHERE sales_channel_id=1)')
                expression_valid = True
                try:
                    validate_expression(sql, aggregate=kind == 'aggregates')
                except (ValueError, TypeError) as error:
                    expression_valid = False
                    reasons.append(str(error))
                if isinstance(sql, str):
                    identifiers = {s.lower() for s in re.findall(r'\b[a-zA-Z_][a-zA-Z_0-9]*\b', sql)}
                    if kind == 'aggregates' and any(s.startswith('raw_') for s in identifiers):
                        reasons.append('raw_* fields absent from history')
                        hints.append('Age bucket belongs in derived: CASE WHEN raw_u_age<30 THEN 0 ELSE 1 END')
                    if kind == 'derived' and identifiers.intersection(HISTORY):
                        reasons.append('History fields absent from derived: ' + ','.join(sorted(identifiers.intersection(HISTORY))))
                        hints.append('First aggregate history into f_*; derived may reference raw_* and earlier f_* only')
                    if "'" in sql or '"' in sql:
                        hints.append('Use numeric CASE results 0/1/2, not quoted strings')
                    if re.search(r'\bover\b|\brows\s+between\b', sql, re.I):
                        hints.append('Host groups rows; no OVER. Use count(*) FILTER(WHERE days_ago<=7) or mode(customer_age ORDER BY customer_age)')
                inferred = 'DOUBLE'
                if expression_valid and safe_name and (kind == 'derived' or safe_keys):
                    query = ('SELECT ' + ','.join(keys) + ',' + sql + ' AS ' + name + ' FROM history GROUP BY ' + ','.join(keys)
                             if kind == 'aggregates' else 'SELECT ' + sql + ' AS ' + name + ' FROM candidate_features')
                    try:
                        con.execute('EXPLAIN ' + query)
                        description = con.execute('DESCRIBE ' + query).fetchall()
                        inferred = description[-1][1]
                    except duckdb.Error as error:
                        reasons.append(str(error).splitlines()[0])
                        hints.append('Check namespace and syntax; mode(x ORDER BY x), not mode(x) ORDER BY x')
                if safe_name:
                    # Actual inferred SQL type preserves BOOL-derived dependencies.
                    con.execute('ALTER TABLE candidate_features ADD COLUMN ' + name + ' ' + inferred)
                    names.add(name)
                if reasons:
                    issues.append(dict(path=path, name=name, sql=sql, reason='; '.join(dict.fromkeys(reasons)),
                                       hint='; '.join(dict.fromkeys(hints)) or ('Allowed history fields: ' + ','.join(HISTORY) if kind == 'aggregates' else 'Allowed: raw_* + aggregate outputs + earlier derived')))
        try:
            validate_program(program)
        except (ValueError, TypeError, KeyError) as error:
            if not issues:
                issues.append(dict(path='$', name='', sql='', reason=str(error), hint='Follow the original SQL JSON interface'))
    finally:
        con.close()
    return issues


class DiagnosticError(ValueError):
    def __init__(self, issues):
        self.issues = issues
        lines = ['Fix ALL listed features; return the COMPLETE JSON, not a patch.',
                 'Aggregates see HISTORY only. Derived sees RAW static fields + aggregate outputs + earlier derived, no history.',
                 KEY_HELP]
        for issue in issues:
            lines.append(f"{issue['path']} {issue['name']} sql={str(issue['sql'])[:140]} | {issue['reason'][:200]} | {issue['hint'][:260]}")
        super().__init__('\n'.join(lines))
