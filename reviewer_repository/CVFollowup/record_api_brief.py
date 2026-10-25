from common import ROOT,REPORT,read,write,sha,record

document=REPORT/'api_method_context_for_chat_ru.md'
sources=[ROOT/'CVBenchmark/PROTOCOL.md',ROOT/'CVFollowup/PROTOCOL.md',
    ROOT/'CVBenchmark/results/medium_v2/fold_0/runtime/api/prompting.py',
    ROOT/'CVBenchmark/results/medium_v2/fold_0/runtime/api/dialog_history.py',
    ROOT/'CVBenchmark/results/medium_v2/fold_0/runtime/api/worker.py',
    REPORT/'gnn_corrected/comparison.json',ROOT/'reports/medium_cv_v2/api_usage.csv']
write(REPORT/'api_method_context_sources.json',{'document_sha256':sha(document),
    'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in sources},
    'confirmed_actual_confirmation_users':[380,420,382],
    'metadata_caveat':'Some selected.json selection descriptions retain hardcoded confirmation88 from old pilot; actual saved confirm metrics and bundle selection use380/420/382. Runtime and old artifacts unchanged.'})
record('api_method_context_documented','Prepared standalone Russian method/context briefing for an external ChatGPT discussion: actual Python-generated-only H008/H009 protocol, data/splits, prompts, validator, downstream model, budget20->30->40, confirmed results, uncertainties and improvement questions. Actual confirmation sizes checked; stale confirmation88 descriptive string identified as metadata only.',
    artifacts=str(document.relative_to(ROOT)))
