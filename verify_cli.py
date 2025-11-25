import subprocess
import time
import os
import shutil

def run_cli_test():
    # Clean up data dir
    if os.path.exists("data"):
        shutil.rmtree("data")

    process = subprocess.Popen(
        ["python", "src/main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.getcwd()
    )

    commands = [
        "register admin admin@test.com 1234567890",
        "adminP@ss1", # Password
        "adminP@ss1", # Confirm
        "login admin",
        "adminP@ss1",
        "create_account SAVINGS 1000",
        "my_accounts",
        "apply_loan 5000 12",
        "my_loans",
        "logout",
        "exit"
    ]

    input_str = "\n".join(commands) + "\n"
    stdout, stderr = process.communicate(input=input_str)

    print("=== CLI OUTPUT ===")
    print(stdout)
    
    if stderr:
        print("=== CLI ERROR ===")
        print(stderr)

    # Basic assertions
    if "User admin registered successfully!" in stdout:
        print("PASS: Registration")
    else:
        print("FAIL: Registration")

    if "Welcome back, admin!" in stdout:
        print("PASS: Login")
    else:
        print("FAIL: Login")

    if "Account created successfully!" in stdout:
        print("PASS: Account Creation")
    else:
        print("FAIL: Account Creation")

    if "Loan application submitted." in stdout:
        print("PASS: Loan Application")
    else:
        print("FAIL: Loan Application")

if __name__ == "__main__":
    run_cli_test()
