from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List
from src.models.transaction import Transaction, TransactionType
from src.utils.validators import validate_amount, ValidationError

@dataclass
class Account(ABC):
    account_id: str
    user_id: str
    balance: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    account_type: str = "GENERIC"

    @abstractmethod
    def can_withdraw(self, amount: float) -> bool:
        pass

    def deposit(self, amount: float):
        validate_amount(amount)
        self.balance += amount

    def withdraw(self, amount: float):
        validate_amount(amount)
        if not self.can_withdraw(amount):
            raise ValidationError("Insufficient funds or withdrawal limit exceeded.")
        self.balance -= amount

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "user_id": self.user_id,
            "balance": self.balance,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
            "account_type": self.account_type
        }

    @staticmethod
    def from_dict(data):
        # Factory method to create specific account types
        if data["account_type"] == "SAVINGS":
            return SavingsAccount.from_dict_specific(data)
        elif data["account_type"] == "CURRENT":
            return CurrentAccount.from_dict_specific(data)
        elif data["account_type"] == "FIXED_DEPOSIT":
            return FixedDepositAccount.from_dict_specific(data)
        else:
            raise ValueError(f"Unknown account type: {data['account_type']}")

@dataclass
class SavingsAccount(Account):
    interest_rate: float = 0.03
    min_balance: float = 500.0
    account_type: str = "SAVINGS"

    def can_withdraw(self, amount: float) -> bool:
        return (self.balance - amount) >= self.min_balance

    @classmethod
    def from_dict_specific(cls, data):
        acc = cls(
            account_id=data["account_id"],
            user_id=data["user_id"],
            balance=data["balance"],
            is_active=data["is_active"]
        )
        acc.created_at = datetime.fromisoformat(data["created_at"])
        return acc

@dataclass
class CurrentAccount(Account):
    overdraft_limit: float = 1000.0
    account_type: str = "CURRENT"

    def can_withdraw(self, amount: float) -> bool:
        return (self.balance + self.overdraft_limit) >= amount

    @classmethod
    def from_dict_specific(cls, data):
        acc = cls(
            account_id=data["account_id"],
            user_id=data["user_id"],
            balance=data["balance"],
            is_active=data["is_active"]
        )
        acc.created_at = datetime.fromisoformat(data["created_at"])
        return acc

@dataclass
class FixedDepositAccount(Account):
    term_months: int = 12
    interest_rate: float = 0.06
    account_type: str = "FIXED_DEPOSIT"
    maturity_date: datetime = field(init=False)

    def __post_init__(self):
        if not hasattr(self, 'maturity_date') or self.maturity_date is None:
            # Simplified maturity calculation: 30 days per month
            self.maturity_date = self.created_at + timedelta(days=30 * self.term_months)

    def can_withdraw(self, amount: float) -> bool:
        # Cannot withdraw before maturity (simplified logic)
        # In real world, maybe with penalty. Here, strict.
        if datetime.now() < self.maturity_date:
            return False
        return self.balance >= amount

    def to_dict(self):
        data = super().to_dict()
        data["term_months"] = self.term_months
        data["maturity_date"] = self.maturity_date.isoformat()
        return data

    @classmethod
    def from_dict_specific(cls, data):
        acc = cls(
            account_id=data["account_id"],
            user_id=data["user_id"],
            balance=data["balance"],
            is_active=data["is_active"],
            term_months=data.get("term_months", 12)
        )
        acc.created_at = datetime.fromisoformat(data["created_at"])
        acc.maturity_date = datetime.fromisoformat(data["maturity_date"])
        return acc
