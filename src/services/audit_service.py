import datetime
import os
from typing import Dict, Any

class AuditService:
    """
    Service to log all system actions for compliance and auditing purposes.
    This is distinct from the transaction ledger; it tracks WHO did WHAT and WHEN.
    """
    def __init__(self, log_file: str = "data/audit.log"):
        self.log_file = log_file
        self._ensure_log_dir()

    def _ensure_log_dir(self):
        directory = os.path.dirname(self.log_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def log_action(self, user_id: str, action: str, details: str, status: str = "SUCCESS"):
        """
        Logs a specific action taken by a user.
        """
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"[{timestamp}] USER:{user_id} ACTION:{action} STATUS:{status} DETAILS:{details}\n"
        
        with open(self.log_file, "a") as f:
            f.write(log_entry)

    def log_system_event(self, event: str, severity: str = "INFO"):
        """
        Logs a system-level event (e.g., startup, shutdown, errors).
        """
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"[{timestamp}] SYSTEM EVENT:{event} SEVERITY:{severity}\n"
        
        with open(self.log_file, "a") as f:
            f.write(log_entry)

    def get_logs_for_user(self, user_id: str) -> list:
        """
        Retrieves all audit logs related to a specific user.
        """
        user_logs = []
        if not os.path.exists(self.log_file):
            return user_logs

        with open(self.log_file, "r") as f:
            for line in f:
                if f"USER:{user_id}" in line:
                    user_logs.append(line.strip())
        return user_logs

    def export_logs(self, filepath: str):
        """
        Exports the current audit log to a specified file.
        """
        if not os.path.exists(self.log_file):
            return
        
        with open(self.log_file, "r") as src, open(filepath, "w") as dst:
            dst.write(src.read())
