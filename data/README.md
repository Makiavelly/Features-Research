# Локальный датасет H&M из RelBench

`rel-hm/` содержит полный опубликованный снимок H&M в формате RelBench:

- `manifest.yaml` — таблицы, связи и временные границы разбиений;
- `db/customer.parquet` — пользователи;
- `db/article.parquet` — товары;
- `db/transactions.parquet` — история покупок;
- `tasks/user-item-purchase/` — покупки товаров в следующие 7 дней;
- `tasks/user-churn/` — отсутствие покупок в следующую неделю;
- `tasks/item-sales/` — сумма продаж товара в следующую неделю;
- для каждой задачи: manifest, train.parquet, val.parquet, test.parquet.

Источник и точная ревизия, размеры файлов и контрольные суммы SHA256:
`download_manifest.json`. Восстановление зафиксированного снимка:
`python RelBenchGNN/restore_downloads.py data` из корня проекта (Python >= 3.11).
Проверка без скачивания: добавьте `--verify-only`. Список других внешних
артефактов и обученных весов приведён в [корневом README](../README.md).

Загрузка в дальнейших экспериментах (RelBench 3):

```python
from pathlib import Path
from relbench import load_dataset

dataset = load_dataset(Path("data/rel-hm").resolve())
db = dataset.get_db()  # строки после test_timestamp скрыты
task = dataset.load_task("user-item-purchase")
train = task.get_table("train")
val = task.get_table("val")
test_inputs = task.get_table("test")  # без целевых товаров
```

Для исследования полного сырого снимка доступен
`dataset.get_db(upto_test_timestamp=False)`. Не используйте будущие
транзакции при построении признаков на момент конкретного примера.
Цели теста сохранены на диске для оценки; они не являются признаками.

Ключи customer_id/article_id уже переиндексированы RelBench.
Это не исходные идентификаторы Kaggle H&M.

Статистика и схемы после проверки загрузки: `dataset_summary.json`.
Оригинальные описание и schema.svg находятся внутри `rel-hm/`.
