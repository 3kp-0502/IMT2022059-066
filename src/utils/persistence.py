import json
import os
from typing import Dict, List, Any

class PersistenceLayer:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.accounts_file = os.path.join(data_dir, "accounts.json")
        self.transactions_file = os.path.join(data_dir, "transactions.json")
        self.loans_file = os.path.join(data_dir, "loans.json")
        self.fraud_file = os.path.join(data_dir, "fraud.json")
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.users_file):
            self._save_json(self.users_file, {})
        if not os.path.exists(self.accounts_file):
            self._save_json(self.accounts_file, {})
        if not os.path.exists(self.transactions_file):
            self._save_json(self.transactions_file, [])
        if not os.path.exists(self.loans_file):
            self._save_json(self.loans_file, {})
        if not os.path.exists(self.fraud_file):
            self._save_json(self.fraud_file, [])

    def _save_json(self, filepath: str, data: Any):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def _load_json(self, filepath: str) -> Any:
        with open(filepath, 'r') as f:
            return json.load(f)

    # User Operations
    def save_user(self, user_dict: Dict):
        users = self._load_json(self.users_file)
        users[user_dict["user_id"]] = user_dict
        self._save_json(self.users_file, users)

    def get_user(self, user_id: str) -> Dict:
        users = self._load_json(self.users_file)
        return users.get(user_id)

    def get_user_by_username(self, username: str) -> Dict:
        users = self._load_json(self.users_file)
        for user in users.values():
            if user["username"] == username:
                return user
        return None
    
    def get_all_users(self) -> List[Dict]:
        users = self._load_json(self.users_file)
        return list(users.values())

    # Account Operations
    def save_account(self, account_dict: Dict):
        accounts = self._load_json(self.accounts_file)
        accounts[account_dict["account_id"]] = account_dict
        self._save_json(self.accounts_file, accounts)

    def get_account(self, account_id: str) -> Dict:
        accounts = self._load_json(self.accounts_file)
        return accounts.get(account_id)
    
    def get_accounts_for_user(self, user_id: str) -> List[Dict]:
        accounts = self._load_json(self.accounts_file)
        return [acc for acc in accounts.values() if acc["user_id"] == user_id]

    # Transaction Operations
    def log_transaction(self, transaction_dict: Dict):
        transactions = self._load_json(self.transactions_file)
        transactions.append(transaction_dict)
        self._save_json(self.transactions_file, transactions)

    def get_transactions_for_account(self, account_id: str) -> List[Dict]:
        transactions = self._load_json(self.transactions_file)
        return [t for t in transactions if t["account_id"] == account_id]
    
    def get_all_transactions(self) -> List[Dict]:
        return self._load_json(self.transactions_file)

    # Loan Operations
    def save_loan(self, loan_dict: Dict):
        loans = self._load_json(self.loans_file)
        loans[loan_dict["loan_id"]] = loan_dict
        self._save_json(self.loans_file, loans)

    def get_loan(self, loan_id: str) -> Dict:
        loans = self._load_json(self.loans_file)
        return loans.get(loan_id)

    def get_loans_for_user(self, user_id: str) -> List[Dict]:
        loans = self._load_json(self.loans_file)
        return [l for l in loans.values() if l["user_id"] == user_id]

    def get_all_loans(self) -> List[Dict]:
        loans = self._load_json(self.loans_file)
        return list(loans.values())

    # Fraud Operations
    def save_fraud_flag(self, flag_dict: Dict):
        flags = self._load_json(self.fraud_file)
        flags.append(flag_dict)
        self._save_json(self.fraud_file, flags)

    def get_fraud_flags(self) -> List[Dict]:
        return self._load_json(self.fraud_file)
