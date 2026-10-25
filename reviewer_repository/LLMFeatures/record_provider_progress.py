"""Keep persistent experiment context in sync with a running remote search."""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record


def main():
    current=json.loads((ROOT/'reports/provider_small_v1/current_run.json').read_text())
    run=Path(current['directory'])
    state=json.loads((run/'gpt61sol_full_sql/search_state.json').read_text())
    message=(f"GPT-6.1-Sol API fullSQL: сейчас{state['measured']}/20оценённых,"
             f"{state['calls']}/300обращений. Тотжеsmall-v1/72813пары/LightGBM150/31/4CPU;"
             'поискнеиспользуетtest,промежуточныйsearchMAPнеитоговыйрезультат.')
    record('provider_feature_search_progress',message,current['run_id'],status='searching',
           artifacts=str(run.relative_to(ROOT)),evaluated_distinct=state['measured'],llm_calls=state['calls'])
    path=ROOT/'CONTEXT.md'
    text=path.read_text(encoding='utf-8-sig')
    heading='## H005: реальный поиск GPT-6.1 Sol через Tooken Club'
    if heading not in text:
        pos=text.index('\n')+1
        entry='\n'+heading+'\n\n'
        entry+=('Пользователь поручил провести эксперимент на более сильной модели через API, '
                'токен в.env ACCESS_TOKEN. Исправленный пользователем адрес https://tooken.club/v1 '
                '(token.club не имел DNS). /models подтвердилgpt-6.1-sol,ответывозвращаютто жеимя. '
                'Runner LLMFeatures/run_provider_small.py; APIадаптер provider_api.py; '
                'APIключ не хранится в request/config/logs. '\
                'Выбран полныйSQL как в последнем Qwen-ноутбуке,источники full_sql_small неизменены;'
                'runtimeадаптациятольконазваниямодели/ветки. '
                '20различных измеренных наборов/300фактическихPOST/до3repair/3популяции/seed42, '
                'max_tokens2048,temp.8,top_p1,reasoning_effortlow;seedпровайдерузапрошен,детерминизмнеподконтролем. '
                'Те же72813пары/LightGBM150/31/4CPU/search128/confirm88/heldout88/val304/test250/all5000. '
                'Testранее просмотрен;впровайдерпередаётсяschema/примерraw3trainingстрок/своипрограммыиsearchfitness,нецелиtest. '
                'РеальныйQwenfullSQLотчётещёнеполучен: старыеQwen7B/H003имелиJSONDSL, '
                'поэтомусравнениепокаизменяетимодель,иинтерфейс. '
                f"Run {current['run_id']}; файлы в {run.relative_to(ROOT)}. "
                'Фактическийстатуспроверятьпоsearch_state ипроцессам;необъявлятьзавершённымдо20иaudit. '
                'APIошибкиостанавливаютпоиск,анепровоцируют300пустыхповторов;попыткисчитаютсяпосохранённымapi_attempts. '
                'Независимыйаудит audit_provider_small.py,сравнение report_provider_small.py.\n\n')
        path.write_text(text[:pos]+entry+text[pos:],encoding='utf-8')
    path=ROOT/'HYPOTHESES.md'
    text=path.read_text(encoding='utf-8')
    heading='## H005 — более сильная API-модель GPT-6.1 Sol на том же small-v1'
    if heading not in text:
        pos=text.index('## H004')
        entry=heading+'\n\nСтатус: **реальный API эксперимент выполняется**.\n'
        entry+=('Пользователь выбралgpt-6.1-sol иразрешилдо300обращенийдля20валидныхрезультатов. '
                'Гипотеза: более сильная модель уменьшит ошибки программ и поможет найти признаки '
                'с лучшимMAP. Проверятьобацеляотдельно. ПолныйSQLинтерфейсH004,старыепары/деревья/'
                'валидационныеразделы/каталогсохранены;20успехов=полноеобучение+searchMAP. '
                'TookenClub https://tooken.club/v1,model_id gpt-6.1-sol. '
                'temperature.8/top_p1/seed42+call−1/max_tokens2048/reasoning_effortlow запрошены. '
                'Обращения/usage/responsemodel сохраняются,секрет не сохраняется. '
                'АвтоповторовHTTPнет;до3исправленийSQLвходятв300POST. '
                'Данные72813train/5000catalog/val304/test250;LightGBM150/31/4CPU. '
                'Search128/top3+raw/confirm88,heldout88,testпослевыбора. '
                'Testранее просмотрен. РеальногоmatchedQwenfullSQLпоканет, '
                'историческийQwenJSONсравниваетвместемодель+интерфейс. '
                'Одинseed,железо/квантизацияAPIиT4различаются;seedпровайдерможетнеобеспечивать. '
                f"Новыйrun {current['run_id']}. Сохранятьвсе20программ/ошибки/'"
                'модели/метрики/время/usage/replays/графики,старыеопытынезаменять.\n\n')
        path.write_text(text[:pos]+entry+text[pos:],encoding='utf-8')


if __name__=='__main__':main()
