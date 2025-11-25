from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class LoanStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PAID = "PAID"

@dataclass
class Loan:
    loan_id: str
    user_id: str
    amount: float
    interest_rate: float
    term_months: int
    status: LoanStatus = LoanStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    remaining_amount: float = field(init=False)

    def __post_init__(self):
        self.remaining_amount = self.amount + (self.amount * self.interest_rate)

    def to_dict(self):
        return {
            "loan_id": self.loan_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "interest_rate": self.interest_rate,
            "term_months": self.term_months,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "remaining_amount": self.remaining_amount
        }

    @classmethod
    def from_dict(cls, data):
        loan = cls(
            loan_id=data["loan_id"],
            user_id=data["user_id"],
            amount=data["amount"],
            interest_rate=data["interest_rate"],
            term_months=data["term_months"],
            status=LoanStatus(data["status"])
        )
        loan.created_at = datetime.fromisoformat(data["created_at"])
        loan.remaining_amount = data["remaining_amount"]
        return loan
