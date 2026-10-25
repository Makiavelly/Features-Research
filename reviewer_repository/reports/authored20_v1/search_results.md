# Authored feature search: 20 evaluated sets

This table contains search scores. Final scoring has subsequently completed: confirmation selected set 9; validation MAP@12 1.260603%, test 2.231032%. See report.md and comparison_all_methods.png for the final audited comparison when available.

LightGBM inputs: generated features PLUS 15 raw fields. This is NOT a blind experiment: the author had access to previous experimental history.

| Set | Population | Parent | Search MAP@12, % | Description |
|---|---|---|---:|---|
| [1](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_001) | 0 | control | 1.526199 | Популярность, активность, давность и разнообразие покупок |
| [2](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_002) | 1 | control | 0.931328 | Продуктовая семья и тип: частота, давность и сглаженные предпочтения |
| [3](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_003) | 2 | control | 1.197607 | Личные предпочтения и совместные покупки категорий |
| [4](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_004) | 0 | 1 | 1.203046 | Развитие временной основы: скорости изменения популярности |
| [5](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_005) | 1 | 2 | 1.765715 | Более широкие личные предпочтения вместо узкой продуктовой семьи |
| [6](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_006) | 2 | 3 | 1.791295 | Совместные покупки типов и секций на90и365днях |
| [7](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_007) | 0 | 1 | 1.473214 | Возврат к компактной основе с непрерывным затуханием |
| [8](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_008) | 1 | 5 | 2.148015 | Широкие предпочтения с плавной свежестью интереса |
| [9](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_009) | 2 | 6 | 1.806486 | Длинная история совместных покупок без коротких графов |
| [10](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_010) | 0 | 1 | 1.049624 | Компактная временная основа плюс ценовая совместимость |
| [11](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_011) | 1 | 8 | 1.614076 | Улучшенный набор интересов с относительной давностью категорий |
| [12](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_012) | 2 | 9 | 1.119637 | Длинные коллективные связи и свежие личные интересы |
| [13](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_013) | 0 | 1 | 1.260293 | Компактный ранжировщик повторных покупок без общих счётчиков пользователя |
| [14](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_014) | 1 | 8 | 1.677489 | Менее избыточные затухающие предпочтения с уровнем отдела |
| [15](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_015) | 2 | 9 | 1.768663 | Абляция коллективных связей: те же личные и временные признаки без графов |
| [16](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_016) | 0 | 1 | 1.441310 | Компактная основа с частотой и давностью личных категорий |
| [17](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_017) | 1 | 8 | 1.181176 | Точечная абляция избыточного абсолютного ценового отклонения |
| [18](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_018) | 2 | 9 | 1.203215 | Длинные коллективные связи по типу, секции, цвету и группе одежды |
| [19](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_019) | 0 | 1 | 1.005704 | Компактная основа плюс возрастная совместимость аудитории товара |
| [20](C:/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9/codex_authored20/candidates/candidate_020) | 1 | 8 | 1.205808 | Сохранение лучшего набора и явные недавние счётчики интересов |

Search scores guided adaptive generation. The final protocol winner has not been selected.
