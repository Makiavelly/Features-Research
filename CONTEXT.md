# Контекст для продолжения проекта

## Medium CV v2: завершено и проверено (2026-10-18)

Дополнительная read-only диагностика по вопросу пользователя о ContextGNN:
старыйsmall даёт248уникальных orderedtop12 для250пользователей/1574товара;
новыеfold0/1/2 всего11/8/11списков для1839/1982/1698пользователей,
24/26/26уникальных рекомендованныхтоваров. Это вырождение персонализации;
точнаяпричина пока НЕустановлена. Необъяснятьпадение лишь размером/знаменателем:
дажеconditionalcatalogMAPновогоContextGNN~0.0648% противстарого3.0156%.
Изменилиськогорта, возрасткаталога(anchorJune29vsSep7), train6vs8срезов,
preprocfitpastvsfull. См.contextgnn_regression_audit.json и
contextgnn_regression_notes_ru.md; ссылкадобавленавsummary_ru.md.
Новогообучения/инференса/изменениямоделей не было. Replay доказывает
повторяемостьoutputs, но неустраняетвозможностьошибкивсемобучающемпайплайне.

ИТОГ: все27 оценок (9методов×3фолда) и frozen-model replays прошли.
Pipeline закончился00:45:56, живых процессов обучения/оценки прифинальнойпроверке
нет. Итоговыеартефакты reports/medium_cv_v2/: report.md, summary_ru.md,
comparison.json/.png/.svg, fold_comparison.png, ap_histograms.png,
paired_heatmap.png, fold_metrics.csv, summary.csv, paired_differences.csv,
api_usage.csv, selected_programs/. Все4PNG визуально просмотрены, читаемы;
45pretestконтрольныхсуммвыбранныхмоделей/программ совпали послеouterоценки.
Свидетельство final_visual_review.json. Модели/отбор поouterметрикам не менялись.

Основной pooled full-target MAP@12(%): Recformer zero-shot0.6286,
H0080.4627, RecformerLR0.4525, H0090.4514, manual0.3473, TDM0.2135,
raw150.1415, ContextGNN0.0274, IDGNN0.0245. Не сравнивать абсолютныецифры
с прежнимsmallpilot: здесь другиепокупатели/каталог/полныеисходныецели.
H008>manual на3/3неделях, но paired95%CI разницы включает0; это сигнал,
не доказанноепревосходство. H009>H008 не подтверждено; inputtokens4.31×больше.
Recformerzero вышеfinetuned на3/3; zero-vs-H008 pairedCI включает0.
Только3недели/1seed, customerbootstrap неоценка нового временного режима.

Все6APIarms по20validstructural (120), численноразличныхtrainматриц
H00817/15/19 иH00920/17/18. Ничего заднимчисломнеудалено/непереотобрано.
APIhistoriesиselectedhashes проверены. Costtimers НЕполноеобщевремязапуска:
H008fold0пауза, recoveryтаймеры могутучитыватьлишьпоследнюючасть;
неизвестнытокены/списанияпровайдера по оборваннымPOST. Подробноreview_notes_ru.md.
finalize_verified_tracking.py сохраняетtest_metrics/complete каждогоиз27run.
Все предыдущие сообщения ниже — хронология, а не актуальныйстатус.

2026-10-18 00:20 МСК: PID4552 жив. Fold0/1 все9методов оценены и проверены.
Fold2 GNN2+TDM evaluation/replay прошли; Recformer оценён, идёт полныйreplay
(child6263, GPUиспользуется). Далее4treeварианта иreport. Новыхошибокнет,
25GiBсвободно. Сводныхграфиковещёнет. Не менятьпротокол поouterрезультатам.

23:48 МСК: PID4552 продолжаетouterоценку. Fold0 ВСЕ9методов оценены,
verification/replay прошли. Наfold1 GNN2+TDM evaluation/replay прошли,
идётRecformer evaluation (child5433 припроверке), затемmanual/raw15/H008/H009.
Новыхошибокнет; failure.json старый22:52. Осталсятакжеfold2 иreport.
Модели/отборзаморожены, не менять поouterметрикам. Итоговыхсводок/графиковещёнет.

23:29 МСК: ВСЕ6 APIsearch завершены (каждый20valid, суммарно120). Helper1973
закончилработу и запустил обычныйpipeline PID4552, теперь идёт OUTER EVALUATION.
selection_pretest.json создан ДОouter, модели/признаки заморожены.
Fold0 GNN/TDM/Recformer evaluation+полныйcheckpoint replay прошли, manual
evaluation завершён, raw15evaluation работает наCPU4 (child4848 припроверке).
Далееfold0 H008/H009, затемfold1/2, verification/report/plots. GPU может быть
свободен наCPU/APIscoring. failure.json от22:52 — старыйCPUfuture, новыхошибокнет.
НЕподстраивать модели/параметры/промпты по уже доступным outer-метрикам.
Финальныхсводныхметрик/графиков ещёнет, отдельныеfoldрезультаты неитогсравнения.

23:12 МСК: H008fold2 завершён (20valid/23ответа, выбранcall4). H009fold2
дошёл до19valid; последнийcall20 получилтаймаут наPOST20 в23:11. Helper1973
автоматически выдержал30сек, переиспользовал19trial и отправилPOST21.
Пользователь вновь перезапустилVPN; responsePOST21 сохранён23:12:10,
preflightcall20 прошёл, идётLightGBM/search. Не считать20valid доtrial.json.
Послеconfirmation helper сам запускает новыйpipeline; весьGPUtrain завершён,
outer-test пока не запускался. ПоследнийживойAPIchild был2793 доretry,
фактическиеPIDперепроверять. Не запускать дополнительныйпоиск.

Проверка22:52–22:54 МСК: GPU-обучение всех3fold завершено; Recformerfold2
имеет complete stage marker (4эпохи). Maincontroller1342 вышел с ранее
сохранённой ошибкой H008, это ожидаемо: егоCPUfuture упал22:27, GPUдоделалработу.
APIhelper1973 и егоchild1986 продолжаютживойпоиск. H008fold2 принялcall23:
теперь20valid/23ответа,25actualPOST (2сетевыхотказа), идётconfirmation/selection.
H009fold2 далее будет выполнен этимжеhelper. ПослеAPIон ждёт выхода1342
(теперьуже вышел), вызываетlaunch.py; готовые этапы переиспользуются,
затем глобальныйpretestбарьер, outer/replay/report. GPU сейчас может быть
свободен закономерно: обучения завершены, следующийGPUэтаппослеAPIпоиска.
Новых сетевыхошибокпослеперезапускаVPN не видно; последниеPOSTfailure005/017.
Read-only аудит4завершённыхAPIarms прошёл22:53:48: selectedхеши, точныеmessages,
20distinctprogram_keyкаждого,17sourcehashes. GNNстатусы всехfold исправлены
поtrained.json. Outer-test пока неоценивался. Не запускать ещё одинcontroller.

Проверка около22:37–22:42 МСК: WSL/PID1342 жив, GPU Recformer fold2
завершил stage1 (2эпохи), начал stage2. GNN/TDM fold2 обучены. APIH008 fold2
дошёл до12valid/15trial, POST17 дляcall16 остановился с connectiontimedout;
CPUfuture основногоcontroller завершился ошибкой, controller ждёт GPU.
Проверка безтокена изWSL получилаHTTP401(сервердоступен), изWindows соединение
неустановилось. Пользователь сообщил о перезапускеVPN; причинная связь не доказана.
Перезапущен helper reports/.../scratch/resume_api_lane.py, PID1973 (перепроверять),
последовательно завершает fold2H008/H009 и ждёт выходаcontroller1342,
затем вызываетCVBenchmark/launch.py для полноценного resume/outer/report.
Helper теперь допускает не более3 последовательных запусков этапа при
transport/HTTP408,429,500,502,503,504 с паузой30сек; 401/лимит300/прочиеошибки
НЕповторяет. Счётчик actualPOST общий сохранённый, старыеответы переиспользуются.
Self-test6checks прошёл, новыхAPI/fit=0 (api_resume_retry_verification.json).
Старая версияhelper сохранена runtime/resume_api_lane_before_bounded_retry.py.
Это изменения только ignored helper; frozenCVBenchmark/runtime/params не менялись.
Первый запуск теста не исполнился из-за сбоя автоapprovalHTTP403; повтор через
тот же механизм согласования успешно выполнен. Блокировкиarm сохраняются.

Проверка22:16–22:18 МСК: WSL ПЕРЕЗАПУСТИЛСЯ (uptime<1мин), все старые
PID2447/3205/10438 исчезли; GPU был свободен. Причина перезапуска не установлена.
Recformer fold1 успешно закончил4эпохи, stage marker имеется. Fold2 IDGNN
имеет trained.json (4эпохи), ContextGNN ещё не начал сохранять свою папку.
H008 fold2 имеет7valid/9trial; response call10 сохранён, model/feature_schema
записаны, search_metrics/trial ещё отсутствуют. Полная копия partialcall10
и прежних process-status сохранена в reports/.../runtime/wsl_restart_2216/.
Незавершённый fit call10 при resume может повториться; APIresponse переиспользуется.
Все17 frozen source hashes совпали. Запущен обычный CVBenchmark/launch.py:
НОВЫЙ pipeline PID1342 (перепроверять). Отдельные старые recovery/resume helpers
запускать НЕ нужно: новый pipeline ведёт обе ветки. pipeline.log append содержит
старые traceback, а failure.json от22:03 — предыдущий transportfailure,
не свидетельство ошибки новогоPID. Проверять свежие строки и процессы.

Продолжение около22:07 МСК: H009 fold1 тоже завершён (20/20, выбранcall1,
confirmation MAP=.004899949036853799). Обе tree-базы fold2 обучены. В H008 fold2
принятыcall1,2,4; call3 корректно отклонён до fit: values от короткого окна z
сопоставлены с MultiIndex полной history h. POST attempt005 для call5 оборван
провайдером: Remote end closed connection without response. Ответа нет,
failure.json сохранён, запрос остаётся в бюджете300. Original controller2447
вышел, записав старый TDM+новый transport failure; GPU recovery3205 и Recformer
fold1 продолжили работу (stage2epoch2). Это НЕ потеря обученных моделей.
В host CVBenchmark/api.py добавлена межпроцессная fcntl-блокировка наarm,
чтобы отдельный resume не пересёкся с будущим автоматическим восстановлением.
Это только оркестрация, модель/данные/промпты/валидация не изменялись.
Старый api.py сохранён runtime/api_before_execution_lock.py, старыйsource_manifest
сохранён source_manifest_before_api_execution_lock.json; новыйhash обновлён.
Проверка actual child lock на завершённом fold0 H008 прошла: child ждал lock,
selected не изменился, новыхAPI/fit=0 (api_execution_lock_verification.json).
Запущен отдельный resume_api_lane.py PID10438 (PID перепроверять), последовательно
доделывает fold2 H008/H009 с reuse всех saved responses. Логи:
api_lane_resume.log/.pid/_status.json плюс stages/f2_h00*_search.log.
Не создавать дополнительные ручные поиски: этот resume держитarm lock.
GPU recovery по завершении GPUлейна вызовет pipeline.main(); APIentrypoints
теперь сериализованы, готовые selected.json переиспользуются без новых запросов.
Outer-test всё ещё не запускался. Helpers находятся в ignored reports/.../scratch/.

Проверка 2026-10-17 21:44 МСК: первый фолд полностью закончил обучение и отбор,
outer-test ещё не запускался. На втором фолде обучены manual/raw15, ID-GNN
(4 эпохи, выбран epoch1), ContextGNN (10 эпох, выбран epoch10), TDM (7 эпох).
Recformer fold1 обучается на GPU (PID8173 на момент проверки); H009 fold1
ищет признаки (PID8207). Основной CPU/API-контроллер2447 и GPU-recovery3205 живы.
H009 fold0: 20/20 приняты, выбран call8, confirmation MAP=.011440098035492771.
H008 fold1: 20 принятых/21 ответ, выбран call14, confirmation MAP=.00783797083648274.
Read-only аудит reports/medium_cv_v2/completed_selection_audit.json прошёл:
в трёх завершённых API-поисках по20 различных program_key, хеши выбранных
программ/моделей совпадают, точная история сообщений проверена (H008 максимум2
сообщения, H009 fold0 максимум14). Все17 frozen source hashes совпадают.
Тестовые метрики аудит не вычислял, новых API/обучений не делал. Скрипт аудита
лежит в ignored reports/medium_cv_v2/scratch/. GNN статусы по trained.json
исправлены на trained_pending_test, validation отражает выбранный checkpoint.
Описание данных/метрик для пользователя: reports/medium_cv_v2/evaluation_explained_ru.md.

Последнеепроверенноесостояние: H008fold0выбралcandidate008поconfirmation
MAP=.007180277081592872 (20принятых/21ответ,searchлидербыл014). НачатH009fold0,
новыйAPIparent4736(перепроверятьPID). Recformerfold0завершилstage1epoch1:
10923строк,527.7секэпоха,searchMAP=.004959753787878787;всегозапланировано4эпохи2+2.
НЕТoutertestметрик. Строкаselectionвlegacyruntimeговоритconfirmation88,
нофактическийselection.json/workerиспользуетновыеconfirmation_usersизconfig;
этостараятекстоваяметка, недействительныйразмер. Считатьпоconfig/metric.users.
ТаймерH008fold0включаеттехническуюSIGSTOPпаузунапроверкусхемы;несравнивать
егокаксобственнуюскоростьLLMсH009,длястоимостииспользоватьтокены/POST.

Доп.проверка:fold0H008достиг20валидныхза21ответ(20-йответотклонён:>36столбцов,
21-йrepairвалиден). ПередконцомconfirmationAPIparent2595краткоSIGSTOP.
Найденлатентныйриск:predictновымпроцессомнеподставлялtrainedschemaвengine.names;
приответесдругимпорядкомколонокмогисказитьсяинференс. Вworker.predictдобавлено
engine.names=model.feature_name() иassertсовпадениясfeature_schema.json.
Fit/предыдущиеsearchнеизменны(тамengineсохраняетnamesизfitвтомжепроцессе).
Синтетическийтестсобратнымпорядкомколонокпрошёл;обеужеимевшиесяconfirmation
оценки(контрольиcandidate014)повтореныТОЧНОсновымworker.47регрессийпрошли.
Результатreports/medium_cv_v2/saved_schema_verification.json;старыйworker
сохранёнвruntime/worker_before_saved_schema_alignment.py,старыеconfig/manifest
сохранены. НовыхAPI/fitкандидатовдляпроверкиНЕбыло(одинуспешныйsyntheticfit,
одинпредыдущийтехническийtestfitдоисправленияWindows/POSIXпутиинвентаря).
Послеуспеха2595SIGCONT,Recformerпродолжалобучатьсявсёвремя. Model/data/параметры
неперенастраивались;финальныйreportтакжетребуетsaved_schema_verificationpassed.

