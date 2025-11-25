# Secure Banking System (CLI)

## Project Overview
This project is a command-line based Secure Banking System developed for CSE 731: Software Testing. It demonstrates a robust banking application with features suitable for **Mutation Testing**.

## Features
- **User Management**: Registration, Login, Role-based access (Admin/Customer).
- **Account Management**: Savings, Current, and Fixed Deposit accounts.
- **Transactions**: Deposits, Withdrawals, Transfers with transactional integrity.
- **Loan System**: Apply for loans, Admin approval/rejection, Repayment.
- **Fraud Detection**: Automated flagging of suspicious transactions.
- **Audit Logging**: Comprehensive logging of all user actions for compliance.
- **Reporting**: Account statements and Admin reports.

## Project Stats
- **Lines of Code (SLOC)**: 1015 (excluding comments/blanks)
- **Total Lines**: 1262

## Team Members
- [Member 1 Name] (Roll No)
- [Member 2 Name] (Roll No)

## AI Acknowledgement
This project was developed with the assistance of Google's AI tools for:
- Code generation and structuring.
- Test case design and mutation testing strategy planning.

## Setup and Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python src/main.py
   ```

## Testing Strategy
We are using **Mutation Testing** to verify the robustness of our test suite.
- **Tool**: `mutmut`
- **Goal**: Achieve a high mutation score by killing generated mutants.

### Mutation Testing Results
- **Initial Run**: Found ~23 surviving mutants in `src/models/account.py`.
- **Example Fix 1**: Mutant #200 changed `is_active` default from `True` to `None`.
- **Example Fix 2**: Mutant #700 changed `balance` default from `0.0` to `1.0`.
- **Action**: Added tests in `tests/test_mutation_kills.py` to assert correct default values.
- **Result**: Mutants #200 and #700 killed.

## Directory Structure
- `src/`: Source code.
- `tests/`: Test suite.
- `data/`: JSON persistence files.
