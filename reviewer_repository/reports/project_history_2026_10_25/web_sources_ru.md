# Веб-источники исследования

Составлено25октября2026года по локальным протоколам, журналу, манифестам и обзорам. Названия и страницы основных статей дополнительно проверены в интернете. Это восстановленная библиография проекта; полного браузерного журнала прежних сессий нет, поэтому восстановление каждого посещения не гарантируется.

## Основа экспериментов

| Материал | Ссылки | Как использовался |
|---|---|---|
| RelBench: A Benchmark for Deep Learning on Relational Databases | [Статья](https://arxiv.org/abs/2407.20060), [использованный HTML v1](https://arxiv.org/html/2407.20060v1), [код](https://github.com/stanford-star/relbench) | Данные H&M, ID-GNN/GraphSAGE, задачи и справочные метрики. Код закреплён на919fb8a61a4b4cb787283860597f45701895578d |
| RelBench User Study | [Экспертные SQL](https://github.com/snap-stanford/relbench-user-study) | Основа адаптации ручных признаков; commit445bb7a3b1230f49f8e5890ae81754d3e365680f. Наши126признаков не являются неизменённым опубликованным ranking baseline |
| LLM-FE: Automated Feature Engineering for Tabular Data with LLMs as Evolutionary Optimizers | [Статья v3](https://arxiv.org/abs/2503.14434v3), [код](https://github.com/nikhilsab/LLMFE) | Популяционный поиск программ признаков; relational/SQL-интерфейсы H&M — наша адаптация |
| ContextGNN: Beyond Two-Tower Recommendation Systems | [Статья](https://arxiv.org/abs/2411.19513) | Локальное/глобальное ранжирование, ContextGNN small/medium, FEATURE/FUSION |
| Recformer — Text Is All You Need: Learning Language Representations for Sequential Recommendation | [Статья](https://arxiv.org/abs/2305.13731), [использованная репликация](https://github.com/AaronHeee/RecFormer), [pretrained model](https://github.com/AaronHeee/RecFormer#pretrained-model) | Репликация26b00a58e7affe0c54a89c143ea7bce37f2e8e08 и внешний checkpoint. Его авторское происхождение отдельно не аттестовано |
| TDM — Learning Tree-based Deep Model for Recommender Systems | [Статья v5](https://arxiv.org/abs/1801.02294v5) | Древовидный retrieval, fixed/cluster и beam/full эксперименты |
| JTM — Joint Optimization of Tree-based Index and Deep Model for Recommender Systems | [Статья v2](https://arxiv.org/abs/1902.07565v2) | Изучена для различения JTM и обычной embedding-кластеризации. Полный JTM не реализован |
| Alibaba TorchEasyRec | [Зафиксированный код](https://github.com/alibaba/TorchEasyRec/tree/4458f1c66f6c32dc672b9c805855f3d2e6e6179e), [TDM tutorial](https://github.com/alibaba/TorchEasyRec/blob/4458f1c66f6c32dc672b9c805855f3d2e6e6179e/docs/source/quick_start/local_tutorial_tdm.md) | Изучены sampler, дерево, clustering и retrieval. Итоговая реализация проекта — своя PyTorch-адаптация |
| Alibaba XDL / x-deeplearning | [Зафиксированный код](https://github.com/alibaba/x-deeplearning/tree/a710108d4457f01992bf0b3b9b6c0f78fdb8e642), [wiki](https://github.com/alibaba/x-deeplearning/wiki) | Изучен старый TDM-стек; сам стек не установлен и не воспроизведён |
| ComiRec — Controllable Multi-Interest Framework for Recommendation | [Статья](https://arxiv.org/abs/2005.09347), [код](https://github.com/THUDM/ComiRec), [model.py](https://github.com/THUDM/ComiRec/blob/master/src/model.py) | Идея нескольких интересов для ContextGNN K1/K4. Локальная версия отличается от ComiRec |
| FREEDOM — A Tale of Two Graphs: Freezing and Denoising Graph Structures for Multimodal Recommendation | [Статья](https://arxiv.org/abs/2211.06924), [код](https://github.com/enoche/FREEDOM) | Идея фиксированного item-item графа; полного воспроизведения FREEDOM нет |

Свидетельства использования: [LLMFeatures README](../../LLMFeatures/README.md), [Recformer report](../recformer_small_v1/report.md), [TDM/JTM assessment](../tdm_assessment/report.md), [обзор глобальной ветки](../medium_followup_v1/novelty_audit_v1/global_branch_research_ru.md).

## Изучены для гипотез; отдельного воспроизведения нет

- [PinSage: Graph Convolutional Neural Networks for Web-Scale Recommender Systems](https://arxiv.org/abs/1806.01973) — графовые представления товаров и признаки.
- [Knowledge Graph Convolutional Networks for Recommender Systems — KGCN](https://arxiv.org/abs/1904.12575) — связи товаров через атрибуты и knowledge graph.
- [On the Theories Behind Hard Negative Sampling for Recommendation](https://arxiv.org/abs/2302.03472) — hard sampling/BPR; эффект поверх нашего full-catalog CE не проверен.

Изучение этих работ не означает выполнения их экспериментов в проекте.

## Семь материалов обзора от21октября

Прочитаны после основной серии экспериментов для анализа дальнейших направлений. GLASS, SID retrieval и новый sequential-контроль по этому обзору не запускались.

| Материал | Ссылка |
|---|---|
| Researchim: обзор рекомендательных систем и инфраструктуры | [GitHub](https://github.com/researchim-ai/state-of-ai/blob/main/Recommender_systems_research.md) |
| A Survey of Foundation Model-Powered Recommender Systems: From Feature-Based, Generative to Agentic Paradigms | [arXiv2504.16420v1](https://arxiv.org/abs/2504.16420v1) |
| A survey on sequential recommendation | [Springer](https://link.springer.com/article/10.1007/s11704-025-41329-w) |
| Transformers for Graph-based Recommender Systems: A Survey | [Springer](https://link.springer.com/article/10.1007/s11633-025-1607-8) |
| Graph Foundation Models for Recommendation: A Comprehensive Survey | [arXiv2502.08346v4](https://arxiv.org/abs/2502.08346v4) |
| A Survey on Generative Recommendation: Data, Model, and Tasks | [Прочитанная авторская arXiv2510.27157v2](https://arxiv.org/abs/2510.27157v2), [запрошенная журнальная публикация](https://www.sciencedirect.com/science/article/pii/S2666651026000100) |
| GLASS: Coarse-to-Fine Long-term Interest Modeling for Generative Recommendation | [arXiv2602.05663v2](https://arxiv.org/abs/2602.05663v2) |

ScienceDirect при исходном исследовании вернул403: журнальный полный текст не прочитан, совпадение с arXiv побуквенно не проверено. Researchim при текущей веб-проверке получить не удалось; прежнее чтение подтверждено локальным конспектом и сохранённым `github_source.md` с SHA256.

Подробные конспекты, прочитанные разделы и замечания: [литературный обзор21октября](../literature_review_2026_10_21/review_ru.md). Библиографии чужих статей не проверялись постатейно и не объявляются прочитанными целиком.

## Данные, модели и техническая документация

- [RelBench dataset snapshot](https://huggingface.co/datasets/stanford-star/relbench-v1/tree/7abf5d46a48534d918704ca2af278861b932f4dc) — ревизия данных H&M из download_manifest.
- [GloVe6B300d](https://huggingface.co/sentence-transformers/average_word_embeddings_glove.6B.300d/tree/e5e8fec6971be8960cfaa853a77a6ddc62a265d7) — входной текстовый encoder из манифеста.
- [Longformer-base-4096](https://huggingface.co/allenai/longformer-base-4096/tree/301e6a42cb0d9976a6d6a26a079fef81c18aa895) — backbone/config/tokenizer Recformer из assets_manifest.
- [Qwen2.5-Coder7B Q4_K_M в Ollama](https://ollama.com/library/qwen2.5-coder:7b-instruct-q4_K_M) — модель локального этапа LLM-FE.
- [DuckDB FILTER](https://www.duckdb.org/docs/current/sql/query_syntax/filter) и [агрегаты DuckDB](https://www.duckdb.org/docs/current/sql/functions/aggregates) — разбор ошибок SQL. Current-документация может отличаться от DuckDB1.4.1 локальных probes.

Не включены служебные GitHub API blob/tree URL, ссылки зависимостей из чужих README и провайдерские endpoints как научные источники. Само наличие ссылки в upstream-файле не доказывает её изучения. Код, данные, веса, прочитанная статья и неисполненная гипотеза разделены явно.
