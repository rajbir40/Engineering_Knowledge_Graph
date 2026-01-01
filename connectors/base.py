from abc import ABC, abstractmethod

class BaseConnector(ABC):
    """
    All connectors must implement this interface
    """

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def parse(self, graph):
        pass
