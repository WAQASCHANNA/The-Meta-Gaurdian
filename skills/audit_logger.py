import json
import os
from datetime import datetime

LOG_FILE = "audit_log.json"

def log_audit(decision_data, compliance_result):
    """
    Logs the decision and compliance result to a local file.
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "original_decision": decision_data,
        "compliance_check": compliance_result
    }

    # Read existing logs
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

    logs.append(entry)

    # Write back
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
    
    return len(logs) # Return ID (index + 1 or similar)
