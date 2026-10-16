"""Download pinned source-model assets on Windows; no package installation."""
from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/models/recformer'
OUT.mkdir(parents=True, exist_ok=True)

def fetch(url, path):
    if path.exists():
        if path.suffix != '.bin' or zipfile.is_zipfile(path):
            print('exists', path.name, path.stat().st_size, flush=True)
            return
        path.replace(path.with_suffix(path.suffix+'.partial'))
    with urllib.request.urlopen(url, timeout=90) as response:
        if 'text/html' in response.headers.get('Content-Type', ''):
            html = response.read().decode()
            fields = dict(re.findall(r'name="([^"]+)" value="([^"]*)"', html))
            if not fields.get('id'):
                raise RuntimeError(html[:500])
            url = 'https://drive.usercontent.google.com/download?' + urllib.parse.urlencode(fields)
            return fetch(url, path)
        temp = path.with_suffix(path.suffix+'.partial')
        total = int(response.headers.get('Content-Length','0'))
        if path.suffix == '.bin':
            response.close()
            for attempt in range(100):
                offset=temp.stat().st_size if temp.exists() else 0
                if total and offset==total:
                    break
                request=urllib.request.Request(url,headers={'Range':f'bytes={offset}-{min(offset+32*1024*1024-1,total-1)}'})
                try:
                    with urllib.request.urlopen(request,timeout=90) as part:
                        if offset and part.status!=206:
                            raise RuntimeError('Server ignored resume range')
                        with temp.open('ab') as dest:
                            while block := part.read(1024*1024):
                                dest.write(block)
                    print('checkpoint bytes',temp.stat().st_size,'/',total,flush=True)
                except (TimeoutError, OSError) as error:
                    print('download retry',type(error).__name__,flush=True)
            assert temp.stat().st_size==total,(temp.stat().st_size,total)
            assert zipfile.is_zipfile(temp),'Incomplete checkpoint ZIP'
        else:
            with temp.open('wb') as dest:
                while block := response.read(1024*1024):
                    dest.write(block)
            assert not total or temp.stat().st_size==total
        temp.replace(path)
    print('downloaded', path.name, path.stat().st_size, flush=True)

fetch('https://drive.google.com/uc?export=download&id=1BEboY3NxAUOBe6YwYZ_RsQ4BR6IIbl0-', OUT/'recformer_seqrec.bin')
revision = '301e6a42cb0d9976a6d6a26a079fef81c18aa895'
for name in ['config.json','vocab.json','merges.txt']:
    fetch(f'https://huggingface.co/allenai/longformer-base-4096/resolve/{revision}/{name}', OUT/name)
manifest = {'checkpoint_source':'https://github.com/AaronHeee/RecFormer#pretrained-model',
            'checkpoint_file_id':'1BEboY3NxAUOBe6YwYZ_RsQ4BR6IIbl0-',
            'backbone_repo':'allenai/longformer-base-4096','backbone_revision':revision,
            'files':{}}
for p in OUT.iterdir():
    if p.is_file() and p.name != 'download_manifest.json':
        with p.open('rb') as file:
            digest=hashlib.file_digest(file,'sha256').hexdigest()
        manifest['files'][p.name]={'bytes':p.stat().st_size,'sha256':digest}
(OUT/'download_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(ROOT/'Recformer/assets_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
