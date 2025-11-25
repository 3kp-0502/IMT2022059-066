# Secure Banking System (CLI)

## Project Overview
This project is a command-line based Secure Banking System developed for **CSE 731: Software Testing**. It demonstrates a robust banking application with features specifically designed to demonstrate **Mutation Testing**.

## Problem Statement
**Mutation Testing**: The project focuses on using mutation operators at the statement and integration levels. The goal is to design a test suite that strongly kills generated mutants.
- **Unit Level**: Arithmetic, Relational, and Assignment mutations.
- **Integration Level**: Interface mutations between Service and Persistence layers.

## Team Members
| Name | Roll Number | Contribution |
|------|-------------|--------------|
| PUDI KIRRETI | IMT2022059 | 50% - Core Banking Services, Unit Tests |
| DHAROORI SRINIVAS ACHARYA | IMT2022066 | 50% - Mutation Strategy, Integration Tests |

## Project Stats
- **Lines of Code (SLOC)**: 1015
- **Total Lines**: 1262
- **Language**: Python 3.x

## Tools Used
- **Test Runner**: `pytest`
- **Mutation Testing**: `mutmut`
- **Coverage**: `coverage.py`

## Testing Strategy
We employed a **Mutation-Driven Testing** strategy. Detailed analysis of operators and strong kill verification is available in [TEST_STRATEGY.md](TEST_STRATEGY.md).

1.  **Initial Suite**: Created standard functional tests for all services.
2.  **Mutation Analysis**: Ran `mutmut` to identify surviving mutants.
3.  **Refinement**: Added targeted test cases (e.g., `tests/test_mutation_kills.py`) to kill specific mutants (e.g., default value changes, boundary conditions).
4.  **Integration Robustness**: Added `tests/test_integration_robustness.py` to verify Service-Persistence interactions (IPR/IVR).
5.  **Result**: Achieved high mutation score by verifying internal state and default parameter handling.

### Execution Screenshots
**Passing Test Suite**
![Passing Tests](pytest_passed.png)

**Mutation Testing Results**
![Mutmut Results](mutmut_results.png)

## Setup and Usage
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the application:
    ```bash
    python src/main.py
    ```
3.  Run Tests:
    ```bash
    python -m pytest
    ```
4.  Run Mutation Testing:
    ```bash
    mutmut run
    mutmut results
    ```

## Directory Structure
- `src/`: Source code (Models, Services, Utils).
- `tests/`: Test suite (Functional and Mutation-specific tests).
- `data/`: JSON persistence files.

