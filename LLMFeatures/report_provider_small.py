"""Compare verified provider results to earlier frozen small-v1 experiments."""
import json
import argparse
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/gpt61sol_small_v1'


def main():
    global OUT
    parser=argparse.ArgumentParser()
    parser.add_argument('--corrected',action='store_true')
    args=parser.parse_args()
    if args.corrected:OUT=ROOT/'reports/gpt61sol_small_v2'
    audit=json.loads((OUT/'audit.json').read_text())
    assert audit['status']=='passed'
    source=Path(audit['source_directory'])
    frame=pd.read_csv(OUT/'comparison.csv')
    old=pd.read_csv(ROOT/'reports/h003_small_v1/comparison_all_methods.csv')
    combined=pd.concat([old,frame[frame.model=='GPT61Sol']],ignore_index=True)
    assert combined.model.is_unique
    combined.to_csv(OUT/'comparison_all_methods.csv',index=False)
    sys.path.insert(0,str(ROOT/'LLMFeatures/kaggle'))
    from report_small_llms import DISPLAY
    labels={**DISPLAY,'h003a':'Qwen7B H003A (JSON)','h003b':'Qwen7B H003A+B (JSON)',
            'h003c':'Qwen7B H003A+B+C (JSON)','GPT61Sol':'GPT-6.1 Sol → LightGBM (полный SQL, API)'}
    indexed=combined.set_index('model')
    order=['Raw15_LightGBM','Qwen7B_LightGBM','h003c','GPT61Sol','lightgbm_manual','idgnn','contextgnn']
    fig,axes=plt.subplots(1,2,figsize=(14,6))
    for axis,split in zip(axes,['val','test']):
        values=indexed.loc[order,split+'_map_percent'].to_numpy()
        axis.barh([labels.get(n,n) for n in order],values,color=['#999999','#577590','#43aa8b','#8e44ad','#999999','#999999','#999999'])
        for y,v in enumerate(values):axis.text(v+.025,y,f'{v:.3f}%',va='center',fontsize=9)
        axis.set(title=split+(' (повторная оценка)' if split=='test' else ' (включает search/confirm)'),
                 xlabel='MAP@12 (%)',xlim=(0,max(values)*1.16))
        axis.grid(axis='x',alpha=.2)
    fig.suptitle('Small-v1: те же пользователи и каталог5000; интерфейсы генерации различаются')
    fig.tight_layout()
    fig.savefig(OUT/'comparison.png',dpi=160)
    plt.close(fig)
    sorted_frame=combined.sort_values('test_map_percent')
    fig,axes=plt.subplots(1,2,figsize=(16,12))
    for axis,split in zip(axes,['val','test']):
        values=sorted_frame[split+'_map_percent'].to_numpy()
        axis.barh([labels.get(n,n) for n in sorted_frame.model],values,
                  color=['#8e44ad' if n=='GPT61Sol' else '#bbbbbb' for n in sorted_frame.model])
        for y,v in enumerate(values):axis.text(v+.02,y,f'{v:.3f}',va='center',fontsize=8)
        axis.set(title=split,xlabel='MAP@12 (%)',xlim=(0,max(values)*1.13))
        axis.grid(axis='x',alpha=.2)
    fig.suptitle('Все методы на small-v1; обучение и бюджеты baseline отличаются')
    fig.tight_layout()
    fig.savefig(OUT/'comparison_all_methods.png',dpi=160)
    plt.close(fig)
    old_eff=pd.read_csv(ROOT/'reports/h003_small_v1/generation_efficiency.csv')
    stats=audit['stats']
    eff=pd.concat([old_eff,pd.DataFrame([dict(model='GPT61Sol',calls=stats['calls'],valid=20,
                       rejected=stats['statuses'].get('rejected',0),duplicate=stats['statuses'].get('duplicate',0),
                       repair_calls=stats['repairs'],generation_minutes=stats['generation_minutes'],
                       outside_corrected_pool=stats.get('outside_corrected_pool',0),
                       generated_tokens=stats['completion_tokens'],max_input_tokens=stats['max_input_tokens'])])],ignore_index=True)
    eff.to_csv(OUT/'generation_efficiency.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(12,5))
    names=['Qwen7B_control','h003c','GPT61Sol']
    display=['Qwen7B контроль (JSON,T4)','Qwen7B H003C (JSON,T4)','GPT6.1 Sol (SQL,API)']
    values=eff.set_index('model').loc[names]
    bottom=np.zeros(3)
    for col,color in [('valid','#43aa8b'),('rejected','#f3722c'),('duplicate','#f9c74f'),('outside_corrected_pool','#999999')]:
        v=values[col].fillna(0).to_numpy()
        axes[0].bar(np.arange(3),v,bottom=bottom,label=col,color=color)
        bottom+=v
    axes[0].set_xticks(np.arange(3),display,rotation=15,ha='right')
    axes[0].set(ylabel='Обращения',title='Везде20 различных оценённых наборов')
    axes[0].set_ylim(0, float(bottom.max()) * 1.15)
    axes[0].legend()
    axes[1].bar(display,values.generation_minutes,color=['#577590','#43aa8b','#8e44ad'])
    axes[1].tick_params(axis='x',rotation=15)
    axes[1].set(ylabel='Минуты',title='Генерация: T4 и удалённый API, разное железо')
    fig.tight_layout()
    fig.savefig(OUT/'generation_efficiency.png',dpi=160)
    plt.close(fig)
    quality=json.loads((OUT/'quality.json').read_text())
    historical=json.loads((ROOT/'reports/hm_small_llms_v1/quality.json').read_text())
    h003=json.loads((ROOT/'reports/h003_small_v1/quality.json').read_text())
    quality.update(Qwen7B_control=historical['Qwen7B_LightGBM'],H003C=h003['h003c'])
    diffs=[]
    for name in ['Raw15','Qwen7B_control','H003C']:
        diff=np.array(quality['GPT61Sol']['test'])-np.array(quality[name]['test'])
        rng=np.random.default_rng(42)
        boot=diff[rng.integers(len(diff),size=(10000,len(diff)))].mean(1)*100
        diffs.append(dict(comparison='GPT61Sol minus '+name,difference_pp=diff.mean()*100,
                          ci95_low_pp=np.quantile(boot,.025),ci95_high_pp=np.quantile(boot,.975),
                          better=int((diff>0).sum()),tied=int((diff==0).sum()),worse=int((diff<0).sum())))
    pd.DataFrame(diffs).to_csv(OUT/'paired_test_bootstrap.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for name in ['Raw15','Qwen7B_control','H003C','GPT61Sol']:
        ap=np.array(quality[name]['test'])*100
        axes[0].hist(ap[ap>0],bins=np.linspace(0,100,21),histtype='step',label=name)
        axes[1].bar(name,100*np.mean(ap==0))
    axes[0].set(xlabel='Test AP@12 (%) среди AP>0',ylabel='Пользователи')
    axes[0].legend(fontsize=8)
    axes[1].set(ylabel='Пользователи с AP=0 (%)',ylim=(0,100))
    fig.tight_layout()
    fig.savefig(OUT/'test_histograms.png',dpi=160)
    plt.close(fig)
    trials=json.loads((source/'gpt61sol_full_sql/search_state.json').read_text())['trials']
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    states={'Qwen7B control':json.loads((ROOT/'reports/hm_small_llms_v1/exports/qwen_llama/qwen/search_state.json').read_text())['trials'],
            'H003C':json.loads((ROOT/'reports/h003_small_v1/states.json').read_text())['h003c'],'GPT61Sol':trials}
    for label,state in states.items():
        valid=[t for t in state if t['status']=='valid']
        values=np.maximum.accumulate([t['score']*100 for t in valid])
        axes[0].step([t['call'] for t in valid],values,where='post',label=label)
        axes[1].plot(np.arange(1,len(valid)+1),values,label=label)
    for axis in axes:axis.set(ylabel='Лучший search MAP@12 (%)');axis.legend(fontsize=8);axis.grid(alpha=.2)
    axes[0].set(xlabel='Все обращения',title='Search128, весь каталог5000')
    axes[1].set(xlabel='Различные оценённые наборы',title='Одинаковый бюджет20 наборов')
    fig.tight_layout()
    fig.savefig(OUT/'search_progress.png',dpi=160)
    plt.close(fig)
    gpt=frame.set_index('model').loc['GPT61Sol']
    summary=dict(run_id=audit['run_id'],audit_passed=True,stats=stats,comparison=combined.to_dict('records'),
                 bootstrap=diffs,test_previously_inspected=True,
                 interpretation='Different model AND full SQL interface relative to historical JSON runs; real matched Qwen full SQL results pending')
    (OUT/'report.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    lines=['# GPT-6.1 Sol через Tooken Club: small-v1 / полный SQL','',
           'Эксперимент выполнен, не smoke. Модель запрошена и возвращена API как gpt-6.1-sol.',
           'Провайдер https://tooken.club/v1; секрет читается из.env, в артефакты не сохраняется.',
           'Независимый CPU audit проверил20 различных обученных программ, метрики/прогнозы,top3+raw/confirmation и4frozen replays(raw/GPT ×val/test).',
           'Raw-control model/predictions байт-в-байт совпадают с прежним контролем.', '',
           '## Результат', '',
           f"Вызовов:{stats['calls']},успехов20,отказов{stats['statuses'].get('rejected',0)},дубликатов{stats['statuses'].get('duplicate',0)};выбранcall{stats['selected_call']} (null=raw).",
           f"Генерация:{stats['generation_minutes']:.2f}мин,APIusage input{stats['prompt_tokens']}/completion{stats['completion_tokens']}токенов.",
           f"GPT valMAP={gpt['val_map_percent']:.6f}%,heldout88={gpt['heldout_val_map_percent']:.6f}%,test={gpt['test_map_percent']:.6f}%.", '',
           '| Метод | Validation MAP,% | Heldout88 MAP,% | Test MAP,% |','|---|---:|---:|---:|']
    for name in order:
        r=indexed.loc[name]
        lines.append(f"| {labels.get(name,name)} | {r['val_map_percent']:.6f} | {r['heldout_val_map_percent']:.6f} | {r['test_map_percent']:.6f} |")
    lines+=['','## Что сравнимо','',
            'Те же72813train-пар,4804user-times/8cutoffs,LightGBM150/31/4CPUthreads/raw15,validation304/test250/все5000товаров.',
            'Search128→top3+raw→confirmation88;выбордоheldout/test. Test ранее просматривался: повторная оценка, не новый закрытый test.',
            'ПолныйSQL-интерфейс/prompt/worker/base features происходят из подготовленного Qwen7B full-SQL ноутбука. Его реальных результатов пока нет. Исправление Boolean-валидации, если применено, описано ниже.',
            'Исторические Qwen7B/H003 писали JSON DSL. Поэтому сравнение с ними меняет и модель, и интерфейс; изолировать эффект мощности модели пока нельзя.',
            'GPT API:temperature0.8,top_p1,seed42+call−1 запрошен,reasoning_effort=low,max_tokens2048. Веса/квантизация/детерминизм провайдера не контролируются; сохраняются requested/returned model IDs иusage.',
            'Лимит300 — фактическиеHTTPPOST к модели без автоматических повторов. GET/models — проверка доступа, не генерация.',
            'API и T4 используют разное железо; затраты времени нельзя приписать только модели. Денежную стоимость из usage без тарифов/чека не вычисляем.',
            'Одинseed250test. Paired-bootstrap10k исследовательский, не неопределённость между запусками. Не выбирать новый prompt по этому test.', '',
            '## Выбранный SQL', '', '```sql',audit['selected_SQL'],'```','',
            '![Сравнение](comparison.png)','', '![Эффективность](generation_efficiency.png)','',
            '![Поиск](search_progress.png)','', '![AP](test_histograms.png)','',
            '![Все методы](comparison_all_methods.png)','',
            '[Профиль модели у провайдера](https://tooken.club/models/gpt-6-1-sol).']
    if args.corrected:
        correction=json.loads((source/'correction.json').read_text())
        lines+=['','## Исправление валидатора без новых API-вызовов','',
                'SQLGlot представляет AND как Func; исходный allowlist ошибочно отклонил корректный SQL вcall14.',
                'Ошибка обнаружена и план исправления записан до итогового selection/test первоначального запуска.',
                'Исправлена только поддержка стандартных AND/OR/NOT/IN/BETWEEN/IS; отдельный source/run ID, исходный прогон сохранён.',
                'Это НЕ независимый LLM-прогон: повторно оценён тот же оплаченный поток ответов, с сохранением реальных prompts/repairhistory.',
                'Взяты первые20различных валидных программ в исходном порядке; top3+raw заново выбраны исключительно поvalidation.',
                f"Дополнительных API-вызовов0; исходных оплаченных запросов{stats['api_attempts']}; ответов вне исправленного20-наборного отбора:{stats['outside_corrected_pool']}.",
                'Повторно использованы неизменные уже обученные модели/поисковые прогнозы; ошибочно отклонённый набор обучен и оценён отдельно.',
                'Результаты/APIusage охватывают исходные оплаченные запросы, не только укороченный correctedpool.',
                'Исходные повреждённые feedback-сообщения остаются в истории; это исправленный анализ одного потока, не доказательство поведения чистого нового запуска.',
                'Correction details: '+json.dumps(correction,ensure_ascii=False)]
    (OUT/'report.md').write_text('\n'.join(lines),encoding='utf-8')
    print(frame.to_string(index=False))
    print(pd.DataFrame(diffs).to_string(index=False))


if __name__=='__main__':main()
