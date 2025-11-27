# Secure Banking System (CLI)

## Project Overview
This project is a command-line based Secure Banking System developed for CSE 731: Software Testing. It demonstrates a robust banking application with features suitable for **Mutation Testing**, specifically targeting both **Unit** and **Integration** levels.

## Features
- **User Management**: Registration, Login, Role-based access (Admin/Customer).
- **Account Management**: Savings, Current, and Fixed Deposit accounts.
- **Transactions**: Deposits, Withdrawals, Transfers with transactional integrity.
- **Loan System**: Apply for loans, Admin approval/rejection, Repayment.
- **Fraud Detection**: Automated flagging of suspicious transactions.
- **Audit Logging**: Comprehensive logging of all user actions for compliance.
- **Reporting**: Account statements and Admin reports.

## Repository Link
- **Code Repository**: https://github.com/3kp-0502/IMT2022059-066

## Team Members
- DHAROORI SRINIVAS ACHARYA IMT2022066
- PUDI KIREETI IM2022059

## AI Acknowledgement
This project was developed with the assistance of Google's AI tools for:
- README structuring.
- Unit test desing and Mutation testing strategy planning.

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
We employ a comprehensive **Mutation Testing** strategy to ensure the robustness of our test suite.
**Detailed Strategy**: See [TEST_STRATEGY.md](TEST_STRATEGY.md) for a full breakdown of mutation operators and our "Strong Kill" approach.

### Key Highlights
- **Unit Level**: Verified Arithmetic (AOR), Relational (ROR), and Assignment (ASR) operators.
- **Integration Level**: Verified Parameter Replacement (IPR), Method Call Deletion (IMCD), and Return Value Replacement (IVR) using `tests/test_integration_robustness.py`.
- **Tool**: `mutmut`

### Mutation Testing Results
- **Initial Run**: Found surviving mutants in `src/models/account.py`.
- **Example Fix 1**: Mutant #200 (Default Value Change) - Killed by `tests/test_mutation_kills.py`.
- **Example Fix 2**: Mutant #700 (Balance Initialization) - Killed by `tests/test_mutation_kills.py`.
- **Integration Fix**: Added `tests/test_integration_robustness.py` to kill mutants that modify service-persistence interactions.

### Test Execution
To reproduce the testing results:
1. **Run Unit & Integration Tests**:
   ```bash
   python -m pytest
   ```
2. **Run Mutation Tests**:
   ```bash
   mutmut run
   ```
3. **View Report**:
   Open `html/index.html` in a browser.

## Testing Tools Used
- **pytest**: For automated unit and integration testing.
- **mutmut**: For mutation testing (Python).
- **coverage**: For code coverage analysis.
- **unittest.mock**: For verifying integration interactions.

## Test Evidence
- **Screenshots**:
  
  **1. Unit Tests Passing**
  ![Unit Tests](screenshots/Screenshot%202025-11-26%20193339.png)

  **2. Mutation Testing Results**
  ![Mutation Results](screenshots/Screenshot%202025-11-26%20193355.png)

  **3. Killed Mutant Example**
  ![Mutant Killed](screenshots/Screenshot%202025-11-26%20193546.png)

- **HTML Report**: See `html/index.html` for the detailed mutation report.

## Directory Structure
- `src/`: Source code.
- `tests/`: Test suite (Unit and Integration).
- `data/`: JSON persistence files.
- `html/`: Mutation testing HTML report.
