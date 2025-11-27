import pytest
import os
import shutil
from src.models.account import SavingsAccount, CurrentAccount, FixedDepositAccount
from src.services.bank_service import BankService
from src.services.auth_service import AuthService
from src.utils.persistence import PersistenceLayer

class TestMutationKillsPhase2:
    
    @pytest.fixture
    def persistence(self):
        test_dir = "test_data_phase2"
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        return PersistenceLayer(data_dir=test_dir)

    @pytest.fixture
    def auth_service(self, persistence):
        return AuthService(persistence)

    @pytest.fixture
    def bank_service(self, persistence):
        return BankService(persistence)

    def test_kill_mutant_205_deposit_adds_to_balance(self, auth_service, bank_service):
        """
        Target: Mutant 205 in src/models/account.py
        Mutation: self.balance += amount  ->  self.balance = amount
        Strategy: Deposit into an account that ALREADY has a balance.
        """
        # Setup
        user = auth_service.register("user_m205", "Pass123", "u@test.com", "1234567890")
        # Create account with initial balance 100
        account = bank_service.create_account(user, "SAVINGS", 100.0)
        
        # Action: Deposit 50 more
        bank_service.deposit(account.account_id, 50.0)
        
        # Verification
        updated_account = bank_service._get_account(account.account_id)
        # If mutant exists (balance = 50), this fails.
        # Correct behavior: 100 + 50 = 150
        assert updated_account.balance == 150.0

    def test_kill_mutant_bank_service_term_months_default(self, auth_service, bank_service):
        """
        Target: Mutants around FixedDepositAccount creation in BankService.
        Likely changing default 'term_months' from 12 to something else.
        """
        user = auth_service.register("user_fd_def", "Pass123", "u2@test.com", "1234567890")
        
        # Action: Create FD without specifying term
        account = bank_service.create_account(user, "FIXED_DEPOSIT", 1000.0)
        
        # Verification
        assert isinstance(account, FixedDepositAccount)
        assert account.term_months == 12

    def test_kill_mutant_bank_service_term_months_custom(self, auth_service, bank_service):
        """
        Target: Mutants around FixedDepositAccount creation in BankService.
        Likely ignoring kwargs or hardcoding values.
        """
        user = auth_service.register("user_fd_cust", "Pass123", "u3@test.com", "1234567890")
        
        # Action: Create FD WITH specific term
        account = bank_service.create_account(user, "FIXED_DEPOSIT", 1000.0, term_months=24)
        
        # Verification
        assert account.term_months == 24
