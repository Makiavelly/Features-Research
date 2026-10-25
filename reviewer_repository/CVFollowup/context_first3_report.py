"""Build the validation-only report after all nine ablation fits finish."""
import json
from pathlib import Path
import shutil
import numpy as np
import context_first3 as base
from common import ROOT, read, write, sha, record


def main():
    for f in range(3):
        for arm in ['categorical','fanout64','gate']:
            assert (base.DEST/f'fold_{f}'/arm/'result.json').exists(),(f,arm)
    base.summarize()
    result=read(base.REP/'summary.json')
    baseline=np.concatenate([np.load(base.DEST/f'fold_{f}/diagnostic/32_16_original_ap.npy') for f in range(3)])
    values=[np.load(base.DEST/f'fold_{f}/gate/val_ap.npy') for f in range(3)]
    delta=np.concatenate(values)-baseline
    customers=np.concatenate([np.load(base.DEST/f'fold_{f}/diagnostic/val_customer_ids.npy') for f in range(3)])
    unique,inverse=np.unique(customers,return_inverse=True)
    cluster_sum=np.bincount(inverse,weights=delta)
    cluster_n=np.bincount(inverse)
    rng=np.random.default_rng(42)
    boot=[]
    for _ in range(5000):
        ix=rng.integers(0,len(unique),len(unique))
        boot.append(cluster_sum[ix].sum()/cluster_n[ix].sum())
    result['variants']['gate_refit']=dict(fold_map=[float(v.mean()) for v in values],
        pooled_map=float(np.concatenate(values).mean()),delta_map=float(delta.mean()),
        delta_customer_bootstrap95=list(map(float,np.quantile(boot,[.025,.975]))))
    ceilings=read(base.REP/'all_history_coverage.json')
    result['all_history_coverage']=ceilings
    diagnostics=[read(base.DEST/f'fold_{f}/diagnostic/diagnostics.json') for f in range(3)]
    fits=[read(base.DEST/f'fold_{f}'/arm/'result.json') for f in range(3) for arm in ['categorical','fanout64','gate']]
    result['refits']=fits
    result['baseline_replay']=[d['replay'] for d in diagnostics]
    for f in range(3):
        original=base.OUT/f'fold_{f}/gnn_timefix_refit/contextgnn/best.pt'
        assert sha(original)==diagnostics[f]['checkpoint_sha256']
        scores=np.load(original.parent/'val_scores.npy',mmap_mode='r')
        tolerance=32*np.finfo(np.float32).eps*max(1.,float(np.abs(scores).max()))
        assert diagnostics[f]['replay']['max_abs_score_difference']<=tolerance
        assert diagnostics[f]['replay']['all_user_ap_identical']
    result['original_checkpoint_hashes_unchanged']=True
    # The inherited setup writes its auto proposal before the explicit overrides.
    # Preserve that proposal under its accurate name and export actual types.
    for f in range(3):
        folder=base.DEST/f'fold_{f}/categorical'
        proposal=folder/'stype_schema.json'
        preserved=folder/'stype_auto_proposal.json'
        if not preserved.exists():
            shutil.copyfile(proposal,preserved)
        fitted=read(folder/'result.json')['materialized_schema']
        actual={table:{column:kind.split('.')[-1] for kind,columns in kinds.items() for column in columns}
                for table,kinds in fitted.items()}
        write(folder/'effective_stype_schema.json',actual)
        assert all(actual['article'][c]=='categorical' for c in base.CODE_COLUMNS)
    write(base.REP/'summary.json',result)
    lines=['# Первые три проверки ContextGNN', '',
        '2026-10-18. Только исходная search-validation: по 256 наблюдений на фолд, всего 768. '
        'Test не оценивался. Это разведочные результаты на выборке выбора эпохи, '
        'не независимое подтверждение улучшения и не новые test-метрики.', '',
        '## Validation MAP@12, %', '',
        '| Вариант | Fold0 | Fold1 | Fold2 | Pooled | Разница с исходным, п.п. | Парный 95% интервал разницы, п.п. |',
        '|---|---:|---:|---:|---:|---:|---:|']
    names={'original':'Исходный ContextGNN','fanout64_frozen':'Fanout 64/32, прежние веса',
        'fanout64_refit':'Fanout 64/32, новое обучение','categorical_refit':'8 кодов → категории, новое обучение',
        'global':'Только глобальная ветка, прежние веса','blend25':'Вес локальной ветки 0,25, прежние веса',
        'blend50':'Вес локальной ветки 0,50, прежние веса','blend75':'Вес локальной ветки 0,75, прежние веса',
        'gate_refit':'Обучаемое смешивание, новое обучение'}
    for key in ['original','fanout64_frozen','fanout64_refit','categorical_refit','global','blend25','blend50','blend75','gate_refit']:
        v=result['variants'][key]
        lo,hi=v['delta_customer_bootstrap95']
        lines.append('| '+names[key]+' | '+' | '.join(f'{100*x:.4f}' for x in v['fold_map'])+
            f" | {100*v['pooled_map']:.4f} | {100*v['delta_map']:+.4f} | [{100*lo:+.4f}; {100*hi:+.4f}] |")
    lines+=['','Изолированные изменения не объединялись: сочетание категориальных кодов '
        'и широкого подграфа этим экспериментом не проверено. Для каждого нового варианта '
        'выбиралась лучшая эпоха по той же validation, поэтому положительная разница '
        'нуждается в независимом подтверждении. Это один seed.', '']
    lines+=['','Интервалы: 5000 парных bootstrap по покупателю с сохранением его наблюдений '
        'между фолдами. Условны на этих моделях и validation; не учитывают повторные '
        'обучения, новые недели и оптимизм выбора лучшей эпохи; без поправки на множество сравнений.',
        '', '## 1. Покрытие подграфа', '',
        'Fanout задаёт число выбираемых соседей на узел и тип связи на каждом шаге. '
        'Удвоение лимитов расширяет историю, но оставляет прежними два шага обхода.', '',
        '| Фолд | Train 32/16 | Train 64/32 | Val 32/16 | Val 64/32 | Val: вся своя прошлая история |',
        '|---|---:|---:|---:|---:|---:|']
    for f,d in enumerate(diagnostics):
        a,b=d['fanouts']['32_16']['coverage'],d['fanouts']['64_32']['coverage']
        nums=[a['train']['covered_fraction_in_catalog'],b['train']['covered_fraction_in_catalog'],
              a['val']['covered_fraction_in_catalog'],b['val']['covered_fraction_in_catalog'],ceilings[str(f)]['val']['fraction_in_catalog']]
        lines.append(f'| {f} | '+' | '.join(f'{100*x:.2f}%' for x in nums)+' |')
    lines+=['','Знаменатель покрытия — число уникальных положительных товаров внутри каталога. '
        'Дополнительно в JSON сохранён знаменатель всех целей. Вся история ограничена cutoff '
        'каждого наблюдения. Покрытие измерено на всех 10923/9583/8548 train-строках.', '',
        'На двух шагах товарные узлы приходят через собственные прошлые транзакции покупателя. '
        'Поэтому увеличение числа соседей главным образом возвращает более старые покупки; '
        'оно не расширяет радиус графа для поиска новых товаров через других покупателей.', '',
        '## 2. Типы признаков', '',
        'Проверены фактические TensorFrame после удаления первичных и внешних ключей. '
        'В отдельном обучении восемь числовых кодов стали categorical; остальная схема сохранена:', '',
        ', '.join('`'+x+'`' for x in base.CODE_COLUMNS)+'.', '',
        'Это совместная абляция восьми полей. Она не определяет вклад каждого отдельного поля. '
        'Использован отдельный кэш, старые веса и их схема не менялись.', '',
        '## 3. Локальная и глобальная ветки', '',
        '| Фолд | Доля локальных товаров в top12 | Правильных товаров добавлено локальными заменами | Правильных глобальных товаров потеряно |',
        '|---|---:|---:|---:|']
    for f,d in enumerate(diagnostics):
        b=d['fanouts']['32_16']['branches']
        lines.append(f"| {f} | {100*b['local_top12_fraction']:.2f}% | {b['gained_hits']} | {b['lost_global_hits']} |")
    lines+=['','Вес локальной ветки у обучаемой смеси на validation:', '',
        '| Фолд | Минимум alpha | Среднее alpha | Максимум alpha |',
        '|---|---:|---:|---:|']
    for f in range(3):
        gate=read(base.DEST/f'fold_{f}/gate/result.json')['validation_gate']
        lines.append(f"| {f} | {gate['min']:.6f} | {gate['mean']:.6f} | {gate['max']:.6f} |")
    lines+=['','Глобальная ветка оценена до локальной замены, но с исходным графовым '
        'представлением пользователя; это не отдельно обученная двухбашенная модель. '
        'Фиксированные смеси — вмешательства в готовую модель. Обучаемая смесь обучена с нуля: '
        '`alpha = sigmoid(w·projected_user + b)`, исходно alpha=0,9; '
        'в локальных позициях `(1-alpha)*global + alpha*local`, вне них прежний global. '
        'Отдельного обучения с фиксированным alpha=0,9 здесь нет, поэтому эффект '
        'персонализации коэффициента не отделён от эффекта изменения масштаба веток.', '',
        '## Обучение и проверки', '',
        'Девять новых fit: три изменения × три фолда. Для каждого прежние seed42, '
        'Adam lr=0,001, loss, batch128, максимум10 эпох, patience3 и выбор по validation. '
        'Для категорий и смеси fanout32/16; для широкого подграфа64/32 и исходные признаки.', '',
        'Проверены cutoff в Unix-секундах и отсутствие будущих временных узлов. '
        'Исходные logits восстановлены из веток точно, baseline replay воспроизвёл AP '
        'каждого пользователя. MAP всех вариантов проверен независимым расчётом AP. '
        'Новые веса перезагружены, повторный AP совпал точно; численные скоры проверены '
        'с ранее документированным FP32-допуском. Исходные checkpoint hashes не изменились.', '',
        'Артефакты: `summary.json`, `diagnostics.json`, `all_history_coverage.json`, '
        '`gate_protocol.json`; полные истории, веса, предсказания и AP — '
        '`CVFollowup/results/v1/context_first3_v1/`.', '']
    (base.REP/'report_ru.md').write_text('\n'.join(lines),encoding='utf-8')
    manifest={}
    for filename in ['context_first3.py','context_first3_gate.py','context_first3_history_ceiling.py','context_first3_report.py','CONTEXT_FIRST3_PROTOCOL.md']:
        path=ROOT/'CVFollowup'/filename
        manifest[str(path.relative_to(ROOT))]=sha(path)
        shutil.copyfile(path,base.REP/filename)
    write(base.REP/'source_manifest.json',manifest)
    record('context_first3_complete','First three ContextGNN checks completed on validation only: subgraph coverage and all-history ceiling, nine isolated ablation fits, branch diagnostics, independent AP and checkpoint reload checks. No test evaluation; original checkpoints unchanged.',base.RUN,status='complete_validation_diagnostics',artifacts=str((base.REP/'report_ru.md').relative_to(ROOT)))
    print('REPORT',base.REP/'report_ru.md',flush=True)


if __name__=='__main__':
    main()
