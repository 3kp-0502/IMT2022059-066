import pytest
from src.models.account import SavingsAccount, CurrentAccount
from src.services.bank_service import BankService
from src.services.auth_service import AuthService
from src.utils.persistence import PersistenceLayer
import shutil
import os

@pytest.fixture
def persistence():
    test_dir = "test_data_mutation"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    return PersistenceLayer(data_dir=test_dir)

@pytest.fixture
def auth_service(persistence):
    return AuthService(persistence)

@pytest.fixture
def bank_service(persistence):
    return BankService(persistence)

def test_kill_mutant_200_account_is_active_default(auth_service, bank_service):
    """
    Mutant 200: Changes default is_active from True to None.
    We assert that it is True.
    """
    user = auth_service.register("mutant_killer", "Pass1234", "m@test.com", "1234567890")
    account = bank_service.create_account(user, "SAVINGS", 100.0)
    
    assert account.is_active is True

def test_kill_mutant_700_initial_balance_default(auth_service, bank_service):
    """
    Mutant 700: Changes default balance from 0.0 to 1.0.
    We assert that a new account (without initial deposit) has 0.0 balance.
    """
    user = auth_service.register("mutant_killer_700", "Pass1234", "m700@test.com", "1234567890")
    # Create account with 0 initial deposit explicitly or implicitly
    account = bank_service.create_account(user, "SAVINGS", 0.0)
    
    assert account.balance == 0.0
