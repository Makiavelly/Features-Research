"""Minimal local MCP stdio server; never prints secrets or banners to stdout."""
import argparse
import json
from pathlib import Path
import sys
import traceback
from toolbox import Toolbox, TOOLS, write


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fold', type=int, required=True)
    parser.add_argument('--session', required=True)
    parser.add_argument('--island', type=int, choices=range(3))
    args = parser.parse_args()
    box = Toolbox(args.fold, args.session, args.island)
    for line in sys.stdin:
        try:
            message = json.loads(line)
            if 'id' not in message:
                continue
            method = message['method']
            if method == 'initialize':
                result = {'protocolVersion': message.get('params', {}).get('protocolVersion', '2024-11-05'),
                          'capabilities': {'tools': {}},
                          'serverInfo': {'name': 'hm-train-fold', 'version': '1.0.0'}}
            elif method == 'ping':
                result = {}
            elif method == 'tools/list':
                result = {'tools': TOOLS}
            elif method == 'tools/call':
                params = message['params']
                try:
                    data = box.call(params['name'], params.get('arguments', {}))
                    result = {'content': [{'type': 'text', 'text': json.dumps(data, ensure_ascii=False)}]}
                except Exception as error:
                    data = {'error': str(error)[:2000]}
                    result = {'isError': True, 'content': [{'type': 'text', 'text': json.dumps(data, ensure_ascii=False)}]}
                with (box.root / 'tool_events.jsonl').open('a', encoding='utf-8') as stream:
                    stream.write(json.dumps({'tool': params['name'], 'arguments': params.get('arguments', {}), 'result': data}, ensure_ascii=False) + '\n')
            else:
                raise ValueError('Unsupported MCP method ' + method)
            response = {'jsonrpc': '2.0', 'id': message['id'], 'result': result}
        except Exception as error:
            response = {'jsonrpc': '2.0', 'id': message.get('id'), 'error': {'code': -32603, 'message': str(error)}}
        print(json.dumps(response, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
