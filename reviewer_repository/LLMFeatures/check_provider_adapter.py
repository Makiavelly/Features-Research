"""No-network checks: budget persistence, redaction, and provider failures."""
import io
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
import urllib.error
from provider_api import ProviderGenerator,ProviderUnavailable


class Response:
    headers={'x-request-id':'test-request'}
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self):return json.dumps({'model':'gpt-6.1-sol','id':'test',
        'choices':[{'message':{'content':'SELECT article_id,count(*) AS f_n FROM history GROUP BY article_id;'},'finish_reason':'stop'}],
        'usage':{'prompt_tokens':100,'completion_tokens':20,'total_tokens':120}}).encode()


def main():
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory)
        env=root/'secret.env'
        env.write_text('ACCESS_TOKEN=secret_test_value')
        out=root/'run'
        out.mkdir()
        config=dict(model_id='gpt-6.1-sol',base_url='https://example.invalid/v1',max_llm_calls=2,
                    max_new_tokens=2048,temperature=.8,reasoning_effort='low')
        client=ProviderGenerator(config,out,env)
        calls=[]
        def success(request,timeout):
            calls.append(json.loads(request.data))
            assert request.get_header('Authorization')=='Bearer secret_test_value'
            return Response()
        with patch('urllib.request.urlopen',success):
            result=client('Prompt1',42)
            assert result['text'].startswith('SELECT') and result['generated_tokens']==20
            assert calls[0]['seed']==42 and calls[0]['max_tokens']==2048
        def denied(request,timeout):
            raise urllib.error.HTTPError(request.full_url,401,'Unauthorized',{},io.BytesIO(b'bad secret_test_value'))
        with patch('urllib.request.urlopen',denied):
            try:client('Prompt2',43)
            except ProviderUnavailable as error:assert 'secret_test_value' not in str(error)
            else:raise AssertionError('Provider failure did not stop search')
        resumed=ProviderGenerator(config,out,env)
        with patch('urllib.request.urlopen',lambda *_a,**_k:(_ for _ in ()).throw(AssertionError('Over budget HTTP call'))):
            try:resumed('Prompt3',44)
            except ProviderUnavailable:pass
            else:raise AssertionError('Budget limit ignored after resume')
        assert len(list((out/'api_attempts').glob('attempt_*')))==2
        for file in out.rglob('*.json'):assert 'secret_test_value' not in file.read_text()
    print('PASSED: no-network API payload, failure stop, credential redaction, persistent attempt budget')


if __name__=='__main__':main()