ПослеCUDAfix:fold0TDMзавершён8эпох/349.6сек,выбранcheckpoint;запущенRecformer.
H008первогоfold17/20валидныхбезотказов(проверятьлоги:счётчикменяется).
pipeline.pidтеперьуказываетнаrecovery3205,чтобынедопуститьдублирующийlaunch;
original2447всёещёведётCPU/API. Добавленaudit_numeric.py:вфинальномотчёте
проверяетзначениявсех20trainматрицкаждогоAPIarm/fold(безновыхAPIилиfit),
отдельноотчислаAST-программ. Reportэкспортируетвыбранныеprogram.py,provenance,
APIusageсчисленнымразнообразиемиcosts.csv. Source_manifestактуален;
предыдущиеревизиисохранены. Программымоделей/генерацииприэтомнеменялись.

Продолжение: первыйTDMостановился ДОуспешногоforward/optimizer из-за отсутствия
CUBLAS_WORKSPACE_CONFIGприdeterministic=True. Failedconfig/tree сохраненыв
fold_0/tdm/fixed_failed_before_first_forward_cublas. CVBenchmark/tdm.py теперь
ставит:4096:8доimporttorch. ИсходныйконтроллерWSL2447остаётсясCPU/APIлейном;
отдельныйrecover_gpu.py3205возобновляетGPUлейн, затемждётвыхода2447иповторяет
pipeline.main() сreuseготовыхэтапов. СледитьТАКЖЕзаgpu_recovery.log/.pid,
непутатьстарыестекивappend-логахсновойошибкой. Полеpipeline_status.json может
показыватьпоследнийзаписавшийлейн; stages/*.jsonявляютсясвидетельствомготовности.
ФактическиеPIDперепроверять. H008уже6принятых/6ответов;новыеответыпереиспользуются.
Дофинальногоотчётадобавленыguards:все7семействverification.jsonкаждогоfold
обязаныpassed; APIusageявнопоказываетвыбранныйcallилиconstantcontrol.
Этоотчётность, неперенастройкамоделей;манифестыревизийисточниковсохранены.

Фактическое продвижение после smoke: fold0 LightGBM manual/raw15 обучены,
IDGNN/ContextGNN обучены (151.5с включая загрузку/подготовку), начатTDM fixed.
H008 APIпоток запущен; первые2ответа приняты и обучены,3-й прошёлpreflight.
Этоsearch, неoutertest. ПриповторномGPUsmoke былнайден cache/schema bug:
get_stype_proposal семплирует1000строк безseed и мог поменятьтипколонки при
загрузкестатистиккэша. ДоAPI/fit исправленыseed42доinfer иinferпрошлогоdb;
новыйcache/gnn_seeded_past_v2. Исправленныйsmoke иполноеобучениеизкэша прошли.
Старыйотказ/манифесты сохраненывreports/medium_cv_v2/preflight_failure_cached_schema.json
иsource_manifest_before_seeded_schema_fix.json. RecformerGPUsmokeуспешен;
егоунаследованныйprobeestimated_4epoch... используетстарое4804 иНЕ является
оценкойновогообучения; корректнаягрубаяоценкапересчитанавtiming_estimate.json.

Пользователь вернулся и поручил продолжить сравнение9 методов. Код: CVBenchmark/.
Главный запуск: hm_medium_temporal_cv_v2; журнал reports/medium_cv_v2/pipeline.log,
машинный статус pipeline_status.json, этапы stages/*.json/*.log. Реальные процессы
проверять по pipeline.pid (WSL), не считать историю доказательством живого процесса.
Оркестратор запускается CVBenchmark/launch.py родным RelBenchGNN/.venv-wsl/bin/python
без audit_deps/NumPy2. Окружения и старые результаты не менялись.

Новая версия данных data/hm-cv-medium-v2 сохраняет20000 пользователей/10000 товаров,
но НЕ удаляет контрольных пользователей с покупками только вне каталога и НЕ
обрезает знаменательAP. Их цели имеют стабильныеID>=10000, предсказания0..9999.
Outer1839/1982/1698 пользователей(5519 наблюдений), прежний v1 сохраняется отдельно.
Пользователю объяснено: вне каталога верно угадать невозможно; первичная метрика
оценивает систему с ограниченным каталогом, отдельная conditional_catalog_map
показывает ранжирование покупок в каталоге. Все методы имеют одинаковые условия.
Тренировочные пары общие:190260/166670/148100 на6 недель каждого фолда.
Search256 пользователей; confirmation20% полногоinner-val, heldout20% невыбирающий.
GNN-препроцессинг транзакций теперь fit до первогоtraincutoff, transform поздних
строк тем же преобразователем; без50stepcap,10эпох/patience3. Stable score ties.
Recformer прежний2+2эпохи/1e-5/warmup100/linear schedule поразмеруfold;
TDM fixed beam64, безcluster/full; LightGBM150/31/4CPU.
H008/H009 независимо накаждомfold:20валидных/300POST/3repair/3популяции;
оба без автоматическихraw15, Python, hasattr исправлен одинаково. ТолькоGPTAPI,
никакихQwen/Llama. H009полнаясвояистория, H008лучшийкодпопуляции.

До запуска прошли47валидационныхпроверок fold0/fold1 иGPUforward/backward
IDGNN/ContextGNN накаталоге10000. Pipeline повторяетпроверкивсех3folds иRecformer
GPUsmoke до API. Два ресурслейна:GPUпоследовательно, CPU/APIпоследовательно;
outertestбудет посчитан только после выбора всехмоделей всехfolds.
Исходники фиксируются source_manifest.json; не менять их подживымзапуском.
Итоговый отчёт создаст CVBenchmark/report.py: foldтаблица, pooled/equal-fold MAP,
парный customer-clusterbootstrap,36исследовательскихсравненийсHolm и графики.
3временныхблока/1seedнеоцениваютустойчивостьксеменам; неделатьбезусловныйвывод
«идеяхорошая/плохая»толькопопобедителюсреднейметрики. Пока итоговыхметрик НЕТ.

## Medium temporal CV: отложено пользователем (2026-10-17)

Пользователь поручил увеличить подвыборку H&M и сравнить кросс-валидацией девять
методов: LightGBM manual/raw15, IDGNN, ContextGNN, Recformer zero-shot/LR warmup,
TDM fixed beam, API GPT H008/H009. Qwen/Llama не запускать. Затем пользователь
сообщил, что уходит и вернётся к задаче позже. Новое обучение/API не запускались.
Созданы CVBenchmark/PROTOCOL.md (предварительный протокол), prepare.py и probe.py.
Подвыборка data/hm-cv-medium-v1:20000 покупателей вне прежнего small-v1,
10000 товаров; состав выбран по истории до2020-06-29. Три временных фолда,
по6 train-недель: train/val/test10923/1410/1276,9583/1301/1191,8548/1069/873.
Тестовые cutoff2020-08-17/08-31/09-14; всего3340 test user-times.
Манифест и отчёт подготовки: reports/medium_cv_v1/dataset_summary.json.
Критичное наблюдение ДО обучения: неподвижный июньский каталог покрывает лишь
46.47%,35.16%,28.52% будущих уникальных покупок по outer-фолдам; исключены
563/791/825 пользователей без целей внутри каталога. Перед возобновлением
пересмотреть дизайн каталога/сохранение исходных целей и знаменателей метрики,
чтобы отбор сохранившихся целей не давал вводящую в заблуждение оценку.
Исходные данные и старые результаты не менялись; адаптеры девяти методов,
проверки и оркестратор ещё НЕ созданы. Не называть CV запущенной/завершённой.
Нейросети планируются наRTX3060 6GB последовательно; LightGBM/признаки CPU,
GPT у провайдера. Проверенный WSL RelBenchGNN/.venv-wsl:torch2.2.2+cu118.
Не подключать audit_deps NumPy2 к нейросетям: torch2.2 требует совместимый
родной NumPy; probe с общим PYTHONPATH показал предупреждение ABI. Сам prepare.py
успешно выполнен в родном окружении без overlays. Процессы перепроверить после паузы.

## H009: API-поиск с полной историей сообщений завершён (2026-10-17)

Run hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0:24 POST,20 принятых
программ,18 численно разных наборов (16/20/23 одинаковы по значениям).
4 отказа:3 ошибки/нарушения контракта программы,1 ограничение хоста hasattr.
Выбран6:search2.916202%,confirmation1.674032%,heldout1.984728%,
validation2.286989%,test0.721596%. Прежний H008:validation1.478563%,test1.426760%.
Разница test -0.705165п.п.; парныйuser-bootstrap95%[-1.366352;-0.154258].
Это один стохастический поиск с ранее просмотренным test; не универсальный вывод о памяти.
Полная история24 запросов независимо проверена:только своя популяция, все assistant
ответы,search-feedback и ошибки;confirmation/test не попадали в сообщения.
Максимум18 messages/38143 входных токена; всего385823 input против55261 вH008 (~6.98x).
Первый API-payload побайтно одинаков сH008, но ответы отличаются:seed не гарантирован.
Новые валидатор/LightGBM не менялись. Аудит пройден, общий график/контекст/гистограммы:
reports/provider_history_v1/report.md. В истории статус complete.

Пользователь поручил передавать историю сообщений, как в чате. Новый поток
gpt-6.1-sol через https://tooken.club/v1, три отдельных диалога:
все прошлые user/assistant и search-feedback своей популяции, включая отказы.
Условия H008 без автоматических raw15 сохранены,20 валидных/до300 POST/3исправления.
Никакого обрезания истории; входных токенов больше, окно провайдера не аттестовано.
Run hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0. Логи/статус проверять
через reports/provider_history_v1/current_run.json и реальные процессы.
13 проверок dialog/mock-адаптера пройдены; движок,worker,prompting точно H008,
поэтому33 проверки валидатора переиспользованы по совпадению хешей.
Протокол LLMFeatures/HISTORY_API_PROTOCOL.md; runner run_provider_history.py.
Финальные метрики и аудит всей истории messages получены.
При попытке15 обнаружено ограничение хоста: разрешённый AST не запрещает hasattr,
но restricted builtins его не содержит. Отдельная копия с единственным добавленным
hasattr проходит preflight и совпадает с принятым16 на всех72813train-парах.
Исходный H009 runtime не менялся для сопоставимости H008. Диагностика без обучения/API:
reports/provider_history_v1/host_builtin_diagnostic.json. Не считать этот отказ ошибкой
обычного Python модели; перед будущим протоколом исправить/явно описать namespace.

## H008: API-поиск без автоматических raw15 завершён (2026-10-17)

Аудит пройден. Run hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde.
23 фактическихPOST,20 валидных программ,3 отказа preflight,0HTTP ошибок.
19 наборов значений train-признаков без учёта порядка столбцов:9/16 совпадают
по значениям, но программы и порядок столбцов отличаются. Дедупликация при поиске
была AST как H006; численные дубликаты выявлены отдельным аудитом.
Выбран ответ12: search2.162423%,confirmation0.973514%,heldout0.988907%,
validation1.478563%,test1.426760%. Всего25 f_* входов:18 исторических признаков
и7 явных копий статических полей по решению модели. Автоматически raw15 не добавлялись.
Прежний H006test1.357362%; разница+0.069399п.п.,user-bootstrap95%[-1.034078;1.273127].
Доказанного улучшения нет. Только один стохастический поиск/seed и ранее просмотренный test.
33 проверки до API; аудит20 схем/матриц,метрик и6 replay пройден,3отказа воспроизведены.
Отчёт, общий график и гистограммы: reports/provider_generated_only_v1/report.md.

Пользователь подтвердил запуск GPT-6.1 Sol через API с только возвращёнными f_*
признаками на входе LightGBM. 20 валидных программ/до300 POST/3 исправления,
три популяции, те же small-v1 72813 пары, LightGBM150/31/4CPU/seed42.
Память прежняя best-only; контроль одна константа вместо raw15. H006/H007 сохранены.
Протокол LLMFeatures/GENERATED_ONLY_PROTOCOL.md; новый runner
LLMFeatures/run_provider_generated_only.py. Текущий run_id и фактический статус:
reports/provider_generated_only_v1/current_run.json и логи/реальные процессы.
Итоговые метрики и аудит получены; в истории статус complete.

## H007: итоговый скоринг выполнен 2026-10-17

Ровно20 наборов сохранены. По confirmation выбран набор9 (не search-лидер8):
confirmation MAP@12 1.053248%, validation 1.260603%, test 2.231032%.
Это признаки текущей сессии плюс15raw; автор знал историю, поиск не является слепым.
Скоринг и шесть frozen replay завершились; дополнительный аудит пройден (audit.json:
passed). Итоговый отчёт и общий график находятся в reports/authored20_v1.
Унаследованный API efficiency_report упал после скоринга из-за отсутствия ключа
target_successful_distinct в конфиге не-API запуска. Выходы проверены отдельным
finalize_authored20_outputs.py; frozen config/код/модели не изменялись.
Промпт для отдельного чата: LLMFeatures/FRESH_CHAT_FEATURE_SEARCH_PROMPT.md.
API-эксперимент только со сгенерированными признаками завершён отдельно как H008.

## H007: текущая сессия Codex — ровно20 наборов, адаптивно по3популяциям

Пользователь подозревает подмену модели у провайдера и поручил этой сессии самостоятельно
написать и оценить ровно20 наборов признаков. Подтвердить точную модель ни этой сессии,
ни провайдера по метрикам невозможно; это сравнение результатов, не аттестация модели.
Пользователь явно потребовал адаптивный поиск по трём популяциям. Первоначальные
неоценённые20 черновиков не являются расписанием: никаких метрик/обучений по ним не было.
Фиксируются отдельные решения до search-оценки; родитель — лучший search своей популяции
или raw, порядок0/1/2, всего7/7/6. Ровно20 новых LightGBM, контроль переиспользуется.
Данные/LightGBM/seed/пулы как H006:72813пары,150rounds/31leaves/4CPU,search128,
top3+raw→confirm88, затем frozen heldout88/val304/test250/все5000товаров.
Никаких внешних API, .env не читается. Контекст этой сессии и объём кода отличаются
от провайдерских2048outputtokens; прошлые результаты известны, test ранее просмотрен.
Протокол LLMFeatures/AUTHORED20_PROTOCOL.md; run_authored20.py,author_step.py,
authored20_proposals/NNN.json. Текущий запуск hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9.
Состояние проверять по state.json/реальнымпроцессам, не считать завершённым до20и независимого аудита.

## Итог H006: Python / GPT-6.1 Sol (2026-10-17)

H006 завершена и независимо проверена: Python test MAP@12 1.357362%, validation 1.079708%; SQL 0.979030%, прежний Qwen7B 1.107143%, raw 0.959630%. 20 оценённых программ, 22 фактическихAPIPOST в одном потоке; отказовкода 1, дубликатов 0, ошибокAPI 1. v1 сохранён, исправлениеv2 выполнено до итогового выбора/test без повторной генерации первых8ответов. 29 регрессий, дополнительный разбор всех ответов и независимые SQL эталоны пройдены. Численно различных train-матриц 18 из20; confirmation-кандидаты численно различаются. Все12признаков победителя выраженыSQL и дают точно те жеfloat32 значения на всех72813train-парах. Одинseed/250ранее просмотренныхtest пользователей; это диагностическое сравнение, не воспроизведение статьи.

Отчёт: reports/gpt61sol_python_v1/report.md; сравнение, графики, гистограммы и разбор валидатора рядом.


## H006 — GPT-6.1 Sol: полная Python-функция



2026-10-17. Пользователь поручил проверить полный Python и отдельно проверить корректность валидатора.
Те же small-v1 72813 пары, LightGBM150/31/4threads, seed42; 20 оценённых программ / до300 POST,
3 популяции / до3 исправлений, модель и sampling как H005. Интерфейс modify_features(X, history),
до36 новых числовых признаков + raw15, полный pandas/NumPy без I/O/случайности.
Физически прошлая история и исходные атрибуты; test/labels не доступны функции.
Search128 → top3+raw → confirmation88 → frozen heldout88/val304/test250/all5000.
Промпт содержит рабочий пример, полную схему и лучший предыдущий код с search MAP.
До запуска модельных генераций проверяются валидатор, сопоставление ID/строк, batching,
raw совпадение и числовые pandas/SQL ответы. Реальные отказы требуют отдельного разбора:
валидность и качество не одно и то же, ложные отказы не считать ошибками модели.
Прошлый test просмотрен; повторная оценка, один seed, интерпретировать осторожно.
Подробности: LLMFeatures/PROVIDER_PYTHON_EXPERIMENT.md. Старые эксперименты сохранены.


## Итог H005: GPT-6.1 Sol / полный SQL (2026-10-17)

Реальный API эксперимент завершён: 26 оплачиваемых запросов, 20 оценённых наборов.
Независимая проверка обоих вариантов оценки прошла, включая frozen inference raw/GPT × val/test.
Test MAP@12: GPT 0.979030%, raw15 0.959630%, прежний Qwen7B 1.107143%,
ручные признаки 1.233880%, ID-GNN 2.653413%, ContextGNN 3.015575%.
Улучшение качества не подтверждено; bootstrap интервалы разниц включают ноль.
Один seed, 250 test пользователей, ранее просмотренный test; прежний Qwen использовал JSON,
а GPT полный SQL, поэтому эффект модели отдельно от интерфейса не установлен.

Обнаружен наш ложный отказ AND в SQLGlot allowlist. Исходный запуск сохранён.
Исправленная оценка первых 20 валидных программ сохранённого потока заняла первые 24 ответа
(4 дубликата, 0 отказов), без дополнительных API вызовов; всего реально вызвано 26.
Выбран тот же candidate_004: 20 новых числовых признаков + 15 исходных полей, LightGBM 150 деревьев.
Исправленный replay не является независимым LLM экспериментом и сохраняет исходную историю промптов.
Отчёт: reports/gpt61sol_small_v2/report.md; графики и гистограммы рядом.
Исходный отчёт: reports/gpt61sol_small_v1/report.md. ZIP обоих запусков в LLMFeatures/results.
Исправлен также отдельный Kaggle full SQL v2 ноутбук Qwen; CPU regression пройден,
реальной Qwen генерации в нём пока нет. Токен не сохраняется в артефактах.


## H004: подготовлен полный SQL-интерфейс Qwen7B (2026-10-17)

По поручению пользователя подготовлен отдельный Kaggle T4 ноутбук Qwen7B full SQL: обычные SELECT/WITH без JSON,host проверяет и присоединяет числовые таблицы признаков. Те же72813пары/LightGBM150/31/4threads/3популяции/20успехов/300calls/3repair. CPU smoke с заданными SQL ответами прошёл,rawконтроль byte-identical, CTE/quantile/window/pandas/future exclusion/ключи/routing/resume/replay/ZIP проверены. Реальной LLM-генерации нет; GPU запустит пользователь.

Ноутбук LLMFeatures/kaggle/hm_small_qwen7b_full_sql_kaggle_t4.ipynb, Input прежний hm_small_sql_compare_v1.zip. До6SELECT/36числовыхвыходов,CTE/joins/windows;политикаduplicate/unchangedкакH003C,ноASTдедупиной.Физически past-onlyhistory в отдельной DuckDB,нетtx/целей/кандидатов/файлов.Final joins/raw encoding прежние,worker.py byte-identical. SQLпрограммысохраняютсявprogram.sql,внутреннийprogram.jsonсоздаётhost.Модель pinned Qwen2.5-Coder-7B-Instruct NF4/FP16/T4/seed42;input6144/output2048,search128/confirm88/heldout88,val304/test250/catalog5000.Testранее просмотрен;повторнаяоценка,никакогоотборапоtest. Изменениепространствапрограмм/лимита36вместо24+12/дедупаобъявлено. Старые ноутбуки/результатынеизменены;оценокреальнойQwenfullSQLещёнет.


## Проверенный результат H003 (2026-10-17)

H003 полностью проверен: A65/36/9,B78/21/37,C51/15/16 (calls/reject/duplicate), каждый20успехов. Cпротивконтроля67calls:на23.9%меньшеобращений,44.88против46.42мингенерации. TestMAP A0.751212/B0.873593/C0.888745% противстарогоQwen7B1.107143% иraw0.959630%; качество не улучшилось. Все4модели×val/test frozenreplayсовпали. A21–23derivedагрегациипропущеныдиагностикой,остановленыpreflight. 9WITHINGROUPвыраженийоказалисьневалиднымquantile_contдиалектом,ложныхотказовсрединихнет. Одинseed250test,повторнаяоценка;всеbootstrapинтервалыразницывключают0.

ИсходныйZIP hm_small_qwen7b_h003_v1_6852748fc0e4_results.zip сохранён;sha256 3745ab14e576e7b179b764f1822014fecd29c7ec3da398ac3edae5743a46b5cf. Независимыйаудит reports/h003_small_v1/audit.json,report.md,5PNG;старыеотчёты/ноутбукинеизменены. ВыбранныеB/Cагрегатытолькоcustomer_id;raw_i_*остаются,причинностьнизкогоMAPнеустановлена. КонтекстA2787/B3148/C3579,обрезаний/переполнений0. H003Cоперационноэкономнее,ноустойчивый/причинныйэффектнеустановлен;H003Aнеулучшилаотказы,H003Bуменьшилаотказыноувеличиладубликаты.


## H003: новый Kaggle-ноутбук Qwen7B

По поручению пользователя подготовлен LLMFeatures/kaggle/hm_small_qwen7b_h003_kaggle_t4.ipynb.
Protocol hm_small_qwen7b_h003_v1. Default ARMS h003a/h003b/h003c = A/AB/ABC;
три независимых поиска20успехов/300обращений/3repair/3популяции каждый.
Одна загрузка Qwen7B NF4 наT4, pinned c03e6d358207e414f1eca0bb1891e29f1db0e242.
A адресная диагностика всех features/EXPLAIN пустойсхемы; B добавляет примеры;
C адресные дубликаты/прекращение неизменённого repair. Автоисправлений нет.
Input прежний hm_small_sql_compare_v1.zip;72813пар,LightGBM150/31/4threads,
search128/confirm88/heldout88,val304/test250/catalog5000. Features/worker/original_prompt
байт-в-байт прежние. Контроль прошлый Kaggle Qwen7B; сравнивать A→B→C.
Все selection доtest; test ранее просмотрен, оценка повторная. Старые ноутбуки не менялись.
CPU smoke с заданными ответами/3раундами пройден отдельно, без LLM-генерации.
Проверка67историческихответов:30отказов диагностированы,37valid/duplicate приняты.
Проверены routing/repair/duplicate/unchanged/resume,full5000,метрики/references/
frozen replay/графики/ZIP. reports/kaggle_llmfe_validation/h003_small_v1/verification.json.
Реальный H003 наGPU ещё не запускался; пользователь запустит вKaggle.


## Выбрана Qwen7B: разбор ошибок генерации (2026-10-16)

Пользователь выбрал Qwen2.5-Coder-7B-Instruct. Разобраны67реальныхответовsmall-v1: 20валидных/30отказов/17дубликатов;JSON67/67,обрезаний0. Первыеошибки9строковыхрезультатов,8OVER,6keys, 4history-в-derived,2SQLsyntax,1ID-в-derived. У18ответов несколько проблемныхfeatures;13/40repair возвращаютнеизменённуюпрограмму(7отказов,6дубликатов).9/17дубликатов=candidate001. Сохраненывсеошибкипоfeatures/цепочки/примеры/promptaddendum/repairtemplate;SQLпримерыEXPLAIN-проверены DuckDB1.4.1насинтетическойсхеме. Нетгенерации/обучения/переоценкиMAP/измененийрабочихноутбуков. H003A/B/CвHYPOTHESES.md предложены,не запущены. Устойчивое превосходство7Bне доказано;testуже просмотрен.

Источник:small-v1/qwen,не смешиватьсошибкамиLlama/v5. Приоритет:адресныеспискиошибоквсехfeatures; затемотдельнопримерыprompt;затемduplicate/unchanged. SQLJSONсохранитьдляпервогосравнения. Рабочиеметрики/ноутбукине менялись;H003ещёнепоручензапускать.


## Проверенные реальные Kaggle результаты трёх LLM на small-v1 (2026-10-16)

Оба ZIP проверены,все60программ. Qwen7Btest1.107143%,Llama8B0.780337%,Qwen14B0.743306%; Raw0.959630%,manual1.233880%,ContextGNN3.015575%. У14B45calls против67/201,но генерация71.61мин против46.42/262.10мин. Выбранные14B/Llama historyагрегатытолькоcustomer_id;Qwen7B включаетcategory/customer×department;причинностьне установлена. Report/таблицы/5PNG/bootstrap10kготовы. Одинseed250test,точечныйпорядокне доказываетустойчивоепревосходство. ИзначальныйWSLстекотклонилnullableboolLlama;точныеCPUверсииKaggleустановленыизолированновaudit_deps,старыеenvне менялись. 4модели×val/testreplayточносовпали. Никакогообучения/измененияисходныхZIP.

Исходные архивы hm_small_qwen_llama_sql_v1_2ecc60d61fd4_results.zip и hm_small_qwen14b_sql_v1_f373011050bf_results.zip сохранены.
Конфиги/версии/T4/4sharedsourceSHA совпали. Data:72813train/4804user-time/8cutoffs,search128/confirm88/heldout88,val304/test250/5000catalog.
Обаrawконтроля идентичны по моделям и прогнозам. Выборtop3+rawпоconfirm проверен;тест не использовался для переотбора.
CPU audit versions:numpy2.1.3,pandas2.3.3,pyarrow23.0.1,duckdb1.4.1,lightgbm4.6.0. Файлы и первоначальные failurelogs в reports/hm_small_llms_v1.
ПрежнейPandasIDошибкинет:joinsownedbyhost;проверкиперестановки/блоковпрошли. Raw item features присутствуют у всех.
Отчёт reports/hm_small_llms_v1/report.md,audit.json,comparison_all_methods.csv,search_efficiency.csv,paired_test_bootstrap.csv;5PNG.
НовыеKaggleрезультатыне smoke;локальныеfakefixturesотдельно. Не сравнивать малыйкаталог со старымполнымH&M/статьёй.

Qwen7B_LightGBM: val/testMAP=0.77717969%/1.10714286%,calls67,selected5,statuses{'valid': 20, 'rejected': 30, 'duplicate': 17}.
Llama8B_LightGBM: val/testMAP=0.84396004%/0.78033670%,calls201,selected144,statuses{'rejected': 181, 'valid': 20}.
Qwen14B_LightGBM: val/testMAP=1.21120945%/0.74330579%,calls45,selected14,statuses{'rejected': 12, 'valid': 20, 'duplicate': 13}.


## Завершённый TDM small-v1 fixed/cluster (2026-10-16)

Оба опыта завершены: fixed7эпох/best3,cluster6эпох/best2;patience4.
Fixedbeam val/testMAP1.016010%/1.395195%;fullleafтемижевесами0.934150%/1.002919%.
Clusterbeam0.745875%/0.551263%;fullleaf0.672455%/0.466389%.
Обучение+val188.61с/132.85с,кластеризация13.29с,peakallocatedCUDA102302720bytes
(~97.6MiB)уобоих. Восемьнезависимыхreplayсовпалиточнопоscores/top12/AP/traces;
дополнительныйаудитпрошёл,обаselectionдоtest,pipeline.exitcode0,триPNGпроверены.
Testbeam7.86/7.18с,full5.49/5.26с;~986/988scorednodesпротив5000.
Этоодиночныепрогонысзагруженноймоделью,неповторныйбенчмаркскорости.
Cluster−fixedbeamtest−0.84393п.п.,pairedbootstrap95%[-2.14275;+0.21911]:
точечныйрезультатниже,ноустойчивыйэффектперестройкинеустановлен.
Одинseed/250test;локальнаяадаптацияTDM,неJTM/неметрикистатьи.
Отчёт reports/tdm_small_v1/report.md,report.json;sourceснимокв
TDM/results/hm_small_v1/source;старыеартефакты/пакеты/unslothнеизменены.

Пользователь поручил начать fixed-treeTDM, сравнитьbeam/fullleafтемижевесами,
затем отдельно проверить перестройку по embeddings. Протокол TDM/PROTOCOL_SMALL.md,
runner TDM/run_small.py, pipeline TDM/run_pipeline.sh. Новые runIDs:
hm_tdm_small_fixed_seed42_v1 и hm_tdm_small_cluster_seed42_v1.
Это явная локальная адаптация TDM в прежнемtorch2.2.2; штатныйTorchEasyRec
не устанавливается,пакеты/unslothне меняются. Small-v1/4804/304/250/5000каталог,
историяpast-only50покупок,attention36/emb24/MLP128-64-24,positionalwindows50,
weeklymulti-positivebalancedBCE,до8негативов/уровеньс исключениемвсехпозитивных
предков,Adam.001/batch32/seed42,до20эпох/patience4/min5/15минбюджетна модель.
Beam64MAPпоvalвыбираетcheckpoint,fullleafдиагностический. Сначалаобаобучения
иselection_pretest,затемtestобоих. Clusterизсобственныхfixedbestleafembeddings,
balancedKMeans2,n_init10;новаямодельснуляseed42,неJTM. Отдельныйsmoke,
восемьнезависимыхreplayоценок,новыйотчёт reports/tdm_small_v1.
Фактическийстатуспроверятьпопроцессам/логам TDM/logs/small_v1.

## Изучение TDM/JTM перед следующим заданием (2026-10-16)

По запросу пользователя изучены arXiv1801.02294v5(TDM),1902.07565v2(JTM),
XDLwiki и реальные исходники Alibaba x-deeplearning/TorchEasyRec.
Отчёт reports/tdm_assessment/report.md; источники/APIдеревья/SHA в sources/.
TorchEasyRec4458f1c66f6c32dc672b9c805855f3d2e6e6179e имеет модель/sampler/
build/cluster/retrieval/localParquetpipeline; XDL a710108d4457f01992bf0b3b9b6c0f78fdb8e642
тоже имеет TDM,но старый стекPython2/MXNet/HDFS/C++. Готовый JTM в проверенных
модулях НЕ подтверждён: KMeansперестройка TDM не равна objective-based
назначению JTM и истории через предков на соответствующем уровне.
Подходит как отдельный рекомендатель/генератор кандидатов. Нужны past-only
user-time истории, недельные multi-positive цели/исключениевсехпозитивных
предковизнегативов, нашMAP@12вместопопаданияодногоitem, полныйкаталог,
повторыразрешены, checkpoint+дерево+mapping, независимыйreplay.
windows_lenвTorchEasyRecпозиционные,недневные. На5000товарахускорение
негарантировано;предложеныfixedTDM,отдельноclusterTDM,затемJTM;
beamvsfullleafконтрольтойжемодели. Текущийmasterтребуетдругойстек
(torch2.14/TorchRec/FBGEMM/GraphLearn);отдельноеокружениеилиявныйперенос.
Ничегонеустанавливалось/необучалось,старыеокружения/результатынеизменялись.
Следующийэкспериментещёнепоручен.

## Kaggle: отдельная Qwen14B на прежнем small SQL протоколе (2026-10-16)

Пользователь сообщил,что Qwen7B/Llama notebook уже работает вKaggle;
результатов ещё нет,не повторять их запуск. Новый отдельный notebook
LLMFeatures/kaggle/hm_small_qwen14b_sql_kaggle_t4.ipynb готов для параллельного
KaggleT4 запуска Qwen/Qwen2.5-Coder-14B-Instruct,NF4/doublequant/FP16,
безодобренияHF/токена. Runprotocol hm_small_qwen14b_sql_v1,пока notebook_ready,
не реальная оценка14B. ПикVRAM не измерен,контекст приOOM не сокращаетсяавто.
Исходный работающий notebook и Input hm_small_sql_compare_v1.zip не менялись.
4sharedмодуля побайтово взяты изнего; добавлен только runtime14 reportadapter.
Те же72813trainпар/4804user-time/8срезов; search128/confirm88/heldout88,
val304/test250/все5000товаров;SQLJSON24/12,raw15,LightGBM150/31/4threads,
seed42,temp.8,tokens6144+2048,20success/300calls/3repairs/3islands.
Метрики/предсказания/графики/гистограммы/программы/models/frozenreplay/ZIP
сохраняются отдельно. По последнему уточнению НЕ импортировать выводы
7B/Llama в14B notebook: пользователь пришлёт отчётытрёхLLM длялокального
сравнения позже. Input только прежний архивмалыхданных.
Проверены nbformat/AST,configs/начальныйprompt/sharedSHA/неизменностьInput
и одномодельныйотчёт с7baseline+Popularity наfrozenCPUfixtures. Это НЕ
метрики14B,новогоLLMинференса/обучения дляпроверки не было. Verification:
reports/kaggle_llmfe_validation/qwen14_small_v1/verification.json.
README/manifest/buildercheck вLLMFeatures/kaggle/qwen14_small.


## Recformer: завершённый длинный опыт (2026-10-16)

Пользователь поручил проверить большее число эпох. Новыйrun:
hm_recformer_small_long_floor_seed42_v1; runner Recformer/run_long.py,
pipeline Recformer/run_long_pipeline.sh,протокол Recformer/PROTOCOL_LONG.md.
Все148Mвесаизтогожеpretrained,small-v1/seed42/256tokens/batch4accum4/weeklyloss
сохранены. Stage1=2эпохи,stage2<=6,patience3поglobalbestval после>=4общихэпох.
LRwarmup100updatesдо1e-5,decayдо1e-6кupdate1204,затемconstant1e-6.
Matchedкороткийконтроль:неизменяемая копияbest первых4эпох внутриЭТОГОзапуска;
прежний4эпохrunсdecayк0неподходиткакmatchedконтроль. Длинныйbestвыбирается
изsupersetдо8эпох;valbestпоопределениюнеубывает,пользасмотритсянаtestпосле
фиксациидвухрешений. Epoch0 допустимотдельно. Trainingbudget45минплюсрезерв
наeval/replay;общийориентирчас. Пакеты/прежниеrunner/результатыне меняются.
Результаты Recformer/results/hm_small_long_floor_seed42_v1,
логи Recformer/logs/long_v1,отчёт reports/recformer_long_v1.
Завершён с pipeline.exitcode=0: фактически 5 эпох (2+3), остановка
stage2_patience3 после трёх эпох без улучшения лучшего validation.
Короткий контроль (выбор среди первых 4 эпох) и длинный (среди всех 5)
выбрали одинаковый checkpoint stage1/epoch2, SHA256
ba88a315d56816dabb226ca5e46ed416dcbeba803cc103db9cdf0af529046ef1.
У обоих val/test MAP@12=3.578065%/3.438889%; дополнительные эпохи
не изменили выбранную модель в этом запуске. Это не общий вывод о числе эпох.
Обучение+validation 1227.21с (20.45мин), 1503 успешных updates/2 AMP skips,
пик памяти 3.19GiB. Все 6 независимых val/test replay точно воспроизвели
scores/top12; zero-shot совпал с прежним. Все три PNG визуально проверены.
Прежний LR/warmup опыт (test 3.857513%) отличается расписанием LR и служит
отдельным ориентиром; его разницу нельзя приписывать только числу эпох.
Один seed, 250 test пользователей; устойчивое превосходство не установлено.
Перед новым обучением проверять реальные процессы/логи, а не только этот статус.

## Recformer: две завершённые отдельные абляции (2026-10-16)

Пользователь поручил сначала меньшийLR/warmup,затем отдельно заморозку.
Протокол Recformer/PROTOCOL_ABLATIONS.md, runner Recformer/run_ablations.py,
pipeline Recformer/run_ablations_pipeline.sh. Run IDs:
hm_recformer_small_low_lr_warmup_seed42_v1 и
hm_recformer_small_freeze_lower6_seed42_v1. Первый: peakLR1e-5,100успешных
optimizer updates warmup,линейныйdecayза1204updates;все веса обучаются.
Второй: прежнийconstantLR5e-5,замороженыembeddings+нижние6из12слоёв.
Оба независимо стартуют изpretrained,small-v1/seed/order/2+2эпохи сохранены.
Завершены последовательно;test обоих только после обоих обучений иvalвыбора.
Zero-shot epoch0 допустим вselection.json; лучшийtrained сохраняется отдельно.
Старыйrunner/результаты ипакеты не менялись. Итоги: LR/warmup val/testMAP
3.554340%/3.857513%,1093.30с(18.22мин),пик3.19GiB;freezeнижних6+embeddings
1.984810%/1.761558%,782.34с(13.04мин),пик2.13GiB. Лучшийtrained обоих:
стадия2,эпоха2. Поvalсдопустимойэпохой0выбраны:LR→finetuned,freeze→zero-shot;
selection_pretest.json записаны доtest. Обучаемыхпараметров148110336/53157888,
замороженных0/94952448. SHA замороженных совпали;AMPskips3/0,updates1201/1204.
Все8val/testreplayточносовпалипоscores/top12;zero-shotточносовпалсстарымконтролем.
pipeline.exitcode=0,verificationpassed;comparison/learning_curves/learning_ratesPNG
визуально проверены. Отчёт reports/recformer_ablations_v1,логи Recformer/logs/ablations_v1.
LR/warmup−старыйfine test+2.621958п.п.,pairedbootstrap95%[0.59927;4.81070].
Противzero-shot+0.55697п.п.,95%[-1.05193;2.20969];противContextGNN+0.84194п.п.,
95%[-0.92051;2.72223]:устойчивое превосходство над ними не доказано.
Концентрация рекомендаций снижена:уLRtest1757различныхtop12товаров,maxitemshare5.6%,
уfreeze1104и28.4%,у прежнегоfine600и54.8%. Одинseed/250test,LR+scheduleизмененывместе.
На вопрос пользователя о числе эпох пояснено: отдельный более длинный опыт
имеет смысл,т.к. прежнийstage2val ещё рос;нынешний2+2бюджет сохраняется ради
сопоставимости. Пользователь согласился с этим разделением; более длинный опыт
в рамках этих двух запусков не проводился.

## Kaggle: одинаковый SQL-поиск Qwen и Llama на small-v1 (2026-10-16)

По поручению пользователя создан отдельный Kaggle T4 notebook
LLMFeatures/kaggle/hm_small_qwen_vs_llama_sql_kaggle_t4.ipynb и Input
hm_small_sql_compare_v1.zip (~0.9MB). Прежние notebooks/результаты сохранены.
Протокол hm_small_qwen_llama_sql_v1, статус notebook_ready, реального нового
запуска Qwen/Llama ещё нет. Модели Qwen/Qwen2.5-Coder-7B-Instruct и официальная
Llama3.1-8B-Instruct (с выбором публикации unsloth), последовательно NF4/FP16.
Ранее локальная Qwen была Q4_K_M/Ollama; это явное изменение квантизации.
Интерфейс прежней Qwen: JSON aggregates{name,keys,sql}/derived{name,sql},
host владеет joins/порядком/фильтром t_dat<=cutoff. Ограничений по грамматике
при генерации нет. Согласованная factorize товарных категорий в raw/history
устраняет огромные sparse categorical bitsets (smoke174MB→1.3MB model.txt).
Данные неизменные ContextGNN small-v1:5000users/items/46442tx,
72813исходныхtrainпар/4804user-times/8срезов; SHA ключей/меток совпал manual.
Оценка всех5000товаров, val304 делится128search/88confirm/88heldout seed42;
test250 только после фиксации обоих победителей. Top3+raw наconfirmation.
Каждой LLM20успешных/300calls/3repairs/3islands/1best-in-island; LGB150/31,
4threads/seeds42. Общийval содержит search/confirm, baseline выбирались на
полномval: heldout88 не закрыт для их старого отбора. Разные budgets/одинseed.
Семь сохранённых baseline (включая Recformer)+Popularity пересчитываются
из top12; graphs/search/loss/AP histograms/bootstrap/frozen replay/ZIP.
CPU integration на реальных данных с фиктивными LLM-ответами пройден;
это НЕ оценка Qwen/Llama. ID joins/known pandas answer/time filtering,
перестановка/блоки/repair/duplicate/islands/resume/fullcatalog/references
проверены. Отчёт проверки reports/kaggle_llmfe_validation/small_compare_v1.
README/исходники/manifest в LLMFeatures/kaggle/small_compare.


## Recformer: завершённый малый эксперимент (2026-10-16)

По поручению пользователя проведён hm_recformer_small_seed42_v1 на прежнем
data/rel-hm-small-v1:4804train/304val/250test,5000товаров. Все10файлов
совпали с прежними SHA256. Полный каталог и недельные цели сохранены.
Zero-shot val/test MAP@12=2.669956%/3.300544%; после2+2эпох дообучения
2.470220%/1.235556%. Fine checkpoint выбран поval:стадия2,эпоха2.
Дообучение+validation1255.72с(20.93мин),пикCUDA3424326656bytes(~3.19GiB).
Это перенос опубликованных предобученных весов, НЕ обучение с нуля.
Все4полных val/test replay дали точное совпадение scores иtop12;
verification.json passed=true,pipeline.exitcode=0. Графики comparison.png
иlearning_curves.png визуально проверены. Отчёт reports/recformer_small_v1,
артефакты Recformer/results/hm_small_seed42_v1,протокол Recformer/PROTOCOL_SMALL.md.
Старые модели, данные и отчёты не менялись. Код runner SHA совпал после запуска.

Zero-shot test выше ContextGNN3.015575% на0.284968п.п., но парный bootstrap
95%[-1.23318;1.79754] пересекает0: устойчивое превосходство не установлено.
В этой короткой конфигурации дообучение ухудшило результат; причины не доказаны.
Один seed и250test пользователей; результат не переносить на полный H&M/статью.
5000товаров дают4846уникальных tokenized описаний: совпадения входов ограничивают
различимость. Features past-only,повторные покупки разрешены,targets не во входе.

Репликация AaronHeee/RecFormer commit26b00a58e7affe0c54a89c143ea7bce37f2e8e08;
авторский репозиторий сейчас содержит README и ссылку на эту репликацию.
Checkpoint749479199bytes/SHA6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022
получен по ссылке репликации; missing=[],unexpected только unusedMLMhead.
Не называть проверенным оригинальным авторским checkpoint. Первая загрузка
оборвалась на277MB; ошибка сохранена, downloader поддерживает range/size/ZIP.
Smoke отделён:148110336параметров,пик2.80GB,catalog26.75s,warmstep.16-.22s.
Пакеты иunsloth не менялись; импорт model/tokenizer без Lightning.
Full run:batch4/accum4,256tokens,FP16,AdamW5e-5,mean-per-user multi-positive
weekly fullsoftmax5000;stage1обновляет itemcache,stage2егофиксирует.

Общая цель пользователя: исследовательский отчёт, сопоставимые H&M рекомендации;
ресурсы RTX3060 6GB иKaggleT4, желательный бюджет эксперимента до часа.
Предварительный разбор сохранён в reports/recformer_assessment.md как история.

## Добавление двухбашенной модели к малому пилоту (2026-10-16)

По поручению пользователя заново обучена существующая двухбашенная
Model из RelBenchGNN/upstream/examples/model.py на data/rel-hm-small-v1.
Run_id hm_twotower_small_seed_42_v1. Shared64d GraphSAGE,2слоя,
encoderResNet64×2,neighbors32/16,batch128,last,seed42,BPR. Batch-группы
по времени включают остатки: все4804trainстроки,42шага/эпоху.
Остановлена после9эпох поpatience3, лучшийcheckpoint эпоха6.
Validation/testMAP1.55256%/0.68368%; train+val38.09с,testinfer0.699с.
Scores/предсказания/embeddings сохранены в
ContextGNN/results/hm_small_v1/two_tower. Независимая проверка завершена:
verification.json passed=true, предсказания совпали, MAP delta=0 на val/test.
Общий отчёт содержит 5 моделей и Popularity; все MAP пересчитаны из
предсказаний, comparison.png и learning_curves.png визуально проверены.
Прежний отчёт в reports/contextgnn_small_v1/before_two_tower сохранён.
Предыдущие модели/данные не переобучались и не менялись.
ГипотезаH001 (независимые веса двух башен) по-прежнему не запускалась.

## Малый ContextGNN эксперимент (2026-10-16)

Пользователь поручил сначала выделить малый датасет, затем провести
ContextGNN эксперимент; дополнительно пересчитать manual LightGBM
и IDGNN→LightGBM на тех же данных для сопоставимого сравнения.
Создан отдельный data/rel-hm-small-v1:5000users/5000items/46442transactions,
train4804/val304/test250 user-time. Состав выбран только по истории доval;
каталог сужен, пустые цели удалены, покрытиеval37.27%/test33.68%.
НЕ сравнивать MAP малого набора с полным H&M или статьёй.
Upstream ContextGNN ca4a96985b7ef73c36a40da32e70710ad9b59a1e, импорт
без установки и изменения прежнего окружения. IDGNN/ContextGNN64d,
2слоя,neighbors32/16,batch128,seed42,до10эпох,patience3. Обучены;
независимый replay пройден. ContextGNN test3.01558%,IDGNN2.65341%.
Оба LightGBM получают72813одинаковых trainпар; eval ВСЕ5000товаров,
manual126фичей и IDGNN64+availability. Все4модели и проверки завершены.
Малый manualLightGBM val/test0.99832%/1.23388%, IDGNN→LightGBM
0.68531%/0.96667%. SHA trainпар совпал; декартовuser×catalog обоих
оценочныхкэшей проверен. ВсеMAPнезависимо пересчитаны изpredictions.
GNncheckpoint replay и повторныйinferизLightGBM model.txt совпали.
Context−IDGNN test+0.3622п.п., paired-user-bootstrap95%[-0.1003,0.9320],
пока не доказано устойчивое превосходство. Seedодин,test250пользователей.
ДляLightGBM-IDGNN безвектора70.50%train и99.77%testпар; это
ограничение full-catalog протокола, не универсальный вывод о GNN-признаках.
Обучение+val GNn около21–28с; тёплыйtestinfer0.055–0.068с, без загрузки
окружения/графа. Cold replay IDvalвключил~12сGPUинициализации.
Графики comparison.png/learning_curves.png просмотрены и проверены.
Скрипт ContextGNN/run_small_pipeline.sh сохраняет фиксированные стадии;
текущие завершённые результаты не переобучаются при повторном вызове.
Протокол ContextGNN/PROTOCOL_SMALL.md, метрики ContextGNN/results/hm_small_v1,
отчёт reports/contextgnn_small_v1. Данные и прежние отчёты сохранены.

## Анализ ContextGNN (2026-10-16)

Прочитаны PDF arXiv:2411.19513v1 и kumo-ai/ContextGNN. Подробности:
reports/contextgnn_assessment.md. Подход уже оценён на нашей задаче H&M:
ContextGNN val/test MAP 3.00%/2.93%, pair-wise baseline 2.64%/2.81%.
Локальная ветвь дополняется GNN-user × RHS embedding ветвью и offsets.
Это адресует локальный охват ID-GNN; не создаёт локальные вектора всех пар.
Новый запуск не выполнялся. Требуются фиксация commit, адаптация API
RelBench1.1.0 к нашему checkout, проверка памяти GPU6GB и полный каталог.
ContextGNN→дерево — наша отдельная гипотеза, не опубликованный результат.

## Итог старого X+history v5: ошибка сопоставления (2026-10-16)

ПолученZIPpreflight_fulltrain_v5_949add5c4fef;указанныйfeatures-llama-plus-lightgbm-v3.ipynb
содержитровнототжеruntime(2SHAсовпали).20техническиоценённыхза154calls/134rejects/103repairs.
Выбранcandidate151:valMAP.009773007347470239,test.007345734694570958;4independentreplayRaw/selected
×val/testточносовпали,20model/programхешейиtrain803377проверены.
КРИТИЧНО:FRangeIndexполучаетSeriesgroupbyIDпрямымприсваиваниембезmapпоX.ID.
Статистикипопадаютпономерустроки,а не поIDпары.На128searchпарах70неверныхmean_price,
52неверныхcustomerstats(фактическиеcustomerколонкивсеNaN).Перестановка/разбиениеменяютвыход.
Такойprobeпровалили4из20:56,131,147,151.Неисправлятьисторическиеметрикизаднимчислом.
Статусcomplete_with_alignment_bug,feature_semantics_valid=false.13generatedнеявляются
корректноID-сопоставленнымиhistoryпризнаками. Этоотдельноотflat(20/23,test.800949%).
Архив/notebookнеизменены;новогообучения/выборапоtestнет.Отчётreports/hm_llmfe_llama_v5_audit/report.md.

## Новый H&M эксперимент: плоская таблица + Python Llama (2026-10-16)

РЕАЛЬНЫЙ flat запуск aa1ed17300ae завершён,ZIPвкорнепроектапроверен.
20оценённыхASTпрограммза23calls/3repairs/3rejects(.max acrossrows).Выбранcandidate003поconfirm512.
LLMvalMAP=.0074474111229482325,test=.008009488544766866(0.744741%/0.800949%).
НаТЕХЖЕval1024/test2048:Raw15test0.713138%,Prepared30test0.737375%,Seeded32test0.723351%,
manual126test1.862883%,GNN→LGBM1.680568%,IDGNN2.254944%.Не сравниватьсfulltest67144.
Все20candidateхешеймоделей/программ/train803377проверены;configfingerprintи7runtimeSHAсовпали.
Независимыйreplay4моделей×val/testсовпалточноtop12/AP/MAP;референсыпересчитаныизbundle.
Парныйbootstrap10kпользователейseed42:LLM−Prepared30 +.063574п.п.,95%[+.010718;+.127851];
LLM−Seeded32 +.077598п.п.,95%[+.026709;+.138419];LLM−Raw15CIпересекает0.
Raw15наval1.026872%вышеLLM.НаэтойвыборкеестьмалыйвкладLLMповерх30/32контролей,
носущественнохужеmanual/GNN,неоснованиесчитатьполныйкаталогLLMлучше.
Выбранные36полей:30base+2ручныхseedlog+4LLMratio.Естьнесогласованные180/30окнавratio,
recencyделитсяпроверкойcountвместоdenominator;inf→NaN.Оценкасмыслапо-прежнемунужна.
flat_manifestнепопалвZIP:byteсравнениеКaggleкэшанедоступно;локальныеданныетогожекода
даютточнотежефинальныепредсказания. Архивнеизменён.
Отчёт/графики:reports/hm_llmfe_flat_v1_audit/report.md,audit.json,export/.

Пользователь одобрил перенос успешной balance-scale постановки на H&M.
Отдельный notebook LLMFeatures/kaggle/llmfe_llama31_hm_flat_kaggle_t4.ipynb,
protocol hm_llmfe_llama31_8b_lightgbm_flat_fulltrain_v1. Исходный Input fulltrain_v2 прежний.
Одна таблица30полей:15raw+15 фиксированных РУЧНЫХ past-only агрегатов (неLLM).
ДоLLM измеряютсяRaw15,Prepared30,Seeded32(+2ручныхlog);рабочийSEEDвсегдавпромпте.
Llama пишет modify_features(X) безhistory/SQL/joins,можетдобавлять/удалятьполя.
Строковыеимена,числовойвыход1–78;rowwiseоперации,preflightпроверяетbatch-invariance.
СравнениевкладаLLMсPrepared30иSeeded32,а не присваивание ручныхагрегатовLLM.
803377 исходныхtrainпар/метки/порядоксохранены;вкэшекопии добавленыслужебныетеги,
никогда невидимыеLLM.52снимка past180days;inputархивнеизменён;кэшвworking.
Seed42/LightGBM150/31/4threads;тежеsearch256/confirm512/val1024/test2048/IDGNNпулы.
3islands,20оценённыхAST-программ/300calls/3repairs;пилот:0успеховпосле6calls→ошибка+ZIP.
HF/ревизия0e9e39f249a16976918f6564b8830bc894c89659/NF4FP16/chat,unslothвыборсохранён.
Графики,контрольныепредсказания,независимыйreplay,ZIPприошибкахвключены.
Исходники/README/проверки:LLMFeatures/kaggle/flat_variant;builderbuild_flat_notebook.py.
Локальныепрограммы-тесты неявляютсягенерациейLlama;реальныйновыйT4запускещёнесделан.

## Диагностика balance-scale перед дальнейшим H&M поиском (2026-10-15)

РЕАЛЬНЫЙ Kaggle v2_cpu завершён, ZIP balance_scale_llama31_diagnostic_v2_cpu_6b5c7786f4b5_results.zip
получен и проверен. КонфигfingerprintиобаruntimeSHAсовпали. Chat3/3valid:CV81.4/91.8/96.8%,
raw87.0%,authorsseed86.2%. НезависимыйCPUreplay3программточносовпалповсем4foldscores.
Это500trainCV,125heldoutнеоцениваются;неtestaccuracy,неH&M,невоспроизведениеитоговстатьи.
Completion3/3rejectedпоtruncated2048:естьполныепервыефункции,потомv2/v3илиповторы;
staticprefixASTпроверен,нонеоценён;нельзяназватьвсютройкунеисполняемымкодом.
Seed44самсоздалweight*distanceдляобеихсторон;NF4Llamaспособнагенерироватьполезныепризнаки
вэтойпостановке. НеобъяснятьH&Mотсутствиемchat-template:тамонужебылисдругиминтерфейсом.
Артефакты: reports/balance_scale_llama31_diagnostic_v2_audit/report.md,audit.json,
export/ (копияZIP),independent_cpu_replay/. Оригинальныйархивнеизменён.

Получен SaveVersion лог balance_scale_llama31_diagnostic_v1_09de7191636d:
rawконтрольупалнаXGBfit/eval cudaErrorNoDeviceприdeviceCPUивскрытомCUDAworker.
0 обращенийLLM,модельещёнезагружалась,доZIPвыполнениенедошло.
Локальныестарыетестыиспользовалиxgboost-cpu,аKaggleустановщикобычныйGPUwheel—различиеисправлено.
Новыйprotocol balance_scale_llama31_diagnostic_v2_cpu:uninstallxgboost+cpu,installxgboost-cpu3.0.5,
проверкаworkerUSE_CUDA=false;ZIPсfailure.jsonприошибкеконтроля/загрузкимодели.
Файл.ipynbтотже,старыйвarchive/v1. НастройкиLlama/задача/6вызововнеизменны.

Получены run_config, первый ответ иrepair structured-запуска. Все4 runtimeSHAсовпадают
снашимивыдаваемымимодулями. Официальный hf/Meta,revision0e9e39f249a16976918f6564b8830bc894c89659,
T4,NF4/FP16,temp.8,top_p1,top_k0;явногонесоответствияконфигунет.
Первыйответ19aggregates,7невалидныхkeys:days_ago,price,raw_*membership/news,customer_age.
12агрегатовсоответствуютструктурнойсхеме;2derivedнеизвестныиз-заотклонённыхродительскихагрегатов.
Repairсохранилневалидныеkeysиудалилвалидныедоходныеагрегаты,нооставилссылкинаихимена.
ЗначитпроблеманетолькоJSONсинтаксиса:несоблюдениегруппировок/зависимостей.
age_diff=0иage_ratio=1длянепустогостатическоговозраста;валидностьнеравнаполезности.
Диагностическийbalance.ipynbтеперьпоумолчаниюhf+точнаяревизияпользователя;
источникиостаютсявыбираемыми.Этообновлениевыборамодели,реальногозапускаLlamaещёнет.

После7 отказов structured v1 (8й вызов только начался вприсланномлоге) пользователь
одобрил короткую проверку Llama на исходной задаче и начальной программе авторов.
Подготовлен llmfe_llama31_balance_scale_diagnostic_t4.ipynb, protocol balance_scale_llama31_diagnostic_v1.
Встроены625строк и исходникиизофициальногорепозитория SHA e9a58ca3416ae74dcc7549dffdf79b9289604091,
domain_head/tail и исходный weight_difference; Inputархивненужен. MODEL_SOURCEhf/unsloth,
NF4/FP16 какранее;пользователювыбратьисточник/ревизиюизпроблемногозапуска.
Всего6calls:3chat+3rawcompletion,seeds42/43/44,temp.8;безrepair/эволюции.
Промптреконструирован,небайтовоеоригинальноевоспроизведениеLLMserver.
CPU XGBoost3.0.5,4foldCVна500trainпервоговнешнегоfold;125heldoutнеоцениваются.
Это диагностика compliance,некачествоH&M/нечисленное воспроизведениестатьи.
Локальныепроверкипроводятсянасинтетическихответах;реальнаяLlamaнаT4здесьнезапускалась.
Исходники/README/manifest: LLMFeatures/kaggle/balance_diagnostic.

## Новый структурированный интерфейс Llama (2026-10-15)

Пользователь остановил SQL Kaggle v1: присланы первые3 отказа одной цепочки;
LLM подставляла raw_u_active/raw_u_fn в агрегаты вместо исправления namespace.
В ответах также неверные ключи sales_channel_id, nested AVG(COUNT), percentile внеallowlist,
несуществующие ссылки derived,MAX вместоMIN дляrecency. Измеренных наборов вприсланных3 нет;
полный итог остановленного запуска неизвестен. Run: sql_fulltrain_v1_6eb8a9ef9ba7.
Пользователь одобрил новый structured язык: выбор op/column/window/keys + деревья формул,
hostкомпилирует SQL. Отдельный llmfe_llama31_hm_structured_kaggle_t4.ipynb,
protocol hm_llmfe_llama31_8b_lightgbm_structured_fulltrain_v1. Сохранены24/12,
803377train/LightGBM/seed42/3islands/20successful/300calls/3repairs/тежеevalпулы.
Это НЕgrammar decoding: samplingJSON+структурнаяпроверка, несколько ошибок заодинrepair.
НовыйинтерфейсболееограниченчемQwenSQL,старые.ipynb/результатынеизменяются.
Исходники/README: LLMFeatures/kaggle/structured_variant; build_structured_notebook.py.

## Отдельный SQL-ноутбук для параллельной Llama (2026-10-15)

Пользователь попросил отдельный ноутбук с задачей как у локальной Qwen и затем явно
уточнил: сохранить также производные формулы, не ограничиваться одними агрегатами.
Новый llmfe_llama31_hm_sql_kaggle_t4.ipynb: JSON aggregates<=24 + derived<=12,
группировки/LEFT JOIN/порядок строк в host; производные видят raw/агрегаты/ранние формулы.
Protocol hm_llmfe_llama31_8b_lightgbm_sql_fulltrain_v1, отдельный llmfe_sql_runtime.
Прежний pandas notebook и присланные результаты не менялись. Данные тот же fulltrain_v2,
803377 train пар, search256/confirm512/val1024/test2048, LightGBM,20/300/3,3 популяции.
MODEL_SOURCE hf/unsloth сохранён. Полное совпадение всего эксперимента с Qwen не заявлять:
другие LLM/промпт/история/бюджет. Реальная генерация Llama в SQL-протоколе пока не выполнена.
Исходники и проверки в LLMFeatures/kaggle/sql_variant; builder build_sql_notebook.py.

## Реальный Kaggle v3 разобран; подготовлен v5 (2026-10-15)

Пользователь предоставил папку hm_llmfe_llama31_8b_lightgbm_fulltrain_v3_3b338cf1f141_results
с полным отчётом и.ipynb. Аудит всех20 попыток:0 измеренныхLLMнаборов,0 созданныхкандидатных
моделей.10 missing_columns,4 другиеpandasruntime,3 row/index,2 truncated,1 запрещённыеimports.
Кодworker/runtime извлечён безопаснымASTиз.ipynb;SHAточно совпалrun_config. Времяпопыток39.7мин.
Этоv3 безисправлений, не тотv4фрагмент0/83. Причинаv4поэтомувсёещёнепроверена.
Raw-controlвыбран; егоMAP ошибочно дублировалсястрокойLLM-FE встаромотчёте. Пересчёт
сохранённыхпредсказаний подтвердилrawval=.010268722027755231,test=.007131381963099318
на1024/2048пользователях. Не называтьэто качествомLLMпризнаков.
Выводпользователю: локальнаяQwenписалаограниченныеSQLвыражениясhostjoins, Llamaписала
полнуюpandasпрограмму; разныеязык/контракт/бюджет/исправления, не чистоесравнениесилымоделей.
Candidate001: mergehistoryсXпоcustomer_id породилarticle_id_x/y; groupbyarticle_idпадает.
Candidate003:rolling(7)считаетстроки,reset_indexдал3колонкипротив2имён;дальшеестьwrongnamespace.
Аудит: reports/kaggle_llama_v3_audit/report.md,audit.json,rejection_categories.png.
17 неизменённыхprogram.pyпроверенынаCPUвboundedpreflight:все17 отклоненырано,обычно2–5с,
безновогообучения/ручныхисправленийформул. Логиpreflight_replay/summary.json.

НовыйготовыйKaggleprotocol hm_llmfe_llama31_8b_lightgbm_preflight_fulltrain_v5 втомже.ipynb:
промпт2–6признаков,короткийкод,FотдельноотX,реальныеhistoryexamples,правилаnamespace/merge/
индексов/дневныхокон;беззаданияручныхформул. Preflight256раннихtrain+256позднихtrain+
256searchпарпередполнымfit;smokeнеувеличиваетцелевыесчётчики. ОшибкаLLMвключаетстроку
еёкодаиобадоступныхнаборастолбцов. Есливыбранrawfallback,егоитоговаястрокаNO LLM features.
LightGBM,803377партренировки,MODEL_SOURCEhf/unsloth,цель20/до300/3исправлениясохраняются.
13тестовисинтетическийend-to-end прошли,настоящаяLLamaсновымпромптомне запускалась.
v4 сохранёнвkaggle/archive/lightgbm_repair_v4. Старыйприсланныйотчётнеизменялся.
## Kaggle v4:20 успешных наборов,300 обращений,3 исправления (2026-10-15)

Последнее прямое указание пользователя после частых отказов вKaggle: цель20 различных
полностью оценённых наборов, максимум300 обращенийLLM суммарно, до3 исправлений каждого
предложения. Подготовлен protocol hm_llmfe_llama31_8b_lightgbm_repair_fulltrain_v4.
Тот же.ipynb LLMFeatures/kaggle/llmfe_llama31_hm_kaggle_t4.ipynb, прежние803377 пары,
LightGBM на всех этапах, MODEL_SOURCE unsloth/hf сохранён. Архивv3: kaggle/archive/lightgbm_v3.
CONFIG: target_successful_distinct=20,max_llm_calls=300,max_repairs_per_proposal=3.
Новая генерация +до3 исправлений =до4 обращений/цепочку. Исправление получает последний
полный ответ и конкретную ошибку, тот же island, исходные правила/схему/5train примеров;
для экономии контекста использует raw-control демонстрацию вместо3 длинных программ.
Формулы человек не переписывает. ДубликатыAST/ошибки/rawcontrol/smoke не входят в20.
Все обращения/исправления входят в300. Запрос перед вызовом фиксируется в request.json;
прерванный запрос наresume расходует слот, не переотправляется без учёта бюджета.
После успеха либо3 неудачных исправлений переход к новому предложению. Новые предложения
по3 на один prompt,3 популяции. По300 обращениям при меньшем числе успехов target_met=false,
confirmation/final идут по доступным программам, недостижение20 не скрывается.
Графики поLLM calls/числуоценённых наборов, столбцыisland/repair/parent_call, budgetsummary,
токены/время сохранены.11 тестов прошли, включая остановку20/300,225 исправлений для75
полностью неудачных цепочек, прерывание/resume. Tiny-data synthetic smoke сLightGBM:
3 первыхошибки→успехтретьегоисправления→дубликат→успехисправления;6 calls,2 distinct.
Это проверка ПО, не результатLLama. Данные/модель/раунды/семплированиенеизменны;
новый бюджет/исправления требуют новогоrunID и новогоноутбука. НастоящаяLLM здесьне запускалась.
## Kaggle v3: отбор только через LightGBM (2026-10-15)

Последнее прямое указание: LLM-наборы выбирать через LightGBM, а не XGBoost.
Обновлён тот же выдаваемый.ipynb LLMFeatures/kaggle/llmfe_llama31_hm_kaggle_t4.ipynb;
protocol/run prefix hm_llmfe_llama31_8b_lightgbm_fulltrain_v3, search_backend=lightgbm.
Все этапы raw_control/search/confirmation/final/replay теперь LightGBM150 rounds31 leaves.
XGBoost не устанавливается и не импортируется основной веткой. Старые notebook/code v2
сохранены в LLMFeatures/kaggle/archive/xgboost_v2. Старые результаты не переиспользуются;
cache с несовпадающим backend отклоняется. Пользователю нужен новый.ipynb и restart kernel,
потом Run All; прежний архив fulltrain_v2 с803377 парами не меняется. MODEL_SOURCE unsloth/hf
сохраняется. Загруженные runtime/worker модули явно reload после создания файлов.
Причина изменения также актуальна для ошибки Kaggle: std::bad_alloc на load_model XGBoost
под4GiB RLIMIT_AS в Python3.13. Этот traceback не доказывает нехватку VRAM/физическойRAM.
Новый raw LightGBM действительно обучен на всех803377 парах/4CPUthreads, reload и search
прошли за22.93с локально.8 тестов и отдельный синтетический end-to-end smoke прошли.
Обучающие объекты освобождаются gc.collect перед reload. Лимит4GiB относится кCPU VMS.
Никакого Llama GPU/Kaggle запуска здесь не было. Проверки отдельно:
reports/kaggle_llmfe_validation/lightgbm_v3_fulltrain_control и lightgbm_v3_synthetic_smoke.
Исторические описания XGBoost v2 ниже больше не являются активным протоколом.
## Подготовлен Kaggle-ноутбук Llama3.1-8B (2026-10-15)

Пользователь поручил подготовить.ipynb для KaggleT4 с моделью из LLM-FE.
После уточнений требует все прежние803377 train пар для сравнения трёх способов.
Ноутбук: LLMFeatures/kaggle/llmfe_llama31_hm_kaggle_t4.ipynb.
Данные: LLMFeatures/kaggle/hm_llmfe_kaggle_fulltrain_v2.zip (~12.6MB);
инструкция LLMFeatures/kaggle/README.md. Старый ограниченный train v1 сохранён,
но используется только новый fulltrain_v2. Байты train_pairs совпадают с оригиналом.
Search256 /confirm512 /heldoutval1024 /test2048, фиксированные общие кандидатыID-GNN.
В ноутбуке MODEL_SOURCE выбирает unsloth (по умолчанию, анонимно) или hf (официальный Meta, одобренный доступ/HF_TOKEN). Оба репозитория на HF, полноразмерные веса квантуются NF4/FP16;
3 острова,temp.8,3 последовательных сэмпла prompt,20 программ суммарно включая ошибки.
Python-программы признаков вместо SQL; XGBoost выбирает, затем отдельные raw/LLM LightGBM.
Архив содержит референсные top12 manualLightGBM/GNN→LightGBM/nativeID-GNN на тех же строках.
Оба старых дерева использовали803377 пар; GNN→LightGBM выбрал15 листьев, manual31;
подбор/производные seeds/GNN pretraining различаются. Сравнивать пересчитанный MAP одной
подвыборки, не с прежними полными testMAP. История ограничена когортой/180днями до cutoff.
Ресурсные отличия от статьи:4GiB evaluator вместо2GiB (2GiB CPU-контроль упал),
1800с общий лимит,30с на один вызов функции; квантизация и H&M/MAP тоже адаптация.
Формат.ipynb и6 исходных тестов прошли; rawXGBoost/LightGBM реально обучены на803377 парах
на1 CPU-потоке (~72с/~35с). Синтетический tiny-data smoke проверил полный цикл,
replay/resume и графики; его метрики не являются результатомLLama.
Проверки: reports/kaggle_llmfe_validation/verification_summary.json.
Пакеты проверок только в LLMFeatures/kaggle/.check-deps, окружения не менялись.
На GPU Llama и вKaggle ноутбук ещё НЕ запускались; качество нового метода неизвестно.
Новый подготовленный run-id: hm_llmfe_llama31_8b_kaggle_fulltrain_v2; фактический Kaggle
run дополняет имя хешем модели/пакетов/конфигурации/данных/кода. H002 не изменялся.
## Новый разрешённый запуск H002 (2026-10-15)

Пользователь поручил проверить вторую гипотезу и разрешил больше2 потоков
LightGBM. Последующее прямое указание: поиск НЕ по всему каталогу, использовать
меньшую выборку. Закреплён run hm_llmfe_qwen25coder7b_seed42_h002_shared_v1:
20 различных оценённых наборов, максимум100 обращений, до2 исправлений,
3 популяции; поиск прежние256 val пользователей на их сохранённых кандидатах
ID-GNN, confirmation другие1024 пользователя/общие кандидаты. Финал все val/test
на общих кандидатах и полный независимый повтор. Test только после фиксации
победителя; прежний test уже известен, это последовательный исследовательский запуск.
Те же803377 train пар, Qwen2.5-Coder7B Q4_K_M, seeds42; обучение/инференс8
потоков. Сначала raw-control проверяет совпадение предсказаний старого2-thread
и нового8-thread обучения на2048 парах. Старый полный каталог остаётся на паузе.
Артефакты: LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1;
отчёт/живые графики: reports/llmfe_h002_shared_v1; запуск h002_pipeline.sh.
H002 меняет несколько факторов, включая меньший search pool; нельзя приписывать
эффект только исправлениям или напрямую сравнивать старый/новый search MAP.
## Текущий приоритет — признаки от локальной LLM (2026-10-15)

Пользователь выбрал новое направление: составление признаков локальной LLM,
чтобы проверить, стоит ли продолжать работу с GNN или перейти к LLM для
создания признаков. Пользователь предоставил статью LLM-FE и 2026-10-15
поручил начать эксперимент; реализация и локальный запуск разрешены.

Активный новый эксперимент: `hm_llmfe_qwen25coder7b_seed42_v2`.
Последнее решение пользователя 2026-10-15: полную каталожную оценку
приостановить; вместо неё выполнить оценку выбранного candidate08 на
точно тех же кандидатах, что ID-GNN seed42 и ручной LightGBM.
Полный каталог остановлен на 5840/74575 validation пользователей;
предсказания/checkpoint сохранены. Маркер full_catalog_paused.json запрещает
автоматическое продолжение; возобновлять только по новому указанию пользователя.
Новая отдельная оценка:
`hm_llmfe_qwen25coder7b_seed42_v2_shared_idgnn_inference_v1`,
артефакты LLMFeatures/results/qwen25coder7b_seed42_v2/shared_idgnn,
запуск LLMFeatures/shared_pipeline.sh. Оценка полных val/test по общим
кандидатам, без обучения/повторного выбора признаков, затем независимый
полный повтор на 2 потоках и отдельный отчёт
reports/llmfe_qwen25coder7b_v2/shared_idgnn/report.md.
Ручной LightGBM уже оценивался на этих точных пулах: val2,088,583 /
test1,892,405 пар. Прежние описания основной полной каталожной оценки ниже
сохраняются как история протокола; текущий приоритет — общий pool.
Оценка на общих кандидатах завершена с exitcode=0. LLM-LightGBM candidate08:
полные validation/test MAP@12 0.854281% / 0.811751%. Полный повтор в отдельном
процессе на 2 потоках воспроизвёл все top-12 и метрики; verification.passed=true.
ID-GNN перепроверена на тех же пользователях/пулах: 2.634419% / 2.784315%.
Ручной LightGBM: 2.093177% / 2.266077%. Этот LLM-набор хуже обоих;
не обобщать на метод в целом: оценены лишь 5 из 20 предложений, интерфейс
ограничен, настройки подбора и производные seeds различаются.
В отдельном shared_idgnn/report.md сохранены итоговая таблица и графики:
comparison.png, ap_histograms.png, first_hit_rank.png, paired_comparison.png;
test_user_ap.csv и plot_manifest.json содержат проверенные данные/хеши.
Средние AP всех четырёх моделей совпали с итоговыми MAP. Нового обучения
не было. Полный каталог остаётся приостановленным и не возобновляется.
Протокол и восстановление: `LLMFeatures/README.md`. Модель Qwen2.5-Coder-7B
Q4_K_M запускается отдельным Ollama localhost:11435, веса внутри проекта.
Проверки будущих данных/меток и exact top-k прошли. Search: 20 предложений,
3 популяции, 256 val пользователей; подтверждение до 3 программ на других
1024 val; финальные val/test полные, весь каталог плюс общий ID-GNN pool.
Программы — ограниченные SQL-выражения, выбранные LLM, и сырые статические
поля; старые ручные/GNN признаки не используются. Те же 803,377 train пар
(50,000 user-times), seed42 модели; прежний seed2026 выбора пар сохранён.
Тест не участвует в поиске. Не называть запуск завершённым до финальных
метрик/проверки. Фактическое состояние смотреть по PID, setup/pipeline logs.
Первый адаптер v1 остановлен и сохранён как superseded: запрет IDs также
ошибочно запрещал корректные counts уникальных покупателей и группировки
товарных категорий. v2 исправляет интерфейс; ID не используются как числовые
предикторы. Поиск v2 начинается заново. Не интерпретировать отклонения v1
как низкое качество метода. Проверенные веса/сырое контрольное обучение
переиспользуются, старые артефакты не перезаписываются.
Проверенный старт v2: Qwen работает на GPU (runtime size_vram=4,924,207,104
байт; nvidia-smi около 5.1 GiB всего), четыре теста протокола прошли.
Предложение candidate_08 прошло реальный SQL/train/full-catalog smoke
(8 val пользователей, 2000 train пар, 10 rounds; не итоговая метрика).
Начата его основная оценка: все 803,377 train пар, 150 rounds, search val256.
Первые 7 предложений v2 отклонены и сохранены с причинами; ошибки возвращаются
LLM. Артефакты/прогресс: LLMFeatures/results/qwen25coder7b_seed42_v2.
Предыдущий оставшийся evaluator v1 остановлен; активен только pipeline v2.
Аудит после поиска v2: 15/20 предложений отклонены до измерения MAP,
реально оценены пять. Первые причины: OVER 6, days_ago вне доступного
scope 2, grouping keys 2, структура программы 2, SELECT 1, строки 1,
ошибка regex-валидатора на WITHIN GROUP 1. У последнего предложения есть
и другие ошибки; исправление regex само по себе не делает его валидным.
Это смесь ошибок LLM и ограничений нашей адаптации, не доказательство
неполезности LLM-признаков. Аудит:
reports/llmfe_qwen25coder7b_v2/progress/rejection_audit.md.
По просьбе пользователя в HYPOTHESES.md добавлена H002: в следующем
LLM-эксперименте отдельно учитывать число обращений/исправлений и число
различных успешно оценённых наборов; добавить исправление программ через
LLM, чтобы проверить больше наборов. Ориентир обсуждения: 20 оценённых
наборов / до 100 обращений, точные лимиты определить перед запуском.
Это запись будущей гипотезы, не изменение текущего протокола v2.
По просьбе пользователя проверено и применено ускорение CPU-предсказаний:
32 validation пользователя, полный каталог (3,377,344 пары за проход),
2/6/8/12 потоков и 8 замеров каждого. Все скоры побитово совпали, top-12
совпал с сохранённым расчётом. Выбраны 8 потоков (2.162 с против 4.440 с
на предсказания пакета; оценка общего ускорения 1.65x). Настройки и hashes
в LLMFeatures/results/qwen25coder7b_seed42_v2/execution.json;
проверка в cpu_acceleration_check.json. Продолжение final с checkpoint3680,
без повторного поиска/обучения; training/model/data/protocol неизменны.
Исполнение имеет отдельный inference run_id:
hm_llmfe_qwen25coder7b_seed42_v2_cpu8_inference_v1.

Условия следующего эксперимента:
- LLM-признаки проверять отдельно, без объединения с ручными или GNN-признаками.
- Оценивать качество рекомендаций по всему каталогу.
- Один seed 42; бюджет времени не ограничен.
- Основной критерий успеха — увеличение MAP@12.
- Уточнение пользователя: организация скоринга должна обеспечивать валидное
  сравнение с ID-GNN. Основная оценка сохраняет полный каталог, одинаковые
  user-time строки, цели, временные границы и evaluator MAP@12 для обоих
  конвейеров. ID-GNN присваивает ненулевые scores только sampled товарам,
  остальным — 0 (run_idgnn.py); это часть её исходного алгоритма, а не
  полноценный обученный скор для каждой пары. Сравнение полных конвейеров
  не изолирует качество признаков. Для изоляции ранжирования дополнительно
  использовать общий сохранённый ID-GNN candidate pool для обеих моделей.
  Результаты полного каталога и общего pool показывать отдельно; не
  отождествлять расходы/число ненулевых scores с числом товаров evaluator.
- Гипотеза независимых башен сейчас не является следующим экспериментом;
  её описание и прежние результаты сохраняются в истории.

При интерпретации сравнения учитывать: прежние ID-GNN/деревья оценивались
на локальных кандидатах, двухбашенная GraphSAGE — по всему каталогу.
Архитектура LLM-эксперимента и конкретный протокол пока не определены.

Пользователь предоставил основу идеи: LLM-FE, arXiv:2503.14434
(https://arxiv.org/html/2503.14434v3), официальный репозиторий
https://github.com/nikhilsab/LLMFE. По запросу изучены статья и ключевой
код main.py, sampler.py, evaluator.py, buffer.py, config.py и пример specs.
LLM-FE ищет программы преобразования признаков через генерацию кода,
оценку downstream-модели и память удачных программ в нескольких популяциях.
Локальная LLM поддерживается через HTTP; fine-tuning не обязателен.
Готовая реализация рассчитана на CSV и classification/regression со случайной
кросс-валидацией, не на временной H&M ranking. Для нашего эксперимента
потребуются временные отсечения, агрегаты из связанных таблиц, MAP@12
и оценка всего каталога. Это адаптация, а не готовое воспроизведение.
У рассмотренного LocalSandbox используется exec; заявленные в статье
лимиты нельзя считать реально обеспеченными этим классом без доработки.
На этом этапе пользователь попросил изучить и объяснить идею; обучение
и установка зависимостей не выполнялись, локальная LLM ещё не выбрана.

Уточнение пользователя о ресурсах: сначала эксперимент на своём оборудовании;
если локальная модель покажет плохой результат, допустим отдельный эксперимент
с моделью из исследования на Kaggle. nvidia-smi подтвердил RTX 3060 Laptop,
6144 MiB VRAM, драйвер 528.02. Рекомендация (ещё не утверждённый выбор):
Qwen2.5-Coder-7B-Instruct GGUF Q4_K_M (файл 4.68 GB), llama.cpp,
одна генерация за раз, начальный контекст 4096 токенов; размещение в VRAM
и скорость требуют smoke-проверки, при необходимости часть слоёв на CPU.
Более компактная альтернатива — Qwen3-4B-Instruct-2507 Q4_K_M.
Для Kaggle — Llama-3.1-8B-Instruct, использовавшаяся в LLM-FE;
формат весов и ресурсы уточняются по фактически доступному GPU.
Ничего не скачивалось и не устанавливалось. Слабый результат одной модели
не считается опровержением всего подхода; смена LLM получает новый run_id.

Пользователь исследует автоматическое создание признаков для моделей
на деревьях. Начальный пример — персональное ранжирование товаров по
истории взаимодействий, характеристикам пользователей и товаров,
агрегатам. Источники: RelBench (arXiv:2407.20060) и RelGNN
(arXiv:2502.06784). Выбрана задача H&M `rel-hm/user-item-purchase`:
рекомендация 12 товаров, которые пользователь купит в следующие 7 дней,
метрика MAP@12. Пользователь поручил скачать данные отдельно в `data`
и запустить воспроизведение RelBench ID-GNN. Далее данные будут
использоваться в других экспериментах.

## Файлы контекста

- `README.md` — восстановление после клонирования: закреплённые данные/GloVe,
  исходники и перечень локальных весов. Публичной ссылки на наши веса пока нет.

- `STATUS.md` — автоматически обновляемый текущий статус.
- `EXPERIMENTS.md` — автоматически обновляемая сводка результатов.
- `WORK_LOG.md` — журнал событий, новые записи добавляются в конец.
- `experiments/events.jsonl` — машиночитаемая неизменяемая история событий.
- `experiments/state.json` — актуальное состояние запусков.
- `HYPOTHESES.md` — гипотезы и возможные эксперименты до запуска.
- `RelBenchGNN/README.md` — подробный протокол и команды.

## Что уже сделано

- Скачаны 18 файлов H&M: сырые Parquet-таблицы, manifest, схемы и
  train/val/test трёх исходных задач. Проверены размеры и SHA256.
- В выбранной задаче: train 3,878,451; val 74,575; test 67,144.
- Код RelBench: `RelBenchGNN/upstream`, commit
  `919fb8a61a4b4cb787283860597f45701895578d`.
- Экспертные SQL: `baseline/expert_upstream`, commit
  `445bb7a3b1230f49f8e5890ae81754d3e365680f`.
  Есть H&M user-churn/item-sales; для user-item-purchase готовых
  экспертных признаков нет. Их адаптация — будущая отдельная работа.
- GloVe 300d, используемый оригинальным примером для усреднения
  векторов слов, скачан в `data/models/glove`. Это входной текстовый
  кодировщик, а не обученные веса ID-GNN.
- Простые baseline завершены: `baseline/results/simple_metrics.json`.
  Validation/test MAP в процентах: popularity 0.35739/0.30456;
  past_visit 0.78166/0.79466. Past visit отличается от статьи;
  точная причина ещё не установлена. Метрики не подгонялись.
- Создан фоновый конвейер: проверка данных -> простые baseline ->
  smoke ID-GNN -> пять полных seeds. Фактический текущий этап смотрите
  в STATUS.md, файлах логов и состоянии процесса.
- Техническая проверка ID-GNN прошла: forward, backward и оценка
  выполнены на GPU. Первый полный seed 42 начал обучение;
  после первой эпохи validation MAP=0.02562482836509997 (2.56248%).
  Это промежуточный результат; тестовый результат ещё не получен.

## Окружение и принятые решения

- Windows, Ubuntu WSL2; GPU RTX 3060 Laptop, 6 GiB VRAM;
  драйвер 528.02. WSL располагает примерно 11 GiB RAM и 4 GiB swap.
- Новое окружение только внутри проекта:
  `RelBenchGNN/.venv-wsl`, Python 3.12.3, PyTorch 2.2.2+cu118,
  PyG 2.5.3, pyg-lib 0.4.0, PyTorch Frame 0.2.3.
- Современный PyArrow 26 оказался несовместим с NumPy 1.26;
  установлен PyArrow 15.0.2. Версии в requirements.lock.txt.
- Проверено имеющееся `/home/maki/miniconda3/envs/unsloth`:
  Python 3.11.15, torch 2.5.1+cu121, GPU работает, библиотек RelBench
  и PyG нет. Это окружение не изменялось и не используется в запуске.
- Системный драйвер/CUDA не изменялись. CUDA-библиотеки установлены
  пакетами Python в локальное окружение; кэш в RelBenchGNN/.uv-cache.
- Архитектура и обучение: 2 слоя, 128 каналов, sum, Adam lr=0.001,
  batch обучения 512, до 2000 заявленных шагов/эпоху, 20 эпох.
  Оценочный batch 128 уменьшает память GPU; validation/test полные.
- Seeds 42..46 выбраны нами; точные seeds авторов не установлены.
- Код 2024 года и текущий пример используют temporal_strategy=last;
  статья пишет uniform. Выбран last для воспроизведения кода;
  отдельное сравнение uniform допустимо только с новым run_id.
- Статья: ID-GNN val 2.64%, test 2.81% MAP@12 по пяти запускам.
  Итоговое воспроизведение ещё не подтверждено.
- Веса, конфигурации, предсказания и JSON метрик сохраняются для
  каждого seed в RelBenchGNN/results. Resume — с завершённой эпохи.

## Продолжение

Пользователь дополнительно поручил после полного обучения проверить
инференс и сохранить наглядные таблицы/графики. Добавлено автоматическое
продолжение из summarize.py: postprocess.py -> отдельный run_inference.py
для каждого best.pt -> build_report.py. Это выполняется после всех пяти
прогонов. До завершения обучения инференс-проверка не выполнена.
Отчёт: reports/relbench_hm_v1/report.md, CSV, PNG и SVG. Монитор обновляет
промежуточные графики после появления новых результатов эпох.
Для повторного агрегирования без инференса: summarize.py --summary-only.

Новая обязательная часть сравнения: локальное одиночное дерево и
LightGBM с 126 вручную заданными признаками. Это наша адаптация
подмножества экспертных user-churn/item-sales SQL плюс признаки пары,
а не опубликованный экспертный ранжирующий набор. Протокол подробно
в baseline/MANUAL_BASELINE.md. Код: baseline/manual_features.py и
run_manual_tree.py. Запуск встроен в postprocess.py после инференса GNN:
используются одинаковые кандидаты для каждой пары seeds, CPU, train
50,000 user-time строк; параметры выбираются только по validation.
Тест полный. В отчёте обязательны отдельно значения из статьи и
фактические локальные метрики; статья LightGBM 0.38% относится к
сырому baseline и не является результатом нашей адаптации.


Проверьте `RelBenchGNN/logs/pipeline.exitcode`, PID и логи. Не запускайте
дубликат. Команды из PowerShell в корне проекта:

```powershell
.\RelBenchGNN\check_status.ps1
wsl -d Ubuntu -- bash RelBenchGNN/runtime_status.sh
# Только если старый процесс завершился:
.\RelBenchGNN\launch_background.ps1
```

Обязательно обновляйте контекст/журнал при новых решениях, эксперименте
или обнаружении ошибки. При завершении проверьте метрики всех seeds,
создайте summary и сообщите отличия от опубликованных значений.


## Изменение плана 2026-10-14: один seed

По просьбе пользователя для ускорения используются только seed 42: ID-GNN,
DecisionTree и LightGBM. План задан в RelBenchGNN/experiment_plan.json.
Seed 42 завершил 20 эпох; начатый seed 43 остановлен, 44–46 исключены.
Артефакты остановленного запуска сохранены, в сравнении не используются.
После seed 42 выполняются независимый инференс, деревья и графики.
Это одиночный локальный результат в сравнении со средним пяти запусков
статьи; стандартное отклонение локальных seeds не оценивается.
Предыдущие описания пяти локальных запусков заменены этим решением.

## Подтверждённое завершение одиночного эксперимента

Конвейер завершился 2026-10-14 в 19:47 по Москве с кодом 0.
ID-GNN seed 42: validation/test MAP@12 2.63442% / 2.78432%.
Независимая загрузка best.pt (эпоха 19) и полный инференс дали
полностью одинаковые предсказания; inference_check.json passed=true.
DecisionTree + 126 ручных признаков: 1.87661% / 2.04076%.
LightGBM + те же признаки: 2.09318% / 2.26608%.
Оба дерева оценены после загрузки сохранённых моделей.
Обучение деревьев: 50,000 user-time строк, 803,377 размеченных пар;
кандидаты для оценки совпадают с ID-GNN. Бюджет обучения GNN больше.
Статья ID-GNN: 2.64% / 2.81% (среднее пяти запусков).
Ручные baseline являются нашей адаптацией, не опубликованными моделями.
Итоговый отчёт reports/relbench_hm_v1/report.md и comparison.png обновлены;
report.json final=true. Активных процессов эксперимента больше нет.
Повторное обучение или продолжение этого конвейера не требуется.

## Новый эксперимент: GNN → LightGBM

Пользователь поручил извлечь представления GNN и обучить на них дерево.
Эксперимент hm_idgnn_lightgbm_embeddings_seed_42_v1 использует замороженный
best.pt seed 42 и LightGBM на 128 представлениях перед линейной головой.
Для отсутствующих в подграфе пар — нулевые представления и availability
(итого 129 входов). Те же 50,000 user-time строк и 803,377 обучающих пар,
те же кандидаты оценки, что manual_v1; tuning только на validation.
Train embeddings in-sample: GNN ранее обучалась на train. Это адаптация
Appendix C.2 к ranking, не опубликованный результат H&M GNN+LightGBM.
Код: RelBenchGNN/run_embedding_experiment.sh. Кэш отдельно в
baseline/cache/gnn_embeddings_v1; модель и метрики в
baseline/results/gnn_embeddings_v1; отчёт reports/gnn_embeddings_v1.
Логи embedding_export.log и embedding_tree.log. Старые результаты сохранены.

Эксперимент завершён 2026-10-14 в 20:36 по Москве, exitcode=0.
GNN embeddings + LightGBM validation/test MAP@12: 1.97116% / 2.12451%.
Выбран num_leaves=15 по validation; seed 42, 150 rounds.
В этом протоколе результат хуже ID-GNN (2.78432% test) и ручного
LightGBM (2.26608% test), лучше одиночного ручного дерева (2.04076%).
Не обобщайте это на все способы передачи GNN признаков деревьям:
у 565,051 из 803,377 train пар нет представления в sampled graph (70.33%),
на test таких пар 201,178 из 1,892,405 (10.63%). Их векторы нулевые,
availability=0. Train представления in-sample, не out-of-fold.
Полное совпадение исходных GNN предсказаний при экспорте val/test проверено.
Модель сохранена и перезагружена для оценки; таблица и график в
reports/gnn_embeddings_v1, прежний reports/relbench_hm_v1 не изменён.

## Двухбашенная модель по поручению пользователя

Новый run_id hm_twotower_sage_seed_42_v1. За основу взят pinned upstream
examples/gnn_recommendation.py: отдельные forward пользователя и товара,
общие параметры heterogeneous GraphSAGE; скалярное произведение 128d,
BPR loss, товарный shallow embedding включён, ID-awareness выключен.
Это shared-backbone two-tower, не две сети с независимыми параметрами.
Train batch 256 для 6GB GPU, 20 эпох, seed 42, uniform sampling.
Ровно 2000 шагов/эпоху (upstream условие допускает 2001).
Sampler один для всех ветвей и оценки, без лишних CSC копий графа.
Фиксированный RNG при каждом evaluation split обеспечивает проверяемый
инференс. Полный каталог 105,542 товаров оценивается для всех пользователей.
После обучения val/test user/item vectors и ID/время сохраняются;
best.pt проверяется независимым процессом. Итоги отчёта после проверки.
Пути: RelBenchGNN/results/two_tower_seed_42, reports/two_tower_v1;
логи two_tower_training.log и two_tower_inference.log.
Запуск: RelBenchGNN/launch_two_tower.ps1; сначала проверяйте PID/exitcode.
Старый основной monitor не отслеживает этот новый pipeline; tracking.py
обновляет STATUS/EXPERIMENTS/WORK_LOG на событиях и завершении эпох.
Статья RDL GraphSAGE validation/test 0.92%/0.80% (пять запусков).
Full-catalog retrieval отличается от старого ID-GNN/manual candidate pool;
сравнивать как целые конвейеры, не как изолированное изменение головы.

Smoke forward/backward/evaluation и независимый инференс прошли:
предсказания val/test после перезагрузки весов совпали полностью.
Полный процесс seed42 запущен через hidden launcher; первая эпоха
началась 2026-10-14 в 21:55 МСК, batch256 проходит GPU без ошибки.
Итоговых полных метрик ещё нет; статус проверяйте по PID/логам.
Пользователю пояснено, что общие веса — один экземпляр GNN для обеих
ветвей с отдельными параметрами по типам узлов/связей внутри модели.

## Продолжение после остановки 2026-10-15

Все 20 эпох двухбашенной GNN завершены. Лучший checkpoint: эпоха 1,
validation/test MAP@12 0.57431% / 0.54301%. Пользователь просил восстановить
процессы. При проверке процессов не было; прежний независимый инференс
сохранил MAP точно, но strict-проверка не приняла разные top-k ID.
Диагностика: max abs difference векторов 4.77e-7. Старый check сохранён
как inference_check.strict_v1.json, прежний лог — .strict_v1.log.
Новый inference run_id имеет суффикс _inference_v2. Верификация проверяет
близость всех векторов и оценок по рангам, shape, ID, уникальность и MAP;
не принимает произвольное несовпадение только на основании равного MAP.
Протокол numerical_ties_v2 допускает лишь численно эквивалентные оценки.
Конвейер перезапущен через launch_two_tower.ps1, обучение пропускается
при наличии metrics.json; текущий результат смотрите в inference/check,
pipeline exitcode и реальном процессе. Оценка времени инференса 3–5 минут,
до 10 минут при медленной загрузке графа. Ожидание финальной проверки.

Возобновлённый конвейер успешно завершился 2026-10-15 в 10:49 МСК,
exitcode=0. Независимый инференс numerical_ties_v2 passed=true;
reports/two_tower_v1/report.json final=true. Активных процессов нет,
восстановление/повторный запуск не требуется. Старый strict-v1 failure
сохранён как история, актуальная проверка имеет суффикс _inference_v2.



### Обновление Kaggle: выбор источника модели (2026-10-15)

По прямому указанию пользователя добавлен MODEL_SOURCE='unsloth'|'hf' в конфиг.ipynb.
Unsloth по умолчанию: unsloth/Meta-Llama-3.1-8B-Instruct, token=False, Secrets не читаются.
HF: meta-llama/Llama-3.1-8B-Instruct; HF_TOKEN из env или KaggleSecrets, ошибка без него.
Используются полноразмерные публикации, одинаковая NF4-квантизация при загрузке, не bnb-4bit.
Источник, repoID и конкретная ревизия включены в run_config/model_runtime и хешrunID.
Автоматического fallback нет; побитовое совпадение весов двух издателей не доказано.
Добавлен отдельный тест веток авторизации; данные803377 пар и evaluator не менялись.



### Реальный Kaggle v3 разобран; подготовлен v5 (2026-10-15)

Пользователь предоставил папку hm_llmfe_llama31_8b_lightgbm_fulltrain_v3_3b338cf1f141_results
с полным отчётом и.ipynb. Аудит всех20 попыток:0 измеренныхLLMнаборов,0 созданныхкандидатных
моделей.10 missing_columns,4 другиеpandasruntime,3 row/index,2 truncated,1 запрещённыеimports.
Кодworker/runtime извлечён безопаснымASTиз.ipynb;SHAточно совпалrun_config. Времяпопыток39.7мин.
Этоv3 безисправлений, не тотv4фрагмент0/83. Причинаv4поэтомувсёещёнепроверена.
Raw-controlвыбран; егоMAP ошибочно дублировалсястрокойLLM-FE встаромотчёте. Пересчёт
сохранённыхпредсказаний подтвердилrawval=.010268722027755231,test=.007131381963099318
на1024/2048пользователях. Не называтьэто качествомLLMпризнаков.
Выводпользователю: локальнаяQwenписалаограниченныеSQLвыражениясhostjoins, Llamaписала
полнуюpandasпрограмму; разныеязык/контракт/бюджет/исправления, не чистоесравнениесилымоделей.
Candidate001: mergehistoryсXпоcustomer_id породилarticle_id_x/y; groupbyarticle_idпадает.
Candidate003:rolling(7)считаетстроки,reset_indexдал3колонкипротив2имён;дальшеестьwrongnamespace.
Аудит: reports/kaggle_llama_v3_audit/report.md,audit.json,rejection_categories.png.
17 неизменённыхprogram.pyпроверенынаCPUвboundedpreflight:все17 отклоненырано,обычно2–5с,
безновогообучения/ручныхисправленийформул. Логиpreflight_replay/summary.json.

НовыйготовыйKaggleprotocol hm_llmfe_llama31_8b_lightgbm_preflight_fulltrain_v5 втомже.ipynb:
промпт2–6признаков,короткийкод,FотдельноотX,реальныеhistoryexamples,правилаnamespace/merge/
индексов/дневныхокон;беззаданияручныхформул. Preflight256раннихtrain+256позднихtrain+
256searchпарпередполнымfit;smokeнеувеличиваетцелевыесчётчики. ОшибкаLLMвключаетстроку
еёкодаиобадоступныхнаборастолбцов. Есливыбранrawfallback,егоитоговаястрокаNO LLM features.
LightGBM,803377партренировки,MODEL_SOURCEhf/unsloth,цель20/до300/3исправлениясохраняются.
13тестовисинтетическийend-to-end прошли,настоящаяLLamaсновымпромптомне запускалась.
v4 сохранёнвkaggle/archive/lightgbm_repair_v4. Старыйприсланныйотчётнеизменялся.
## Kaggle v4: пользователь сообщает0 успешных после83 вызовов (2026-10-15)

Получен только фрагмент удалённого Kaggleлога:call83/300 repair2 rejected measured0/20,
call84 repair3 начат, elapsed~11184с. Причина отбраковок в предоставленном логе отсутствует.
У пользователя асинхронно запрошены error из2–3 последнихtrial.json; дополнительно нужны
response.generated_tokens/truncated. Нельзя приписывать это качествуLLM либо памяти без этихполей.
Время~136с/вызов допускает гипотезу об обрезке2048 токенов, но это НЕ установленная причина.
Рекомендовано прервать удалённую ячейку и сначала прочитать сохранённые ошибки.
Создан read-only LLMFeatures/kaggle/diagnose_failures.py: error_counts, последниеtraceback,
обрезка/токены и наличие schema/model/searchmetrics. Проверен на сохранённомsynthetic smoke.
Рабочий.ipynb/параметры модели/признаков не изменены до получения фактической причины.
Местные11 тестов проверяли ПО; настоящаяLlama вKaggle ими не проверялась. Не выдавать
прошедшийsynthetic smoke за подтверждение способностиLLM генерировать валидныепрограммы.

### Диагностика Save Version (2026-10-15)

Пользователь уточнил: Kaggle запускается черезSave Version, прямого доступа к ячейкам нет.
Нельзя предлагать выполнить новую ячейку внутри фоновой сессии. ВкладкаOutput выбранной
версии может датьtrial.json; доступность файлов до завершения и сохранениепослеCancel
не гарантировать. Исправлен недостатокstdout: теперь REJECTION печатает error целиком,
failure_stage(generation/parse_and_validate/feature_train_score), generated_tokens/truncated.
Есть строка началаCPU evaluator, чтобы отличить генерацию от вычислений. Тот жеv4 ipynb
пересобран,11 тестов прошли, модель/пары/бюджетнеизменны. При сменеruntime sourcehash
Kaggle получитновый fingerprint. Причина0/83 всёещёнеизвестна; ожидается actualerror.

