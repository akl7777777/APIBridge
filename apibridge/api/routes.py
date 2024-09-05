import json

from flask import Blueprint, request, jsonify, stream_with_context, Response, current_app
from apibridge.core.api_bridge import APIBridge
from apibridge.core.unified_request import UnifiedRequest

bp = Blueprint('api', __name__)

@bp.route('/<provider>/v1/chat/completions', methods=['POST'])
def chat_completions(provider):
    api_bridge = current_app.config['API_BRIDGE']
    data = request.json
    unified_request = UnifiedRequest()
    unified_request.set_api_type(provider)
    if provider == 'snova':
        unified_request.set_endpoint('https://fast.snova.ai/api/completion')
    else:
        unified_request.set_endpoint(f"https://api.{provider}.com/v1/chat/completions")
    unified_request.set_method('POST')
    unified_request.set_headers(request.headers)
    unified_request.set_data(data)
    unified_request.set_stream(data.get('stream', False))

    try:
        response = api_bridge.process_request(unified_request)

        if unified_request.stream:
            def generate():
                for chunk in response.content:
                    if isinstance(chunk, dict):
                        if 'done' in chunk:
                            yield 'data: [DONE]\n\n'
                        elif 'error' in chunk:
                            yield f"data: {json.dumps(chunk)}\n\n"
                        else:
                            yield f"data: {json.dumps(chunk)}\n\n"
                    elif isinstance(chunk, (str, bytes)):
                        if isinstance(chunk, bytes):
                            chunk = chunk.decode('utf-8')
                        lines = chunk.split('\n')
                        for line in lines:
                            if line.strip():
                                yield f"{line}\n\n"

            headers = {
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Content-Type': 'text/event-stream',
            }
            return Response(stream_with_context(generate()), content_type='text/event-stream', headers=headers)
        else:
            return jsonify(response.content)
    except Exception as e:
        return jsonify({'error': {'message': str(e), 'type': 'internal_error'}}), 500

@bp.route('/<provider>/v1/models', methods=['GET'])
def list_models(provider):
    # 这里可以根据不同的提供商返回不同的模型列表
    models = {
        'openai': [
            {"id": "gpt-3.5-turbo", "object": "model", "created": 1677610602, "owned_by": "openai"},
            {"id": "gpt-4", "object": "model", "created": 1687882411, "owned_by": "openai"}
        ],
        'anthropic': [
            {"id": "claude-2", "object": "model", "created": 1687882411, "owned_by": "anthropic"},
            {"id": "claude-instant-1", "object": "model", "created": 1687882411, "owned_by": "anthropic"}
        ],
        # 可以添加更多提供商的模型列表
    }
    return jsonify({"object": "list", "data": models.get(provider, [])})


@bp.route('/<provider>/v1/engines', methods=['GET'])
def list_engines(provider):
    # 为了向后兼容，可以保留 engines 端点
    return list_models(provider)
