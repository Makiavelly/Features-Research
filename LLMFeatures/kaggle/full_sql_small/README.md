# Qwen7B: полные SQL-запросы на Kaggle T4

Файл [hm_small_qwen7b_full_sql_kaggle_t4.ipynb](../hm_small_qwen7b_full_sql_kaggle_t4.ipynb)
самодостаточен: все Python-модули встроены. В Kaggle нужны только этот `.ipynb`
и прежний Input [hm_small_sql_compare_v1.zip](../hm_small_sql_compare_v1.zip).
Включите Internet и GPU T4, выполните Save Version → Run All. Qwen публична,
HF_TOKEN не нужен. Другие отчёты как Input не требуются.

Qwen2.5-Coder-7B-Instruct возвращает обычный SQL, например:

```sql
WITH counts AS (
  SELECT customer_id, count(*) AS total,
         count(*) FILTER (WHERE days_ago <= 7) AS recent
  FROM history GROUP BY customer_id
)
SELECT customer_id, total AS f_total,
       recent / nullif(total, 0) AS f_recent_share
FROM counts;

SELECT article_id, count(*) AS f_item_count
FROM history GROUP BY article_id;
```

Это пример синтаксиса, а не заранее измеренный победитель.
JSON от модели не требуется. `program.json` создаёт наш код для внутреннего
сохранения; человекочитаемый `program.sql` хранит все её запросы.

До6 самостоятельных SELECT/WITH запросов, до36 выходных числовых f_* признаков.
Разрешены CTE, aliases, joins между собственной history/CTE, числовые окна,
CASE и SQL-преобразования в тех же запросах. Каждая выходная таблица имеет
одну строку на ключ: customer_id, article_id, одна товарная категория,
customer_id+article_id либо customer_id+категория. Имена/значения ключей сохраняются.
Host выполняет конечные joins и добавляет прежние15 raw полей.

Общего доступа к SQL нет: модель работает с отдельным соединением, где
физически зарегистрирована только история до cutoff. Полная tx, цели,
кандидаты и произвольные таблицы/файлы недоступны. Проверяются AST, доступные
источники/операции, binding, числовая схема, уникальность ключей, порядок
строк, инвариантность к перестановке/размеру блока. Каждый запрос ограничен
60секундами; таблица больше250000строк отклоняется, не принимается усечённой.
Неисполняемый/неверный SQL исправляет сама LLM, не host.

Protocol `hm_small_qwen7b_full_sql_v1`, уникальный fingerprint модели/данных/
параметров/исходников. Один поиск:20 разных измеренных наборов,до300обращений,
до3repair,3популяции/один лучший набор своей популяции в промпте.
Все обращения учитываются. Для дубля передаются номер совпавшей попытки и ось
изменения; полный совпавший SQL уже находится в Previous SQL response и не
дублируется третий раз в сообщении об ошибке. Неизменённый repair прекращает
цепочку, как политика H003C.
Дедуп — консервативный SQL AST с нормализацией регистра/пробелов/комментариев
и имён f_*. Переименование CTE/табличных aliases и общая SQL-эквивалентность
не распознаются. Это не идентичный критерий старого DSL.

Сравнение: те же72813 train-пар/4804 user-time/8cutoff; LightGBM150/31/4CPU,
raw15/компактное кодирование категорий. NF4/doublequant/FP16,temperature0.8,
input6144/output2048,seed42+call−1,T4GPU0. Revision Qwen закреплена:
c03e6d358207e414f1eca0bb1891e29f1db0e242. Worker обучения/оценки байт-в-байт прежний;
base_features сохраняет прежний host raw/joins. Изменены SQL-интерфейс,
prompt, пространство программ (36 выходов вместо24+12) и дедупликация.

Search128 оценивает все5000товаров; top3+raw выбираются наconfirmation88.
Heldout88/val304/test250 и независимые frozen replays сохраняются после выбора.
Val304 включает search/confirmation. Test уже просматривался в прежних опытах:
повторная диагностическая оценка, не новый закрытый test. По test ничего не
выбирается. Старый Qwen7B и H003 сравним локально после получения нового ZIP.
Reference GNN/manual/Recformer в Input не переобучаются; их бюджеты отличались.

Output `hm_small_qwen7b_full_sql_v1_<hash>_results.zip`: запросы/ответы/ошибки,
program.sql,program.json,диагностика каждого запроса,island/proposal/repair/parent,
модели/предсказания/метрики,графики поиска/обучения/MAP/эффективности и AP-гистограммы.
ZIP обновляется после каждого вызова и при исключениях. Cancel Kaggle не гарантирует
публикацию Output. Скачайте итоговый ZIP для локального аудита.

Сборка: `python LLMFeatures/kaggle/build_full_sql_small_notebook.py`.
CPU-проверка `check_delivery.py` использует заданные SQL-ответы, не настоящую
LLM. Проверяет CTE/квантили/окна/прошлую историю, pandas known-answer,
ключи/дубликаты, routing/resume, raw-control identity и полный frozen replay.
Проверка контекста — `check_context.py`, скачивается только токенизатор.
Артефакты: `reports/kaggle_llmfe_validation/full_sql_small_v1`.
