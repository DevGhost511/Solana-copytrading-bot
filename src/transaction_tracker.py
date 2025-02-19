from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed
import json
from datetime import datetime
from .data_logger import DataLogger
from .utils import convert_lamports_to_sol

class TransactionTracker:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.client = Client(self.config['rpc_url'])
        self.data_logger = DataLogger(self.config['output_path'])
        
    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def track_transactions(self):
        for wallet_address in self.config['wallet_addresses']:
            try:
                txs = self.client.get_signatures_for_address(
                    wallet_address,
                    limit=10,
                    commitment=Confirmed
                )
                
                if txs.value:
                    for tx in txs.value:
                        tx_data = self.client.get_transaction(
                            tx.signature,
                            commitment=Confirmed
                        )
                        
                        if tx_data.value:
                            transaction_info = {
                                'timestamp': datetime.now().isoformat(),
                                'signature': tx.signature,
                                'wallet_address': wallet_address,
                                'slot': tx_data.value.slot,
                                'amount': convert_lamports_to_sol(tx_data.value.meta.pre_balances[0] - 
                                                                tx_data.value.meta.post_balances[0]),
                                'success': tx_data.value.meta.status.Ok is not None
                            }
                            
                            self.data_logger.log_transaction(transaction_info)
                            
            except Exception as e:
                print(f"Error tracking transactions for {wallet_address}: {str(e)}")
