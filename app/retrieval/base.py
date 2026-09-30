from abc import ABC, abstractmethod

class BaseRetriever(ABC):
    @abstractmethod
    def search(self, query, top_k=5, **kwargs):
        raise NotImplementedError
