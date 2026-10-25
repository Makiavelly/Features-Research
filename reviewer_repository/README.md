# Материалы для проверки исследования H&M / RelBench

Пакет подготовлен по окончательному пользовательскому `report_ru.md`. Отчёт:
`report/report_ru.pdf`; неизменённый Markdown:
`reports/project_history_2026_10_25/report_ru.md`.
PDF содержит встроенные изображения и переносится одним файлом.

## Зависимости: что нужно установить

| Действие | Зависимости |
|---|---|
| Проверить сохранённые результаты | Только Python 3.11+, без сторонних библиотек и API-ключа |
| Проверить протокол и обучить CPU baseline | Ubuntu/WSL2, Python 3.11; `pip install -r requirements-cpu.txt` |
| Обучить GNN | NVIDIA GPU и совместимый драйвер; PyTorch 2.2.2+cu118, PyG 2.5.3, pytorch-frame 0.2.3; полный список — `requirements-gpu-lock.txt`, команды установки — раздел 5 |
| Запустить API-поиск признаков | CPU-зависимости, доступ к соответствующему API и **свой ключ в `.env`**; раздел «Настройка API» ниже |
| Пересобрать PDF | `pip install -r requirements-pdf.txt`, Arial в Windows или DejaVu Sans в Linux |

Основные CPU-библиотеки: NumPy 1.26.4, pandas 2.2.3, PyArrow 15.0.2,
DuckDB 1.1.3, LightGBM 4.3.0, scikit-learn 1.5.2, SciPy 1.13.1,
Matplotlib 3.9.2. Остальные зависимости и версии указаны в requirements-файлах.
Для локальных LLM дополнительно нужны веса выбранной модели и её runtime;
библиотеки исторического GPU-окружения включают Transformers 4.46.3,
tokenizers 0.20.3 и sentence-transformers 3.3.1.

## 1. Проверка без установки библиотек, данных, GPU и ключей

Из корня этой папки, Python 3.11 или новее, Windows/Linux:

```bash
python verify_saved_results.py
```

Проверяется SHA256 каждого файла поставки; из 695394 сохранённых построчных
записей заново агрегируются MAP, вклад AP и recall доступных новых товаров
21 метода на medium. Для всех методов проверяются 5519 пользователей-недель
и одинаковые 3178 наблюдений с доступными новыми целями.
Отдельная реализация AP@12 пересчитывает **16557 настоящих top-12** manual,
ID-GNN corrected и H009/20 по полным целям, включая товары вне каталога.
Каждая AP сверяется с сохранённой построчной оценкой, затем с итоговым CSV.

Это проверка сохранённых прогнозов и агрегации. Она не запускает модели,
не доказывает отсутствие утечки в обучении и не является новым экспериментом.
Для остальных 18 методов в этой быстрой проверке проверяется агрегация
сохранённых построчных метрик; их инференс требует отдельных весов.

`evidence/ranking_replay.json.gz` содержит локальные ID и цели для проверки;
`evidence/per_user_metrics.csv.gz` — построчные метрики без исходных ID покупателей.
`evidence/metrics_all_methods.csv` — эталонная сводка.

## 2. Окружение для проверок протокола и CPU baseline

Реальное обучение рассчитано на Ubuntu/WSL2; используются `fcntl` и Linux-пути.
Рекомендуется **Python 3.11**. Не устанавливайте обучение в Python 3.14:
старые версии PyTorch/NumPy могут не иметь подходящих колёс.

```bash
python3.11 -m venv .venv-review
source .venv-review/bin/activate
python -m pip install -r requirements-cpu.txt
python check_protocol.py
```

Последняя команда проверяет реальный `unix_seconds` на ns/us/ms/s, часовой
пояс, отказ на неоднозначных числах и NaT, а также реальный расчёт MAP:
знаменатель сохраняет недоступные цели, дубликаты рекомендаций запрещены.
Она не использует данные и не обучает модели.

