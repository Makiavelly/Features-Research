"""Search/boosting curves and verified per-user comparison artifacts for H002."""
import json
from pathlib import Path
from h002_common import ROOT, OUT, OLD, REPORT, CONFIG
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from evaluate import atomic_json


def save(fig, name):
    REPORT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(REPORT / name, dpi=150, bbox_inches='tight')
    plt.close(fig)


def search_plots(state):
    trials = state['trials']
    valid = [t for t in trials if t['status']=='valid']
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    if valid:
        x = [t['call'] for t in valid]
        y = 100*np.array([t['score'] for t in valid])
        axes[0].scatter(x, y, label='Search MAP')
        axes[0].step(x, np.maximum.accumulate(y), where='post', label='Best so far')
        axes[0].legend()
        axes[1].plot(np.arange(1,len(valid)+1), np.maximum.accumulate(y), marker='.')
    axes[0].set(xlabel='LLM requests (repairs included)', ylabel='Search MAP@12 (%)')
    axes[1].set(xlabel='Distinct evaluated feature sets', ylabel='Best search MAP@12 (%)')
    fig.suptitle('H002: fixed 256 validation users, shared ID-GNN pools; not test')
    save(fig, 'search_progress.png')
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    labels = ['valid','rejected','duplicate']
    axes[0].bar(labels, [sum(t['status']==s for t in trials) for s in labels])
    axes[0].set(ylabel='Requests', title='Outcome of each LLM request')
    if valid:
        axes[1].hist(100*np.array([t['score'] for t in valid]), bins=min(10, len(valid)), edgecolor='white')
    axes[1].set(xlabel='Search MAP@12 (%)', ylabel='Feature sets', title='Measured quality distribution')
    save(fig, 'search_histograms.png')
    fig, ax = plt.subplots(figsize=(9,4))
    for t in valid:
        p = Path(t['directory']) / 'learning_curve.json'
        if p.exists():
            values = json.loads(p.read_text())['history']['train']['binary_logloss']
            ax.plot(np.arange(1,len(values)+1), values, alpha=.65, label=str(t['call']))
    ax.set(xlabel='Boosting round', ylabel='Train binary logloss', title='LightGBM training curves (not selection criterion)')
    if valid:
        ax.legend(title='LLM request', ncol=5, fontsize=7)
    save(fig, 'lightgbm_learning_curves.png')
    (REPORT / 'progress.md').write_text((OUT / 'progress.md').read_text() +
        '\n![Search](search_progress.png)\n![Histograms](search_histograms.png)\n![Training](lightgbm_learning_curves.png)\n', encoding='utf-8')


