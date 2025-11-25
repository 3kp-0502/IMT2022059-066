import uuid
from datetime import datetime
from typing import List, Optional
from src.models.account import Account, SavingsAccount, CurrentAccount, FixedDepositAccount
from src.models.transaction import Transaction, TransactionType
from src.models.user import User
from src.services.fraud_service import FraudDetectionService
from src.services.audit_service import AuditService
from src.utils.persistence import PersistenceLayer
from src.utils.validators import ValidationError

class BankService:
    def __init__(self, persistence: PersistenceLayer):
        self.persistence = persistence
        self.fraud_service = FraudDetectionService(persistence)
        self.audit_service = AuditService()

    def create_account(self, user: User, account_type: str, initial_deposit: float = 0.0, **kwargs) -> Account:
        account_id = str(uuid.uuid4())
        
        # Create account instance based on type
        if account_type == "SAVINGS":
            account = SavingsAccount(account_id=account_id, user_id=user.user_id, balance=0.0)
        elif account_type == "CURRENT":
            account = CurrentAccount(account_id=account_id, user_id=user.user_id, balance=0.0)
        elif account_type == "FIXED_DEPOSIT":
            term_months = kwargs.get("term_months", 12)
            account = FixedDepositAccount(account_id=account_id, user_id=user.user_id, balance=0.0, term_months=term_months)
        else:
            raise ValidationError("Invalid account type.")

        # Initial Deposit
        if initial_deposit > 0:
            account.deposit(initial_deposit)
            self._log_transaction(account_id, initial_deposit, TransactionType.DEPOSIT, "Initial Deposit")

        # Save Account
        self.persistence.save_account(account.to_dict())
        
        # Update User
        user.add_account(account_id)
        self.persistence.save_user(user.to_dict())
        
        self.audit_service.log_action(user.user_id, "CREATE_ACCOUNT", f"Type: {account_type}, ID: {account_id}")
        return account

    def deposit(self, account_id: str, amount: float):
        account = self._get_account(account_id)
        account.deposit(amount)
        self.persistence.save_account(account.to_dict())
        tx = self._log_transaction(account_id, amount, TransactionType.DEPOSIT, "Deposit")
        
        # Check for fraud
        if self.fraud_service.analyze_transaction(tx):
            print(f"WARNING: Transaction {tx.transaction_id} flagged for review.")
            self.audit_service.log_action(account.user_id, "FRAUD_ALERT", f"Tx: {tx.transaction_id}")
        
        self.audit_service.log_action(account.user_id, "DEPOSIT", f"Amount: {amount}, Acc: {account_id}")

    def withdraw(self, account_id: str, amount: float):
        account = self._get_account(account_id)
        account.withdraw(amount)
        self.persistence.save_account(account.to_dict())
        tx = self._log_transaction(account_id, amount, TransactionType.WITHDRAWAL, "Withdrawal")

        # Check for fraud
        if self.fraud_service.analyze_transaction(tx):
            print(f"WARNING: Transaction {tx.transaction_id} flagged for review.")
            self.audit_service.log_action(account.user_id, "FRAUD_ALERT", f"Tx: {tx.transaction_id}")

        self.audit_service.log_action(account.user_id, "WITHDRAWAL", f"Amount: {amount}, Acc: {account_id}")

    def transfer(self, from_account_id: str, to_account_id: str, amount: float):
        if from_account_id == to_account_id:
            raise ValidationError("Cannot transfer to the same account.")
        
        from_acc = self._get_account(from_account_id)
        to_acc = self._get_account(to_account_id)

        # Check withdrawal first
        if not from_acc.can_withdraw(amount):
            raise ValidationError("Insufficient funds for transfer.")

        # Perform Transfer (Atomic-ish)
        from_acc.withdraw(amount)
        to_acc.deposit(amount)

        self.persistence.save_account(from_acc.to_dict())
        self.persistence.save_account(to_acc.to_dict())

        self._log_transaction(from_account_id, amount, TransactionType.TRANSFER, f"Transfer to {to_account_id}", related_account_id=to_account_id)
        tx = self._log_transaction(to_account_id, amount, TransactionType.TRANSFER, f"Transfer from {from_account_id}", related_account_id=from_account_id)

        # Check for fraud (on the receiver side mainly for money laundering logic, but check both in real life)
        if self.fraud_service.analyze_transaction(tx):
            print(f"WARNING: Transaction {tx.transaction_id} flagged for review.")

    def get_user_accounts(self, user_id: str) -> List[Account]:
        accounts_data = self.persistence.get_accounts_for_user(user_id)
        return [Account.from_dict(data) for data in accounts_data]

    def get_account_transactions(self, account_id: str) -> List[Transaction]:
        tx_data = self.persistence.get_transactions_for_account(account_id)
        return [Transaction.from_dict(data) for data in tx_data]

    def calculate_interest(self):
        """Admin function to apply interest to all Savings Accounts."""
        all_users = self.persistence.get_all_users()
        count = 0
        for user_data in all_users:
            accounts_data = self.persistence.get_accounts_for_user(user_data["user_id"])
            for acc_data in accounts_data:
                if acc_data["account_type"] == "SAVINGS":
                    acc = Account.from_dict(acc_data)
                    interest = acc.balance * acc.interest_rate
                    if interest > 0:
                        acc.deposit(interest)
                        self.persistence.save_account(acc.to_dict())
                        self._log_transaction(acc.account_id, interest, TransactionType.INTEREST, "Annual Interest Applied")
                        count += 1
        return count

    def _get_account(self, account_id: str) -> Account:
        data = self.persistence.get_account(account_id)
        if not data:
            raise ValidationError("Account not found.")
        return Account.from_dict(data)

    def _log_transaction(self, account_id: str, amount: float, type: TransactionType, desc: str, related_account_id: str = None) -> Transaction:
        tx = Transaction(
            transaction_id=str(uuid.uuid4()),
            account_id=account_id,
            amount=amount,
            transaction_type=type,
            description=desc,
            related_account_id=related_account_id
        )
        self.persistence.log_transaction(tx.to_dict())
        return tx
