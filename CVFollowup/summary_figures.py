"""Human-readable available-results summary and predeclared budget/grid figures."""
import itertools
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from common import ROOT,OUT,REPORT,read,write,sha

def main():
    dest=REPORT/'final_comparison';result=read(dest/'comparison.json')
    summary={s['method']:s for s in result['summary']};rf=read(REPORT/'recformer_pretest_freeze.json')
    folds=pd.read_csv(dest/'fold_metrics.csv')
    fig,axes=plt.subplots(2,2,figsize=(12,9))
    for mode,color in [('h008','#4c78a8'),('h009','#e45756')]:
        values=[summary[f'{mode}_{b}']['pooled_map']*100 for b in [20,30,40]]
        lower=[summary[f'{mode}_{b}']['ci95_low']*100 for b in [20,30,40]]
        upper=[summary[f'{mode}_{b}']['ci95_high']*100 for b in [20,30,40]]
        axes[0,0].errorbar([20,30,40],values,yerr=np.maximum(0,np.array([np.array(values)-lower,np.array(upper)-values])),
            color=color,marker='o',capsize=3,label=mode.upper())
        for f,ax in enumerate(axes.flat[1:]):
            ys=[summary[f'{mode}_{b}']['fold_maps'][f]*100 for b in [20,30,40]]
            ax.plot([20,30,40],ys,marker='o',color=color,label=mode.upper())
    for index,ax in enumerate(axes.flat):
        ax.set(xticks=[20,30,40],xlabel='Accepted structurally distinct programs',ylabel='Outer-test MAP@12',
            title='Pooled; paired customer-cluster 95% intervals' if index==0 else f'Fold {index-1}: outer test')
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=100,decimals=2));ax.legend();ax.grid(alpha=.2)
    fig.suptitle('API search budget: continuing the same streams from 20 to 30 to 40')
    fig.tight_layout();fig.savefig(dest/'api_budget_curves.png',dpi=170);fig.savefig(dest/'api_budget_curves.svg');plt.close(fig)
    grid=rf['validation_grid'];fig,ax=plt.subplots(figsize=(11,6))
    x=np.arange(len(grid));means=np.array([r['mean_search_map'] for r in grid])*100
    ax.bar(x,means,color=['#999999' if r['label']=='baseline' else '#4c78a8' for r in grid],alpha=.45,label='Equal-fold mean')
    for f,color in enumerate(['#4c78a8','#f58518','#54a24b']):
        ax.plot(x,[r['fold_search_maps'][f]*100 for r in grid],marker='o',color=color,label=f'Fold{f}')
    for j,m in enumerate(means):ax.text(j,m+.02,f'{m:.3f}%',ha='center',fontsize=9)
    ax.set(xticks=x,xticklabels=[r['label'] for r in grid],ylabel='Inner-validation MAP@12',title='Recformer: available settings, not outer-test performance')
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100,decimals=1));ax.legend();ax.grid(axis='y',alpha=.2)
    fig.text(.5,.01,'lr3e6_w100 unavailable; no score assigned. Kaggle lr1e5_w300 uses T4, others use local RTX3060.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.04,1,1]);fig.savefig(dest/'recformer_validation_grid.png',dpi=170);plt.close(fig)
    wanted=[('h008_40','h008_20'),('h009_40','h009_20'),('h009_40','h008_40'),
        ('recformer_tuned','recformer_baseline'),('recformer_tuned','recformer_zero'),
        ('contextgnn','idgnn'),('h008_40','manual'),('h009_40','manual'),('contextgnn','h008_40')]
    contrasts=[]
    for a,b in wanted:
        if a not in summary or b not in summary:continue
        row=next(p for p in result['paired_comparisons'] if {p['a'],p['b']}=={a,b})
        sign=1 if row['a']==a else -1
        lo,hi=(row['ci95_low'],row['ci95_high']) if sign==1 else (-row['ci95_high'],-row['ci95_low'])
        contrasts.append({'a':a,'b':b,'difference_pp':100*sign*row['difference'],
            'ci95_low_pp':100*lo,'ci95_high_pp':100*hi,'interval_excludes_zero':bool(lo>0 or hi<0),
            'fold_differences_pp':[100*(u-v) for u,v in zip(summary[a]['fold_maps'],summary[b]['fold_maps'])]})
    usage=[];selections=[];incumbent_drops=[]
    for f in range(3):
        for mode in ['h008','h009']:
            folder=OUT/f'fold_{f}'/mode;cfg=read(folder/'run_config_budget40.json')
            trials=[read(p) for p in (folder/cfg['arm']/'candidates').glob('*/trial.json')]
            responses=[read(p) for p in (folder/cfg['arm']/'candidates').glob('*/response.json')]
            assert sum(t['status']=='valid' for t in trials)==40
            usage.append({'fold':f,'mode':mode,'accepted':40,'responses':len(trials),
                'rejected':sum(t['status']=='rejected' for t in trials),'duplicates':sum(t['status']=='duplicate' for t in trials),
                'actual_POST':len(list((folder/'api_attempts').glob('attempt_*'))),
                'known_input_tokens':sum(r.get('prompt_tokens',0) for r in responses),
                'known_output_tokens':sum(r.get('generated_tokens',0) for r in responses)})
            for b in [20,30,40]:
                chosen=read(folder/f'budgets/{b}/selected.json')
                if b>20:
                    previous_budget=20 if b==30 else 30
                    previous=read(folder/f'budgets/{previous_budget}/selected.json')
                    eligible=[c['call'] for c in chosen['confirmation']]
                    if previous['call'] not in eligible:
                        incumbent_drops.append({'fold':f,'mode':mode,'previous_budget':previous_budget,'budget':b,
                            'previous_selected_call':previous['call'],'eligible_calls':eligible,
                            'previous_confirmation_map':previous['confirmation_map'],
                            'new_confirmation_map':chosen['confirmation_map']})
                winner=Path(chosen['directory'])
                assert sha(winner/'program.json')==chosen['program_sha256']
                assert sha(winner/'model.txt')==chosen['model_sha256']
                exported=dest/'selected_programs';exported.mkdir(exist_ok=True)
                (exported/f'fold_{f}_{mode}_budget{b}.py').write_text(read(winner/'program.json')['code'],encoding='utf-8')
                selections.append({'fold':f,'mode':mode,'budget':b,'selected_call':chosen['call'],
                    'confirmation_map':chosen['confirmation_map'],'model_sha256':chosen['model_sha256'],
                    'program_sha256':chosen['program_sha256'],'structurally_distinct_accepted':chosen['successful_distinct'],
                    'features':len(read(winner/'feature_schema.json')['features'])})
    pd.DataFrame(usage).to_csv(dest/'api_usage.csv',index=False)
    pd.DataFrame(selections).to_csv(dest/'api_selected_calls.csv',index=False)
    pd.DataFrame(grid).to_csv(dest/'recformer_validation_grid.csv',index=False)
    pd.DataFrame(contrasts).to_csv(dest/'key_contrasts.csv',index=False)
    write(dest/'incumbent_selection_audit.json',{'dropped_previous_confirmation_winners':incumbent_drops,
        'reason':'Top3 search shortlist is rebuilt at each budget; previous confirmation winner is not automatically retained',
        'no_reselection_performed':True})
    write(dest/'available_summary.json',{'scope':'available_three_of_four_new_Recformer_settings',
        'excluded_unavailable':rf['excluded_unavailable'],'selected_recformer':rf['selected_label'],
        'test_summary':result['summary'],'contrasts':contrasts,'api_usage':usage,'budget_selections':selections,
        'recformer_validation_grid':grid,'incumbent_drops':incumbent_drops,'notes':['one model seed, three previously inspected weeks',
            'customer bootstrap conditions on observed weeks; intervals not corrected for multiple comparisons',
            'actual_POST includes failed connections; token usage of failed requests may be unknown',
            'numeric diversity checked only for original20; accepted budget means conservative AST distinction',
            'Recformer grid incomplete; unavailable means not evaluated, not inferior']})
    lines=['# Сводка доступных результатов','',
        'Данные: 20 000 покупателей, 10 000 товаров, три временных фолда, seed 42. Итоговая метрика — full-target MAP@12 по 5519 наблюдениям «покупатель — тестовая неделя» (4548 разных покупателей). В целях сохранены покупки вне доступного каталога.',
        'Столбец общего графика — среднее AP@12 по всем 5519 наблюдениям. Это среднее результатов трёх фолдов с весами 1839, 1982 и 1698 пользователей, а не простое среднее трёх чисел. Простое среднее и отдельные фолды сохранены в report.md и summary.csv. Каждый метод ранжирует один и тот же каталог из 10 000 товаров.',
        '', '| Метод | Test MAP@12 | 95% customer-bootstrap интервал |','|---|---:|---:|']
    for s in sorted(result['summary'],key=lambda r:-r['pooled_map']):
        lines.append(f"|{s['label']}|{100*s['pooled_map']:.4f}%|[{100*s['ci95_low']:.4f}%; {100*s['ci95_high']:.4f}%]|")
    lines+=['','## API: увеличение бюджета','',
        '| Режим | 20 наборов | 30 наборов | 40 наборов |','|---|---:|---:|---:|']
    for mode in ['h008','h009']:
        lines.append('|'+mode.upper()+'|'+ '|'.join(f"{100*summary[f'{mode}_{b}']['pooled_map']:.4f}%" for b in [20,30,40])+'|')
    lines+=['','Это продолжение одних и тех же поисков, не независимые перезапуски. Все 18 отборов 20/30/40 зафиксированы до новой outer-оценки. Все выбранные API-модели прошли повторный расчёт предсказаний и независимый расчёт AP. H008 передаёт лучшие решения своей популяции, H009 дополнительно сохраняет историю её сообщений. В обоих режимах LightGBM получает только возвращённые программой признаки; 15 исходных полей автоматически не добавляются.',
        'Важная особенность: shortlist из трёх лучших search-программ пересобирается на каждом бюджете; старый победитель confirmation не сохраняется автоматически. Это может ухудшить итог даже при расширении пула программ. Аудит: incumbent_selection_audit.json. Старые результаты не переотбирались задним числом. Проверить сохранение incumbent — отдельный будущий эксперимент.', '',
        '## Парные разницы','', '| Сравнение A−B | Разница, п.п. | 95% интервал, п.п. |','|---|---:|---:|']
    for c in contrasts:lines.append(f"|{c['a']} − {c['b']}|{c['difference_pp']:+.4f}|[{c['ci95_low_pp']:+.4f}; {c['ci95_high_pp']:+.4f}]|")
    lines+=['', '## Как читать результаты', '',
        'ContextGNN и IDGNN следует оценивать по исправленным результатам. Причиной прежнего провала была ошибка единиц времени: даты validation/test в миллисекундах обрабатывались как наносекунды, и при построении графа история покупок оказывалась за пределами ошибочного cutoff. Исправление затронуло общий загрузчик двух GNN. Обе модели заново обучены и оценены; старые результаты сохранены отдельно.',
        'Увеличение бюджета API до 40 наборов не дало последовательного роста тестового MAP. Поиск, отбор на confirmation и случайность отдельных ответов нужно различать. Текущая серия — одно продолжение на каждом фолде, поэтому она не доказывает, что больший бюджет сам по себе бесполезен.',
        'Для оценки преимуществ используются парные интервалы разности из таблицы выше. Пересечение интервалов отдельных столбцов само по себе не является проверкой разницы. Интервал разности, содержащий ноль, означает, что это сравнение не подтвердило преимущество в рамках применённой проверки; это также не доказывает равенство методов.',
        'Отбор top-3 по search сам по себе допустим. Его ограничение для продолженного поиска: ранее найденный победитель confirmation может быть исключён. Например, на fold0 H008 программа №8 имела confirmation MAP 0,7180% при бюджете 20, но при 30/40 в shortlist остались №26, №36 и №14; победила №14 с 0,6966%. Сохранение прежнего победителя обеспечит неубывание лучшего известного confirmation, но не гарантирует роста test и может усиливать подгонку к confirmation.',
        'Следующий контролируемый эксперимент API: сохранять прежнего победителя confirmation вместе с новыми кандидатами из search. Новый протокол нужно зафиксировать до запуска и оценивать на новых отложенных неделях. По этой сводке нельзя задним числом выбирать программу с лучшим test.']
    lines+=['','## Recformer','',
        'Проверены 3 из 4 новых настроек на всех 3 фолдах. LR=3e-6/warmup100 не запустилась в Kaggle и отсутствует в сравнении; это не отрицательный результат качества. Существующий baseline также участвует в отборе.',
        f"Выбрана {rf['selected_label']} по среднему inner validation; веса зафиксированы до новой test-оценки. Нового обучения при составлении сводки не было.",
        '', '| Настройка | Val fold0 | Val fold1 | Val fold2 | Среднее val |','|---|---:|---:|---:|---:|']
    for row in grid:lines.append('|'+row['label']+'|'+'|'.join(f'{v*100:.4f}%' for v in [*row['fold_search_maps'],row['mean_search_map']])+'|')
    lines+=['','## Ограничения выводов','',
        '95%-интервалы: 5000 парных bootstrap по исходным покупателям, seed 42. В каждом повторе выбираются с возвращением 4548 ID покупателей; для выбранного ID берутся все его наблюдения в разных фолдах. Для каждого метода заново считается среднее AP по полученным наблюдениям, затем разница A−B на той же выборке. Границы — 2,5-й и 97,5-й процентили 5000 разностей. Это условная неопределённость для этих недель и обученных моделей, не независимые обучения и не новые временные режимы. Указанные интервалы разностей не скорректированы за множество сравнений.',
        'Сравниваемые деревья используют одинаковые train-пары. GNN/Recformer/TDM имеют собственные objectives и эффективные примеры обучения. Статические поля взяты из снимка H&M; их полная историческая доступность не установлена.',
        'В GNN исправлена подтверждённая ms/ns-ошибка. В таблице только исправленные результаты. Ограничение численного replay ContextGNN fold2 сохранено в отчёте report.md и NUMERIC_REPLAY_AMENDMENT.md.',
        'Kaggle-настройка Recformer обучена на T4, локальные — на RTX3060. AMP/численная воспроизводимость могут различаться; исходные версии, данные и параметры сохранены.',
        'Сырые проценты MAP — не доля довольных пользователей или угаданных покупок. Недоступные товары остаются в знаменателе. Полный H&M каталог здесь не оценивался.',
        'Test-недели ранее просматривались: это внутреннее сравнение. Не выбирать будущие решения только по лучшему outer-test столбцу; подтверждать на новых заранее выделенных неделях.',
        '', '## Артефакты','',
        '![Сравнение методов](comparison.png)','![API budget](api_budget_curves.png)','![Recformer validation](recformer_validation_grid.png)',
        '![По временным фолдам](fold_comparison.png)','![Гистограммы AP](ap_histograms.png)',
        '', 'Все парные интервалы: paired_differences.csv. Выбранные вызовы и число признаков: api_selected_calls.csv. Код 18 выбранных наборов: selected_programs/. Запросы и известные токены: api_usage.csv.']
    (dest/'summary_ru.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('AVAILABLE SUMMARY',dest,flush=True)

if __name__=='__main__':main()
