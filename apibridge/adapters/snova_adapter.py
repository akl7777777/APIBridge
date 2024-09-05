import json
import requests
from .base_adapter import BaseAdapter
from apibridge.core.unified_response import UnifiedResponse


class SnovaAdapter(BaseAdapter):
    def process(self, unified_request):
        # 直接使用unified_request中的数据构造Snova API所需的请求体
        snova_data = {
            "body": {
                "messages": unified_request.data.get('messages', []),
                "max_tokens": unified_request.data.get('max_tokens', 800),
                "stop": unified_request.data.get('stop', ["<|eot_id|>"]),
                "stream": unified_request.data.get('stream', True),
                "stream_options": unified_request.data.get('stream_options', {"include_usage": True}),
                "model": unified_request.data.get('model', "llama3-405b")
            },
            "env_type": unified_request.data.get('env_type', "tp16405b")
        }

        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json'
        }

        # 发送请求到 Snova API
        response = requests.post(
            'https://fast.snova.ai/api/completion',
            headers=headers,
            json=snova_data,
            stream=snova_data['body']['stream']
        )

        unified_response = UnifiedResponse()
        unified_response.set_status_code(response.status_code)
        unified_response.set_headers(dict(response.headers))

        if snova_data['body']['stream']:
            unified_response.set_content(response.iter_lines())
        else:
            unified_response.set_content(response.json())

        unified_response.set_is_stream(snova_data['body']['stream'])

        return unified_response

    def to_chat_format(self, unified_response):
        if unified_response.is_stream:
            return self._format_stream(unified_response.content)
        else:
            return self._format_response(unified_response.content)

    def _format_stream(self, content):
        for line in content:
            if line:
                try:
                    if isinstance(line, bytes):
                        text = line.decode('utf-8').strip()
                    else:
                        text = line.strip()

                    if text.startswith('data: '):
                        text = text[6:]  # 移除 'data: ' 前缀

                    if text == '[DONE]':
                        yield {'done': True}
                        continue

                    chunk = json.loads(text)

                    if 'error' in chunk:
                        yield {'error': chunk['error']}
                    elif 'choices' in chunk:
                        formatted_chunk = {
                            'id': chunk['id'],
                            'object': chunk['object'],
                            'created': chunk['created'],
                            'model': chunk['model'],
                            'choices': [
                                {
                                    'index': choice['index'],
                                    'delta': choice.get('delta', {}),
                                    'finish_reason': choice['finish_reason']
                                } for choice in chunk['choices']
                            ]
                        }
                        if 'usage' in chunk:
                            formatted_chunk['usage'] = chunk['usage']
                        yield formatted_chunk
                except json.JSONDecodeError:
                    yield {'error': {'message': 'Failed to parse JSON response'}}
                except Exception as e:
                    yield {'error': {'message': str(e)}}

    def _format_response(self, response):
        if 'error' in response:
            return {'error': response['error']}
        return {
            'id': response['id'],
            'object': 'chat.completion',
            'created': response['created'],
            'model': response['model'],
            'choices': [
                {
                    'index': choice['index'],
                    'message': {
                        'role': 'assistant',
                        'content': choice['delta']['content']
                    },
                    'finish_reason': choice['finish_reason']
                } for choice in response['choices']
            ],
            'usage': response.get('usage', {})
        }
