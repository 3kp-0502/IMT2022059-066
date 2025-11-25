from typing import List
from src.models.transaction import Transaction
from src.models.user import User
from src.models.account import Account
from src.utils.persistence import PersistenceLayer

class ReportService:
    def __init__(self, persistence: PersistenceLayer):
        self.persistence = persistence

    def generate_account_statement(self, account_id: str) -> str:
        account_data = self.persistence.get_account(account_id)
        if not account_data:
            return "Account not found."
        
        transactions = self.persistence.get_transactions_for_account(account_id)
        # Sort by timestamp
        transactions.sort(key=lambda x: x["timestamp"], reverse=True)

        report = []
        report.append(f"Statement for Account: {account_id}")
        report.append(f"Type: {account_data['account_type']}")
        report.append(f"Current Balance: ${account_data['balance']:.2f}")
        report.append("-" * 50)
        report.append(f"{'Date':<20} | {'Type':<12} | {'Amount':<10} | {'Description'}")
        report.append("-" * 50)

        for tx in transactions:
            report.append(f"{tx['timestamp'][:19]:<20} | {tx['transaction_type']:<12} | ${tx['amount']:<9.2f} | {tx['description']}")
        
        report.append("-" * 50)
        return "\n".join(report)

    def generate_admin_report(self) -> str:
        users = self.persistence.get_all_users()
        total_users = len(users)
        total_accounts = 0
        total_balance = 0.0

        # Calculate totals manually to add complexity for testing
        for user in users:
            accounts = self.persistence.get_accounts_for_user(user["user_id"])
            total_accounts += len(accounts)
            for acc in accounts:
                total_balance += acc["balance"]

        report = []
        report.append("=== ADMIN REPORT ===")
        report.append(f"Total Users: {total_users}")
        report.append(f"Total Accounts: {total_accounts}")
        report.append(f"Total Assets Held: ${total_balance:.2f}")
        report.append("====================")
        
        return "\n".join(report)
