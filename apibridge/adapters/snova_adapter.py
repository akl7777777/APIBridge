import json
import requests
from flask import Response, stream_with_context
from .base_adapter import BaseAdapter
from apibridge.core.unified_response import UnifiedResponse


class SnovaAdapter(BaseAdapter):
    def process(self, unified_request):
        snova_data = {
            "body": {
                "messages": unified_request.data.get('messages', []),
                "max_tokens": unified_request.data.get('max_tokens', 800),
                "stop": unified_request.data.get('stop', ["<|eot_id|>"]),
                "stream": True,  # 总是使用流式请求
                "stream_options": {
                    "include_usage": True
                },
                "model": unified_request.data.get('model', "llama3-405b")
            },
            "env_type": unified_request.data.get('env_type', "tp16405b")
        }

        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json'
        }

        response = requests.post(
            'https://fast.snova.ai/api/completion',
            headers=headers,
            json=snova_data,
            stream=True
        )

        unified_response = UnifiedResponse()
        unified_response.set_status_code(response.status_code)
        unified_response.set_headers(dict(response.headers))
        unified_response.set_content(response)
        unified_response.set_is_stream(unified_request.data.get('stream', False))

        return unified_response

    def to_chat_format(self, unified_response):
        if unified_response.is_stream:
            return self._format_stream(unified_response.content)
        else:
            return self._format_non_stream(unified_response.content)

    def _format_stream(self, content):
        for chunk in self._parse_stream(content):
            yield f"data: {json.dumps(chunk)}\n\n"
        yield "data: [DONE]\n\n"

    def _format_non_stream(self, content):
        def generate():
            full_response = {
                'id': None,
                'object': 'chat.completion',
                'created': None,
                'model': None,
                'choices': [{
                    'index': 0,
                    'message': {
                        'role': 'assistant',
                        'content': ''
                    },
                    'finish_reason': None
                }],
                'usage': {}
            }

            for chunk in self._parse_stream(content):
                if 'id' in chunk and full_response['id'] is None:
                    full_response['id'] = chunk['id']
                if 'created' in chunk and full_response['created'] is None:
                    full_response['created'] = chunk['created']
                if 'model' in chunk and full_response['model'] is None:
                    full_response['model'] = chunk['model']

                if 'choices' in chunk and chunk['choices']:
                    choice = chunk['choices'][0]
                    if 'delta' in choice and 'content' in choice['delta']:
                        full_response['choices'][0]['message']['content'] += choice['delta']['content']
                    if 'finish_reason' in choice and choice['finish_reason'] is not None:
                        full_response['choices'][0]['finish_reason'] = choice['finish_reason']

                if 'usage' in chunk:
                    full_response['usage'] = chunk['usage']

            yield full_response

        return generate()

    def _parse_stream(self, content):
        for line in content.iter_lines():
            if line:
                try:
                    text = line.decode('utf-8').strip()
                    if text.startswith('data: '):
                        text = text[6:]
                    if text == '[DONE]':
                        break
                    chunk = json.loads(text)
                    yield chunk
                except json.JSONDecodeError:
                    yield {'error': {'message': 'Failed to parse JSON response'}}
                except Exception as e:
                    yield {'error': {'message': str(e)}}
