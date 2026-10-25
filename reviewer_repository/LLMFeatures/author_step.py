"""Sequentially commit/evaluate assistant-written decisions; no feature search."""
from contextlib import redirect_stdout
from pathlib import Path
import sys
import run_authored20 as experiment


def main():
    info=experiment.read(experiment.REGISTRY)
    out=Path(info['directory'])
    config=experiment.read(out/'run_config.json')
    assert experiment.sha(Path(experiment.__file__))==config['runtime_sha256']['run_authored20.py']
    for filename in sys.argv[1:]:
        with (out/'host_commit.log').open('a',encoding='utf-8') as log,redirect_stdout(log):
            experiment.commit(Path(filename))
        experiment.evaluate_pending()


if __name__=='__main__':main()
