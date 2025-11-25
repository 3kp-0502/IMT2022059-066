import pytest
import os
import shutil
from src.services.auth_service import AuthService
from src.services.bank_service import BankService
from src.services.loan_service import LoanService
from src.services.fraud_service import FraudDetectionService
from src.utils.persistence import PersistenceLayer
from src.models.transaction import TransactionType

@pytest.fixture
def persistence():
    # Use a test data directory
    test_dir = "test_data"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    return PersistenceLayer(data_dir=test_dir)

@pytest.fixture
def auth_service(persistence):
    return AuthService(persistence)

@pytest.fixture
def bank_service(persistence):
    return BankService(persistence)

@pytest.fixture
def loan_service(persistence):
    return LoanService(persistence)

def test_registration_and_login(auth_service):
    user = auth_service.register("testuser", "Password123", "test@test.com", "1234567890")
    assert user.username == "testuser"
    
    logged_in_user = auth_service.login("testuser", "Password123")
    assert logged_in_user.user_id == user.user_id

def test_account_creation_and_deposit(auth_service, bank_service):
    user = auth_service.register("user2", "Password123", "u2@test.com", "1234567890")
    account = bank_service.create_account(user, "SAVINGS", 1000.0)
    
    assert account.balance == 1000.0
    assert account.account_type == "SAVINGS"
    
    bank_service.deposit(account.account_id, 500.0)
    updated_account = bank_service._get_account(account.account_id)
    assert updated_account.balance == 1500.0

def test_transfer(auth_service, bank_service):
    user = auth_service.register("user3", "Password123", "u3@test.com", "1234567890")
    acc1 = bank_service.create_account(user, "SAVINGS", 1000.0)
    acc2 = bank_service.create_account(user, "CURRENT", 0.0)
    
    bank_service.transfer(acc1.account_id, acc2.account_id, 300.0)
    
    acc1_updated = bank_service._get_account(acc1.account_id)
    acc2_updated = bank_service._get_account(acc2.account_id)
    
    assert acc1_updated.balance == 700.0
    assert acc2_updated.balance == 300.0

def test_loan_application(auth_service, loan_service):
    user = auth_service.register("user4", "Password123", "u4@test.com", "1234567890")
    loan = loan_service.apply_for_loan(user, 5000.0, 12)
    
    assert loan.amount == 5000.0
    assert loan.status.value == "PENDING"

def test_fraud_detection(auth_service, bank_service, persistence):
    user = auth_service.register("user5", "Password123", "u5@test.com", "1234567890")
    acc = bank_service.create_account(user, "SAVINGS", 20000.0)
    
    # This should trigger fraud detection (Amount > 10000)
    bank_service.withdraw(acc.account_id, 15000.0)
    
    fraud_service = FraudDetectionService(persistence)
    flags = fraud_service.get_flagged_transactions()
    assert len(flags) > 0
    assert "Large transaction amount" in flags[0]["reasons"]
