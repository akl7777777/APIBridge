from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    @abstractmethod
    def process(self, unified_request):
        pass

    @abstractmethod
    def to_chat_format(self, unified_response):
        pass
