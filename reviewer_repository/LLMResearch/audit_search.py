"""Audit a completed search without opening heldout/test targets or predictions."""
import argparse
from common import OUT, read, record
from report import audit


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fold', type=int, choices=range(3))
    args = parser.parse_args()
    folder = OUT / f'fold_{args.fold}'
    assert (folder / 'trained.json').exists(), 'Search and confirmation not finished'
    trials, queries, usage = audit(args.fold)
    counts = {'accepted': sum(t['status'] == 'valid' for t in trials),
              'research_queries': len(queries), 'successful_research_queries': sum(q['ok'] for q in queries),
              'API_attempts': len(usage)}
    record('h010_search_audited',
           f'Fold{args.fold}: exact real API histories, own-population isolation, saved tool results, retry accounting and frozen database hash verified; no outer data read.',
           read(folder / 'run_config.json')['protocol'], status='selected_pending_test', audit=counts)
    print(counts, flush=True)
