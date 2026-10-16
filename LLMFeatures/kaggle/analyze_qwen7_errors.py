"""Read-only forensic analysis of Qwen7B's completed small-v1 search."""
import json
from pathlib import Path
import re
import sys
from collections import Counter, defaultdict
import hashlib
import csv

sys.path.insert(0, str(Path(__file__).resolve().parent / 'qwen14_small'))
from features import GROUP_COLUMNS, ITEM_COLUMNS, USER_COLUMNS, validate_expression
from original_prompt import program_key
import duckdb

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'reports/hm_small_llms_v1/exports/qwen_llama/qwen'
OUT = ROOT / 'reports/qwen7b_generation_errors_v1'


def parse_response(text):
    blocks = re.findall(r'```(?:json)?\s*\n(.*?)```', text, re.S | re.I)
    return json.loads(blocks[0] if blocks else text)


def inspect():
    state = json.loads((SOURCE / 'search_state.json').read_text())
    rows = []
    for trial in state['trials']:
        directory = SOURCE / 'candidates' / f"candidate_{trial['call']:03d}"
        response = json.loads((directory / 'response.json').read_text())
        try:
            program = parse_response(response['text'])
        except Exception:
            program = None
        entry = {'call': trial['call'], 'proposal': trial['proposal'], 'repair': trial['repair'],
                 'status': trial['status'], 'error': trial.get('error', ''), 'program': program,
                 'text': response['text'], 'stage': trial.get('failure_stage'), 'truncated': response['truncated']}
        rows.append(entry)
        if trial['status'] == 'rejected':
            error = trial['error']
            lines = [line for line in error.splitlines() if re.search(r'(?:Error|Exception):', line)]
            print('\nCALL', trial['call'], 'proposal', trial['proposal'], 'repair', trial['repair'], 'ERROR', lines[-1] if lines else error)
            if program:
                for kind in ['aggregates', 'derived']:
                    for feature in program.get(kind, []):
                        print(kind, feature)
            else:
                print(response['text'])
    OUT.mkdir(exist_ok=True)
    (OUT / 'response_inventory.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')


def primary(row):
    error = row['error'].lower()
    if row['status'] != 'rejected':
        return row['status']
    if 'only numeric sql' in error:
        return 'string_values'
    if "forbidden token 'over'" in error:
        return 'window_functions'
    if 'invalid grouping keys' in error:
        return 'grouping_keys'
    if 'referenced column' in error and 'not found' in error:
        return 'history_in_derived'
    if 'parser error' in error:
        return 'sql_syntax'
    if "forbidden token 'customer_id'" in error:
        return 'id_in_derived'
    raise ValueError(row)


def valid_keys(keys):
    return (isinstance(keys, list) and 1 <= len(keys) <= 2 and len(keys) == len(set(keys))
            and all(k in GROUP_COLUMNS for k in keys) and (len(keys) == 1 or 'customer_id' in keys))


