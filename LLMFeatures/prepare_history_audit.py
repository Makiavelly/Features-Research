"""Derive a standalone H009 auditor from the already reviewed H008 auditor."""
import ast
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if (ROOT/'LLMFeatures/audit_report_history.py').exists():
    raise SystemExit('Bootstrap already completed; do not overwrite the reviewed standalone auditor.')
source=(ROOT/'LLMFeatures/audit_report_generated_only.py').read_text(encoding='utf-8')
source=source.replace('H008','H009').replace('H006','H008')
source=source.replace("OUT = ROOT / 'reports/provider_generated_only_v1'", "OUT = ROOT / 'reports/provider_history_v1'")
source=source.replace("artifacts='reports/provider_generated_only_v1'", "artifacts='reports/provider_history_v1'")
source=source.replace("'memory_programs_per_prompt', ", '')
source=source.replace('GPT61Sol_GeneratedOnly','GPT61Sol_FullHistory')
source=source.replace('ConstantControl','HistoryConstantControl')
source=source.replace("'reports/authored20_v1/comparison_all_methods.csv'", "'reports/provider_generated_only_v1/comparison_all_methods.csv'")
source=source.replace("old_quality = read(ROOT / 'reports/gpt61sol_python_v1/quality.json')['GPT61Sol']['test']",
                      "old_quality = read(ROOT / 'reports/provider_generated_only_v1/quality.json')['GPT61Sol_GeneratedOnly']['test']")
source=source.replace("'GPT61Sol_FullHistory': 'API GPT: generated features ONLY'",
                      "'GPT61Sol_FullHistory': 'API GPT: FULL HISTORY', 'GPT61Sol_GeneratedOnly': 'API GPT: best-only (H008)'")
source=source.replace("'GPT61Sol_FullHistory', 'GPT61Sol_Python'", "'GPT61Sol_FullHistory', 'GPT61Sol_GeneratedOnly', 'GPT61Sol_Python'")
source=source.replace("'Generated only': quality['GPT61Sol_FullHistory']", "'Full history': quality['GPT61Sol_FullHistory']")
source=source.replace("'Generated + raw15': old_quality", "'Best-only history': old_quality")
source=source.replace('H009: no automatic raw15 inputs | same small data and downstream settings',
                      'H009: full own-island message history | no automatic raw15 inputs')
source=source.replace('One stochastic run; historical interfaces and generation budgets differ',
                      'Same data/downstream/call budget; full history uses more input tokens')
source=source.replace('# H009: GPT API — только сгенерированные признаки', '# H009: GPT API — полная история сообщений каждой популяции')
source=source.replace("'Те же72813пар/LightGBM150/31/4CPU/seed42/каталог5000. Память по-прежнему: лучший код своей '\n             'популяции плюс ошибки текущего предложения, без полной истории. Валидатор проверен до API; '",
                      "'Те же72813пар/LightGBM150/31/4CPU/seed42/каталог5000. Память: все прошлые запросы и ответы '\n             'своей популяции плюс результаты проверок/search, включая неудачные попытки. История не обрезается. Валидатор проверен до API; '")
source=source.replace('Не следует приписывать всю разницу одному удалению raw15.',
                      'Разница не доказывает эффект памяти по одному запуску; полный контекст использует больше входных токенов.')
source=source.replace('Это проверка отсутствия автоматического добавления raw15, а не запрет модели выбирать исходные атрибуты.',
                      'Автоматического raw15 нет в обоих сравниваемых режимах. Изменено хранение истории сообщений.')
source=source.replace('provider_generated_only_audited','provider_history_audited')
source=source.replace('H009 complete: generated-only inputs verified; final metrics and plots audited.',
                      'H009 complete: full own-island message histories verified; final metrics and plots audited.')
source=source.replace('    used_attempts = []', '    used_attempts = []\n    dialog_rows = []\n    from dialog_history import build_messages')
old="        assert request['messages'][1]['content'] == (folder / 'prompt.txt').read_text(encoding='utf-8')"
assert old in source
source=source.replace(old, """        prompt = (folder / 'prompt.txt').read_text(encoding='utf-8')
        expected_messages = build_messages(config, source, prompt, response['seed'])
        assert request['messages'] == expected_messages
        past_own = [t for t in trials if t['call'] < trial['call'] and t['island'] == trial['island']]
        assistants = [m['content'] for m in request['messages'] if m['role'] == 'assistant']
        expected_assistants = [read(Path(t['directory']) / 'response.json')['text'] for t in past_own]
        assert assistants == expected_assistants
        assert len(request['messages']) == 2*len(past_own)+2
        dialog_rows.append({'call': trial['call'], 'island': trial['island'],
                            'message_count': len(request['messages']), 'past_own_attempts': len(past_own),
                            'prompt_tokens': response['prompt_tokens'],
                            'own_history_calls': ','.join(str(t['call']) for t in past_own)})""")
source=source.replace("assert 'Host passes ONLY your returned f_* columns' in request['messages'][1]['content']",
                      "assert 'Host passes ONLY your returned f_* columns' in request['messages'][-1]['content']")
source=source.replace("assert 'Host appends the same 15 raw fields.' not in request['messages'][1]['content']",
                      "assert 'Host appends the same 15 raw fields.' not in request['messages'][-1]['content']")
source=source.replace("    audit['rejection_review'] = rejection_review",
                      "    audit['rejection_review'] = rejection_review\n    audit['full_own_island_history_verified'] = True\n    audit['max_messages'] = max(r['message_count'] for r in dialog_rows)\n    audit['max_prompt_tokens'] = max(r['prompt_tokens'] for r in dialog_rows)\n    pd.DataFrame(dialog_rows).to_csv(OUT/'dialog_audit.csv', index=False)")
ast.parse(source)
(ROOT/'LLMFeatures/audit_report_history.py').write_text(source,encoding='utf-8')
print('Created standalone audit_report_history.py')
