"""Restore one actual paid request prompt overwritten by resume bookkeeping.

Preserve the reconstructed-but-unsent prompt. No model/data/selection changes.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record


def main():
    info=json.loads((ROOT/'reports/provider_python_v1/current_run.json').read_text())
    root=Path(info['directory'])
    changes=[]
    for path in sorted(root.glob('gpt61sol_python/candidates/*/response.json')):
        response=json.loads(path.read_text())
        request=json.loads((root/'api_attempts'/f"attempt_{response['api_attempt']:03d}"/'request.json').read_text())
        actual=request['messages'][1]['content']
        prompt=path.parent/'prompt.txt'
        if prompt.read_text()==actual:continue
        assert path.parent.name=='candidate_008' and response['api_attempt']==9
        source=ROOT/'LLMFeatures/results/hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1/gpt61sol_python/candidates/candidate_008/prompt.txt'
        assert source.read_text()==actual
        backup=path.parent/'resumed_prompt_not_sent.txt'
        assert not backup.exists()
        prompt.rename(backup)
        prompt.write_text(actual,encoding='utf-8')
        changes.append({'call':8,'api_attempt':9,'actual_prompt_sha256':hashlib.sha256(actual.encode()).hexdigest(),
                        'unused_reconstructed_prompt_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),
                        'source':'immutable api_attempts/attempt_009/request.json matches preserved v1 prompt'})
    result={'changes':changes,'api_calls':0,'model_data_selection_changes':False,
            'reason':'Resume reconstructed the v2 prompt before reusing the already saved v1 response8. That v2 reconstruction was never sent. The actual request body is authoritative; both texts are preserved.'}
    if changes:
        (root/'prompt_log_reconciliation.json').write_text(json.dumps(result,indent=2))
        record('provider_python_prompt_log_reconciled',
               'Независимый аудит нашёл неточность лога приresume call8: prompt.txt был заменён '
               'реконструированнымv2 текстом, хотя ответ повторно не запрашивался. '
               'Фактически отправленныйprompt восстановлен из неизменного APIrequest (совпадаетсv1); '
               'неотправленный текст сохранён отдельно. Данные, код модели, отбор и метрики не менялись.',
               info['run_id'],status='completed_pending_audit',artifacts=str(root.relative_to(ROOT)))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
