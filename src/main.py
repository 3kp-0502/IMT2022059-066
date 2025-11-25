import sys
import os
import cmd
from getpass import getpass

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.auth_service import AuthService
from src.services.bank_service import BankService
from src.services.report_service import ReportService
from src.services.loan_service import LoanService
from src.services.fraud_service import FraudDetectionService
from src.utils.persistence import PersistenceLayer
from src.utils.validators import ValidationError

class BankingCLI(cmd.Cmd):
    intro = 'Welcome to the Secure Banking System. Type help or ? to list commands.\n'
    prompt = '(banking) '

    def __init__(self):
        super().__init__()
        self.persistence = PersistenceLayer()
        self.auth_service = AuthService(self.persistence)
        self.bank_service = BankService(self.persistence)
        self.report_service = ReportService(self.persistence)
        self.loan_service = LoanService(self.persistence)
        self.fraud_service = FraudDetectionService(self.persistence)

    def do_register(self, arg):
        """Register a new user: register <username> <email> <phone>"""
        args = arg.split()
        if len(args) != 3:
            print("Usage: register <username> <email> <phone>")
            return
        
        username, email, phone = args
        password = getpass("Enter password: ")
        confirm_password = getpass("Confirm password: ")

        if password != confirm_password:
            print("Passwords do not match.")
            return

        try:
            user = self.auth_service.register(username, password, email, phone)
            print(f"User {user.username} registered successfully!")
        except ValidationError as e:
            print(f"Error: {e}")

    def do_login(self, arg):
        """Login to the system: login <username>"""
        if not arg:
            print("Usage: login <username>")
            return
        
        username = arg
        password = getpass("Enter password: ")

        try:
            user = self.auth_service.login(username, password)
            print(f"Welcome back, {user.username}!")
            self.prompt = f'({user.username}) '
        except ValidationError as e:
            print(f"Error: {e}")

    def do_logout(self, arg):
        """Logout from the current session."""
        if self.auth_service.is_authenticated():
            self.auth_service.logout()
            print("Logged out successfully.")
            self.prompt = '(banking) '
        else:
            print("You are not logged in.")

    def do_create_account(self, arg):
        """Create a new account: create_account <SAVINGS|CURRENT|FIXED_DEPOSIT> [initial_deposit]"""
        if not self.auth_service.is_authenticated():
            print("Please login first.")
            return

        args = arg.split()
        if len(args) < 1:
            print("Usage: create_account <type> [initial_deposit]")
            return

        acc_type = args[0].upper()
        initial_deposit = float(args[1]) if len(args) > 1 else 0.0

        try:
            account = self.bank_service.create_account(self.auth_service.current_user, acc_type, initial_deposit)
            print(f"Account created successfully! ID: {account.account_id}")
        except ValidationError as e:
            print(f"Error: {e}")
        except ValueError:
             print("Invalid amount.")

    def do_my_accounts(self, arg):
        """List all your accounts."""
        if not self.auth_service.is_authenticated():
            print("Please login first.")
            return

        accounts = self.bank_service.get_user_accounts(self.auth_service.current_user.user_id)
        if not accounts:
            print("No accounts found.")
            return

        print(f"{'Account ID':<38} | {'Type':<15} | {'Balance'}")
        print("-" * 65)
        for acc in accounts:
            print(f"{acc.account_id:<38} | {acc.account_type:<15} | ${acc.balance:.2f}")

    def do_deposit(self, arg):
        """Deposit money: deposit <account_id> <amount>"""
        if not self.auth_service.is_authenticated():
            print("Please login first.")
            return
        
        args = arg.split()
        if len(args) != 2:
            print("Usage: deposit <account_id> <amount>")
            return

        try:
            self.bank_service.deposit(args[0], float(args[1]))
            print("Deposit successful.")
        except ValidationError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Invalid amount.")

    def do_withdraw(self, arg):
        """Withdraw money: withdraw <account_id> <amount>"""
        if not self.auth_service.is_authenticated():
            print("Please login first.")
            return
        
        args = arg.split()
        if len(args) != 2:
            print("Usage: withdraw <account_id> <amount>")
            return

        try:
            self.bank_service.withdraw(args[0], float(args[1]))
            print("Withdrawal successful.")
        except ValidationError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Invalid amount.")

    def do_transfer(self, arg):
        """Transfer money: transfer <from_acc_id> <to_acc_id> <amount>"""
        if not self.auth_service.is_authenticated():
            print("Please login first.")
            return
        
        args = arg.split()
        if len(args) != 3:
            print("Usage: transfer <from_id> <to_id> <amount>")
            return

        try:
            self.bank_service.transfer(args[0], args[1], float(args[2]))
            print("Transfer successful.")
        except ValidationError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Invalid amount.")

    def do_statement(self, arg):
        """Get account statement: statement <account_id>"""
        if not self.auth_service.is_authenticated():
            print("Please login first.")
            return
        
        if not arg:
            print("Usage: statement <account_id>")
            return

        # Verify ownership
        accounts = self.bank_service.get_user_accounts(self.auth_service.current_user.user_id)
        if arg not in [acc.account_id for acc in accounts]:
            print("Account not found or access denied.")
            return

        print(self.report_service.generate_account_statement(arg))

    def do_admin_report(self, arg):
        """Generate admin report (Admin only)."""
        if not self.auth_service.is_authenticated() or not self.auth_service.is_admin():
            print("Access denied. Admin only.")
            return
        
        print(self.report_service.generate_admin_report())

    def do_apply_interest(self, arg):
        """Apply interest to all savings accounts (Admin only)."""
        if not self.auth_service.is_authenticated() or not self.auth_service.is_admin():
            print("Access denied. Admin only.")
            return
        
        count = self.bank_service.calculate_interest()
        print(f"Interest applied to {count} accounts.")

    def do_apply_loan(self, arg):
        """Apply for a loan: apply_loan <amount> <term_months>"""
        if not self.auth_service.is_authenticated():
            print("Please login first.")
            return
        
        args = arg.split()
        if len(args) != 2:
            print("Usage: apply_loan <amount> <term_months>")
            return
        
        try:
            loan = self.loan_service.apply_for_loan(self.auth_service.current_user, float(args[0]), int(args[1]))
            print(f"Loan application submitted. ID: {loan.loan_id}")
        except ValidationError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Invalid input.")

    def do_my_loans(self, arg):
        """List my loans."""
        if not self.auth_service.is_authenticated():
            print("Please login first.")
            return
        
        loans = self.loan_service.get_user_loans(self.auth_service.current_user.user_id)
        if not loans:
            print("No loans found.")
            return
        
        print(f"{'Loan ID':<38} | {'Amount':<10} | {'Status':<10} | {'Remaining'}")
        print("-" * 75)
        for loan in loans:
            print(f"{loan.loan_id:<38} | ${loan.amount:<9.2f} | {loan.status.value:<10} | ${loan.remaining_amount:.2f}")

    def do_pay_loan(self, arg):
        """Repay loan: pay_loan <loan_id> <amount>"""
        if not self.auth_service.is_authenticated():
            print("Please login first.")
            return
        
        args = arg.split()
        if len(args) != 2:
            print("Usage: pay_loan <loan_id> <amount>")
            return
        
        try:
            self.loan_service.repay_loan(args[0], float(args[1]))
            print("Repayment successful.")
        except ValidationError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Invalid amount.")

    def do_approve_loan(self, arg):
        """Approve a loan (Admin only): approve_loan <loan_id>"""
        if not self.auth_service.is_authenticated() or not self.auth_service.is_admin():
            print("Access denied. Admin only.")
            return
        
        if not arg:
            print("Usage: approve_loan <loan_id>")
            return
        
        try:
            self.loan_service.approve_loan(arg)
            print("Loan approved.")
        except ValidationError as e:
            print(f"Error: {e}")

    def do_reject_loan(self, arg):
        """Reject a loan (Admin only): reject_loan <loan_id>"""
        if not self.auth_service.is_authenticated() or not self.auth_service.is_admin():
            print("Access denied. Admin only.")
            return
        
        if not arg:
            print("Usage: reject_loan <loan_id>")
            return
        
        try:
            self.loan_service.reject_loan(arg)
            print("Loan rejected.")
        except ValidationError as e:
            print(f"Error: {e}")

    def do_fraud_report(self, arg):
        """View fraud report (Admin only)."""
        if not self.auth_service.is_authenticated() or not self.auth_service.is_admin():
            print("Access denied. Admin only.")
            return
        
        flags = self.fraud_service.get_flagged_transactions()
        if not flags:
            print("No flagged transactions.")
            return
        
        print("=== FRAUD REPORT ===")
        for flag in flags:
            print(f"Tx ID: {flag['transaction_id']}")
            print(f"Reasons: {', '.join(flag['reasons'])}")
            print(f"Time: {flag['timestamp']}")
            print("-" * 30)

    def do_exit(self, arg):
        """Exit the application."""
        print("Goodbye!")
        return True

if __name__ == '__main__':
    BankingCLI().cmdloop()
