"""Combine independently audited real Kaggle runs and frozen small-v1 baselines."""
import json
from itertools import combinations
from pathlib import Path
import re
import sys
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/hm_small_llms_v1'
DATA = ROOT / 'data/kaggle_hm_small_sql_compare_v1'
sys.path.insert(0, str(ROOT / 'LLMFeatures/kaggle/qwen14_small'))
from worker import ap12, write

LLMS = ['Qwen7B_LightGBM', 'Llama8B_LightGBM', 'Qwen14B_LightGBM']
COLORS = dict(zip(LLMS, ['#2678b8', '#d78529', '#2c9b70']))
DISPLAY = {'Raw15_LightGBM': 'LightGBM: исходные 15 полей', 'Qwen7B_LightGBM': 'Qwen 7B → LightGBM',
           'Llama8B_LightGBM': 'Llama 8B → LightGBM', 'Qwen14B_LightGBM': 'Qwen 14B → LightGBM',
           'contextgnn': 'ContextGNN', 'idgnn': 'ID-GNN', 'lightgbm_idgnn': 'ID-GNN → LightGBM',
           'lightgbm_manual': 'LightGBM: ручные признаки', 'recformer_finetuned': 'Recformer: исходное дообучение',
           'recformer_zero_shot': 'Recformer: zero-shot', 'two_tower': 'Две башни (GraphSAGE)',
           'Recformer_LR_warmup': 'Recformer: LR + warmup', 'Recformer_freeze6_trained': 'Recformer: заморозка 6 слоёв',
           'Recformer_long_selected': 'Recformer: длинный запуск', 'TDM_fixed_beam': 'TDM: фикс. дерево, beam',
           'TDM_fixed_full': 'TDM: фикс. дерево, полный поиск', 'TDM_cluster_beam': 'TDM: кластеризация, beam',
           'TDM_cluster_full': 'TDM: кластеризация, полный поиск', 'popularity': 'Популярность'}


