"""Explicit, audited transient retry; never delete or discount a POST attempt."""
import argparse
from pathlib import Path
from common import OUT, REPORT, read, write, record


def main(fold, generation, step_index):
    if (REPORT / 'pipeline.pid').exists():
        pid = int((REPORT / 'pipeline.pid').read_text())
        path = Path(f'/proc/{pid}/cmdline')
        if path.exists() and b'LLMResearch/pipeline.py' in path.read_bytes():
            raise RuntimeError('Stop live controller before explicit recovery')
    folder = OUT / f'fold_{fold}'
    step = folder / f'generations/call_{generation:03d}/step_{step_index:02d}'
    assert not (step / 'response.json').exists()
    plan = read(step / 'request_plan.json')
    old = plan['api_attempt']
    attempt = folder / 'api_attempts' / f'attempt_{old:03d}'
    assert not (attempt / 'response.json').exists(), 'Use saved paid response instead'
    failure = read(attempt / 'failure.json')
    detail = failure.get('error', '').lower()
    assert failure.get('http_status', 0) in [429, 500, 502, 503, 504] or any(
        text in detail for text in ['timed out', 'timeout', 'connection reset', 'connection refused', 'temporary failure'])
    historypath = step / 'explicit_retries.json'
    history = read(historypath) if historypath.exists() else []
    assert len(history) < 3, 'Three explicit retries exhausted; inspect provider availability'
    upcoming = len(list((folder / 'api_attempts').glob('attempt_*'))) + 1
    cfg = read(folder / 'run_config.json')
    assert upcoming <= cfg['max_llm_calls']
    history.append({'failed_attempt': old, 'next_attempt': upcoming, 'failure': failure,
                    'reason': 'Explicit retry after inspected transient provider/transport failure; preserve all attempts in global cap'})
    write(historypath, history)
    write(step / 'request_plan.json', {'api_attempt': upcoming})
    record('h010_explicit_transport_retry',
           f'Fold{fold} generation{generation} step{step_index}: attempt{old} failed transiently; preserve failure, explicitly schedule attempt{upcoming}. No successful response or evaluated program repeated.',
           cfg['protocol'], status='resuming', failed_attempt=old, next_attempt=upcoming,
           failure=failure)
    print('Explicit retry', old, '->', upcoming, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fold', type=int, choices=range(3))
    parser.add_argument('generation', type=int)
    parser.add_argument('step', type=int)
    args = parser.parse_args()
    main(args.fold, args.generation, args.step)
