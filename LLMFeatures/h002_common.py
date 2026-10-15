"""Frozen H002 protocol; environment is set before importing the evaluator."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = "hm_llmfe_qwen25coder7b_seed42_h002_shared_v1"
OUT = ROOT / "LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1"
CACHE = ROOT / "baseline/cache/llmfe_h002_shared_v1"
REPORT = ROOT / "reports/llmfe_h002_shared_v1"
OLD = ROOT / "LLMFeatures/results/qwen25coder7b_seed42_v2"
os.environ.update(LLMFE_OUT=str(OUT), LLMFE_CACHE=str(CACHE), LLMFE_RUN=RUN,
                  LLMFE_TRAIN_THREADS="8", LLMFE_PREDICT_THREADS="8",
                  LLMFE_VALIDATOR_VERSION="h002", OMP_NUM_THREADS="8", MKL_NUM_THREADS="8")
CONFIG = {"run_id": RUN, "hypothesis": "H002", "seed": 42,
          "llm": "qwen2.5-coder:7b-instruct-q4_K_M",
          "model_digest": "dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364",
          "target_successful_distinct": 20, "max_llm_calls": 100, "max_repairs_per_proposal": 2,
          "islands": 3, "memory_programs": 1, "context_tokens": 4096,
          "generation_tokens": 1800, "temperature": .8, "train_pairs": 803377,
          "train_user_times": 50000, "pair_selection_seed": 2026,
          "training_threads": 8, "prediction_threads": 8, "rounds": 150,
          "search_users": 256, "confirmation_users": 1024, "confirmation_candidates": 3,
          "search_protocol": "fixed saved ID-GNN candidates; same user selections as v2",
          "final_protocol": "all val/test users, exact saved ID-GNN candidate pools, independent full replay",
          "full_catalog": False, "validator": "h002: WITHIN GROUP syntax false rejection fixed",
          "control": "v2 five measured sets; different search pool, increased calls, repair and prompt changes confound isolated attribution",
          "downstream": "same binary LightGBM150/leaves31/seeds42 as v2, 8 threads",
          "test_policy": "test only after selection frozen on disjoint validation confirmation"}