def feature_diagnostics(program):
    """Collect independent errors, unlike the original first-error validator.

    EXPLAIN binds an empty synthetic schema only. No features are silently fixed,
    no user data/labels are queried, no training or metric selection is performed.
    """
    issues = []
    history_cols = ['customer_id', 'article_id', 'price', 'sales_channel_id', 'days_ago', 'customer_age', *ITEM_COLUMNS]
    raw_cols = ['raw_u_' + n.lower() for n in USER_COLUMNS] + ['raw_i_' + n for n in ITEM_COLUMNS]
    con = duckdb.connect(config={'enable_external_access': 'false', 'threads': '1', 'memory_limit': '128MB'})
    con.execute('CREATE TABLE history (' + ','.join(c + ' DOUBLE' for c in history_cols) + ')')
    agg_names = [e['name'] for e in program.get('aggregates', [])]
    con.execute('CREATE TABLE candidate_features (' + ','.join(c + ' DOUBLE' for c in raw_cols + agg_names) + ')')
    try:
        for kind in ['aggregates', 'derived']:
            for index, feature in enumerate(program.get(kind, [])):
                path = f'{kind}[{index}]'
                sql = feature['sql']
                identifiers = {s.lower() for s in re.findall(r'\b[a-zA-Z_][a-zA-Z_0-9]*\b', sql)}
                notes = []
                if kind == 'aggregates':
                    keys = feature.get('keys')
                    if not valid_keys(keys):
                        notes.append('Invalid keys: ' + repr(keys))
                    if any(s.startswith('raw_') for s in identifiers):
                        notes.append('raw_* fields are unavailable in history aggregates')
                else:
                    bad = sorted(identifiers.intersection(history_cols))
                    if bad:
                        notes.append('History fields unavailable in derived: ' + ','.join(bad))
                    aggregate_calls = re.findall(r'\b(count|sum|avg|min|max|mode|median|approx_count_distinct)\s*\(', sql, re.I)
                    if aggregate_calls:
                        notes.append('Aggregate function in derived: ' + ','.join(aggregate_calls))
                if "'" in sql or '"' in sql:
                    notes.append('Quoted SQL strings/identifiers forbidden by numeric interface')
                if re.search(r'\bover\b|\brows\s+between\b', sql, re.I):
                    notes.append('Window syntax forbidden')
                try:
                    validate_expression(sql, aggregate=kind == 'aggregates')
                except Exception as error:
                    notes.append('Validator: ' + str(error))
                else:
                    if kind == 'derived' or valid_keys(feature.get('keys')):
                        query = ('SELECT ' + ','.join(feature['keys']) + ',' + sql + ' AS ' + feature['name']
                                 + ' FROM history GROUP BY ' + ','.join(feature['keys'])) if kind == 'aggregates' else (
                                     'SELECT ' + sql + ' AS ' + feature['name'] + ' FROM candidate_features')
                        try:
                            con.execute('EXPLAIN ' + query)
                        except Exception as error:
                            notes.append('DuckDB bind: ' + str(error).splitlines()[0])
                if notes:
                    issues.append({'path': path, 'name': feature['name'], 'sql': sql, 'issues': notes})
                if kind == 'derived':
                    con.execute('ALTER TABLE candidate_features ADD COLUMN ' + feature['name'] + ' DOUBLE')
    finally:
        con.close()
    return issues


