class APIBridge:
    def __init__(self):
        self.adapters = {}

    def register_adapter(self, api_type, adapter):
        self.adapters[api_type] = adapter

    def process_request(self, unified_request):
        if unified_request.api_type not in self.adapters:
            raise ValueError(f"Unsupported API type: {unified_request.api_type}")

        adapter = self.adapters[unified_request.api_type]
        return adapter.process(unified_request)

    def to_chat_format(self, unified_response, api_type):
        if api_type not in self.adapters:
            raise ValueError(f"Unsupported API type: {api_type}")

        adapter = self.adapters[api_type]
        return adapter.to_chat_format(unified_response)
