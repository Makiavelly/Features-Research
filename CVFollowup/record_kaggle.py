from common import ROOT,REPORT,read,write,sha,record

assert read(REPORT/'kaggle_portability_verification.json')['passed']
bundle=read(ROOT/'CVFollowup/kaggle/bundle_manifest.json')
record('recformer_kaggle_handoff','Two notebooks and762MB common input ZIP prepared and checked. Existing local fit retained; distributed scheduler now runs only two local settings, waits for three-fold results from each Kaggle setting, then original validation selection/evaluation. No Kaggle jobs submitted by Codex.',
    'hm_medium_recformer_distributed_v1',status='training_local_awaiting_user_kaggle',
    artifacts='CVFollowup/kaggle/README.md',input_zip_sha256=bundle['sha256'],
    local=['lr1e6_w100','lr3e6_w300'],kaggle=['lr3e6_w100','lr1e5_w300'])
path=ROOT/'CONTEXT.md';text=path.read_text(encoding='utf-8')
note='''## Recformer распределён между локальным GPU и Kaggle (2026-10-18)

Пользователь запускает два Kaggle Notebook параллельно через Save Version.
CVFollowup/kaggle/: два ipynb и общий recformer_medium_cv_inputs_v1.zip (~762МБ).
README.md содержит инструкции. Назначения:
локально lr1e6_w100 + lr3e6_w300; Kaggle1 lr3e6_w100; Kaggle2 lr1e5_w300.
Каждая настройка проходит все3 исходных фолда, batch4/accum4/FP16/2+2 эпохи.
Прежний recformer_lane scheduler остановлен БЕЗ остановки дочернего обучения.
Новый CVFollowup/recformer_distributed.py ждёт текущий fit и выполняет только
локальные назначения, затем ждёт external_import.json для6Kaggle fits.
НЕзапускать recformer_lane.py вручную, пока распределённый контроллер жив!
PID: reports/medium_followup_v1/recformer_distributed.pid. Старый recformer_lane.pid устарел.
Импорт: nativeWSL python CVFollowup/import_kaggle.py ARCHIVE.zip. Всефолды/параметры/
исходныевеса/данные/runtime проверяются до копирования. Готовыеfitнеперезаписываются.
Checkpointepoch0 при импорте берётся из старого локального frozenbaseline для
совместимости evaluator; T4trained checkpoint сохраняется неизменным.
Только после12fitконтроллер передаст отбор исходному recformer_lane.py:
среднееinner-valтрёхфолдов включаяbaseline; freeze, outer/replay, общийreport.
KaggleиспользуетотдельныйPython3.11, torch2.2.2+cu118, transformers4.46.3;
различияGPU/AMPобязательноказывать. Локально GPU/T4неэмулировался: проверены
всеSHA/таблицы и ASTидентичность6runtime. SaveVersionнужно запустить пользователю.
recover_wsl.py обновлён: восстановление черезdistributedcontroller, прерванные
Recformerfitсохраняются отдельно перед полным повтором; optimizerresumeнет.

'''
if note not in text:path.write_text(note+text,encoding='utf-8')
