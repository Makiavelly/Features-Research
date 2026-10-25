"""Bundle audited reports alongside the unchanged experiment outputs."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]


def main():
    info=json.loads((ROOT/'reports/provider_python_v1/current_run.json').read_text())
    out=Path(info['directory'])
    report=ROOT/'reports/gpt61sol_python_v1'
    audit=json.loads((report/'audit.json').read_text())
    review=json.loads((report/'validator_review.json').read_text())
    assert audit['status']==review['status']=='passed'
    target=out/'audited_report'
    target.mkdir(exist_ok=True)
    copied=[]
    for path in report.iterdir():
        if path.is_file() and path.suffix in {'.md','.json','.csv','.png'}:
            shutil.copy2(path,target/path.name);copied.append(path.name)
    bundle=out.parent/(out.name+'_results.zip')
    temporary=bundle.with_suffix('.partial')
    with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(out.rglob('*')):
            if path.is_file() and not any(part=='scratch' or part=='__pycache__' or part.endswith('_scratch') for part in path.relative_to(out).parts):
                archive.write(path,str(path.relative_to(out)))
    temporary.replace(bundle)
    result={'status':'audited_complete','run_id':out.name,'reports':sorted(copied),
            'bundle':str(bundle.relative_to(ROOT)),'sha256':hashlib.sha256(bundle.read_bytes()).hexdigest(),
            'api_requests':audit['stats']['calls'],'additional_api_requests_for_finalization':0}
    (ROOT/'reports/provider_python_v1/final_delivery.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
