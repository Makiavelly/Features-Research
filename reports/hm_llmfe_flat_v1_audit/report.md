# Проверенный реальный H&M flat-table эксперимент

20 оценённых программ /23 обращения,3 отказа,3 исправления. Выбран candidate_003 по confirmation512.
Одинаковые803377 train пар; val1024/test2048 пользователей и общие кандидаты ID-GNN.

| Модель | Val MAP@12, % | Test MAP@12, % |
|---|---:|---:|
| Raw15 LightGBM | 1.02687 | 0.71314 |
| Prepared30 LightGBM | 0.71542 | 0.73737 |
| Seeded32 LightGBM | 0.71077 | 0.72335 |
| LLM-FE flat LightGBM | 0.74474 | 0.80095 |
| Manual features → LightGBM | 1.61426 | 1.86288 |
| GNN → LightGBM | 1.69983 | 1.68057 |
| ID-GNN (graph training budget) | 2.24926 | 2.25494 |

Все20 обученных кандидатов проверены по program/model hashes и train_pairs. Конфиг fingerprint и7 runtimeSHA совпадают.
Независимый повтор из сохранённых деревьев:4 модели×val/test, точное совпадение top12/AP/MAP.
Три референса пересчитаны из исходных top12 на тех же пользователях.
Оригинальный ZIP не изменён. Экспортированные файлы: export/. Повторные проверки: independent_frozen_replay/.
flat_manifest отсутствует в ZIP; byte-level сравнение Kaggle-кэша невозможно. Локальные подготовленные
данные восстановлены тем же кодом/исходным bundle; совпадение всех предсказаний проверено.

Прирост LLM к Prepared30 на test небольшой; см. парный exploratory bootstrap ниже.
95% интервал к Prepared30 и Seeded32 положителен на этой выборке; к Raw15 включает0.
На val Raw15 выше выбранной LLM-модели. Поиск256/confirmation512 дают шумный отбор,
но причина разницы не установлена отдельным экспериментом. Не выбирать новую программу по этому test.

Выбранные36 полей:15 raw+15 ручных агрегатов+2 ручных seed log+4 новых LLM отношения.
Один purchase ratio делит180-дневное user-article count на30-дневное article count: это не доля одного окна.
Recency ratios защищены проверкой counts, а не знаменателя recency; inf преобразуется вNaN evaluator.
Это допустимый код, но семантические ограничения остаются; выигрыш в исполнении не означает сильных признаков.

| Сравнение test: LLM минус контроль | Разница, п.п. | 95% парный bootstrap, п.п. |
|---|---:|---|
| Raw15 LightGBM | +0.08781 | [-0.17900; +0.34391] |
| Prepared30 LightGBM | +0.06357 | [+0.01072; +0.12785] |
| Seeded32 LightGBM | +0.07760 | [+0.02671; +0.13842] |
| Manual features → LightGBM | -1.06193 | [-1.42057; -0.73965] |
| GNN → LightGBM | -0.87962 | [-1.24041; -0.54936] |
| ID-GNN (graph training budget) | -1.45400 | [-1.86758; -1.07751] |

Bootstrap:10000 перевыборок пользователей,seed42; exploratory, не оценка эффекта всех random seeds.
Не весь каталог/не полный test, не воспроизведение статьи. ID-GNN имеет иной upstream-бюджет.

![Сравнение](export/comparison.png)
![Поиск](export/search_progress.png)
![AP](export/ap_histograms.png)
