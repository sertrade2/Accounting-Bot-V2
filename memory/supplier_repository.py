# memory/supplier_repository.py

import json
import os
from typing import Dict, Optional


class SupplierRepository:

    def __init__(self, db_path: str = "storage/suppliers.json"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        if not os.path.exists(db_path):
            with open(db_path, "w") as f:
                json.dump({}, f)

    def _load(self) -> Dict:
        with open(self.db_path, "r") as f:
            return json.load(f)

    def _save(self, data: Dict):
        with open(self.db_path, "w") as f:
            json.dump(data, f, indent=2)

    def get_supplier(self, key: str) -> Optional[Dict]:
        return self._load().get(key)

    def save_supplier(self, key: str, supplier_data: Dict):
        data = self._load()
        data[key] = supplier_data
        self._save(data)

    def get_all(self) -> Dict:
        return self._load()
