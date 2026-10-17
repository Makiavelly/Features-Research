"""Small explicit Chat Completions adapter. No automatic/billable hidden retries."""
import json
from pathlib import Path
import time
import urllib.error
import urllib.request


class ProviderUnavailable(BaseException):
    """Do not let a search loop treat a provider outage as bad feature code."""


def load_secret(path):
    for line in Path(path).read_text(encoding='utf-8-sig').splitlines():
        if '=' in line and line.split('=',1)[0].strip()=='ACCESS_TOKEN':
            value=line.split('=',1)[1].strip().strip('\"').strip("'")
            if value:return value
    raise RuntimeError('ACCESS_TOKEN missing in project .env')


class ProviderGenerator:
    def __init__(self,config,out,secret_path):
        self.config=config
        self.out=Path(out)
        self.folder=self.out/'api_attempts'
        self.folder.mkdir(exist_ok=True)
        self.secret=load_secret(secret_path)

    def __call__(self,prompt,seed):
        number=len(list(self.folder.glob('attempt_*')))+1
        if number>self.config['max_llm_calls']:
            raise ProviderUnavailable('API attempt limit300 reached; no additional request sent')
        directory=self.folder/f'attempt_{number:03d}'
        directory.mkdir()
        payload={'model':self.config['model_id'],
                 'messages':[{'role':'system','content':'Return only a complete DuckDB SQL script of SELECT/WITH queries following the user interface.'},
                             {'role':'user','content':prompt}],
                 'max_tokens':self.config['max_new_tokens'],'temperature':self.config['temperature'],
                 'top_p':1.0,'seed':seed,'reasoning_effort':self.config['reasoning_effort']}
        (directory/'request.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
        request=urllib.request.Request(self.config['base_url'].rstrip('/')+'/chat/completions',
                    data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+self.secret,
                    'Content-Type':'application/json','Accept':'application/json','User-Agent':'Features-Experiment/1.0'},method='POST')
        started=time.perf_counter()
        try:
            with urllib.request.urlopen(request,timeout=240) as response:
                raw=response.read().decode().replace(self.secret,'[REDACTED]')
                result=json.loads(raw)
                request_id=response.headers.get('x-request-id')
        except urllib.error.HTTPError as error:
            detail=error.read().decode(errors='replace').replace(self.secret,'[REDACTED]')[:2000]
            failure={'api_attempt':number,'http_status':error.code,'error':detail,'seconds':time.perf_counter()-started}
            (directory/'failure.json').write_text(json.dumps(failure,ensure_ascii=False,indent=2))
            raise ProviderUnavailable(f'API HTTP{error.code}: {detail}') from None
        except Exception as error:
            detail=str(error).replace(self.secret,'[REDACTED]')
            (directory/'failure.json').write_text(json.dumps({'api_attempt':number,'error':detail,'seconds':time.perf_counter()-started}))
            raise ProviderUnavailable('API transport failure: '+detail) from None
        (directory/'response.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
        try:
            choice=result['choices'][0]
            content=choice['message'].get('content') or ''
            if isinstance(content,list):content='\n'.join(x.get('text','') for x in content if isinstance(x,dict))
            if not isinstance(content,str):raise ValueError('Non-text model response')
        except (KeyError,IndexError,TypeError,ValueError):
            raise ProviderUnavailable('Unexpected API response schema; saved sanitized response for inspection') from None
        usage=result.get('usage',{})
        return {'text':content,'seed':seed,'prompt_tokens':usage.get('prompt_tokens',0),
                'generated_tokens':usage.get('completion_tokens',0),'seconds':time.perf_counter()-started,
                'truncated':choice.get('finish_reason')=='length','finish_reason':choice.get('finish_reason'),
                'api_attempt':number,'provider_model':result.get('model'),'provider_response_id':result.get('id'),
                'request_id':request_id,'usage':usage}
