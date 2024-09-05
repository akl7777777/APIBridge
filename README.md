# APIBridge
APIBridge A bridge that converts any interface into a chat format API.


# APIBridge 使用指南

本文档将指导你如何使用 APIBridge 项目来调用不同 AI provider 的接口。

## 目录

1. [概述](#概述)
2. [基本用法](#基本用法)
3. [支持的 Providers](#支持的-providers)
4. [请求格式](#请求格式)
5. [响应格式](#响应格式)
6. [流式与非流式请求](#流式与非流式请求)
7. [错误处理](#错误处理)
8. [示例](#示例)
9. [高级用法](#高级用法)
10. [常见问题解答](#常见问题解答)

## 概述

APIBridge 是一个统一的 AI 接口调用平台，允许你使用一致的 API 格式来访问多个 AI provider 的服务。

## 基本用法

APIBridge 的基本端点格式如下：

```
POST https://your-api-bridge-domain.com/{provider}/v1/chat/completions
```

其中 `{provider}` 是你想要使用的 AI provider 的标识符。

## 支持的 Providers

目前，APIBridge 支持以下 providers：

- OpenAI: `openai`
- Snova: `snova`
- Anthropic: `anthropic`
- (其他已集成的 providers...)

## 请求格式

请求体应该是一个 JSON 对象，格式类似于 OpenAI 的 API：

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "temperature": 0.7,
  "max_tokens": 150,
  "stream": false
}
```

注意：具体参数可能因 provider 而异，但 APIBridge 会尽可能进行统一转换。

## 响应格式

响应也会尽可能遵循 OpenAI 的格式：

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-3.5-turbo-0613",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Hello! As an AI language model, I don't have feelings, but I'm functioning well and ready to assist you. How can I help you today?"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 29,
    "total_tokens": 38
  }
}
```

## 流式与非流式请求

### 非流式请求

默认情况下，请求是非流式的。你会收到一个完整的 JSON 响应。

### 流式请求

要进行流式请求，设置 `"stream": true` 在你的请求体中。响应将以 Server-Sent Events (SSE) 格式返回：

```
data: {"id": "chatcmpl-123", "object": "chat.completion.chunk", "created": 1677652288, "model": "gpt-3.5-turbo", "choices": [{"index": 0, "delta": {"content": "Hello"}, "finish_reason": null}]}

data: {"id": "chatcmpl-123", "object": "chat.completion.chunk", "created": 1677652288, "model": "gpt-3.5-turbo", "choices": [{"index": 0, "delta": {"content": "!"}, "finish_reason": null}]}

data: [DONE]
```

## 错误处理

如果发生错误，你将收到一个带有错误详情的 JSON 响应：

```json
{
  "error": {
    "message": "Error message here",
    "type": "error_type",
    "param": null,
    "code": null
  }
}
```

## 示例

### 使用 cURL

```bash
curl -X POST https://your-api-bridge-domain.com/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Say this is a test"}],
    "temperature": 0.7
  }'
```

### 使用 Python

```python
import requests

url = "https://your-api-bridge-domain.com/snova/v1/chat/completions"
headers = {"Content-Type": "application/json"}
data = {
    "model": "llama3-405b",
    "messages": [{"role": "user", "content": "Say this is a test"}],
    "temperature": 0.7
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## 高级用法

### 切换 Providers

你可以通过简单地更改 URL 中的 provider 标识符来切换不同的 AI providers：

```python
# 使用 OpenAI
url = "https://your-api-bridge-domain.com/openai/v1/chat/completions"

# 切换到 Snova
url = "https://your-api-bridge-domain.com/snova/v1/chat/completions"
```

### 自定义请求头

某些 providers 可能需要额外的认证或自定义头。你可以在请求中包含这些：

```python
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY",
    "X-Custom-Header": "custom_value"
}
```

## 常见问题解答

1. **Q: 如何获取 API 密钥？**
   A: API 密钥管理取决于你的 APIBridge 部署。请联系你的系统管理员获取适当的认证信息。

2. **Q: 支持哪些模型？**
   A: 支持的模型取决于各个 provider。通常，你可以在请求中指定模型名称，APIBridge 将尝试使用最接近的可用模型。

3. **Q: 如何处理速率限制？**
   A: APIBridge 可能实现了自己的速率限制，或者传递底层 provider 的限制。请参考你的 APIBridge 部署的具体文档。

4. **Q: 可以同时使用多个 providers 吗？**
   A: 是的，你可以通过发送请求到不同的端点来使用多个 providers。这允许你在不同的 AI 服务之间进行负载均衡或比较结果。

## 开发者信息

如果你需要对 APIBridge 项目进行二次开发，或者想要为项目添加新的 provider，请参阅我们的开发者文档：

[开发者指南](docs/Develop.md)

这份文档提供了详细的指导，包括如何设置开发环境、项目结构说明、如何添加新的 provider 适配器，以及贡献指南。

如果你有任何其他问题、建议或需要进一步的澄清，请随时联系 APIBridge 的维护团队。我们欢迎社区贡献，共同改进这个项目！