def main():
    pending = '--pending-replay' in sys.argv
    audit = json.loads((OUT / ('audit_pre_replay.json' if pending else 'audit.json')).read_text())
    audit['report_replays_pending'] = pending
    if not pending:
        assert audit['status'] == 'passed' and len(audit['replays']) == 4
    target = {split: pd.read_parquet(DATA / f'{split}_targets.parquet') for split in ['val', 'test']}
    selection = json.loads((DATA / 'selection.json').read_text())
    quality, initial = {}, []
    for name in ['Raw15_LightGBM', *LLMS]:
        if name == 'Raw15_LightGBM':
            folder = OUT / 'exports/qwen_llama/raw_control'
        else:
            source_name = 'qwen14b' if name == 'Qwen14B_LightGBM' else 'qwen_llama'
            label = {'Qwen7B_LightGBM': 'qwen', 'Llama8B_LightGBM': 'llama', 'Qwen14B_LightGBM': 'qwen14b'}[name]
            folder = OUT / 'exports' / source_name / label / 'candidates' / f"candidate_{audit['models'][name]['selected_call']:03d}"
        row = {'model': name, 'source': str(folder.relative_to(ROOT))}
        quality[name] = {}
        for split in ['val', 'test']:
            pred = np.load(folder / f'{split}_predictions.npy')
            assert np.array_equal(np.load(folder / f'{split}_users.npy'), target[split].customer_id.to_numpy())
            values = ap12(pred, target[split].article_id)
            metric = json.loads((folder / f'{split}_metrics.json').read_text())
            assert abs(float(values.mean()) - metric['map']) < 1e-12
            quality[name][split] = values
            row[split + '_map_percent'] = float(values.mean() * 100)
            if split == 'val':
                for stage, indices in selection.items():
                    quality[name][stage] = values[indices]
                    row[stage + '_map_percent'] = float(values[indices].mean() * 100)
        initial.append(row)
    frame = pd.DataFrame(initial)
    rows = []

    def reference(name, folder, metrics, predictions=None):
        row = {'model': name, 'source': str(folder.relative_to(ROOT))}
        quality[name] = {}
        for split in ['val', 'test']:
            pred = np.load(predictions[split] if predictions else folder / f'{split}_predictions.npy')
            assert ((pred >= 0) & (pred < 5000)).all()
            ap = ap12(pred, target[split].article_id)
            assert abs(float(ap.mean()) - metrics[f'{split}_metrics']['map']) < 1e-10, name
            if (folder / f'{split}_user_ids.npy').exists():
                assert np.array_equal(np.load(folder / f'{split}_user_ids.npy'), target[split].customer_id.to_numpy())
            quality[name][split] = ap
            row[split + '_map_percent'] = 100 * float(ap.mean())
            if split == 'val':
                for stage, indices in selection.items():
                    row[stage + '_map_percent'] = 100 * float(ap[indices].mean())
                    quality[name][stage] = ap[indices]
        rows.append(row)

    # Original seven references: exactly the data bundle attached to all three LLMs.
    for entry in json.loads((DATA / 'references/sources.json').read_text()):
        reference(entry['model'], ROOT / entry['source'], entry['metrics'],
                  {split: DATA / f"references/{entry['model']}_{split}.npy" for split in ['val', 'test']})
    # Later completed small-v1 variants, kept separately identifiable.
    for name, relative in [
        ('Recformer_LR_warmup', 'Recformer/results/hm_small_low_lr_warmup_seed42_v1/finetuned'),
        ('Recformer_freeze6_trained', 'Recformer/results/hm_small_freeze_lower6_seed42_v1/finetuned'),
        ('Recformer_long_selected', 'Recformer/results/hm_small_long_floor_seed42_v1/finetuned'),
        ('TDM_fixed_beam', 'TDM/results/hm_small_v1/fixed/beam'),
        ('TDM_fixed_full', 'TDM/results/hm_small_v1/fixed/full'),
        ('TDM_cluster_beam', 'TDM/results/hm_small_v1/cluster/beam'),
        ('TDM_cluster_full', 'TDM/results/hm_small_v1/cluster/full'),
    ]:
        folder = ROOT / relative
        if (folder / 'metrics.json').exists():
            reference(name, folder, json.loads((folder / 'metrics.json').read_text()))
    tx = pd.read_parquet(DATA / 'transactions.parquet')
    pop = {}
    for split in ['val', 'test']:
        counts = tx[tx.t_dat <= target[split].timestamp.iloc[0]].article_id.value_counts().reindex(np.arange(5000), fill_value=0)
        ranking = np.lexsort((np.arange(5000), -counts.values))[:12]
        pop[f'{split}_metrics'] = {'map': float(ap12(np.tile(ranking, (len(target[split]), 1)), target[split].article_id).mean())}
    # Popularity is preserved from the original report; no need to duplicate its label.
    original_csv = pd.read_csv(OUT / 'exports/qwen_llama/comparison.csv')
    pop_row = original_csv[original_csv.model == 'popularity'].iloc[0]
    assert abs(pop_row.test_map_percent - pop['test_metrics']['map'] * 100) < 1e-10
    rows.append({'model': 'popularity', 'val_map_percent': pop['val_metrics']['map'] * 100,
                 'test_map_percent': pop['test_metrics']['map'] * 100,
                 'heldout_val_map_percent': pop_row.heldout_val_map_percent, 'source': 'same time-safe popularity control'})
    combined = pd.concat([frame, pd.DataFrame(rows)], ignore_index=True)
    combined.to_csv(OUT / 'comparison_all_methods.csv', index=False)
    study = []
    for title in LLMS:
        value = audit['models'][title]
        export = 'qwen14b' if title == 'Qwen14B_LightGBM' else 'qwen_llama'
        label = {'Qwen7B_LightGBM': 'qwen', 'Llama8B_LightGBM': 'llama', 'Qwen14B_LightGBM': 'qwen14b'}[title]
        trials = json.loads((OUT / 'exports' / export / label / 'search_state.json').read_text())['trials']
        failures = Counter()
        for trial in trials:
            if trial['status'] == 'rejected':
                lines = [line.strip() for line in trial.get('error', '').splitlines() if re.search(r'(?:Exception|Error):', line)]
                failures[(lines[-1] if lines else trial.get('error', ''))[:220]] += 1
        study.append({'model': title, 'calls': value['calls'], 'successful': 20,
                      'rejected': value['statuses'].get('rejected', 0), 'duplicate': value['statuses'].get('duplicate', 0),
                      'success_percent': 2000 / value['calls'], 'repairs': value['repairs'],
                      'generation_minutes': value['generation_seconds'] / 60,
                      'selected_call': value['selected_call'], 'aggregates': value['aggregates'], 'derived': value['derived'],
                      'customer_only_aggregates': all(keys == ['customer_id'] for keys in value['aggregate_groupings'])})
        write(OUT / (label + '_failure_causes.json'), failures.most_common(15))
    efficiency = pd.DataFrame(study)
    efficiency.to_csv(OUT / 'search_efficiency.csv', index=False)
    pairs = list(combinations(LLMS, 2)) + [(name, reference_name) for name in LLMS
            for reference_name in ['Raw15_LightGBM', 'lightgbm_manual', 'contextgnn', 'Recformer_LR_warmup']]
    rng = np.random.default_rng(42)
    indices = rng.integers(0, 250, size=(10000, 250))
    intervals = []
    for first, second in pairs:
        diff = quality[first]['test'] - quality[second]['test']
        lower, upper = np.quantile(diff[indices].mean(1) * 100, [.025, .975])
        intervals.append({'first': first, 'second': second, 'difference_pp': float(diff.mean() * 100),
                          'ci95_lower_pp': float(lower), 'ci95_upper_pp': float(upper),
                          'better_users': int((diff > 0).sum()), 'tied_users': int((diff == 0).sum()), 'worse_users': int((diff < 0).sum())})
    pd.DataFrame(intervals).to_csv(OUT / 'paired_test_bootstrap.csv', index=False)
    write(OUT / 'report.json', {'comparison': combined.to_dict('records'), 'search': study, 'bootstrap': intervals,
                              'audit_passed': not pending, 'replays_pending': pending, 'new_training': False, 'references_recomputed': len(rows),
                              'test_users': 250, 'validation_users': 304, 'catalog': 5000, 'seed': 42})
    plot(combined, efficiency, quality, audit)
    make_markdown(combined, efficiency, intervals, audit)
    print(efficiency.to_string(index=False))
    print(pd.DataFrame(intervals).iloc[:3].to_string(index=False))


