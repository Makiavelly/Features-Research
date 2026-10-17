"""Read-only provider discovery; never print or store credentials."""
import json
from pathlib import Path
import urllib.request
import urllib.error
import argparse

ROOT=Path(__file__).resolve().parents[1]


def credential():
    for line in (ROOT/'.env').read_text(encoding='utf-8-sig').splitlines():
        if '=' in line and line.split('=',1)[0].strip()=='ACCESS_TOKEN':
            value=line.split('=',1)[1].strip().strip('\"').strip("'")
            if value:return value
    raise RuntimeError('ACCESS_TOKEN missing in project .env')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base-url',default='https://tooken.club/v1')
    args=parser.parse_args()
    token=credential()
    request=urllib.request.Request(args.base_url.rstrip('/')+'/models',headers={'Authorization':'Bearer '+token,'Accept':'application/json','User-Agent':'Features-Experiment/1.0'})
    try:
        with urllib.request.urlopen(request,timeout=60) as response:
            result=json.loads(response.read())
    except urllib.error.HTTPError as error:
        message=error.read().decode(errors='replace').replace(token,'[REDACTED]')[:1200]
        print(json.dumps({'status':error.code,'error':message},ensure_ascii=False))
        raise SystemExit(1)
    folder=ROOT/'reports/tokenclub_probe_v1'
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'models.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    models=result.get('data',[]) if isinstance(result,dict) else result
    print(json.dumps({'http_status':200,'models':models},ensure_ascii=False)[:6500])


if __name__=='__main__':main()
