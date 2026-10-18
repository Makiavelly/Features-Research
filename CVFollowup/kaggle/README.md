# Recformer: параллельный подбор на двух Kaggle T4

Готовые ноутбуки:

- `recformer_medium_lr3e6_w100_kaggle_t4.ipynb`: LR=3e-6, warmup=100 обновлений.
- `recformer_medium_lr1e5_w300_kaggle_t4.ipynb`: LR=1e-5, warmup=300 обновлений.

Каждый проходит три сохранённых medium-CV фолда. Те же исходные веса,
seed42, batch4, accumulation4, FP16 и2+2 эпохи. Локально остаются
LR=1e-6/warmup100 и LR=3e-6/warmup300. Другой GPU может дать численные
отличия и другое число пропущенных AMP-обновлений; это сохраняется в отчёте.

## Запуск

1. Загрузите `recformer_medium_cv_inputs_v1.zip` (около762МБ) в один приватный
   Kaggle Dataset. Архив содержит данные трёх фолдов, код и pretrained weights.
   Если Kaggle автоматически распакует ZIP, это также поддерживается.
2. Импортируйте каждый `.ipynb` в отдельный Kaggle Notebook.
3. Подключите один и тот же созданный Dataset к обоим через Add Input.
4. Для каждого включите Internet и GPU T4. HF_TOKEN не нужен.
5. Запустите оба через Save Version → Save & Run All.

Ноутбуки создают отдельный Python3.11 в `/tmp`, устанавливают torch2.2.2+cu118,
transformers4.46.3 и остальные сохранённые версии. Используется одна GPU;
multi-GPU не требуется. Входные файлы сверяются по SHA256 до обучения.
Потребуется место в Output под checkpoint и результирующий ZIP.

## Результаты

Скачайте из Output соответствующий файл:

- `recformer_medium_lr3e6_w100_kaggle_v1_results.zip`
- `recformer_medium_lr1e5_w300_kaggle_v1_results.zip`

Каждый содержит три выбранных обученных checkpoint, параметры, историю всех
четырёх эпох, validation-метрики и контрольные суммы. Объём результата
порядка1.9ГБ на ноутбук. После скачивания передайте пути архивов Codex.

Импорт в native WSL окружении проекта:

```text
RelBenchGNN/.venv-wsl/bin/python CVFollowup/import_kaggle.py PATH_TO_RESULT_ZIP
```

Импорт проверяет все три фолда, исходные данные/веса, параметры, четыре эпохи,
SHA256 и происхождение runtime; отказывается перезаписывать обучение.
Только после завершения локальных запусков и импорта обоих архивов выбирается
настройка по среднему inner-validation MAP трёх фолдов, с прежним baseline.
Затем проводится общая outer-оценка и строится финальное сравнение.

В Kaggle test не оценивается. Незавершённый ZIP может сохранить диагностику,
но не импортируется как три завершённых обучения. Полный GPU-запуск T4
локально не проверялся: проведены CPU/data preflight, AST-сравнение кода и
проверки ноутбуков. Смена batch/числа эпох потребует отдельного протокола.

Установка CUDA118 соответствует [инструкции PyTorch2.2.2](https://pytorch.org/get-started/previous-versions/#v222),
отдельный Python управляется [uv](https://docs.astral.sh/uv/concepts/python-versions/).
