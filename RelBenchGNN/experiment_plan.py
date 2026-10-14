"""Shared selection of seeds for training, inference, baselines and reports."""
import json
from pathlib import Path


def selected_seeds():
    plan = json.loads(Path(__file__).with_suffix(".json").read_text())
    seeds = plan["seeds"]
    if not seeds or len(set(seeds)) != len(seeds) or not all(isinstance(seed, int) for seed in seeds):
        raise ValueError("Expected unique integer seeds")
    return seeds


if __name__ == "__main__":
    print(" ".join(map(str, selected_seeds())))
