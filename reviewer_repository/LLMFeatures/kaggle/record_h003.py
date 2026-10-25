"""Persist verified H003 results without overwriting earlier experiments."""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'reports/h003_small_v1'
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record


def main():
    audit=json.loads((OUT/'audit.json').read_text())
    report=json.loads((OUT/'report.json').read_text())
    assert audit['status']=='passed' and report['audit_passed']
    metrics={r['model']:r for r in report['comparison']}
    efficiency={r['model']:r for r in report['efficiency']}
    for arm in ['h003a','h003b','h003c']:
        row,e=metrics[arm],efficiency[arm]
        record('h003_kaggle_arm_audited',
               f"{arm}:20измеренных/{e['calls']}вызовов;отказов{e['rejected']},дубликатов{e['duplicate']}; "
               f"val/testMAP={row['val_map_percent']:.6f}/{row['test_map_percent']:.6f}%. "
               'Верифицированы данные/исходники/selection/frozen CPU replay. Без обучения/новой генерации.',
               audit['run_id']+'_'+arm,status='complete',artifacts='reports/h003_small_v1',
               val_metrics={'map':row['val_map_percent']/100},test_metrics={'map':row['test_map_percent']/100},
               llm_calls=e['calls'],evaluated_distinct=20,selected_call=audit['arms'][arm]['selected_call'])
    message=('H003 полностью проверен: A65/36/9,B78/21/37,C51/15/16 (calls/reject/duplicate), '
             'каждый20успехов. Cпротивконтроля67calls:на23.9%меньшеобращений,44.88против46.42мингенерации. '
             'TestMAP A0.751212/B0.873593/C0.888745% противстарогоQwen7B1.107143% иraw0.959630%; '
             'качество не улучшилось. Все4модели×val/test frozenreplayсовпали. '
             'A21–23derivedагрегациипропущеныдиагностикой,остановленыpreflight. '
             '9WITHINGROUPвыраженийоказалисьневалиднымquantile_contдиалектом,ложныхотказовсрединихнет. '
             'Одинseed250test,повторнаяоценка;всеbootstrapинтервалыразницывключают0.')
    record('h003_kaggle_results_audited',message,audit['run_id'],status='complete',
           artifacts='reports/h003_small_v1',report='reports/h003_small_v1/report.md',
           test_previously_inspected=True)
    heading='## Проверенный результат H003 (2026-10-17)'
    path=ROOT/'CONTEXT.md'
    text=path.read_text(encoding='utf-8-sig')
    if heading not in text:
        split=text.index('\n')+1
        section='\n'+heading+'\n\n'+message+'\n\n'
        section+=('ИсходныйZIP hm_small_qwen7b_h003_v1_6852748fc0e4_results.zip сохранён;sha256 '
                  '3745ab14e576e7b179b764f1822014fecd29c7ec3da398ac3edae5743a46b5cf. '
                  'Независимыйаудит reports/h003_small_v1/audit.json,report.md,5PNG;'
                  'старыеотчёты/ноутбукинеизменены. ВыбранныеB/Cагрегатытолькоcustomer_id;'
                  'raw_i_*остаются,причинностьнизкогоMAPнеустановлена. '
                  'КонтекстA2787/B3148/C3579,обрезаний/переполнений0. '
                  'H003Cоперационноэкономнее,ноустойчивый/причинныйэффектнеустановлен;'
                  'H003Aнеулучшилаотказы,H003Bуменьшилаотказыноувеличиладубликаты.\n\n')
        path.write_text(text[:split]+section+text[split:],encoding='utf-8')
    path=ROOT/'HYPOTHESES.md'
    text=path.read_text(encoding='utf-8')
    text=text.replace('Статус: **Kaggle-ноутбук подготовлен; реальный запуск H003 ещё не выполнен**.',
                      'Статус: **реальный Kaggle запуск завершён и проверен 2026-10-17; C экономнее по вызовам, улучшения MAP нет**.')
    marker='### H003 — проверенный результат'
    if marker not in text:
        section=('### H003 — проверенный результат\n\n'+message+'\n\n'
                 'Подробности reports/h003_small_v1/report.md и audit.json. '
                 'Наблюдаемый эффект одного запуска не означает устойчивого превосходства. '
                 'Проверять меньшую долю ошибок и MAP отдельно.\n\n')
        text=text.replace('## H001 — Двухбашенная GNN с независимыми весами',section+'## H001 — Двухбашенная GNN с независимыми весами',1)
        path.write_text(text,encoding='utf-8')


if __name__=='__main__':main()
