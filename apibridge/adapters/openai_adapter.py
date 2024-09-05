import requests

from apibridge.adapters.base_adapter import BaseAdapter
from apibridge.core.unified_response import UnifiedResponse


class OpenAIAdapter(BaseAdapter):
    def process(self, unified_request):
        # 处理请求，调用OpenAI API
        response = requests.request(
            method=unified_request.method,
            url=unified_request.endpoint,
            headers=unified_request.headers,
            params=unified_request.params,
            json=unified_request.data,
            stream=unified_request.stream,
            timeout=unified_request.timeout
        )

        unified_response = UnifiedResponse()
        unified_response.set_status_code(response.status_code)
        unified_response.set_headers(dict(response.headers))
        unified_response.set_content(response.text)
        unified_response.set_is_stream(unified_request.stream)

        return unified_response

    def to_chat_format(self, unified_response):
        # 将OpenAI的响应转换为统一的chat格式
        # 这里需要根据OpenAI的响应格式进行具体实现
        pass
