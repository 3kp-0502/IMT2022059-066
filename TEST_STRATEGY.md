# Test Strategy & Mutation Testing Report

## 1. Overview
This project employs **Mutation Testing** to ensure the robustness of the Secure Banking System. We use `mutmut` to generate mutants and `pytest` to run the test suite. Our goal is to achieve a high mutation score by "strongly killing" mutants at both the Unit and Integration levels.

## 2. Mutation Operators Selected

### A. Unit Level Operators
These operators modify logic within a single method or function.
1.  **Arithmetic Operator Replacement (AOR)**:
    -   Replaces `+`, `-`, `*`, `/` with other operators.
    -   *Target*: Interest calculation, balance updates.
    -   *Verification*: `tests/test_services.py` asserts exact balance values.
2.  **Relational Operator Replacement (ROR)**:
    -   Replaces `>`, `<`, `==`, `!=`, etc.
    -   *Target*: Validation checks (e.g., `if amount > 0`), loop conditions.
    -   *Verification*: Boundary value analysis tests (e.g., depositing 0 or negative amounts).
3.  **Assignment Operator Replacement (ASR)**:
    -   Replaces `=` or `+=` with `-=` or similar.
    -   *Target*: Variable initialization and updates.
    -   *Verification*: State verification tests.

### B. Integration Level Operators
These operators target the interaction between modules, specifically `BankService` <-> `PersistenceLayer`.
1.  **Integration Parameter Replacement (IPR)**:
    -   Modifies arguments passed to external function calls.
    -   *Example*: `persistence.save_account(data)` -> `persistence.save_account(None)` or `persistence.save_account(modified_data)`.
    -   *Verification*: `tests/test_integration_robustness.py` uses `unittest.mock` to verify `assert_called_with` exact arguments.
2.  **Integration Method Call Deletion (IMCD)**:
    -   Removes the call to an external service entirely.
    -   *Example*: Deleting `persistence.save_user(user)`.
    -   *Verification*: Tests check that side effects (file persistence) occur or mocks are called.
3.  **Integration Return Value Replacement (IVR)**:
    -   Modifies the return value from a dependency.
    -   *Example*: `persistence.get_account` returns `None` instead of data.
    -   *Verification*: Tests ensure the service handles `None` or invalid data correctly (e.g., raising `ValidationError`).

## 3. Strong Kill Strategy
A mutant is "strongly killed" when the test case execution produces a different *output* or *state* than the original program, not just a crash.
-   **State Verification**: We check `account.balance`, `user.accounts`, etc.
-   **Behavior Verification**: We check that specific exceptions are raised for invalid inputs.
-   **Interaction Verification**: We check that dependencies are called with the correct data using mocks.

## 4. Tools Used
-   **pytest**: Test runner.
-   **mutmut**: Mutation testing tool.
-   **coverage**: Code coverage analysis.
-   **unittest.mock**: For integration interaction verification.

## 5. Execution Results
-   **LOC**: 1109 lines of source code (excluding tests).
-   **Mutation Score**: High (Verified via `mutmut results`).
