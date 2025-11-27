import pytest
import os
import shutil
import json
from src.services.report_service import ReportService
from src.utils.persistence import PersistenceLayer

class TestReportPersistence:
    
    @pytest.fixture
    def persistence(self):
        test_dir = "test_data_rep_pers"
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        return PersistenceLayer(data_dir=test_dir)

    @pytest.fixture
    def report_service(self, persistence):
        return ReportService(persistence)

    # --- Persistence Layer Tests ---
    def test_persistence_initialization(self):
        test_dir = "test_data_init"
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            
        p = PersistenceLayer(data_dir=test_dir)
        
        # Verify all files created
        assert os.path.exists(os.path.join(test_dir, "users.json"))
        assert os.path.exists(os.path.join(test_dir, "accounts.json"))
        assert os.path.exists(os.path.join(test_dir, "transactions.json"))
        assert os.path.exists(os.path.join(test_dir, "loans.json"))
        assert os.path.exists(os.path.join(test_dir, "fraud.json"))
        
        # Verify content is empty JSON structure
        with open(os.path.join(test_dir, "users.json")) as f:
            assert json.load(f) == {}
        with open(os.path.join(test_dir, "transactions.json")) as f:
            assert json.load(f) == []

    def test_persistence_save_load_user(self, persistence):
        user_data = {"user_id": "u1", "username": "test", "accounts": []}
        persistence.save_user(user_data)
        
        loaded = persistence.get_user("u1")
        assert loaded == user_data
        
        # Verify file content directly
        with open(persistence.users_file) as f:
            data = json.load(f)
            assert data["u1"] == user_data

    def test_persistence_get_by_username(self, persistence):
        user_data = {"user_id": "u1", "username": "unique_name", "accounts": []}
        persistence.save_user(user_data)
        
        found = persistence.get_user_by_username("unique_name")
        assert found == user_data
        
        not_found = persistence.get_user_by_username("nonexistent")
        assert not_found is None

    def test_persistence_fraud_flags(self, persistence):
        flag = {"id": "f1", "reason": "test"}
        persistence.save_fraud_flag(flag)
        
        flags = persistence.get_fraud_flags()
        assert len(flags) == 1
        assert flags[0] == flag

    # --- Report Service Tests ---
    def test_account_statement_exact_format(self, persistence, report_service):
        # Setup data
        acc_data = {
            "account_id": "acc1",
            "user_id": "u1",
            "balance": 1000.0,
            "account_type": "SAVINGS",
            "is_active": True
        }
        persistence.save_account(acc_data)
        
        tx1 = {
            "transaction_id": "t1",
            "account_id": "acc1",
            "amount": 500.0,
            "transaction_type": "DEPOSIT",
            "timestamp": "2023-01-01T10:00:00.000000",
            "description": "Initial"
        }
        tx2 = {
            "transaction_id": "t2",
            "account_id": "acc1",
            "amount": 200.0,
            "transaction_type": "WITHDRAWAL",
            "timestamp": "2023-01-02T10:00:00.000000",
            "description": "ATM"
        }
        persistence.log_transaction(tx1)
        persistence.log_transaction(tx2)
        
        # Generate Report
        report = report_service.generate_account_statement("acc1")
        
        # Verify Exact String Content (kills formatting mutants)
        expected_lines = [
            "Statement for Account: acc1",
            "Type: SAVINGS",
            "Current Balance: $1000.00",
            "-" * 50,
            f"{'Date':<20} | {'Type':<12} | {'Amount':<10} | {'Description'}",
            "-" * 50,
            # tx2 is newer, so it comes first
            f"{'2023-01-02T10:00:00':<20} | {'WITHDRAWAL':<12} | ${200.0:<9.2f} | {'ATM'}",
            f"{'2023-01-01T10:00:00':<20} | {'DEPOSIT':<12} | ${500.0:<9.2f} | {'Initial'}",
            "-" * 50
        ]
        expected_report = "\n".join(expected_lines)
        
        assert report == expected_report

    def test_admin_report_exact_format(self, persistence, report_service):
        # Setup data
        u1 = {"user_id": "u1", "username": "a", "accounts": ["a1"]}
        u2 = {"user_id": "u2", "username": "b", "accounts": ["a2", "a3"]}
        persistence.save_user(u1)
        persistence.save_user(u2)
        
        persistence.save_account({"account_id": "a1", "user_id": "u1", "balance": 100.0})
        persistence.save_account({"account_id": "a2", "user_id": "u2", "balance": 200.0})
        persistence.save_account({"account_id": "a3", "user_id": "u2", "balance": 300.0})
        
        # Generate Report
        report = report_service.generate_admin_report()
        
        expected_lines = [
            "=== ADMIN REPORT ===",
            "Total Users: 2",
            "Total Accounts: 3",
            "Total Assets Held: $600.00",
            "===================="
        ]
        expected_report = "\n".join(expected_lines)
        
        assert report == expected_report
