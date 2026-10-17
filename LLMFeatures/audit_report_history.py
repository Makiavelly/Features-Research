"""Audit and plot H009 saved results. No training and no network calls."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import sys
import numpy as np
import pandas as pd
import lightgbm as lgb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/provider_history_v1'
DATA = ROOT / 'data/kaggle_hm_small_sql_compare_v1'

def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ap_reference(predictions, targets):
    result = []
    for row, target in zip(predictions, targets):
        wanted = set(target)
        assert len(row) == 12 and len(set(row)) == 12 and wanted
        hits, total = 0, 0.
        for position, item in enumerate(row, 1):
            if item in wanted:
                hits += 1
                total += hits / position
        result.append(total / min(12, len(wanted)))
    return np.array(result)

def main():
    registry = read(OUT / 'current_run.json')
    assert registry['status'] == 'finished'
    source = Path(registry['directory'])
    config = read(source / 'run_config.json')
    assert config['automatic_raw_features'] == 0
    digest = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()[:12]
    assert source.name == config['protocol'] + '_' + digest
    for name, value in config['runtime_sha256'].items():
        assert sha(source / 'runtime_sources' / name) == value
    manifest = read(DATA / 'manifest.json')
    assert sha(DATA / 'manifest.json') == config['bundle_manifest_sha256']
    for name, value in manifest['files'].items():
        assert sha(DATA / name) == value
    reference = read(ROOT / 'LLMFeatures/results' / config['matched_reference_run'] / 'run_config.json')
    matched = ['seed', 'model_id', 'base_url', 'temperature', 'reasoning_effort', 'max_new_tokens',
               'train_pairs', 'train_pair_sha256', 'lightgbm_rounds',
               'cpu_threads', 'scoring_user_batch', 'search_users', 'confirmation_users',
               'heldout_val_users', 'validation_users', 'test_users', 'evaluation_catalog']
    assert all(config[k] == reference[k] for k in matched)
    history_reference = ROOT/'LLMFeatures/results'/config['history_comparison_run']
    reference_config = read(history_reference/'run_config.json')
    assert all(config[k] == reference_config[k] for k in matched)
    for name in ['python_features.py','base_features.py','worker.py','prompting.py','runtime.py','features.py']:
        assert sha(source/'runtime_sources'/name) == sha(history_reference/'runtime_sources'/name)
    sys.path.insert(0, str(source / 'runtime_sources'))
    from python_features import FeatureEngine, parse, program_key, RAW
    from worker import preflight
    arm = source / config['arm']
    trials = read(arm / 'search_state.json')['trials']
    valid = [t for t in trials if t['status'] == 'valid']
    assert len(valid) == 20
    assert len({t['program_key'] for t in valid}) == 20
    attempts = sorted((source / 'api_attempts').glob('attempt_*'))
    assert 20 <= len(attempts) <= 300
    model_files = list(arm.glob('candidates/*/model.txt'))
    assert all((Path(t['directory']) / 'model.txt').exists() for t in valid)
    used_attempts = []
    dialog_rows = []
    from dialog_history import build_messages
    for trial in trials:
        assert trial['island'] == trial['proposal'] % 3
        assert 0 <= trial['repair'] <= 3
        folder = Path(trial['directory'])
        response = read(folder / 'response.json')
        request = read(source / 'api_attempts' / f"attempt_{response['api_attempt']:03d}" / 'request.json')
        used_attempts.append(response['api_attempt'])
        prompt = (folder / 'prompt.txt').read_text(encoding='utf-8')
        expected_messages = build_messages(config, source, prompt, response['seed'])
        assert request['messages'] == expected_messages
        past_own = [t for t in trials if t['call'] < trial['call'] and t['island'] == trial['island']]
        assistants = [m['content'] for m in request['messages'] if m['role'] == 'assistant']
        expected_assistants = [read(Path(t['directory']) / 'response.json')['text'] for t in past_own]
        assert assistants == expected_assistants
        assert len(request['messages']) == 2*len(past_own)+2
        assert [m['role'] for m in request['messages']] == ['system']+['user','assistant']*len(past_own)+['user']
        if past_own:
            first_line,feedback_json,_ = request['messages'][-1]['content'].split('\n',2)
            assert first_line=='EVALUATION_FEEDBACK_FOR_PREVIOUS_RESPONSE:'
            feedback_data=json.loads(feedback_json)
            last=past_own[-1]
            assert all(feedback_data[k]==last[k] for k in ['call','island','proposal','repair','status'])
            if last['status']=='valid':
                assert feedback_data['search_map_fraction']==last['score']
            else:
                assert feedback_data['error']==last['error']
            assert not any(k in feedback_data for k in ['confirmation_map','test_map','val_map'])
        else:
            assert request['messages'][-1]['content']==prompt
        dialog_rows.append({'call': trial['call'], 'island': trial['island'],
                            'message_count': len(request['messages']), 'past_own_attempts': len(past_own),
                            'prompt_tokens': response['prompt_tokens'],
                            'own_history_calls': ','.join(str(t['call']) for t in past_own)})
        assert request['model'] == config['model_id']
        assert 'Host passes ONLY your returned f_* columns' in request['messages'][-1]['content']
        assert 'Host appends the same 15 raw fields.' not in request['messages'][-1]['content']
    assert len(used_attempts) == len(set(used_attempts))
    targets = {s: pd.read_parquet(DATA / f'{s}_targets.parquet') for s in ['val', 'test']}
    selection = read(DATA / 'selection.json')
    targets.update({s: targets['val'].iloc[rows].reset_index(drop=True) for s, rows in selection.items()})
    def metrics(folder, stage):
        metric = read(folder / f'{stage}_metrics.json')
        assert metric['program_sha256'] == sha(folder / 'program.json')
        assert metric['model_sha256'] == sha(folder / 'model.txt')
        assert metric['predictions_sha256'] == sha(folder / f'{stage}_predictions.npy')
        pred = np.load(folder / f'{stage}_predictions.npy')
        np.testing.assert_array_equal(np.load(folder / f'{stage}_users.npy'), targets[stage].customer_id)
        assert ((pred >= 0) & (pred < 5000)).all()
        ap = ap_reference(pred, targets[stage].article_id)
        np.testing.assert_allclose(ap, np.load(folder / f'{stage}_ap.npy'), atol=1e-15, rtol=0)
        np.testing.assert_allclose(ap.mean(), metric['map'], atol=1e-15, rtol=0)
        return metric, ap
    pairs = pd.read_parquet(DATA / 'train_pairs.parquet')
    engine = FeatureEngine(OUT / 'audit_scratch', DATA)
    numeric, trial_rows, memory = [], [], [None, None, None]
    rejection_review = []
    control = source / 'raw_control'
    assert read(control / 'program.json')['code'] == RAW
    assert read(control / 'feature_schema.json')['features'] == ['f_control']
    baseline = metrics(control, 'search')[0]['map']
    memory = [{'code': RAW, 'score': baseline} for _ in range(3)]
    try:
        for trial in trials:
            prompt = (Path(trial['directory']) / 'prompt.txt').read_text(encoding='utf-8')
            parent = memory[trial['island']]
            assert f"search MAP fraction={parent['score']}:" in prompt
            assert parent['code'] in prompt
            if trial['status'] != 'valid':
                if trial['status'] == 'rejected':
                    response = read(Path(trial['directory']) / 'response.json')
                    if response.get('truncated'):
                        rejection_review.append({'call': trial['call'], 'verified': 'provider output truncated'})
                    else:
                        try:
                            rejected_program = parse(response['text'])
                            if trial['failure_stage'] == 'preflight':
                                preflight(engine, pairs, rejected_program)
                            elif trial['failure_stage'] == 'training_and_search':
                                for cutoff, frame in pairs.groupby('timestamp', sort=True):
                                    engine.prepare(cutoff, frame.customer_id.values, rejected_program)
                                    engine.matrix(frame)
                            else:
                                raise AssertionError('Parse rejection no longer reproduced')
                        except AssertionError:
                            raise
                        except Exception as error:
                            rejection_review.append({'call': trial['call'], 'verified': 'failure reproduced without training',
                                                     'error': str(error)[:1200]})
                        else:
                            raise AssertionError(f"Rejection needs manual review: call{trial['call']}")
                continue
            folder = Path(trial['directory'])
            program = parse(read(folder / 'response.json')['text'])
            assert program == read(folder / 'program.json')
            assert program_key(program) == trial['program_key']
            schema = read(folder / 'feature_schema.json')
            assert 1 <= len(schema['features']) <= 36
            assert all(n.startswith('f_') for n in schema['features'])
            assert schema['categorical'] == [] and schema['train_pairs'] == 72813
            assert all(schema['preflight'].values())
            assert schema['params'] == read(ROOT / 'LLMFeatures/results' / config['matched_reference_run'] /
                'gpt61sol_python/candidates/candidate_010/feature_schema.json')['params']
            model = lgb.Booster(model_file=str(folder / 'model.txt'))
            assert model.feature_name() == schema['features']
            del model
            parts = []
            for cutoff, frame in pairs.groupby('timestamp', sort=True):
                engine.prepare(cutoff, frame.customer_id.values, program)
                values = engine.matrix(frame)
                assert engine.feature_names == schema['features']
                assert values.shape[1] == len(schema['features'])
                parts.append(values)
            matrix = np.concatenate(parts)
            columns = sorted(set(hashlib.sha256(np.ascontiguousarray(matrix[:, i]).tobytes()).hexdigest()
                                 for i in range(matrix.shape[1])))
            fingerprint = hashlib.sha256(''.join(columns).encode()).hexdigest()
            numeric.append(fingerprint)
            value, _ = metrics(folder, 'search')
            assert value['map'] == trial['score']
            trial_rows.append({'call': trial['call'], 'island': trial['island'], 'features': len(schema['features']),
                               'search_map_percent': 100*value['map'], 'numeric_signature': fingerprint})
            if trial['score'] > parent['score']:
                memory[trial['island']] = {'code': program['code'], 'score': trial['score']}
            print('Verified generated-only matrix and search:', trial['call'], flush=True)
    finally:
        engine.close()
    selected = read(arm / 'selected.json')
    ranked = sorted(valid, key=lambda t: (-t['score'], t['call']))[:3]
    assert [c['call'] for c in selected['confirmation']] == [None] + [t['call'] for t in ranked]
    for item in selected['confirmation']:
        assert metrics(Path(item['directory']), 'confirm')[0]['map'] == item['confirmation_map']
    assert max(selected['confirmation'], key=lambda x: x['confirmation_map'])['call'] == selected['call']
    winner = Path(selected['directory'])
    winner_features = read(winner / 'feature_schema.json')['features']
    explicit_static_copies = [n for n in winner_features if n.startswith('f_static_')]
    assert sha(winner / 'model.txt') == selected['model_sha256']
    assert sha(winner / 'program.json') == selected['program_sha256']
    comparisons, quality = [], {}
    for label, folder in [('HistoryConstantControl', control), ('GPT61Sol_FullHistory', winner)]:
        row = {'model': label, 'source': str(folder.relative_to(ROOT))}
        quality[label] = {}
        for stage in ['search', 'confirm', 'heldout_val', 'val', 'test']:
            metric, ap = metrics(folder, stage)
            row[stage + '_map_percent'] = metric['map'] * 100
            quality[label][stage] = ap.tolist()
            if stage in ['heldout_val', 'val', 'test']:
                replay = read(folder / f'replay_{stage}_metrics.json')
                assert replay['passed'] and replay['predictions_sha256'] == metric['predictions_sha256']
        comparisons.append(row)
    failures = [read(p / 'failure.json') for p in attempts if (p / 'failure.json').exists()]
    stats = {'api_posts': len(attempts), 'responses': len(trials), 'valid': len(valid),
             'statuses': dict(Counter(t['status'] for t in trials)), 'http_transport_failures': len(failures),
             'numeric_distinct_sets': len(set(numeric)), 'saved_candidate_models': len(model_files),
             'control_models': 1,
             'prompt_tokens': sum(t.get('prompt_tokens', 0) for t in trials),
             'completion_tokens': sum(t.get('generated_tokens', 0) for t in trials),
             'api_generation_seconds': sum(t.get('seconds', 0) for t in trials),
             'valid_programs_per_island': dict(Counter(t['island'] for t in valid))}
    audit = {'status': 'passed', 'run_id': source.name, 'source_directory': str(source),
             'stats': stats, 'selected_call': selected['call'], 'matched_fields': matched,
             'no_automatic_raw_columns': True, 'all_search_metrics_recomputed': True,
             'request_prompts_verified': True, 'six_saved_frozen_replays_verified': True}
    audit['rejection_review'] = rejection_review
    host_diagnostic = read(OUT/'host_builtin_diagnostic.json')
    assert host_diagnostic['status']=='passed' and host_diagnostic['live_runtime_changed'] is False
    assert host_diagnostic['identical_to_accepted_call16_all72813_train_pairs']
    assert host_diagnostic['original_module_sha256']==sha(source/'runtime_sources/python_features.py')
    for item in rejection_review:
        if item['call']==15:
            item['classification']='host builtin limitation, not invalid ordinary Python; accepted repair16 is numerically identical'
    audit['host_builtin_limitation_diagnostic']=host_diagnostic
    audit['full_own_island_history_verified'] = True
    audit['max_messages'] = max(r['message_count'] for r in dialog_rows)
    audit['max_prompt_tokens'] = max(r['prompt_tokens'] for r in dialog_rows)
    pd.DataFrame(dialog_rows).to_csv(OUT/'dialog_audit.csv', index=False)
    audit['winner_features'] = winner_features
    audit['winner_feature_names_with_static_prefix'] = explicit_static_copies
    (OUT / 'audit.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
    pd.DataFrame(trial_rows).to_csv(OUT / 'all_candidates.csv', index=False)
    own = pd.DataFrame(comparisons)
    own.to_csv(OUT / 'comparison.csv', index=False)
    (OUT / 'quality.json').write_text(json.dumps(quality, indent=2), encoding='utf-8')
    previous = pd.read_csv(ROOT / 'reports/provider_generated_only_v1/comparison_all_methods.csv')
    combined = pd.concat([previous, own], ignore_index=True)
    assert combined.model.is_unique
    combined.to_csv(OUT / 'comparison_all_methods.csv', index=False)
    labels = {'GPT61Sol_FullHistory': 'API GPT: FULL HISTORY', 'GPT61Sol_GeneratedOnly': 'API GPT: best-only (H008)', 'GPT61Sol_Python': 'API GPT: Python + raw15',
              'HistoryConstantControl': 'Constant-only control', 'CodexAuthored20': 'Codex: prior history known'}
    for filename, frame in [('comparison_all_methods', combined), ('comparison', combined[combined.model.isin([
            'GPT61Sol_FullHistory', 'GPT61Sol_GeneratedOnly', 'GPT61Sol_Python', 'GPT61Sol_SQL', 'Qwen7B_LightGBM',
            'Raw15_LightGBM', 'HistoryConstantControl', 'lightgbm_manual', 'idgnn', 'contextgnn'])])]:
        frame = frame.sort_values('test_map_percent')
        fig, axes = plt.subplots(1, 2, figsize=(18, max(6, .39*len(frame))), sharey=True, constrained_layout=True)
        colors = ['#d73027' if n == 'GPT61Sol_FullHistory' else '#557b9d' for n in frame.model]
        for ax, stage in zip(axes, ['val', 'test']):
            values = frame[stage+'_map_percent'].to_numpy()
            ax.barh(np.arange(len(frame)), values, color=colors)
            for y, v in enumerate(values):
                ax.text(v+.025, y, f'{v:.3f}%', va='center', fontsize=8)
            ax.set(yticks=np.arange(len(frame)), yticklabels=[labels.get(n, n) for n in frame.model],
                   xlabel='MAP@12 (%)', title=stage, xlim=(0, values.max()*1.17))
            ax.grid(axis='x', alpha=.2)
        fig.suptitle('H009: full own-island message history | no automatic raw15 inputs\nSame data/downstream/call budget; full history uses more input tokens')
        fig.savefig(OUT / (filename+'.png'), dpi=150)
        fig.savefig(OUT / (filename+'.svg'))
        plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True)
    old_quality = read(ROOT / 'reports/provider_generated_only_v1/quality.json')['GPT61Sol_GeneratedOnly']['test']
    values_by_name = {'Full history': quality['GPT61Sol_FullHistory']['test'],
                      'Best-only history': old_quality, 'Constant': quality['HistoryConstantControl']['test']}
    for label, values in values_by_name.items():
        values = np.array(values)
        axes[0].hist(values[values > 0]*100, bins=np.linspace(0, 100, 21), histtype='step', label=label)
        axes[1].bar(label, 100*np.mean(values == 0))
    axes[0].set(xlabel='Per-user AP@12 (%) among AP>0', ylabel='Users')
    axes[0].legend(fontsize=8)
    axes[1].set(ylabel='Users with AP@12=0 (%)', ylim=(0,100))
    axes[1].tick_params(axis='x', rotation=15)
    fig.savefig(OUT/'test_histograms.png', dpi=150)
    plt.close(fig)
    for name, target in [('search_progress.png', arm/'search_progress.png'), ('lightgbm_training.png', source/'lightgbm_training.png')]:
        shutil.copy2(target, OUT/name)
    delta = np.array(quality['GPT61Sol_FullHistory']['test']) - np.array(old_quality)
    rng = np.random.default_rng(42)
    bootstrap = delta[rng.integers(0, len(delta), size=(10000, len(delta)))].mean(axis=1)*100
    bootstrap_result = {'difference_pp': float(delta.mean()*100), 'ci95_pp': np.quantile(bootstrap,[.025,.975]).tolist()}
    (OUT/'paired_bootstrap.json').write_text(json.dumps(bootstrap_result, indent=2))
    lines = ['# H009: GPT API — полная история сообщений каждой популяции', '',
             'Реальный новый API-поиск, независимый от потока H008. Точная реализация провайдера не аттестована.',
             'Хост не добавлял исходные15 полей. Все входы каждой обученной модели — возвращённые f_*; '
             'при этом модель могла явно вернуть выбранные статические поля. Контроль — одна константа.',
             f"20 валидных программ, {stats['numeric_distinct_sets']} численно разных наборов; "
             f"{stats['api_posts']} фактическихPOST; статусы: {stats['statuses']}; HTTP/transport {stats['http_transport_failures']}.",
             f"Выбранный ответ: {selected['call']}; отбор top3 search + константный контроль → confirmation88 до test.",
             f"В выбранной модели {len(winner_features)} входов f_*. Имена с префиксом f_static_: "
             f"{explicit_static_copies}. Статические атрибуты могут возвращаться моделью и под другими именами. "
             'Автоматического raw15 нет в обоих сравниваемых режимах. Изменено хранение истории сообщений.',
             '', '```text', own.to_string(index=False), '```', '',
             'Те же72813пар/LightGBM150/31/4CPU/seed42/каталог5000. Память: все прошлые запросы и ответы '
             'своей популяции плюс результаты проверок/search, включая неудачные попытки. История не обрезается. Валидатор проверен до API; '
             'все матрицы, имена входов дерева, search/confirmation/finalAP и frozen replay проверены.',
             'Один seed; test250 уже просматривался в проекте. Разные API-поиски могут давать разные наборы '
             'даже при неизменной политике входов. Разница не доказывает эффект памяти по одному запуску; полный контекст использует больше входных токенов.',
             f"Парная разница test относительно H008: {bootstrap_result['difference_pp']:+.6f}п.п., "
             f"95% user-bootstrap {bootstrap_result['ci95_pp']}; это не неопределённость между запусками.",
             '', '![Сравнение](comparison.png)', '', '![Все методы](comparison_all_methods.png)',
             '', '![Поиск](search_progress.png)', '', '![Гистограммы](test_histograms.png)',
             '', '![Обучение](lightgbm_training.png)', '']
    (OUT/'report.md').write_text('\n'.join(lines), encoding='utf-8')
    baseline_source = ROOT/'LLMFeatures/results'/config['history_comparison_run']
    baseline_trials = read(baseline_source/config['arm']/'search_state.json')['trials']
    context = pd.DataFrame(dialog_rows)
    fig, axes = plt.subplots(1,2,figsize=(13,5),constrained_layout=True)
    for island,color in enumerate(['#2166ac','#d95f02','#1b9e77']):
        rows=context[context.island==island]
        axes[0].plot(rows.call,rows.prompt_tokens,marker='o',color=color,label=f'Full history: population {island}')
    axes[0].plot([t['call'] for t in baseline_trials],[t['prompt_tokens'] for t in baseline_trials],
                 color='0.5',ls='--',label='H008 best-only')
    axes[0].set(xlabel='Response number',ylabel='Actual API input tokens',title='Context grows with retained messages')
    axes[0].legend(fontsize=8)
    for label,items,color in [('H009 full history',trials,'#d73027'),('H008 best-only',baseline_trials,'#557b9d')]:
        successful=[t for t in items if t['status']=='valid']
        axes[1].step([t['call'] for t in successful],np.maximum.accumulate([100*t['score'] for t in successful]),
                     where='post',marker='o',color=color,label=label)
    axes[1].set(xlabel='Response number',ylabel='Best search MAP@12 (%)',title='Search feedback only; not final test')
    axes[1].legend(fontsize=8)
    fig.savefig(OUT/'context_and_search.png',dpi=150)
    plt.close(fig)
    first_payload_identical = sha(source/'api_attempts/attempt_001/request.json') == sha(baseline_source/'api_attempts/attempt_001/request.json')
    with (OUT/'report.md').open('a',encoding='utf-8') as stream:
        stream.write('\n\nИз отказов отдельно выделена попытка15: hasattr отсутствует в ограниченном namespace хоста. '
                     'Это ограничение исполнителя, а не ошибка обычного Python. В отдельной диагностической копии '
                     'разрешён только hasattr при сохранении AST/I/O проверок: preflight проходит, все72813train-пары '
                     'дают точно те же значения, что принятый ответ16. Текущий runtime не менялся, дополнительного '
                     'обучения/API не было. Нельзя считать все отклонения этого запуска ошибками модели.\n')
        stream.write(f'\n\nПолная история проверена в каждом фактическом запросе: максимум '
                     f"{audit['max_messages']} messages, {audit['max_prompt_tokens']} входных токенов. "
                     'Данные message_count/own_history_calls/prompt_tokens — в dialog_audit.csv. '
                     f'Первый API-payload побайтно совпадает с H008: {first_payload_identical}. '
                     'Seed провайдера не гарантирует детерминированность; различие первых ответов до накопления истории '
                     'также ограничивает вывод о причинном эффекте памяти.\n\n![Контекст и поиск](context_and_search.png)\n')
    delivery = source / 'audited_report'
    delivery.mkdir(exist_ok=True)
    for artifact in OUT.iterdir():
        if artifact.is_file() and artifact.name != 'current_run.json':
            shutil.copy2(artifact, delivery / artifact.name)
    if (source / 'report.md').exists() and not (source / 'legacy_report.md').exists():
        shutil.copy2(source / 'report.md', source / 'legacy_report.md')
    shutil.copy2(OUT / 'report.md', source / 'report.md')
    for name in ['comparison.png', 'comparison_all_methods.png', 'test_histograms.png',
                 'search_progress.png', 'lightgbm_training.png', 'context_and_search.png']:
        shutil.copy2(OUT / name, source / name)
    (source / 'README_RESULTS.md').write_text(
        '# H009 generated-only results\n\n'
        'The canonical report is [audited_report/report.md](audited_report/report.md).\n'
        'The compatibility folder `raw_control` contains ONE CONSTANT, not raw15 inputs.\n'
        'The original generic report is preserved as legacy_report.md.\n', encoding='utf-8')
    from runtime import archive_run
    archive_run(source)
    sys.path.insert(0, str(ROOT/'RelBenchGNN'))
    from tracking import record
    row = own[own.model=='GPT61Sol_FullHistory'].iloc[0]
    record('provider_history_audited', 'H009 complete: full own-island message histories verified; final metrics and plots audited.',
           source.name, status='complete', automatic_raw_features=0, audit_status='passed',
           api_requests=stats['api_posts'], measured=20, numeric_distinct_sets=stats['numeric_distinct_sets'],
           selected_call=selected['call'], val_metrics={'map': row.val_map_percent/100},
           test_metrics={'map': row.test_map_percent/100}, artifacts='reports/provider_history_v1')
    print(own.to_string(index=False), flush=True)
    print(json.dumps(stats), flush=True)

if __name__ == '__main__':
    main()
