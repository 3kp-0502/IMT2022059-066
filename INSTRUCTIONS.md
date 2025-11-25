# Step-by-Step Guide to Running and Testing

## 1. Navigate to the Project Directory
Open your terminal (Command Prompt or PowerShell) and navigate to the project folder:
```powershell
cd "c:\Users\3kp05\Downloads\ST Project\banking_system"
```

## 2. Install Dependencies
Install the required Python libraries (pytest, mutmut, etc.):
```powershell
pip install -r requirements.txt
```

## 3. Run the Application (CLI)
To start the banking system and interact with it manually:
```powershell
python src/main.py
```
**Commands to try:**
- `register myuser password123 my@email.com 1234567890`
- `login myuser`
- `create_account SAVINGS 1000`
- `my_accounts`
- `exit`

## 4. Run Unit Tests
To run the automated test suite (verifies the code works correctly):
```powershell
python -m pytest
```
*Expected Output:* You should see green dots indicating tests passed.

## 5. Run Mutation Testing (The "Full Marks" Feature)
To perform mutation testing (which modifies your code to ensure tests catch bugs):
```powershell
mutmut run
```
*Note:* This might take a few minutes.

To see the results (which mutants survived vs killed):
```powershell
mutmut results
```

To see a specific mutant (e.g., mutant #200):
```powershell
mutmut show 200
```
