# APIBridge
APIBridge A bridge that converts any interface into a chat format API.


# 创建APIBridge实例
api_bridge = APIBridge()

# 注册适配器
api_bridge.register_adapter('openai', OpenAIAdapter())

# 创建统一请求
request = UnifiedRequest()
request.set_api_type('openai')
request.set_endpoint('https://api.openai.com/v1/chat/completions')
request.set_headers({
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
})
request.set_data({
    'model': 'gpt-3.5-turbo',
    'messages': [{'role': 'user', 'content': 'Hello, how are you?'}]
})

# 处理请求
response = api_bridge.process_request(request)

# 转换为chat格式
chat_response = api_bridge.to_chat_format(response)

print(chat_response)