def final_report(final, check, trials, selected):
    assert check['passed']
    from relbench import load_dataset
    task = load_dataset(ROOT / 'data/rel-hm').load_task('user-item-purchase')
    table = task.get_table('test', mask_input_cols=False).df
    manual = json.loads((ROOT/'baseline/results/manual_v1/lightgbm/seed_42/metrics.json').read_text())
    idgnn = json.loads((ROOT/'RelBenchGNN/results/seed_42/metrics.json').read_text())
    old = json.loads((OLD/'shared_idgnn/metrics.json').read_text())
    rows = [('ID-GNN', idgnn['val_metrics']['map'], idgnn['test_metrics']['map']),
            ('Manual LightGBM', manual['val_metrics']['map'], manual['test_metrics']['map']),
            ('LLM-FE v2', old['val']['metrics']['map'], old['test']['metrics']['map']),
            ('LLM-FE H002', final['val_metrics']['map'], final['test_metrics']['map'])]
    frame = pd.DataFrame(rows, columns=['model','val_map','test_map'])
    frame.to_csv(REPORT/'comparison.csv', index=False)
    fig, ax = plt.subplots(figsize=(9,4))
    for i, split in enumerate(['val','test']):
        ax.barh(np.arange(4)+(i-.5)*.32,100*frame[split+'_map'], height=.32, label=split)
    ax.set_yticks(np.arange(4),frame.model)
    ax.set_xlabel('MAP@12 (%) — identical ID-GNN candidate pools')
    ax.legend()
    save(fig,'comparison.png')
    files = [ROOT/'RelBenchGNN/results/seed_42/test_predictions.npy',
             ROOT/'baseline/results/manual_v1/lightgbm/seed_42/test_predictions.npy',
             OLD/'shared_idgnn/shared_test_predictions.npy', Path(selected['directory'])/'shared_test_predictions.npy']
    aps = {}
    for (name,_,expected), file in zip(rows,files):
        pred = np.load(file)
        hits = np.array([np.isin(p,t) for p,t in zip(pred,table.article_id)])
        ap = (hits.cumsum(axis=1)/np.arange(1,13)*hits).sum(axis=1)/np.minimum(12,table.article_id.map(len).values)
        assert abs(ap.mean()-expected)<1e-12
        aps[name] = ap
    pd.DataFrame({'customer_id':table.customer_id.values, **aps}).to_csv(REPORT/'test_user_ap.csv',index=False)
    fig, axes = plt.subplots(1,2,figsize=(12,4.5))
    axes[0].barh(list(aps),[100*np.mean(a==0) for a in aps.values()])
    axes[0].set(xlabel='Test users without hits (%)', xlim=(0,100))
    for name,a in aps.items():
        axes[1].hist(100*a[a>0],bins=np.linspace(0,100,21),histtype='step',label=name)
    axes[1].set(xlabel='User AP@12 (%) among positive AP',ylabel='Users',yscale='log')
    axes[1].legend(fontsize=8)
    save(fig,'ap_histograms.png')
    delta = aps['LLM-FE H002']-aps['LLM-FE v2']
    fig,axes = plt.subplots(1,2,figsize=(11,4))
    axes[0].bar(['H002 better','Equal','v2 better'],[(delta>0).sum(),(delta==0).sum(),(delta<0).sum()])
    if np.any(delta):
        axes[1].hist(100*delta[delta!=0], bins=40)
        axes[1].set_yscale('log')
    axes[1].set(xlabel='H002 minus v2 user AP (percentage points)',ylabel='Users (ties excluded)')
    save(fig,'paired_comparison.png')
    valid = [t for t in trials if t['status']=='valid']
    summary = {'calls':len(trials),'repairs':sum(t['repair']>0 for t in trials),
               'evaluated_distinct':len(valid),'target_met':len(valid)==20,
               'tokens':sum(t.get('prompt_tokens',0)+t.get('generated_tokens',0) for t in trials),
               'llm_seconds':sum(t.get('llm_seconds',0) for t in trials)}
    oldstate=json.loads((OLD/'search_state.json').read_text())
    fig,ax=plt.subplots(figsize=(8,4))
    ax.bar(['v2 requests','v2 measured','H002 requests','H002 distinct measured'],
           [len(oldstate['trials']),sum(t['status']=='valid' for t in oldstate['trials']),len(trials),len(valid)])
    ax.set_ylabel('Count')
    save(fig,'budget_comparison.png')
    lines=['# H002: repair loop and separate successful-set budget','',
           'Проверенная итоговая оценка на общих кандидатах ID-GNN. Один seed42.', '',
           '| Модель | Validation MAP, % | Test MAP, % |','|---|---:|---:|']
    lines += [f'| {name} | {100*v:.5f} | {100*t:.5f} |' for name,v,t in rows]
    lines += ['',f"Различных оценённых наборов: {len(valid)}/20; запросов: {len(trials)}/100; исправлений: {summary['repairs']}.",
              'Независимый полный повтор val/test из сохранённой модели на 2 потоках воспроизвёл top12 и MAP.',
              'Поиск256 и confirmation1024 используют непересекающиеся validation строки и сохранённые пулы ID-GNN.',
              'Test использован только после фиксации выбранной программы. Старый полный каталог остаётся приостановленным.',
              'H002 проверяет пакет изменений: бюджет, исправления LLM, уточнение prompt, исправление валидатора и меньший пул поиска.',
              'Причину изменения качества нельзя приписывать только исправлениям: старый search использовал весь каталог.',
              'Контроль v2 уже оценён на test до планирования H002: это следующий исследовательский эксперимент, не нетронутый test holdout.',
              'Те же803377 train пар; LightGBM150 rounds31 leaves, все seeds42; обучение8 потоков вместо2.',
              'Изменения только программ признаков делает LLM; ручные исторические признаки не добавлялись.',
              '',f"Выбранная программа: `{selected['directory']}/program.json`.",
              '', '![MAP](comparison.png)','![AP](ap_histograms.png)','![Paired](paired_comparison.png)',
              '![Budget](budget_comparison.png)','![Search](search_progress.png)',
              '![Search histograms](search_histograms.png)','![Training](lightgbm_learning_curves.png)']
    (REPORT/'report.md').write_text('\n'.join(lines),encoding='utf-8')
    atomic_json(REPORT/'report.json',{'final':True,'config':CONFIG,'summary':summary,'metrics':final,'verification':check,'selected':selected})
