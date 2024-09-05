from flask import Flask

from apibridge.adapters.snova_adapter import SnovaAdapter
from apibridge.api import routes
from config import Config
from apibridge.core.api_bridge import APIBridge
from apibridge.adapters.openai_adapter import OpenAIAdapter
from apibridge.core.bridge_manager import init_api_bridge, get_api_bridge


# from apibridge.adapters.anthropic_adapter import AnthropicAdapter  # 假设你有这个适配器

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 注册蓝图
    app.register_blueprint(routes.bp)

    # 注册适配器
    # 初始化并获取 APIBridge
    init_api_bridge()
    app.config['API_BRIDGE'] = get_api_bridge()
    # api_bridge.register_adapter('anthropic', AnthropicAdapter())
    # 可以注册更多适配器
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['FLASK_ENV'] = 'development'  # 这会禁用输出缓冲

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5566, debug=True)
