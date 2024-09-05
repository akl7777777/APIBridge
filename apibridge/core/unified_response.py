class UnifiedResponse:
    def __init__(self):
        self.status_code = None
        self.headers = {}
        self.content = None
        self.is_stream = False
        self.error = None
        self.custom_data = {}  # 用于存储额外的响应数据

    def set_status_code(self, status_code):
        self.status_code = status_code
        return self

    def set_headers(self, param):
        self.headers = param
        return self

    def set_content(self, text):
        self.content = text
        return self

    def set_is_stream(self, stream):
        self.is_stream = stream
        return self


    def add_custom_data(self, key, value):
        self.custom_data[key] = value
        return self
