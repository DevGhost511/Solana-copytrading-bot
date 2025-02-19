import json
from typing import Dict
import os

class DataLogger:
    def __init__(self, output_path: str):
        self.output_path = output_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        if not os.path.exists(self.output_path):
            with open(self.output_path, 'w') as f:
                json.dump([], f)
    
    def log_transaction(self, transaction: Dict):
        try:
            with open(self.output_path, 'r') as f:
                transactions = json.load(f)
            
            transactions.append(transaction)
            
            with open(self.output_path, 'w') as f:
                json.dump(transactions, f, indent=4)
                
        except Exception as e:
            print(f"Error logging transaction: {str(e)}")
