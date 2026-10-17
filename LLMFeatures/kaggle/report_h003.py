"""H003 efficiency and quality report; all historic comparisons stay immutable."""
from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import re
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import duckdb

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/h003_small_v1'
LABEL = {'Qwen7B_control': 'Qwen7B: контроль', 'h003a': 'A: диагностика',
         'h003b': 'A+B: примеры', 'h003c': 'A+B+C: повторы', 'Raw15': 'LightGBM: raw15'}
COLORS = dict(zip(LABEL, ['#577590', '#f8961e', '#43aa8b', '#277da1', '#999999']))


def main():
    audit = json.loads((OUT / 'audit.json').read_text())
    assert audit['status'] == 'passed' and len(audit['replays']) == 4
    frame = pd.read_csv(OUT / 'comparison.csv')
    efficiency = pd.read_csv(OUT / 'generation_efficiency.csv')
    quality = json.loads((OUT / 'quality.json').read_text())
    states = json.loads((OUT / 'states.json').read_text())
    diagnostics = json.loads((OUT / 'diagnostics.json').read_text())
    failures = json.loads((OUT / 'failures.json').read_text())
    bootstrap = []
    for a, b in [('h003a','Qwen7B_control'), ('h003b','h003a'), ('h003c','h003b'),
                 ('h003c','Qwen7B_control'), ('h003c','Raw15')]:
        diff = np.array(quality[a]['test']) - np.array(quality[b]['test'])
        rng = np.random.default_rng(42)
        draws = diff[rng.integers(len(diff), size=(10000,len(diff)))].mean(1)*100
        bootstrap.append(dict(a=a, b=b, difference_pp=diff.mean()*100,
                              ci95_low_pp=np.quantile(draws,.025), ci95_high_pp=np.quantile(draws,.975),
                              better=int((diff>0).sum()), tied=int((diff==0).sum()), worse=int((diff<0).sum())))
    pd.DataFrame(bootstrap).to_csv(OUT / 'paired_test_bootstrap.csv', index=False)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    order = ['Raw15','Qwen7B_control','h003a','h003b','h003c']
    indexed = frame.set_index('model')
    for axis, split in zip(axes, ['val','test']):
        vals = [indexed.loc[n,split+'_map_percent'] for n in order]
        axis.barh([LABEL[n] for n in order], vals, color=[COLORS[n] for n in order])
        for y,v in enumerate(vals): axis.text(v+.015,y,f'{v:.3f}%',va='center',fontsize=9)
        axis.set(title=('Validation304 (включает search/confirm)' if split=='val' else 'Test250 (повторная оценка)'),
                 xlabel='MAP@12 (%)', xlim=(0,max(vals)*1.2))
        axis.grid(axis='x', alpha=.2)
    fig.suptitle('H003: те же данные, каталог5000, 20 измеренных наборов на вариант')
    fig.tight_layout()
    fig.savefig(OUT / 'comparison.png', dpi=160)
    plt.close(fig)
    e = efficiency.set_index('model')
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    names = list(states)
    bottom = np.zeros(4)
    for col,color in [('valid','#43aa8b'),('rejected','#f3722c'),('duplicate','#f9c74f')]:
        vals = e.loc[names,col].to_numpy()
        axes[0].bar(np.arange(4),vals,bottom=bottom,label=col,color=color)
        bottom += vals
    axes[0].set_xticks(np.arange(4),[LABEL[n] for n in names],rotation=20,ha='right')
    axes[0].set(title='Все вызовы; везде20 успехов',ylabel='Обращения к LLM')
    axes[0].legend(fontsize=8)
    for y,v in enumerate(bottom): axes[0].text(y,v+1,str(int(v)),ha='center')
    axes[1].bar([LABEL[n] for n in names],e.loc[names,'generation_minutes'],color=[COLORS[n] for n in names])
    axes[1].tick_params(axis='x',rotation=20)
    axes[1].set(title='Время генерации (T4)',ylabel='Минуты')
    axes[2].bar([LABEL[n] for n in names],e.loc[names,'unchanged_repairs'],color=[COLORS[n] for n in names])
    axes[2].tick_params(axis='x',rotation=20)
    axes[2].set(title='Неизменённые repair',ylabel='Обращения')
    fig.tight_layout()
    fig.savefig(OUT / 'generation_efficiency.png', dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1,2,figsize=(12,4.5))
    for name,trials in states.items():
        valid = [t for t in trials if t['status']=='valid']
        scores = np.maximum.accumulate([t['score']*100 for t in valid])
        axes[0].step([t['call'] for t in valid], scores, where='post',label=LABEL[name],color=COLORS[name])
        axes[1].plot(np.arange(1,21),scores,label=LABEL[name],color=COLORS[name])
    for axis in axes:
        axis.set(ylabel='Лучший search MAP@12 (%)')
        axis.grid(alpha=.2)
        axis.legend(fontsize=8)
    axes[0].set(xlabel='Все обращения к LLM',title='Качество на search128')
    axes[1].set(xlabel='Различные измеренные наборы',title='Одинаковый бюджет:20 наборов')
    fig.tight_layout()
    fig.savefig(OUT / 'search_progress.png',dpi=160)
    plt.close(fig)
    fig,axes = plt.subplots(1,2,figsize=(12,4.5))
    for name in order:
        ap = np.array(quality[name]['test'])*100
        axes[0].hist(ap[ap>0],bins=np.linspace(0,100,21),histtype='step',label=LABEL[name],color=COLORS[name])
        axes[1].bar(LABEL[name],100*np.mean(ap==0),color=COLORS[name])
    axes[0].set(title='Test AP@12 >0',xlabel='AP@12 (%)',ylabel='Пользователи')
    axes[0].legend(fontsize=8)
    axes[1].set(title='Пользователи без попаданий',ylabel='Доля пользователей (%)',ylim=(0,100))
    axes[1].tick_params(axis='x',rotation=25)
    fig.tight_layout()
    fig.savefig(OUT / 'test_histograms.png',dpi=160)
    plt.close(fig)
    # Append new results; never rewrite the previously audited comparison.
    old = pd.read_csv(ROOT / 'reports/hm_small_llms_v1/comparison_all_methods.csv')
    all_methods = pd.concat([old, frame[frame.model.str.startswith('h003')]],ignore_index=True)
    assert all_methods.model.is_unique
    all_methods.to_csv(OUT / 'comparison_all_methods.csv',index=False)
    from report_small_llms import DISPLAY
    displayed = {**DISPLAY,**LABEL}
    sorted_frame = all_methods.sort_values('test_map_percent')
    fig,axes=plt.subplots(1,2,figsize=(15,12))
    for axis,split in zip(axes,['val','test']):
        vals=sorted_frame[split+'_map_percent'].to_numpy()
        labels=[displayed.get(n,n) for n in sorted_frame.model]
        axis.barh(labels,vals,color=[COLORS.get(n,'#bbbbbb') for n in sorted_frame.model])
        for y,v in enumerate(vals): axis.text(v+.025,y,f'{v:.3f}',va='center',fontsize=8)
        axis.set(title=split,xlabel='MAP@12 (%)',xlim=(0,max(vals)*1.14))
        axis.grid(axis='x',alpha=.2)
    fig.suptitle('Все методы на small-v1: общий каталог5000; H003 — повторная test-оценка')
    fig.tight_layout()
    fig.savefig(OUT / 'comparison_all_methods.png',dpi=160)
    plt.close(fig)
    diagnostic_categories(diagnostics, failures)
    probes = binder_probes(diagnostics, audit)
    report = dict(audit_passed=True, comparison=frame.to_dict('records'), efficiency=efficiency.to_dict('records'),
                  paired_test_bootstrap=bootstrap, protocol_limit_probes=probes,
                  test_previously_inspected=True, single_seed=True, test_users=250,
                  hypotheses=dict(A='No clear efficiency gain in this run:65 vs67 calls,36 vs30 rejections',
                                  B='Fewer rejections but37 duplicates and78 calls',
                                  C='51 calls and15 rejections; better call efficiency, no test MAP improvement over control/raw'))
    (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    lines=['# H003: результат эксперимента Qwen7B', '',
           'Реальный Kaggle запуск hm_small_qwen7b_h003_v1_6852748fc0e4, все три ветки завершены.',
           'Проверены ZIP/конфиги/исходники/данные, все60различных измеренных программ, выбор top3+raw по confirmation.',
           'Независимый локальный CPU replay raw/A/B/C: val/test top12, AP и MAP совпали точно. Обучения и новых LLM-вызовов не было.', '',
           '## Эффективность генерации', '',
           '| Вариант | Вызовы | Успехи | Отказы | Дубликаты | Генерация, мин |', '|---|---:|---:|---:|---:|---:|']
    for row in efficiency.to_dict('records'):
        lines.append(f"| {LABEL[row['model']]} | {row['calls']} | {row['valid']} | {row['rejected']} | {row['duplicate']} | {row['generation_minutes']:.2f} |")
    lines += ['', 'A: подробной диагностики самой по себе не хватило:65 против67 вызовов; отказов36 против30.',
              'B: отказов21, но дубликатов37; суммарно78вызовов. Примеры не гарантируют разнообразие.',
              'C:51вызов,15отказов,16дубликатов. Против контроля вызовов на23.9%меньше, генерация44.88против46.42мин (на3.3%меньше).',
              'По сравнению сB: на34.6%меньше вызовов. Это один seed; время — одиночные измерения Kaggle, не устойчивый скоростной бенчмарк.',
              'Неизменённых repair:контроль13/40,A9/38,B20/50,C8/23. Контроль считает совпадение JSON безrationale, H003 дополнительно канонические совпадения; числа не полностью идентичны по определению.', '',
              '## Качество рекомендаций', '', '| Вариант | Val MAP,% | Heldout88 MAP,% | Test MAP,% |', '|---|---:|---:|---:|']
    for row in frame.to_dict('records'):
        lines.append(f"| {LABEL[row['model']]} | {row['val_map_percent']:.6f} | {row['heldout_val_map_percent']:.6f} | {row['test_map_percent']:.6f} |")
    lines += ['', 'Ни одна ветка не превысила старый Qwen7B или raw15 по test. При выборе по confirmation raw тоже участвовал.',
              'C выше контроля на полномval304, но ниже наheldout88 иtest: улучшение search/confirmation не доказывает обобщения.',
              'Полныйval304 включает поисковые строки. Нельзя выбирать лучшую модификацию по уже просмотренному test.',
              'Ручной LightGBM test1.233880%,ID-GNN2.653413%,ContextGNN3.015575%. Их обучение/отбор имеют иные бюджеты.', '',
              '## Что осталось в ошибках', '',
              'Все194ответа сохранены; A maxinput2787/B3148/C3579, обрезаний0, превышений6144нет. Переполнение контекста не объясняет отказы.',
              'УA сохранялись OVER, неверные aliases AS внутри выражений, группировки по каналу/возрасту, ссылки на отсутствующие f_*.',
              'УB заметны WITHIN GROUP, неизвестные функции/поля, ссылки на f_recent_count/f_purchase_count, отсутствующие в его же наборе.',
              'УC ошибки namespace/ссылок/OVER/строк тоже остались. Группировка по gender и raw_u_gender в других ветках показывает выдумывание полей.',
              'failure_categories.csv содержит многометочную классификацию по ответам; категории пересекаются и не суммируются в число отказов.', '',
              'Диагностика имела два ограничения:',
              '1. A calls21–23:sum/avg вderived по f_* прошли EXPLAIN одиночного SELECT, но меняли число строк. Настоящий FeatureEngine сохранил rid и отклонил их на preflight. Нужна проверка реальной формы SELECT *, expr, а не одиночного агрегата. Эти3ответа не засчитаны как успехи.',
              '2. Сообщение allowlist про GROUP скрывало реальную SQL-проблему. Все9таких выражений используют quantile_cont(q) WITHIN GROUP: DuckDB1.4.1 отвергает их как Unknown ordered aggregate quantile_cont. Ложных отказов среди этих9выражений не подтверждено. Для разрешённого quantile_cont нужен синтаксис quantile_cont(column,q), проверенный отдельно. Некоторые выражения дополнительно вкладывали агрегат в другой агрегат/FILTER. См.protocol_limit_probes.json. Диагностика должна объяснять диалект, а не только запрет GROUP. Исходники/метрики не исправлялись задним числом.', '',
              'Выбранные B/C имеют только customer_id history-агрегаты: отсутствуют товарные/customer×товар-category исторические сигналы. Статические raw_i_* остаются; LightGBM может взаимодействовать с ними. Причина низкого MAP этим не доказана.',
              'A содержит customer×department/product_type статистики, но хуже по test; само наличие группировок тоже не гарантирует качества.',
              'Следующий проверяемый шаг: исправить диагностику формы derived и явно описать поддерживаемый синтаксис quantile, затем отдельно проверять разнообразие товарных/парных статистик. Текущие H003-артефакты сохранить.', '',
              '## Ограничения вывода', '',
              'Один seed,250testпользователей; paired bootstrap10k в paired_test_bootstrap.csv — исследовательский интервал, не неопределённость между запусками.',
              'Test уже просматривался до H003: это повторная оценка. Бюджет20наборов одинаковый; одинаковый seed не создаёт общую траекторию после изменения prompt/feedback.',
              'H003 подтверждает снижение числа вызовов вC в этом запуске; улучшение MAP не получено. Отдельный причинный/устойчивый эффект требует повторений.', '',
              '![Качество](comparison.png)', '', '![Эффективность](generation_efficiency.png)', '',
              '![Поиск](search_progress.png)', '', '![AP](test_histograms.png)', '', '![Все методы](comparison_all_methods.png)']
    (OUT/'report.md').write_text('\n'.join(lines),encoding='utf-8')
    print(frame[['model','val_map_percent','test_map_percent']].to_string(index=False))
    print(pd.DataFrame(bootstrap).to_string(index=False))


def diagnostic_categories(diagnostics, failures):
    tags = defaultdict(set)
    for e in diagnostics:
        reason = e['reason'].lower()
        key = (e['arm'],e['call'])
        checks = {'window_OVER': "forbidden token 'over'" in reason,
                  'grouping_keys': 'grouping keys' in reason,
                  'raw_in_history': 'raw_* fields absent' in reason,
                  'history_in_derived': 'history fields absent' in reason,
                  'unknown_feature_reference': 'referenced column "f_' in reason,
                  'sql_syntax': 'parser error' in reason,
                  'strings_or_qualified_names': 'only numeric sql' in reason,
                  'unsupported_function_or_GROUP': 'outside allowlist' in reason,
                  'nested_aggregates': 'aggregate function calls cannot be nested' in reason,
                  'SQL_statements': "forbidden token 'select'" in reason or "forbidden token 'from'" in reason,
                  'feature_schema': 'name' in reason or 'maximum24' in reason}
        tags[key].update(n for n,yes in checks.items() if yes)
    for e in failures:
        if e['stage']=='preflight': tags[(e['arm'],e['call'])].add('derived_row_shape_escaped_diagnostics')
        if e['error'].startswith("Expecting ',' delimiter"): tags[(e['arm'],e['call'])].add('invalid_JSON')
    counts=Counter((arm,tag) for (arm,call),values in tags.items() for tag in values)
    pd.DataFrame([dict(arm=arm,category=tag,rejected_responses=count) for (arm,tag),count in sorted(counts.items())]).to_csv(OUT/'failure_categories.csv',index=False)


def binder_probes(diagnostics,audit):
    columns=['customer_id','article_id','price','days_ago','sales_channel_id','customer_age',
             'product_code','product_type_no','graphical_appearance_no','colour_group_code',
             'perceived_colour_value_id','perceived_colour_master_id','department_no','index_group_no','section_no','garment_group_no']
    con=duckdb.connect(config={'enable_external_access':'false','threads':'1','memory_limit':'128MB'})
    con.execute('CREATE TABLE history ('+','.join(n+' DOUBLE' for n in columns)+')')
    con.execute('EXPLAIN SELECT customer_id,quantile_cont(price,0.5) AS f_probe FROM history GROUP BY customer_id')
    probes=[]
    for e in diagnostics:
        if 'outside allowlist' not in e['reason'].lower() or 'group' not in e['reason'].lower(): continue
        # Only EXPLAIN of these inspected numeric expressions on an empty schema.
        assert ';' not in e['sql'] and not re.search(r'\b(select|from|read_|attach|copy)\b',e['sql'],re.I)
        result=dict(arm=e['arm'],call=e['call'],name=e['name'],sql=e['sql'])
        try:
            con.execute('EXPLAIN SELECT customer_id,'+e['sql']+' AS f_probe FROM history GROUP BY customer_id')
            result['empty_schema_bind_passed']=True
        except duckdb.Error as error:
            result.update(empty_schema_bind_passed=False,error=str(error).splitlines()[0])
        probes.append(result)
    con.close()
    (OUT/'protocol_limit_probes.json').write_text(json.dumps(probes,ensure_ascii=False,indent=2))
    assert len(probes)==9 and not any(p['empty_schema_bind_passed'] for p in probes)
    return probes


if __name__=='__main__': main()
