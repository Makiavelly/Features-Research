"""Record preparation only; CPU SQL smoke is not an actual Qwen experiment."""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record


def main():
    folder=ROOT/'reports/kaggle_llmfe_validation/full_sql_small_v1'
    verification=json.loads((folder/'verification.json').read_text())
    budget=json.loads((folder/'context_budget.json').read_text())
    assert verification['status']=='passed' and max(budget['counts'].values())<=6144
    message=('По поручению пользователя подготовлен отдельный Kaggle T4 ноутбук Qwen7B full SQL: '
             'обычные SELECT/WITH без JSON,host проверяет и присоединяет числовые таблицы признаков. '
             'Те же72813пары/LightGBM150/31/4threads/3популяции/20успехов/300calls/3repair. '
             'CPU smoke с заданными SQL ответами прошёл,rawконтроль byte-identical, '
             'CTE/quantile/window/pandas/future exclusion/ключи/routing/resume/replay/ZIP проверены. '
             'Реальной LLM-генерации нет; GPU запустит пользователь.')
    record('full_sql_kaggle_notebook_prepared',message,
           notebook='LLMFeatures/kaggle/hm_small_qwen7b_full_sql_kaggle_t4.ipynb',
           protocol='hm_small_qwen7b_full_sql_v1',hypothesis='H004',
           verification='reports/kaggle_llmfe_validation/full_sql_small_v1/verification.json',
           context_counts=budget['counts'],actual_llm_experiment_started=False)
    path=ROOT/'CONTEXT.md'
    text=path.read_text(encoding='utf-8-sig')
    heading='## H004: подготовлен полный SQL-интерфейс Qwen7B (2026-10-17)'
    if heading not in text:
        split=text.index('\n')+1
        entry='\n'+heading+'\n\n'+message+'\n\n'
        entry+=('Ноутбук LLMFeatures/kaggle/hm_small_qwen7b_full_sql_kaggle_t4.ipynb, '
                'Input прежний hm_small_sql_compare_v1.zip. До6SELECT/36числовыхвыходов,'
                'CTE/joins/windows;политикаduplicate/unchangedкакH003C,ноASTдедупиной.'
                'Физически past-onlyhistory в отдельной DuckDB,нетtx/целей/кандидатов/файлов.'
                'Final joins/raw encoding прежние,worker.py byte-identical. '
                'SQLпрограммысохраняютсявprogram.sql,внутреннийprogram.jsonсоздаётhost.'
                'Модель pinned Qwen2.5-Coder-7B-Instruct NF4/FP16/T4/seed42;'
                'input6144/output2048,search128/confirm88/heldout88,val304/test250/catalog5000.'
                'Testранее просмотрен;повторнаяоценка,никакогоотборапоtest. '
                'Изменениепространствапрограмм/лимита36вместо24+12/дедупаобъявлено. '
                'Старые ноутбуки/результатынеизменены;оценокреальнойQwenfullSQLещёнет.\n\n')
        path.write_text(text[:split]+entry+text[split:],encoding='utf-8')
    path=ROOT/'HYPOTHESES.md'
    text=path.read_text(encoding='utf-8')
    heading='## H004 — Qwen7B пишет полные SQL-запросы вместо JSON DSL'
    if heading not in text:
        split=text.index('## H003')
        section=heading+'''\n
Дата2026-10-17. Статус: **подготовлен Kaggle-ноутбук; реальная Qwen ещё не запущена**.
Пользователь поручил проверить обычные SQL SELECT/WITH вместо aggregates/derived JSON.
Гипотеза: знакомый SQL уменьшит ошибки интерфейса и позволит находить полезные признаки;
эффект на долю валидных наборов и MAP измерять отдельно, улучшение не гарантировано.
Ноутбук LLMFeatures/kaggle/hm_small_qwen7b_full_sql_kaggle_t4.ipynb,
protocol hm_small_qwen7b_full_sql_v1, отдельный fingerprint. Qwen7B/pinned revision/NF4/
FP16/T4/temp0.8/input6144/output2048/seed42;72813пары/LightGBM150/31/4threads,
20измеренных/300обращений/3repair/3популяции/одинлучшийнабор. Input прежниймалыйZIP.
До6независимых SELECT и36числовыхвыходов; CTE,aliases,joins/windows разрешены
внутри history-запросов. Отдельная DuckDB получает толькофизически прошлуюhistory;
host владеет конечными joins/raw15/кандидатами/целями. Проверяются schema/уникальные
ключи/порядок/блоки;60секнаquery,oversize>250000строк отклоняется,неусекаетсявуспех.
Worker обучения/оценки прежний, rawконтроль CPU byte-identical прежнему.
ДедупASTконсервативный,переименованиеf_*нормализуется,CTE/алгебраневсе. Политика
duplicate/unchanged какH003C. Интерфейс/пространствоSQL/лимиты36вместо24+12/
критерийдубликатов меняются: это новая адаптация, не изолированный тест одного промпта.
Search128/top3+raw/confirm88;heldout88,val304/test250/all5000,выбордоtest.
Testуже просмотрен;повторнаядиагностика,неподбиратьпромптыпоtest. Контроли — старые
Qwen7B иH003C;отчётыподключатьвInputненужно,сопоставитьпозжелокально.
Сохранять SQL/ответы/ошибки/популяции/repair/дубликаты,время/токены/числовалидных,
learningcurves/MAP/предсказания/frozenreplays/гистограммы/ZIP. CPU smoke заданнымиSQL
ответами отдельно отбудущегореальногоопыта;подробности full_sql_small/README.md.

'''
        path.write_text(text[:split]+section+text[split:],encoding='utf-8')


if __name__=='__main__':main()
