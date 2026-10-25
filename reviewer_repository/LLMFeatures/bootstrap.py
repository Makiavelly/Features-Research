"""Project-local Ollama instance and pinned model, without touching user models."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "LLMFeatures/results/qwen25coder7b_seed42_v1"
MODEL = "qwen2.5-coder:7b-instruct-q4_K_M"
URL = "http://127.0.0.1:11435"
sys.path.insert(0, str(ROOT / "RelBenchGNN"))
from tracking import record


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, OLLAMA_HOST="127.0.0.1:11435",
               OLLAMA_MODELS=str(ROOT / "data/models/ollama_llmfe"),
               OLLAMA_NUM_PARALLEL="1", OLLAMA_MAX_LOADED_MODELS="1",
               OLLAMA_CONTEXT_LENGTH="4096")
    try:
        requests.get(URL + "/api/version", timeout=3).raise_for_status()
    except requests.RequestException:
        with (OUT / "ollama.log").open("a") as log:
            process = subprocess.Popen(["ollama", "serve"], env=env, stdout=log,
                                       stderr=subprocess.STDOUT, start_new_session=True)
        (OUT / "ollama.pid").write_text(str(process.pid))
        for _ in range(60):
            try:
                requests.get(URL + "/api/version", timeout=1).raise_for_status()
                break
            except requests.RequestException:
                time.sleep(1)
        else:
            raise RuntimeError("Project-local Ollama did not start")
    record("llmfe_model_setup", "Загрузка Qwen2.5-Coder-7B-Instruct Q4_K_M в отдельное хранилище проекта",
           "hm_llmfe_qwen25coder7b_seed42_v1", status="setup")
    previous = -1
    with requests.post(URL + "/api/pull", json={"model": MODEL, "stream": True},
                       stream=True, timeout=(30, 3600)) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            event = json.loads(line)
            if "error" in event:
                raise RuntimeError(event["error"])
            step = int(event.get("completed", 0)) // (512 * 1024 * 1024)
            if step != previous or event.get("status") == "success":
                print(json.dumps(event), flush=True)
                previous = step
    tags = requests.get(URL + "/api/tags", timeout=30).json()
    info = next(item for item in tags["models"] if item["name"] == MODEL)
    show = requests.post(URL + "/api/show", json={"model": MODEL}, timeout=30).json()
    manifest = {"model": info, "show": show,
                "ollama_version": requests.get(URL + "/api/version", timeout=10).json()}
    (OUT / "model_manifest.json").write_text(json.dumps(manifest, indent=2))
    smoke = requests.post(URL + "/api/generate", timeout=(30, 1800), json={
        "model": MODEL, "prompt": "Return JSON with key sql and value a DuckDB expression for average price.",
        "format": "json", "stream": False, "keep_alive": "30m",
        "options": {"seed": 42, "num_ctx": 4096, "num_predict": 80, "temperature": 0.2}})
    smoke.raise_for_status()
    (OUT / "llm_smoke.json").write_text(json.dumps(smoke.json(), indent=2))
    ps = requests.get(URL + "/api/ps", timeout=10).json()
    (OUT / "llm_runtime.json").write_text(json.dumps(ps, indent=2))
    print(json.dumps({"smoke": smoke.json(), "runtime": ps}), flush=True)
    record("llmfe_model_ready", "Локальная Qwen загрузилась и выполнила тестовую генерацию",
           "hm_llmfe_qwen25coder7b_seed42_v1", status="preparing", model=info, runtime=ps)


if __name__ == "__main__":
    main()
