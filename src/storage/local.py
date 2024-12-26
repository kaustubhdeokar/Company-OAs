import os
import json
from typing import List, Dict
from .base import StorageStrategy

class LocalStorageStrategy(StorageStrategy):
    def save(self, data: List[Dict[str, str]]):
        
        file_path = os.path.join(os.getcwd(), "products.json")
        with open(file_path, 'w') as file:
            json.dump(data, file)
        print(f"Data saved to {file_path}")