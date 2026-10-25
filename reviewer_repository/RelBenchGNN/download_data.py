"""Download a pinned, reusable H&M snapshot without importing ML libraries."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPO = "stanford-star/relbench-v1"
DEST = ROOT / "data"


def get_json(url):
    with urllib.request.urlopen(url, timeout=120) as response:
        return json.load(response)


def main():
    info = get_json(f"https://huggingface.co/api/datasets/{REPO}")
    revision = info["sha"]
    files = get_json(f"https://huggingface.co/api/datasets/{REPO}/tree/{revision}/rel-hm?recursive=true")
    files = [item for item in files if item["type"] == "file"]
    DEST.mkdir(exist_ok=True)

    def download(item):
        target = DEST / item["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.stat().st_size != item["size"]:
            url = f"https://huggingface.co/datasets/{REPO}/resolve/{revision}/{item['path']}"
            partial = target.with_suffix(target.suffix + ".partial")
            with urllib.request.urlopen(url, timeout=180) as source, partial.open("wb") as output:
                while chunk := source.read(1024 * 1024):
                    output.write(chunk)
            if partial.stat().st_size != item["size"]:
                raise RuntimeError(f"Incomplete download: {target}")
            partial.replace(target)
        digest = hashlib.file_digest(target.open("rb"), "sha256").hexdigest()
        expected = item.get("lfs", {}).get("oid")
        if expected and digest != expected:
            raise RuntimeError(f"Checksum mismatch: {target}")
        print(f"OK {item['path']} ({item['size']:,} bytes)", flush=True)
        return {"path": item["path"], "size": item["size"], "sha256": digest}

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(download, files))
    (DEST / "download_manifest.json").write_text(
        json.dumps({"repo": REPO, "revision": revision, "files": results}, indent=2), encoding="utf-8"
    )
    print(f"Downloaded {len(results)} files to {DEST / 'rel-hm'}", flush=True)


if __name__ == "__main__":
    main()
