from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"
    INTEREST = "INTEREST"
    FEE = "FEE"

@dataclass
class Transaction:
    transaction_id: str
    account_id: str
    amount: float
    transaction_type: TransactionType
    timestamp: datetime = field(default_factory=datetime.now)
    description: str = ""
    related_account_id: Optional[str] = None # For transfers

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "account_id": self.account_id,
            "amount": self.amount,
            "transaction_type": self.transaction_type.value,
            "timestamp": self.timestamp.isoformat(),
            "description": self.description,
            "related_account_id": self.related_account_id
        }

    @classmethod
    def from_dict(cls, data):
        tx = cls(
            transaction_id=data["transaction_id"],
            account_id=data["account_id"],
            amount=data["amount"],
            transaction_type=TransactionType(data["transaction_type"]),
            description=data.get("description", ""),
            related_account_id=data.get("related_account_id")
        )
        tx.timestamp = datetime.fromisoformat(data["timestamp"])
        return tx
