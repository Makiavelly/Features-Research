"""One isolated provider-compatibility request, with no dataset or tools executed."""
import json
import sys
import time
import urllib.error
import urllib.request
from common import ROOT, REPORT, read, write, record

sys.path.insert(0, str(ROOT / 'LLMFeatures'))
from provider_api import load_secret


def main():
    folder = REPORT / 'responses_compatibility_probe'
    resultpath = folder / 'result.json'
    assert not resultpath.exists(), 'Probe already recorded; inspect it instead of repeating'
    token = load_secret(ROOT / '.env')
    config = read(ROOT / 'CVBenchmark/results/medium_v2/fold_0/h009/run_config.json')
    payload = {'model': config['model_id'], 'input': 'Call compatibility_ping with nonce="fold-agent-probe". No other work.',
               'max_output_tokens': 128, 'reasoning': {'effort': 'low'}, 'stream': False,
               'tools': [{'type': 'function', 'name': 'compatibility_ping', 'description': 'Compatibility check; no filesystem access or dataset.',
                          'parameters': {'type': 'object', 'properties': {'nonce': {'type': 'string'}},
                                         'required': ['nonce'], 'additionalProperties': False}, 'strict': True}],
               'tool_choice': {'type': 'function', 'name': 'compatibility_ping'}}
    write(folder / 'request.json', payload)
    request = urllib.request.Request(config['base_url'].rstrip('/') + '/responses',
              data=json.dumps(payload).encode(), headers={'Authorization': 'Bearer ' + token,
              'Content-Type': 'application/json', 'User-Agent': 'Features-Responses-Compatibility/1.0'}, method='POST')
    tick = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            text = response.read().decode().replace(token, '[REDACTED]')
            result = json.loads(text)
        write(folder / 'response.json', result)
        calls = [x for x in result.get('output', []) if x.get('type') == 'function_call']
        status = {'supported_response_schema': isinstance(result.get('output'), list),
                  'function_call_returned': any(x.get('name') == 'compatibility_ping' for x in calls),
                  'provider_model': result.get('model'), 'usage': result.get('usage'),
                  'seconds': time.monotonic() - tick, 'dataset_sent': False, 'executed_tools': 0}
    except urllib.error.HTTPError as error:
        status = {'supported_response_schema': False, 'http_status': error.code,
                  'error': error.read().decode(errors='replace').replace(token, '[REDACTED]')[:1600],
                  'seconds': time.monotonic() - tick, 'dataset_sent': False, 'executed_tools': 0}
    except Exception as error:
        status = {'supported_response_schema': None, 'error': str(error).replace(token, '[REDACTED]'),
                  'seconds': time.monotonic() - tick, 'dataset_sent': False, 'executed_tools': 0}
    write(resultpath, status)
    record('responses_agent_compatibility_probe', 'Separate Responses API/function-call compatibility probe for requested agent environment. No fold data sent and no tools executed.',
           'hm_gpt61sol_agent_environment_probe_v1', status='probe_recorded', result=status)
    print(json.dumps(status, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
