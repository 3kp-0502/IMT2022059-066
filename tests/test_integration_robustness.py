import pytest
from unittest.mock import Mock, patch
from src.services.bank_service import BankService
from src.models.user import User
from src.models.account import SavingsAccount

class TestIntegrationRobustness:
    """
    Tests specifically designed to 'strongly kill' Integration Level Mutants.
    We verify that the Service layer interacts with the Persistence layer correctly.
    Mutations that change arguments (IPR), delete calls (IMCD), or ignore return values (IVR)
    should cause these tests to fail.
    """

    @pytest.fixture
    def mock_persistence(self):
        return Mock()

    @pytest.fixture
    def bank_service(self, mock_persistence):
        return BankService(mock_persistence)

    def test_create_account_calls_persistence_correctly(self, bank_service, mock_persistence):
        """
        Verifies Integration Parameter Replacement (IPR) and Method Call Deletion (IMCD).
        If mutmut changes the arguments passed to save_account, this test must fail.
        """
        user = User("u1", "user1", "pass", "valid@email.com", "1234567890")
        
        # Action
        account = bank_service.create_account(user, "SAVINGS", 100.0)

        # Verification (Strong Kill for IPR/IMCD)
        # 1. Verify save_account was called
        assert mock_persistence.save_account.called
        
        # 2. Verify exact arguments (IPR check)
        # We expect a dict with specific keys. 
        # If mutmut changes `account.to_dict()` to `None` or modifies values, this fails.
        call_args = mock_persistence.save_account.call_args[0][0]
        assert call_args["account_id"] == account.account_id
        assert call_args["balance"] == 100.0
        assert call_args["account_type"] == "SAVINGS"

        # 3. Verify user update was saved (IMCD check)
        assert mock_persistence.save_user.called
        user_save_args = mock_persistence.save_user.call_args[0][0]
        assert account.account_id in user_save_args["accounts"]

    def test_deposit_verifies_persistence_interaction(self, bank_service, mock_persistence):
        """
        Verifies that deposit updates are persisted.
        """
        # Setup mock return
        account_data = {
            "account_id": "acc1",
            "user_id": "u1",
            "account_type": "SAVINGS",
            "balance": 500.0,
            "is_active": True,
            "created_at": "2023-01-01"
        }
        mock_persistence.get_account.return_value = account_data

        # Action
        bank_service.deposit("acc1", 200.0)

        # Verification
        # Check that save_account was called with UPDATED balance
        assert mock_persistence.save_account.called
        saved_data = mock_persistence.save_account.call_args[0][0]
        assert saved_data["balance"] == 700.0  # 500 + 200

    def test_get_account_handles_missing_data(self, bank_service, mock_persistence):
        """
        Verifies Integration Return Value Replacement (IVR).
        If persistence returns None (simulating not found), service should raise error.
        """
        mock_persistence.get_account.return_value = None

        with pytest.raises(Exception) as exc: # validator raises ValidationError
            bank_service._get_account("invalid_id")
        
        assert "Account not found" in str(exc.value)
