# 如何新增 Provider 模块

本文档将指导你如何在 APIBridge 项目中新增一个 provider 模块。

## 目录

1. [概述](#概述)
2. [步骤](#步骤)
   1. [创建新的适配器类](#1-创建新的适配器类)
   2. [注册新的适配器](#2-注册新的适配器)
   3. [更新路由](#3-更新路由)
   4. [配置文件更新](#4-配置文件更新)
3. [最佳实践](#最佳实践)
4. [测试](#测试)
5. [故障排除](#故障排除)

## 概述

APIBridge 项目使用适配器模式来支持不同的 AI 提供商。要添加一个新的 provider，你需要创建一个新的适配器类，并在系统中注册它。

## 步骤

### 1. 创建新的适配器类

在 `apibridge/adapters/` 目录下创建一个新的 Python 文件，命名为 `your_provider_adapter.py`。

```python
from .base_adapter import BaseAdapter
from apibridge.core.unified_response import UnifiedResponse
import requests
import json

class YourProviderAdapter(BaseAdapter):
    def process(self, unified_request):
        # 将统一请求转换为你的 provider 特定的请求
        provider_specific_data = {
            # 根据你的 provider API 要求设置数据
        }

        headers = {
            # 设置必要的请求头
        }

        response = requests.post(
            unified_request.endpoint,
            headers=headers,
            json=provider_specific_data,
            stream=unified_request.data.get('stream', False)
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
        # 实现流式响应的格式化
        pass

    def _format_non_stream(self, content):
        # 实现非流式响应的格式化
        pass

    def _parse_stream(self, content):
        # 实现流式内容的解析
        pass
```

确保实现所有必要的方法，并根据你的 provider 的特定 API 要求进行调整。

### 2. 注册新的适配器

在 `app.py` 文件中，导入你的新适配器并注册它：

```python
from apibridge.adapters.your_provider_adapter import YourProviderAdapter

def create_app(config_class=Config):
    # ... 其他代码 ...

    # 注册适配器
    api_bridge = APIBridge()
    api_bridge.register_adapter('your_provider', YourProviderAdapter())

    # ... 其他代码 ...
```

### 3. 更新路由

在 `apibridge/api/routes.py` 文件中，确保你的新 provider 可以被正确路由：

```python
@bp.route('/<provider>/v1/chat/completions', methods=['POST'])
def chat_completions(provider):
    # ... 其他代码 ...

    if provider == 'your_provider':
        unified_request.set_endpoint('https://api.your-provider.com/v1/chat/completions')
    
    # ... 其他代码 ...
```

### 4. 配置文件更新

如果你的新 provider 需要特定的配置（如 API 密钥），请在 `config.py` 文件中添加相应的配置项：

```python
class Config:
    # ... 其他配置 ...
    YOUR_PROVIDER_API_KEY = os.environ.get('YOUR_PROVIDER_API_KEY')
```

## 最佳实践

1. **错误处理**：确保在你的适配器中妥善处理可能出现的错误，并返回有意义的错误消息。

2. **日志记录**：在关键点添加日志记录，以便于调试和监控。

3. **代码注释**：为你的代码添加清晰的注释，特别是对于复杂的逻辑或 provider 特定的行为。

4. **保持一致性**：尽量保持与现有适配器的接口和行为一致，除非你的 provider 有特殊需求。

## 测试

1. 为你的新适配器创建单元测试，放在 `tests/test_adapters/` 目录下。

2. 创建集成测试，确保你的适配器能够正确地与整个系统集成。

3. 测试各种场景，包括流式和非流式请求，错误处理等。

## 故障排除

如果你在集成过程中遇到问题，请检查以下几点：

1. 确保所有必要的依赖都已安装。
2. 检查配置文件中的 API 密钥和端点 URL 是否正确。
3. 查看日志以获取更详细的错误信息。
4. 确保你的适配器正确地处理了 provider 的响应格式。

如果问题仍然存在，请联系项目维护者寻求帮助。