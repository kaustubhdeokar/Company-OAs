from abc import ABC, abstractmethod
from typing import List, Dict

class StorageStrategy(ABC):
    @abstractmethod
    def save(self, data: List[Dict[str, str]]):
        pass