`requirements-cpu.txt` — выделенный набор для этих проверок и деревьев.
`RelBenchGNN/requirements.lock.txt` — исторический полный снимок окружения;
там сохранён первоначальный абсолютный editable-путь.
В `requirements-gpu-lock.txt` он заменён на `./RelBenchGNN/upstream`.
Версии отдельных Kaggle/LLM запусков могут отличаться; смотрите их протоколы.

## 3. Получение исходных данных

Из корня пакета в активированном окружении:

```bash
python RelBenchGNN/restore_downloads.py all
python RelBenchGNN/restore_downloads.py all --verify-only
```

Восстанавливаются H&M и GloVe из зафиксированных ревизий с SHA256 в
`data/download_manifest.json` и `data/glove_download_manifest.json`.
Нужны сеть, свободное место и доступность внешнего хранилища.
Код сторонних библиотек включён вместе с их LICENSE; точные исходные commits
записаны в `evidence/source_provenance.json`.
Копирование исходников не отменяет лицензий данных, моделей и библиотек.

## 4. Реальный контрольный запуск LightGBM на medium

В **новой копии пакета**, после разделов 2–3:

```bash
python CVBenchmark/prepare.py
python CVBenchmark/prepare_v2.py
python CVBenchmark/pairs.py
python CVBenchmark/trees.py 0 manual train
python CVBenchmark/trees.py 0 manual evaluate
```

Это полный CPU-запуск одного фолда, не быстрый smoke: оценка перебирает весь
каталог из 10000 товаров. Выходы —
`CVBenchmark/results/medium_v2/fold_0/lightgbm_manual/`:
`model.txt`, `trained.json`, `test_predictions.npy`, `test_metrics.json`,
`verification.json`. Оценка дополнительно проверяет повторную загрузку модели
и инвариантность признаков к перестановке строк.
Эталон pooled MAP manual в отчёте — 0,3473%; это среднее по всем трём фолдам,
поэтому один fold нельзя сравнивать с pooled как с одной и той же оценкой.

Для Raw15 замените `manual` на `raw15`. Для полного трёхфолдового сравнения
выполните обе команды trees для фолдов 0, 1, 2; сравнивайте исходные доли MAP
с `evidence/metrics_all_methods.csv`, строками normal/all. Умножение на 100
нужно только для отображения процентов.

Не запускайте старый общий `CVBenchmark/launch.py` для проверки исправленного
GNN: он сохраняет исторический ошибочный перевод времени и также вызывает
платный API. Этот код оставлен для аудита ошибки, а не как рекомендуемый запуск.

## 5. GPU: ID-GNN и графовые продолжения

Нужны NVIDIA GPU, совместимый драйвер, Linux/WSL2 и окружение Python 3.11.
Исторический стек: torch 2.2.2+cu118, PyG 2.5.3, pytorch-frame 0.2.3.
Пример установки бинарных частей перед полным lock:

```bash
python -m pip install torch==2.2.2+cu118 --index-url https://download.pytorch.org/whl/cu118
python -m pip install pyg-lib==0.4.0+pt22cu118 torch-scatter==2.1.2+pt22cu118 torch-sparse==0.6.18+pt22cu118 -f https://data.pyg.org/whl/torch-2.2.2+cu118.html
python -m pip install -r requirements-gpu-lock.txt
python -m pip install -e ContextGNN/upstream --no-deps
```

Наличие всех старых колёс на внешних серверах и полная установка на новом
компьютере при подготовке пакета не проверялись.

Полный RelBench: сначала smoke с отдельным именем, затем настоящий запуск:

```bash
python RelBenchGNN/run_idgnn.py --smoke --output_dir RelBenchGNN/results/reviewer_smoke --run_id reviewer_idgnn_smoke_v1
python RelBenchGNN/run_idgnn.py --epochs 20 --seed 42 --temporal_strategy last --output_dir RelBenchGNN/results/reviewer_full_seed42 --run_id reviewer_idgnn_full_seed42_v1
```

Smoke не сравнивается с финальными цифрами. Для полного исторического запуска
seed42 в отчёте val 2,63442%, test 2,78432%; один seed, `last`, отличие от
табличного `uniform` статьи явно описано в отчёте.

