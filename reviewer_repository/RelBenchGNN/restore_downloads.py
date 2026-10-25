"""Restore exact public snapshots from committed manifests (Python >= 3.11)."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def restore(name, verify_only=False):
    manifest_path, destination, category = {
        "data": (ROOT / "data/download_manifest.json", ROOT / "data", "datasets/"),
        "glove": (ROOT / "data/glove_download_manifest.json", ROOT / "data/models/glove", ""),
    }[name]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for entry in manifest["files"]:
        target = (destination / entry["path"]).resolve()
        if not target.is_relative_to(destination.resolve()):
            raise ValueError(f"Path outside destination: {entry['path']}")
        def valid(path):
            if not path.is_file() or path.stat().st_size != entry["size"]:
                return False
            with path.open("rb") as stream:
                return hashlib.file_digest(stream, "sha256").hexdigest() == entry["sha256"]
        if not valid(target):
            if verify_only:
                raise RuntimeError(f"Missing or invalid file: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            url = f"https://huggingface.co/{category}{manifest['repo']}/resolve/{manifest['revision']}/{entry['path']}"
            partial = target.with_name(target.name + ".partial")
            with urllib.request.urlopen(url, timeout=180) as source, partial.open("wb") as output:
                while chunk := source.read(1024 * 1024):
                    output.write(chunk)
            if not valid(partial):
                raise RuntimeError(f"Checksum mismatch: {partial}")
            partial.replace(target)
        print(f"OK {target.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", choices=["data", "glove", "all"])
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    for snapshot in (["data", "glove"] if args.snapshot == "all" else [args.snapshot]):
        restore(snapshot, args.verify_only)