def plot(frame, efficiency, quality, audit):
    focused = frame[frame.model.isin(LLMS + ['Raw15_LightGBM', 'lightgbm_manual', 'contextgnn', 'idgnn', 'Recformer_LR_warmup'])]
    for basename, values in [('comparison_llms', focused), ('comparison_all_methods', frame)]:
        values = values.sort_values('test_map_percent', ascending=False)
        fig, axes = plt.subplots(1, 2, figsize=(15, max(5, len(values) * .36)))
        for axis, split in zip(axes, ['val', 'test']):
            colors = [COLORS.get(name, '#9aa4ae') for name in values.model]
            labels = [DISPLAY.get(name, name) for name in values.model]
            axis.barh(labels, values[split + '_map_percent'], color=colors)
            axis.invert_yaxis()
            axis.set(title='Validation · 304 пользователя' if split == 'val' else 'Test · 250 пользователей', xlabel='MAP@12 (%)')
            axis.tick_params(axis='y', labelsize=9)
            for index, score in enumerate(values[split + '_map_percent']):
                axis.text(score + .025, index, f'{score:.3f}', va='center', fontsize=8)
            axis.set_xlim(0, max(values[split + '_map_percent']) * 1.17)
            axis.grid(axis='x', alpha=.2)
        fig.suptitle('Малый H&M · общий каталог из 5000 товаров · сортировка по test', fontsize=12)
        fig.tight_layout()
        fig.savefig(OUT / (basename + '.png'), dpi=160)
        plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for name in LLMS:
        value = audit['models'][name]
        export = 'qwen14b' if '14B' in name else 'qwen_llama'
        label = {'Qwen7B_LightGBM': 'qwen', 'Llama8B_LightGBM': 'llama', 'Qwen14B_LightGBM': 'qwen14b'}[name]
        trials = json.loads((OUT / 'exports' / export / label / 'search_state.json').read_text())['trials']
        valid = [t for t in trials if t['status'] == 'valid']
        axes[0].plot(np.arange(1, 21), np.maximum.accumulate([t['score'] * 100 for t in valid]), color=COLORS[name], label=name)
        axes[1].plot(np.arange(1, len(trials) + 1), np.cumsum([t['status'] == 'valid' for t in trials]), color=COLORS[name], label=name)
    axes[0].set(xlabel='Successfully evaluated distinct feature sets', ylabel='Best search MAP@12 (%)', title='Search fitness, not final test')
    axes[1].set(xlabel='LLM calls (including repairs)', ylabel='Successfully evaluated distinct sets', title='Generation efficiency')
    for axis in axes:
        axis.legend(fontsize=8)
        axis.grid(alpha=.2)
    fig.tight_layout()
    fig.savefig(OUT / 'search_progress.png', dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for status, color in [('successful', '#2c9b70'), ('rejected', '#d65d5d'), ('duplicate', '#a2a2a2')]:
        bottom = np.zeros(len(efficiency)) if status == 'successful' else efficiency.successful.to_numpy()
        if status == 'duplicate':
            bottom = bottom + efficiency.rejected.to_numpy()
        axes[0].bar(efficiency.model, efficiency[status], bottom=bottom, label=status, color=color)
    axes[0].set(ylabel='LLM calls', title='Budget use')
    axes[0].legend()
    axes[1].bar(efficiency.model, efficiency.generation_minutes, color=[COLORS[n] for n in efficiency.model])
    axes[1].set(ylabel='Minutes', title='Generation only; not full wall time')
    for axis in axes:
        axis.tick_params(axis='x', labelrotation=15)
    fig.tight_layout()
    fig.savefig(OUT / 'generation_efficiency.png', dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for name in LLMS + ['Raw15_LightGBM', 'lightgbm_manual', 'contextgnn']:
        values = quality[name]['test']
        axes[0].hist(values[values > 0] * 100, bins=np.linspace(0, 100, 21), histtype='step', label=name, color=COLORS.get(name))
        axes[1].bar(name, np.mean(values == 0) * 100, color=COLORS.get(name, '#9aa4ae'))
    axes[0].set(xlabel='Per-user AP@12 (%) among AP>0', ylabel='Users', title='Test AP distribution')
    axes[0].legend(fontsize=7)
    axes[1].set(ylabel='Test users with AP@12=0 (%)', ylim=(0, 100))
    axes[1].tick_params(axis='x', labelrotation=35)
    fig.tight_layout()
    fig.savefig(OUT / 'test_histograms.png', dpi=160)
    plt.close(fig)


def make_markdown(frame, efficiency, intervals, audit):
    lines = ['# Qwen7B, Llama8B и Qwen14B: проверенные результаты на малом H&M', '',
             'Все три LLM завершили поиск20различных оценённых наборов. На test выше Qwen7B; Qwen14B эффективнее по числу вызовов, но выше по test не стала.',
             'Одинаковые72813trainпар,4804user-time/8срезов,raw15,SQL/JSON-интерфейс,LightGBM150/31/4threads,seed42,NF4/FP16.',
             'Search128/confirm88/heldout88; итоговыеval304/test250,все5000товаров. Версии библиотек/GPU и4sharedsourceSHA совпали.',
             'Оба raw-контроля совпали по моделям и всем прогнозам. Все60 оценённых программ/моделей проверены поSHA/схеме/метрикам.',
             ('Независимый replay четырёх frozen моделей ещё проверяется. MAP в графиках пересчитан из сохранённых прогнозов.' if audit.get('report_replays_pending') else
              'Четыре frozen модели (raw+3LLM) независимо пересчитаны отдельными CPU-процессами: val/test top12/AP/MAP совпали точно.'),
             'Нового обучения,генерацииLLM или выбора поtest при аудите не было; исходныеZIP сохранены.', '',
             '| Модель | Validation MAP,% | Test MAP,% |', '|---|---:|---:|']
    for row in frame.to_dict('records'):
        lines.append(f"| {row['model']} | {row['val_map_percent']:.5f} | {row['test_map_percent']:.5f} |")
    lines += ['', '| LLM | Вызовы | Успех | Ошибка | Дубликат | Генерация,мин |', '|---|---:|---:|---:|---:|---:|']
    for row in efficiency.to_dict('records'):
        lines.append(f"| {row['model']} | {row['calls']} | {row['successful']} | {row['rejected']} | {row['duplicate']} | {row['generation_minutes']:.1f} |")
    lines += ['', 'Генерация — сумма сохранённых секунд generate(), без загрузкиLLM/деревьев/оценки. Это не полное время запуска.', '',
              '## Что выбрано', '',
              '- Qwen7B candidate005:6агрегатов+5формул. Есть статистики категорий и customer×department; названия discount относятся к price, а не к наблюдаемой скидке.',
              '- Llama8B candidate144:9агрегатов+5формул, все агрегаты по customer_id. f_article_popularity фактически отношение разнообразия покупок клиента; f_temporal_change_rate сравнивает mode с mode−1 и равнаtrue для непустого mode.',
              '- Qwen14B candidate014:13агрегатов+5формул, все по customer_id. Нет исторической популярности конкретного товара или customer×article/category агрегатов; min/max(days_ago) вычисляются корректно, но названия first/last перепутаны.',
              'Это ограничения содержания выбранных признаков, не обнаруженная прежняя ошибка Pandas-сопоставления. Raw item поля присутствуют у всех; деревья могут строить взаимодействия с ними.',
              'Связь отсутствия candidate-specific агрегатов с худшим test правдоподобна, но причинно отдельным опытом не проверена.', '',
              '## Неопределённость и границы сравнения', '',
              'Один seed,250test пользователей; парный bootstrap10k,seed42 является разведочной оценкой по пользователям, не многосидовой оценкой и не исправлен за множественные сравнения.',
              'Общийval304 включает search/confirmation. heldout88 не использовался LLM-отбором, но был частью исходного отбора baseline.',
              'Разные методы имеют разные бюджеты graph training/tuning/pretraining. Метрики малого каталога не сравниваются с полным H&M или статьёй.',
              'Точечный порядок test не доказывает устойчивого превосходства моделей; интервалы см. paired_test_bootstrap.csv.', '',
              '| Разность test | п.п. | 95% парный bootstrap,п.п. |', '|---|---:|---|']
    for row in intervals[:3]:
        lines.append(f"| {row['first']} − {row['second']} | {row['difference_pp']:+.4f} | [{row['ci95_lower_pp']:+.4f};{row['ci95_upper_pp']:+.4f}] |")
    lines += ['', '![Сравнение LLM](comparison_llms.png)', '', '![Поиск](search_progress.png)', '',
              '![Эффективность](generation_efficiency.png)', '', '![AP](test_histograms.png)', '',
              '![Все методы](comparison_all_methods.png)', '',
              'Программы победителей:',
              '- [Qwen7B](exports/qwen_llama/qwen/candidates/candidate_005/program.json)',
              '- [Llama8B](exports/qwen_llama/llama/candidates/candidate_144/program.json)',
              '- [Qwen14B](exports/qwen14b/qwen14b/candidates/candidate_014/program.json)']
    (OUT / 'report.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
