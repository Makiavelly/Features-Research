"""Synthetic dialog and mocked-adapter tests; no real network/API requests."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT/'LLMFeatures/provider_history_runtime_v1'
OUT = ROOT/'reports/provider_history_v1'
sys.path.insert(0,str(CODE))
from dialog_history import build_messages,next_island
from provider_api import ProviderGenerator,ProviderUnavailable

def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj),encoding='utf-8')

def main():
    config={'arm':'gpt61sol_generated_only','seed':42,'islands':3,'max_repairs_per_proposal':3,
            'system_message':'SYSTEM ONLY','max_llm_calls':1,'model_id':'mock-model',
            'base_url':'https://invalid.example/v1','max_new_tokens':2048,'temperature':.8,'reasoning_effort':'low'}
    passed=[]
    with tempfile.TemporaryDirectory(prefix='dialog_test_') as temporary:
        out=Path(temporary)/'fixture'
        out.mkdir()
        def store(call,island,proposal,repair,status,score=None,error=None):
            prompt='TASK_'+str(call)
            messages=build_messages(config,out,prompt,42+call-1)
            folder=out/config['arm']/'candidates'/f'candidate_{call:03d}'
            trial={'call':call,'island':island,'proposal':proposal,'repair':repair,'status':status,
                   'directory':str(folder),'unchanged_repair':False}
            if score is not None:trial['score']=score
            if error:trial.update(error=error,failure_stage='preflight')
            write(folder/'trial.json',trial)
            write(folder/'response.json',{'text':'ASSISTANT_'+str(call),'api_attempt':call})
            write(out/'api_attempts'/f'attempt_{call:03d}'/'request.json',{'messages':messages})
            return messages
        assert build_messages(config,out,'TASK_1',42)==[
            {'role':'system','content':'SYSTEM ONLY'},{'role':'user','content':'TASK_1'}]
        passed.append('first_call_system_user_only')
        store(1,0,0,0,'valid',.1)
        second=store(2,1,1,0,'valid',.2)
        third=store(3,2,2,0,'valid',.3)
        assert len(second)==len(third)==2
        passed.append('initial_islands_do_not_share_history')
        fourth=store(4,0,3,0,'rejected',error='BAD_COLUMN')
        assert len(fourth)==4 and fourth[2]['content']=='ASSISTANT_1'
        assert 'search_map_fraction' in fourth[-1]['content'] and '0.1' in fourth[-1]['content']
        passed.append('accepted_response_and_search_feedback_retained')
        fifth=build_messages(config,out,'TASK_5',46)
        assert fifth[:4]==fourth
        assert fifth[4]=={'role':'assistant','content':'ASSISTANT_4'}
        assert 'BAD_COLUMN' in fifth[-1]['content']
        assert all('ASSISTANT_2' not in m['content'] and 'ASSISTANT_3' not in m['content'] for m in fifth)
        passed.extend(['rejected_response_and_error_retained','exact_prefix_preservation_no_truncation','no_cross_island_assistants'])
        assert build_messages(config,out,'TASK_5',46)==fifth
        passed.append('resume_reconstructs_identical_payload')
        store(5,0,3,1,'valid',.4)
        sixth=build_messages(config,out,'TASK_6',47)
        assert len(sixth)==4 and sixth[2]['content']=='ASSISTANT_2'
        passed.append('successful_repair_advances_to_next_population')
        last={'proposal':3,'repair':3,'status':'rejected'}
        assert next_island(config,[last])==1
        assert next_island(config,[{**last,'repair':1,'unchanged_repair':True}])==1
        passed.extend(['repair_budget_moves_population','unchanged_repair_matches_search_semantics'])
        mockout=Path(temporary)/'adapter'
        mockout.mkdir()
        fake_secret=Path(temporary)/'fake.env'
        fake_secret.write_text('ACCESS_TOKEN=synthetic-test-secret\n')
        captured=[]
        class Response:
            headers={'x-request-id':'mock-request'}
            def __enter__(self):return self
            def __exit__(self,*args):return False
            def read(self):
                return json.dumps({'model':'mock-model','choices':[{'message':{'content':'MOCK_RESPONSE'},'finish_reason':'stop'}],
                                   'usage':{'prompt_tokens':17,'completion_tokens':3}}).encode()
        def urlopen(request,timeout):
            captured.append(json.loads(request.data))
            return Response()
        with patch('urllib.request.urlopen',urlopen):
            generator=ProviderGenerator(config,mockout,fake_secret)
            response=generator('TASK_1',42)
            assert response['text']=='MOCK_RESPONSE'
            assert captured[0]['messages']==build_messages(config,mockout,'TASK_1',42)
            saved=(mockout/'api_attempts/attempt_001/request.json').read_text()
            assert 'synthetic-test-secret' not in saved and 'Authorization' not in saved
            try:generator('TASK_1',42)
            except ProviderUnavailable:pass
            else:raise AssertionError('API budget not enforced')
        assert len(captured)==1
        passed.extend(['adapter_sends_exact_message_list','saved_payload_excludes_secret','actual_attempt_budget_enforced'])
    result={'status':'passed','checks':passed,'real_api_calls':0,'mock_requests':1,
            'dialog_module_sha256':hashlib.sha256((CODE/'dialog_history.py').read_bytes()).hexdigest(),
            'provider_module_sha256':hashlib.sha256((CODE/'provider_api.py').read_bytes()).hexdigest()}
    OUT.mkdir(exist_ok=True)
    (OUT/'dialog_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':main()