Medium GNN: сначала подготовьте данные (раздел 4) и создайте свежий runtime:

```bash
python run_medium_gnn.py build --run-name reviewer_corrected_v1
python run_medium_gnn.py train --run-name reviewer_corrected_v1
python run_medium_gnn.py evaluate --run-name reviewer_corrected_v1
python run_medium_gnn.py verify --run-name reviewer_corrected_v1
```

Этот отдельный драйвер использует исходные генератор и исправление времени,
меняет только пути выходов/run_id и выполняет шесть fit: ID-GNN и ContextGNN
на трёх фолдах. После всех fit он фиксирует хеши выбранных checkpoint, и только
затем разрешает outer-оценку. API не вызывается. Выходы:
`CVFollowup/results/reviewer_corrected_v1/`; при изменении настроек или новом
эксперименте выбирайте новое `--run-name`. Команда build только создаёт код.
Она проверена при подготовке; train/evaluate/verify здесь не запускались.

Историческое исправление и последующие абляции находятся в `CVFollowup/`.
`gnn_timefix.py FOLD train` требует предварительного
`reports/medium_followup_v1/graph_time_fix_verification.json`, а
`gnn_timefix.py FOLD evaluate` — pretest freeze. Эти барьеры нельзя обходить
копированием финального JSON без его фактического воспроизведения.
`check_time_fix.py` также проверяет реальные данные и использует старые веса
для отдельной диагностики existing. Поэтому он не заменён фиктивным «PASS»:
минимальную проверку самой ошибки обеспечивает `check_protocol.py`.

Для точного исторического инференса запросите у автора отсутствующие
`best.pt`, `model.txt` и исходные каталоги результатов, сохраняя пути и SHA256
из соответствующих `pretest_freeze.json`/`comparison.json`/протоколов.
Эти файлы не опубликованы и не включены в пакет. Без них нужен новый fit с
новым run_id (например, через драйвер выше) и выполнение pretest-процедур; совпадение результатов
и побитовое совпадение CUDA не гарантируются.

## 6. Где искать остальные эксперименты

| Части отчёта | Реализация и протокол |
|---|---|
| 2, полный RelBench и ручные признаки | `RelBenchGNN/README.md`, `baseline/`, `RelBenchGNN/run_idgnn.py` |
| 3, эмбеддинги и две башни | `baseline/`, `RelBenchGNN/` — embedding/two_tower scripts |
| 4–6, Qwen/Llama и Balance-scale | `LLMFeatures/README.md`, `LLMFeatures/`, соответствующие Kaggle runtime и отчёты |
| 7, малая выборка | `ContextGNN/prepare_small_dataset.py`, `ContextGNN/run_small.py`, `Recformer/`, `TDM/` |
| 8, H005–H009 на small | `LLMFeatures/provider*_runtime*/`, `LLMFeatures/README.md` |
| 9, medium и продолжение бюджета | `CVBenchmark/PROTOCOL.md`, `CVFollowup/gnn_timefix.py`, `api_budgets.py`, `recformer_grid.py` |
| 10, ContextGNN | `CVFollowup/context_first3.py`, `context_combined.py`, `context_combined_test.py` |
| 11, H010/H011 | `LLMResearch/README.md`, `PROTOCOL.md`, протоколы Codex в `LLMResearch/` |
| 12, global CE, FEATURE, интересы | `CVFollowup/context_global_aux_v3.py`, `item_encoder_followup.py`, `context_multi_interest_v2.py` |
| 13, аудит новых/повторных | `CVFollowup/novelty_audit.py`, `novelty_scores.py`, `novelty_tdm.py`, `multi_interest_test.py`, `LLMResearch/novelty_extension.py` |

Скрипты продолжений опираются на результаты предыдущих стадий. Их нельзя
считать независимыми однокомандными запусками. Архив сгенерированных исходников
в `evidence/frozen_sources/` помогает проверить фактически использованный код,
но содержит исторические абсолютные пути; выполняемый runtime на новом
компьютере нужно заново создавать генераторами.