def analyze():
    rows = json.loads((OUT / 'response_inventory.json').read_text())
    state = json.loads((SOURCE / 'search_state.json').read_text())
    assert len(rows) == 67 and all(r['program'] is not None and not r['truncated'] for r in rows)
    causes = Counter(primary(r) for r in rows if r['status'] == 'rejected')
    assert causes == {'string_values': 9, 'window_functions': 8, 'grouping_keys': 6,
                      'history_in_derived': 4, 'sql_syntax': 2, 'id_in_derived': 1}
    for row in rows:
        if row['status'] == 'rejected' and primary(row) == 'string_values':
            assert any("'" in feature['sql'] or '"' in feature['sql'] for kind in ['aggregates', 'derived'] for feature in row['program'].get(kind, []))
    chains = defaultdict(list)
    valid_keys_seen = {}
    duplicates = []
    unchanged = []
    latent = []
    inventory = []
    for row in rows:
        chain = chains[row['proposal']]
        signature = lambda p: json.dumps({k: v for k, v in p.items() if k != 'rationale'}, sort_keys=True)
        if row['repair'] and signature(row['program']) == signature(chain[-1]['program']):
            unchanged.append({'call': row['call'], 'previous_call': chain[-1]['call'], 'status': row['status']})
        chain.append(row)
        if row['status'] == 'valid':
            valid_keys_seen[program_key(row['program'])] = row['call']
        elif row['status'] == 'duplicate':
            first = valid_keys_seen[program_key(row['program'])]
            duplicates.append({'call': row['call'], 'duplicate_of': first, 'repair': row['repair']})
        if row['status'] == 'rejected':
            diagnostics = feature_diagnostics(row['program'])
            latent.append({'call': row['call'], 'primary': primary(row), 'features': diagnostics})
            inventory.append({'call': row['call'], 'proposal': row['proposal'], 'repair': row['repair'],
                              'category': primary(row), 'error': row['error'].splitlines()[0],
                              'issues_detected': len(diagnostics)})
    # Test proposed valid examples on DuckDB's binder, not by retraining.
    examples = {
        'aggregates': [
            {'name': 'f_recent_count', 'keys': ['customer_id'], 'sql': 'count(*) FILTER (WHERE days_ago <= 7)'},
            {'name': 'f_channel1_count', 'keys': ['customer_id'], 'sql': 'count(*) FILTER (WHERE sales_channel_id = 1)'},
            {'name': 'f_age_mode', 'keys': ['customer_id'], 'sql': 'mode(customer_age ORDER BY customer_age)'},
            {'name': 'f_purchase_count', 'keys': ['customer_id'], 'sql': 'count(*)'},
        ],
        'derived': [
            {'name': 'f_age_bucket', 'sql': 'CASE WHEN raw_u_age < 20 THEN 0 WHEN raw_u_age < 40 THEN 1 ELSE 2 END'},
            {'name': 'f_recent_share', 'sql': 'f_recent_count / nullif(f_purchase_count, 0)'},
        ]}
    assert not feature_diagnostics(examples)
    failures_multi = [e for e in latent if len(e['features']) > 1]
    chain_rows = [{'proposal': key, 'calls': [r['call'] for r in values], 'statuses': [r['status'] for r in values],
                   'successful': any(r['status'] == 'valid' for r in values)} for key, values in chains.items()]
    repairs = [r for r in rows if r['repair']]
    repairs_by_depth = {str(depth): dict(Counter(r['status'] for r in rows if r['repair'] == depth)) for depth in range(4)}
    results = {'calls': 67, 'valid': 20, 'rejected': 30, 'duplicate': 17, 'json_parseable': 67, 'truncated': 0,
               'primary_failure_counts': dict(causes), 'primary_calls': {cause: [r['call'] for r in rows if r['status'] == 'rejected' and primary(r) == cause] for cause in causes},
               'proposals': len(chains), 'successful_proposals': sum(r['successful'] for r in chain_rows),
               'repair_calls': len(repairs), 'repair_status_by_depth': repairs_by_depth,
               'unchanged_program_repairs': unchanged, 'duplicate_targets': dict(Counter(d['duplicate_of'] for d in duplicates)),
               'multi_issue_rejected_responses': [e['call'] for e in failures_multi],
               'diagnostic_limit': 'Synthetic DOUBLE schema: binder validation, not proof of numeric values/feature usefulness/data-dependent semantics.',
               'duckdb_version': duckdb.__version__, 'no_model_training_or_generation': True,
               'candidate2_to5': [r['call'] for r in chains[1]],
               'proposed_examples_bind_checked': True}
    for name, value in [('analysis.json', results), ('repair_chains.json', chain_rows), ('duplicate_map.json', duplicates),
                         ('all_detected_issues.json', latent), ('checked_examples.json', examples)]:
        (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    with (OUT / 'rejections.csv').open('w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(inventory[0]))
        writer.writeheader()
        writer.writerows(inventory)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    report(results, chain_rows, duplicates)


def report(stats, chains, duplicates):
    labels = {'string_values': 'Строковые значения вместо числовых', 'window_functions': 'Оконные функции OVER',
              'grouping_keys': 'Неподдерживаемая группировка', 'history_in_derived': 'Поля истории внутри derived',
              'sql_syntax': 'Неверный синтаксис SQL', 'id_in_derived': 'Недопустимый ID внутри derived'}
    lines = ['# Ошибки генерации Qwen2.5-Coder-7B-Instruct: реальный small-v1 запуск', '',
             'Источник: hm_small_qwen_llama_sql_v1_2ecc60d61fd4, ветка qwen. Все67ответов изучены;20наборов оценены,30отклонены,17дубликатов.',
             'JSON читался у67/67,обрезанных ответов0. Поэтому диагноз «модель не умеет выдавать JSON» этим запуском не подтверждается.',
             'Ни обучения,ни новых LLM вызовов,ни изменения исторических метрик. Разбор использует prompts/responses/errors; test не используется для исправления программ.', '',
             '| Первая причина отклонения | Ответов | Вызовы |', '|---|---:|---|']
    for cause, count in stats['primary_failure_counts'].items():
        lines.append(f"| {labels[cause]} | {count} | {stats['primary_calls'][cause]} |")
    lines += ['', 'Это первая ошибка в каждом ответе: сумма30. В одном ответе часто есть несколько независимых ошибок; полный перечень all_detected_issues.json. Не складывать многометочные категории.', '',
              '## Конкретные ошибки и корректные конструкции', '',
              '1. Call6–8:CASE возвращает young/middle/old и находится в aggregate сraw_u_age. Строки запрещены; raw_u_age отсутствует в history. Возрастную корзину следует вычислять вderived изraw_u_age, возвращая0/1/2.',
              '2. Call3:mode(customer_age) OVER(PARTITION BY customer_age). OVER запрещён нашим интерфейсом; host уже делаетGROUP BY. Для mode корректно mode(customer_age ORDER BY customer_age), а не ORDER BY после закрывающей скобки(call2).',
              '3. Call4:keys=[customer_id,department_no,product_type_no] — host поддерживает не более2ключей. Call9/43/60–62:группировка поsales_channel_id невозможна, поскольку будущий канал покупки отсутствует уcandidate-пары. Альтернатива:count(*) FILTER(WHERE sales_channel_id=1) сkeys=[customer_id] или[article_id].',
              '4. Call47–48/56:derived используетsum(CASE WHEN days_ago<=...); days_ago доступен только вhistory агрегатах. Создать f_recent_count сcount(*) FILTER(WHERE days_ago<=7), затемderived=f_recent_count/nullif(f_purchase_count,0). Call31 использует product_code иdays_ago вderived, где их нет.',
              '5. Call30 использует FILTER(WHERE customer_id) вderived. После запретаID модель вcall31 заменилаcustomer_id наproduct_code,но проблема namespace иагрегации вderived сохранилась. Это не доказательство вычисления численногоID-признака: неверная конструкция фильтра использовалаID в отсутствующемnamespace.', '',
              'Корректные примеры проверены черезEXPLAIN вDuckDB1.4.1:checked_examples.json. Это проверка binding на пустой синтетической схеме, не оценка качества признаков.', '',
              '## Почему исправления расходовали вызовы', '',
              f"27предложений,40repair-вызовов. Полностью неизменённых программ вrepair: {len(stats['unchanged_program_repairs'])}; сравнение игнорируетrationale и форматирование, но не переименования.",
              'Сообщения Only numeric SQL expressions и Invalid grouping keys не называли индекс/имя конкретного признака, неверное поле и допустимую замену. При нескольких ошибках сообщалась только первая.',
              'Например6→7→8 сохраняли неверные строковые корзины,9 исправил строки, но всё ещё имел запрещённую группировку. Цепочка2→3→4→5 в конце стала валидной, однако по пути получила новые ошибки.',
              'Для повторов старыйrepair просилdistinct complete set, но основнойprompt продолжал показывать один лучший набор; перечень уже проверенных аналогов не передавался.', '',
              f"17каноническихдубликатов; ссылкинапервоисточники: {stats['duplicate_targets']}. Это технически повторные формулы, а не обязательно невалидныйSQL.", '',
              '## Что изменить следующим, сохраняя SQL-интерфейс', '',
              '1. Вернуть сразу список ошибок сpath/name/sql,причиной и конкретной допустимой заменой. Отделить namespacehistory отnamespacecandidate/derived. Не посылать длинную трассировку вместо объяснения.',
              '2. Добавить вprompt компактный рабочий пример сaggregate FILTER,derived NULLIF ичисловойкорзиной; рядом триантипримера:строковаякорзина,OVER,days_ago вderived.',
              '3. Зафиксировать конечный список сочетанийkeys; дляканалов показатьFILTER,длятройнойгруппировки — двеотдельныеcustomer×category статистики. Можно ограничитьkeys JSON-схемой,сохранивSQLполе свободным.',
              '4. Вrepair требоватьминимальныеизменения перечисленныхfeatures. Еслипрограмма не изменилась или вернулась таже canonicalsignature, не повторятьтотжепромпт; перейти кцелевомуисправлению/новому предложению. Не удалятьпризнаки молча и не превращатьневалидныйответвуспех безобучения.',
              '5. Приduplicate передаватьномер/формулы совпавшегонабора иконкретнуюосьизменения:окно7→30,новаяcandidate-specific группировка,новаястатистика. Менятьне толькословесныеимена.',
              '6. Считать отдельноуспехи/ошибки/дубликаты/неизменённыеrepair; менятьодинкомпонент заопыт. Сначала сравнитьдиагностику+prompt противстарогоконтроля на техжепарах/search,безвыборапоtest.', '',
              'Это рекомендации по наблюдаемым ошибкам. Их влияние на долю успехов иMAP ещё не проверено; прошлые30отказов нельзя считать гарантированно устранимыми однимпромптом.', '',
              '## Смысл признаков — отдельная проверка', '',
              'Упобедителяcall5 названияdiscount означаютsum/avg(price),не наблюдаемуюскидку. Частотаapprox_count_distinct(product_code) — разнообразие,не просто число покупок. Кодможет исполняться,но имя/объяснение неточны.',
              'Более высокий процентвалидныхответов сампособе не доказывает повышенияMAP. Статистикипризнаков иэкономическийсмысл нужно проверятьотдельно.', '',
              'Источники SQL:[DuckDB FILTER](https://www.duckdb.org/docs/current/sql/query_syntax/filter),[агрегаты DuckDB](https://www.duckdb.org/docs/current/sql/functions/aggregates).']
    (OUT / 'report.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    if not (OUT / 'response_inventory.json').exists():
        inspect()
    analyze()
