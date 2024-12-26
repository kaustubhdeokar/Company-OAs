import os
import json
from typing import List, Dict
from .base import StorageStrategy
from datetime import datetime

class LocalStorageStrategy(StorageStrategy):
    def save(self, data: List[Dict[str, str]]):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"products_{timestamp}.json"
        file_path = os.path.join(os.getcwd(), file_name)
        with open(file_path, 'w') as file:
            json.dump(data, file)
        print(f"Data saved to {file_path}")