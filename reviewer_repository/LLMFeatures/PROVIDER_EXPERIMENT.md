# GPT-6.1 Sol через Tooken Club

Реальный эксперимент H005 по поручению пользователя. API base URL подтверждён
пользователем: `https://tooken.club/v1`. Requested/returned model ID `gpt-6.1-sol`.
Ключ читается из `ACCESS_TOKEN` в корневом `.env`, только в HTTP Authorization.
В config/requests/response-архивы ключ не сохраняется. `.env` игнорируется Git.

Основной runner: `LLMFeatures/run_provider_small.py` под WSL Python проекта,
с изолированными `audit_deps` и `full_sql_delivery_v1/check_deps` на PYTHONPATH.
Локальный GPU/загрузка весов не нужны. API adapter `provider_api.py` использует
стандартный HTTPS Chat Completions. Платных скрытых повторов нет: каждыйPOST
сохраняется в api_attempts до отправки; максимум300попыток после возобновления.
Ошибки API останавливают поиск, а не превращаются в300пустых исправлений SQL.

Та же малая выборка H&M из ContextGNN:72813пар/4804user-times/8cutoff,
raw15/LightGBM150rounds/31leaves/4CPUthreads. Search128/top3+raw/confirm88,
heldout88/val304/test250/catalog5000. Схема/prompt/SQL host из последнего
Qwen7B full-SQL ноутбука, до6SELECT/36числовыхвыходов, CTE/joins/windows.
20разных обученных/измеренных наборов,до3repair,3популяции,одинлучшийсвоейпопуляции.
API запрашивает temperature0.8/top_p1/seed42+call−1/max_tokens2048/
reasoning_effortlow. Семплирование/детерминизм/веса/железо провайдера не контролируются.

В SQL-соединение физически попадает только прошлая history; в запросах к API —
schema,3строки rawизраннеготренировочногосреза,своипрограммы/ошибки/searchfitness.
Train/test цели вprompt не попадают. Подбор по test не выполняется. Test был
просмотрен ранее: это повторная оценка, а не новый закрытый test.

Реальные совпадающие Qwen7B full-SQL результаты пока не предоставлены. Старые
Qwen7B/H003 использовалиJSONDSL, поэтому сравнение с ними меняет одновременно
модель и интерфейс. Время T4/API измеряется на разном железе.

Исходный run `hm_small_gpt61sol_full_sql_seed42_v1_f33bb22767c0` сохраняется.
Вcall14 выявлен ложный отказ: SQLGlot считаетAND узломFunc, старыйallowlist
не учитывал стандартные Boolean-операторы. План исправления записан до
первоначальных итоговых selection/test. Старый генерационный поток не переписывается.

`correct_provider_evaluation.py` создаёт отдельный corrected-eval run:
поддержаны AND/OR/NOT/IN/BETWEEN/IS; тот же сохранённый поток ответов повторно
проверяется, берутся первые20разных валидных программ в исходном порядке,
затемtop3+raw/confirmation. Дополнительных APIвызовов нет. Неизменные ранее
обученные программы используют свои сохранённые модели/searchpredictions,
ошибочно отклонённый набор действительно обучается/оценивается.
Исходные prompts/ошибочная feedback-цепочка остаются в истории. Это исправленный
анализ одного потока ответов, не новый независимый LLM-прогон.

Аудит: `audit_provider_small.py`, для исправленного анализа `--corrected`.
Отчёт: `report_provider_small.py`, для исправленного анализа `--corrected`.
Проверяются все20программ, данные/source/model SHA,предсказания/AP/MAP,
выбор top3+raw поconfirmation и независимыйCPU frozenreplay raw/GPT×val/test.
Старые отчёты/ноутбуки/запуски сохраняются. Денежную стоимость по usage
без тарифов/чека не вычисляем; фактические входные/выходные токены сохраняются.
