class UnifiedRequest:
    def __init__(self):
        self.api_type = None  # 例如: 'openai', 'snova', 'custom'
        self.endpoint = None  # API endpoint
        self.method = 'POST'  # HTTP 方法，默认为 POST
        self.headers = {}  # 请求头
        self.params = {}  # URL 参数
        self.data = {}  # 请求体数据
        self.stream = False  # 是否为流式请求
        self.timeout = 30  # 超时时间
        self.custom_options = {}  # 自定义选项，用于扩展

    def set_api_type(self, api_type):
        self.api_type = api_type
        return self

    def set_endpoint(self, param):
        self.endpoint = param
        return self

    def set_method(self, param):
        self.method = param
        return self

    def set_headers(self, param):
        self.headers = param
        return self

    def set_data(self, param):
        self.data = param
        return self

    def set_stream(self, param):
        self.stream = param
        return self

    def set_params(self, param):
        self.params = param
        return self

    def add_custom_option(self, key, value):
        self.custom_options[key] = value
        return self
