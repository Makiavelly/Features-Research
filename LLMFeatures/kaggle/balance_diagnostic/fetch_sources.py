"""Freeze original public LLMFE inputs; never execute downloaded source."""
import hashlib
import json
from pathlib import Path
import urllib.request

HERE=Path(__file__).resolve().parent
def fetch(url):
    request=urllib.request.Request(url,headers={'User-Agent':'LLMFE-diagnostic'})
    return urllib.request.urlopen(request,timeout=60).read()
revision=json.loads((HERE/'upstream_manifest.json').read_text())['revision'] if (HERE/'upstream_manifest.json').exists() else json.loads(fetch('https://api.github.com/repos/nikhilsab/LLMFE/commits/main'))['sha']
tree=[] if (HERE/'upstream_manifest.json').exists() else json.loads(fetch('https://api.github.com/repos/nikhilsab/LLMFE/git/trees/'+revision+'?recursive=1'))['tree']
paths=['LICENSE','specs/specification_balance-scale.txt','data/balance-scale.csv','llmfe/buffer.py',
       'llmfe/sampler.py','utils.py','preprocessing.py']
paths.extend(item['path'] for item in tree if item['path'].startswith('prompts/') and item['type']=='blob')
if (HERE/'upstream_manifest.json').exists():
    paths=list(dict.fromkeys(paths+list(json.loads((HERE/'upstream_manifest.json').read_text())['files'])))
manifest={'repository':'https://github.com/nikhilsab/LLMFE','revision':revision,'files':{}}
for path in paths:
    url='https://raw.githubusercontent.com/nikhilsab/LLMFE/'+revision+'/'+path
    destination=HERE/'upstream'/path;destination.parent.mkdir(parents=True,exist_ok=True)
    payload=destination.read_bytes() if destination.exists() else fetch(url)
    destination.write_bytes(payload)
    manifest['files'][path]={'url':url,'sha256':hashlib.sha256(payload).hexdigest()}
(HERE/'upstream_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'revision':revision,'files':list(manifest['files'])},indent=2))
