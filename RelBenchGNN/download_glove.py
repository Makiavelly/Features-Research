"""Download the original text encoder locally; skip the duplicate safetensors copy."""
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPO = "sentence-transformers/average_word_embeddings_glove.6B.300d"
DEST = ROOT / "data/models/glove"


def read_json(url):
    with urllib.request.urlopen(url, timeout=120) as response:
        return json.load(response)


def main():
    revision = read_json(f"https://huggingface.co/api/models/{REPO}")["sha"]
    tree = read_json(f"https://huggingface.co/api/models/{REPO}/tree/{revision}?recursive=true")
    manifest = []
    for item in tree:
        if item["type"] != "file" or item["path"].endswith(".safetensors"):
            continue
        target = DEST / item["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.stat().st_size != item["size"]:
            url = f"https://huggingface.co/{REPO}/resolve/{revision}/{item['path']}"
            partial = target.with_suffix(target.suffix + ".partial")
            with urllib.request.urlopen(url, timeout=180) as source, partial.open("wb") as output:
                while chunk := source.read(1024 * 1024):
                    output.write(chunk)
            if partial.stat().st_size != item["size"]:
                raise RuntimeError(f"Incomplete download: {target}")
            partial.replace(target)
        with target.open("rb") as file:
            digest = hashlib.file_digest(file, "sha256").hexdigest()
        expected = item.get("lfs", {}).get("oid")
        if expected and digest != expected:
            raise RuntimeError(f"Checksum mismatch: {target}")
        manifest.append({"path": item["path"], "size": item["size"], "sha256": digest})
        print(f"OK GloVe {item['path']}", flush=True)
    (DEST / "download_manifest.json").write_text(json.dumps({"repo": REPO, "revision": revision, "files": manifest}, indent=2))


if __name__ == "__main__":
    main()
