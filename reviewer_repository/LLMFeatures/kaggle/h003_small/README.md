# H003: Qwen7B на Kaggle T4

Ноутбук: [hm_small_qwen7b_h003_kaggle_t4.ipynb](../hm_small_qwen7b_h003_kaggle_t4.ipynb).
Все модули встроены: отдельные `.py` в Kaggle загружать не нужно.

Input: прежний [hm_small_sql_compare_v1.zip](../hm_small_sql_compare_v1.zip).
Internet включён, GPU T4. Qwen публична, HF_TOKEN не требуется.
Run All или Save Version → Run All. Старые отчёты моделей не нужны как Input.

В конфиге `ARMS = ['h003a', 'h003b', 'h003c']`:

- A: подробная диагностика всех проблемных признаков. Пустая синтетическая
  схема DuckDB проверяет SQL binding до preflight; численные признаки и MAP
  проверяются прежним worker. Автоматических исправлений/удаления признаков нет.
- B: A плюс примеры в основном промпте.
- C: B плюс формулы/номер ранее оценённого дубликата и предложение изменить
  окно/статистику/группировку; после неизменённого repair цепочка прекращается.

Каждый вариант: 20 различных измеренных наборов, до300 обращений, до3 repair,
3 популяции; все вызовы учитываются. Варианты независимы, памяти между ними нет.
Одна Qwen7B загружается на GPU один раз, RNG фиксируется seed42+call−1.
При необходимости оставьте один вариант в ARMS. Это изменит fingerprint/run ID.

Контроль — прежний `hm_small_qwen_llama_sql_v1_2ecc60d61fd4/qwen`, 67calls/20valid.
Сравнивать A с ним, B с A, C с B. Старый контроль не перезапускается.
Модель закреплена на revision c03e6d358207e414f1eca0bb1891e29f1db0e242.
NF4/doublequant/FP16, temperature0.8, input6144/output2048, один T4.
В отсутствие GPU-проверки здесь не заявляется, что реальное поколение H003 завершено.

Сохранены 72813 исходных пар/4804 user-time/8 cutoff, LightGBM150rounds/31leaves/
4threads, raw15, search128/confirmation88/heldout88, val304/test250/catalog5000.
features.py, worker.py и original_prompt.py байт-в-байт совпадают с контролем.
История только до cutoff; test не участвует в генерации/выборе. Все выборы
закрепляются до итоговой оценки. Test уже просматривался: это повторная оценка,
не новый закрытый test. Уменьшение ошибок не гарантирует улучшение MAP.

ZIP `hm_small_qwen7b_h003_v1_<hash>_results.zip` содержит отдельные каталоги вариантов,
config каждого, prompts/responses, diagnostics.json, trial/status/parent/island,
дубликаты/неизменённые repair, программы, модели, frozen replays, метрики и графики.
generation_efficiency.csv/.png: обращения/валидные/ошибки/дубликаты/repair/
неизменённые repair/токены/время. Search-графики в каталогах вариантов.
Итоговые comparison.png, test_histograms.png, lightgbm_training.png в корне отчёта.
ZIP обновляется после каждого вызова и при исключениях; Cancel Kaggle не гарантирует
публикацию Output. После завершения скачайте ZIP для локального сравнения.

Сборка: `python LLMFeatures/kaggle/build_h003_small_notebook.py`.
Проверка: `h003_small/check_delivery.py` под WSL с изолированными audit_deps и
`.check-deps` на PYTHONPATH. Проверка использует заданные ответы и3 раунда LightGBM;
это технический CPU smoke, не результат эксперимента с Qwen.

Контекст проверен точным токенизатором закреплённой Qwen7B с системным
сообщением и chat template: реконструированы67 исторических обращений для
каждой ветки (201промпт). Максимумы A2693/B3184/C3297 входных токенов,
лимит6144 не превышен; примеры добавляют491токен. Это проверка сохранённой
траектории, не гарантия для всех будущих ответов. Runtime перед каждой
генерацией считает длину; превышение отклоняется без скрытой обрезки.
Артефакт reports/kaggle_llmfe_validation/h003_small_v1/context_budget.json.
Скрипт check_context.py скачивает только токенизатор, веса модели не нужны.
