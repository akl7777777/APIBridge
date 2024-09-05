from apibridge.core.api_bridge import APIBridge
from apibridge.adapters.openai_adapter import OpenAIAdapter
from apibridge.adapters.snova_adapter import SnovaAdapter

api_bridge = APIBridge()

def init_api_bridge():
    api_bridge.register_adapter('openai', OpenAIAdapter())
    api_bridge.register_adapter('snova', SnovaAdapter())
    # 注册其他适配器...

def get_api_bridge():
    return api_bridge