Для Recformer нужны дополнительные исходные pretrained-веса; для локальных
LLM — соответствующие веса и доступ/лицензия. Для API-экспериментов нужен
собственный `.env` по `.env.example`, оплачиваемый провайдер и явный выбор
бюджета. Быстрые проверки выше API не вызывают. Новая генерация LLM не
гарантирует прежние программы: API-модель и сервис могут измениться.
Выбранные программы присутствуют среди `reports/**/selected_program*`,
где они были сохранены. Полные необработанные диалоги/API-ответы не включены.
Невыполненные и оборванные эксперименты не превращены в завершённые.

### Настройка API: проверяющий должен вписать свой ключ

Ключ автора в поставку не включён. Для **новых API-экспериментов** скопируйте
`.env.example` в `.env` в корне этой папки и впишите собственный ключ:

```bash
cp .env.example .env
```

В PowerShell вместо этой команды:

```powershell
Copy-Item .env.example .env
```

Содержимое `.env`:

```dotenv
ACCESS_TOKEN=YOUR_PROVIDER_API_KEY
```

Замените `YOUR_PROVIDER_API_KEY` своим действительным ключом. Код читает
именно **`ACCESS_TOKEN` из файла `.env`**, а не `OPENAI_API_KEY` из окружения.
Этот файл исключён из Git; не добавляйте в репозиторий заполненный ключ.

Исторические API-запуски настроены на провайдера TookenClub
(`https://tooken.club/v1`) и идентификатор модели `gpt-6.1-sol`.
Поэтому нужен ключ, подходящий именно к настроенному провайдеру;
произвольный ключ другого сервиса автоматически не подойдёт.
Поля `base_url` и `model_id` задаются конфигурацией запуска, а в некоторых
исторических runner дополнительно проверяются через assert. Для смены сервиса
нужны согласованное изменение конфигурации/проверок и новый run_id — это уже
новый эксперимент. Доступность исторического сервиса/модели сейчас не проверялась.

API-запуски расходуют средства на счёте проверяющего. Заранее выберите лимит
запросов. Для `verify_saved_results.py`, `check_protocol.py`, CPU/GNN-обучения
и сборки PDF API-ключ не требуется; эти команды к LLM API не обращаются.

## 7. Размещение на GitHub

В поставке на GitHub эта папка находится внутри корневого репозитория рядом
с двумя итоговыми отчётами. Перед выполнением проверочных команд перейдите
в неё: `cd reviewer_repository`. Вложенного Git-репозитория здесь нет.
Локальный `.gitignore` исключает ключи,
данные, веса, окружения, кэши, API-сессии и новые результаты. Компактные
проверочные CSV.gz/JSON.gz в evidence намеренно включаются.
Пакет не содержит исходные таблицы, их ZIP-экспорты и trained weights.

Команды Git выполняйте из корня внешнего репозитория. Если origin уже
настроен, используйте существующий адрес; для нового репозитория добавьте
свой origin. Проверочные команды из остальных разделов выполняются из
`reviewer_repository`. Ссылки на окончательные Markdown/PDF находятся
в корневом README.

Удалённый репозиторий не создан и push при подготовке не выполнялся.
`MANIFEST.json` позволяет проверить состав поставки и обнаружить изменение
любого включённого файла. Проверенные здесь действия и ограничения перечислены
в `VALIDATION.md`.

## 8. Повторная сборка PDF

Установите инструменты в отдельное окружение, затем выполните:

```bash
python -m pip install -r requirements-pdf.txt
python tools/build_final_pdf.py
python tools/inspect_pdf.py
```

Сборщик берёт текст только из окончательного Markdown, добавляет существующие
27 графиков и пишет `output/pdf/report_ru.pdf`. Проверка отрисовывает страницы
в `tmp/pdfs/`, проверяет полноту текста и поля. На Linux необходимы шрифты
DejaVu Sans в `/usr/share/fonts/truetype/dejavu`; на Windows используется Arial.
