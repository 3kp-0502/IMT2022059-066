import uuid
from typing import List
from src.models.loan import Loan, LoanStatus
from src.models.user import User
from src.utils.persistence import PersistenceLayer
from src.utils.validators import ValidationError

class LoanService:
    def __init__(self, persistence: PersistenceLayer):
        self.persistence = persistence
        self.loans_file = "loans.json" # We might need to update persistence layer to handle generic files or add this specific one
        # For now, let's hack it into persistence layer or just use a new file here?
        # Better to update PersistenceLayer.
        
    def apply_for_loan(self, user: User, amount: float, term_months: int) -> Loan:
        if amount <= 0:
            raise ValidationError("Loan amount must be positive.")
        if term_months <= 0:
            raise ValidationError("Loan term must be positive.")
        
        # Simple credit check simulation
        if self._calculate_credit_score(user) < 600:
            raise ValidationError("Credit score too low for loan.")

        loan_id = str(uuid.uuid4())
        interest_rate = 0.10 # Flat 10% for simplicity
        
        loan = Loan(
            loan_id=loan_id,
            user_id=user.user_id,
            amount=amount,
            interest_rate=interest_rate,
            term_months=term_months
        )
        
        self.persistence.save_loan(loan.to_dict())
        return loan

    def approve_loan(self, loan_id: str):
        loan = self._get_loan(loan_id)
        if loan.status != LoanStatus.PENDING:
            raise ValidationError("Loan is not pending approval.")
        
        loan.status = LoanStatus.APPROVED
        self.persistence.save_loan(loan.to_dict())
        
        # Disburse funds (would need integration with BankService, but for now just mark approved)
        # In a real app, we'd deposit to their account.

    def reject_loan(self, loan_id: str):
        loan = self._get_loan(loan_id)
        if loan.status != LoanStatus.PENDING:
            raise ValidationError("Loan is not pending approval.")
        
        loan.status = LoanStatus.REJECTED
        self.persistence.save_loan(loan.to_dict())

    def repay_loan(self, loan_id: str, amount: float):
        loan = self._get_loan(loan_id)
        if loan.status != LoanStatus.APPROVED:
            raise ValidationError("Loan is not active.")
        
        if amount <= 0:
            raise ValidationError("Repayment amount must be positive.")
        
        loan.remaining_amount -= amount
        if loan.remaining_amount <= 0:
            loan.remaining_amount = 0
            loan.status = LoanStatus.PAID
            
        self.persistence.save_loan(loan.to_dict())

    def get_user_loans(self, user_id: str) -> List[Loan]:
        loans_data = self.persistence.get_loans_for_user(user_id)
        return [Loan.from_dict(data) for data in loans_data]

    def get_pending_loans(self) -> List[Loan]:
        all_loans = self.persistence.get_all_loans()
        return [Loan.from_dict(data) for data in all_loans if data["status"] == "PENDING"]

    def _get_loan(self, loan_id: str) -> Loan:
        data = self.persistence.get_loan(loan_id)
        if not data:
            raise ValidationError("Loan not found.")
        return Loan.from_dict(data)

    def _calculate_credit_score(self, user: User) -> int:
        # Mock credit score calculation
        # Base score
        score = 650
        
        # Length of history (mocked by account count)
        score += len(user.accounts) * 10
        
        # Random factor or based on email domain for "complexity"
        if user.email.endswith(".edu"):
            score += 50
            
        return min(score, 850)
