import json
import random
import time
from datetime import datetime

def generate_loan_decision():
    # Mock inputs
    applicants = ["Alice Smith", "Bob Jones", "Charlie Brown", "Diana Prince", "Evan Wright"]
    applicant = random.choice(applicants)
    loan_amount = random.randint(5000, 100000)
    credit_score = random.randint(500, 850)
    
    decision_data = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": "LoanApprovalBot",
        "applicant": applicant,
        "loan_amount": loan_amount,
        "credit_score": credit_score,
        "decision": "PENDING",
        "risk_level": "UNKNOWN",
        "reason": ""
    }

    # Simple Logic
    if loan_amount > 50000:
        decision_data["risk_level"] = "HIGH"
        decision_data["decision"] = "FLAGGED"
        decision_data["reason"] = "Loan amount exceeds auto-approval limit of $50k"
    elif credit_score < 600:
        decision_data["risk_level"] = "HIGH"
        decision_data["decision"] = "REJECTED"
        decision_data["reason"] = "Credit score below minimum threshold"
    else:
        decision_data["risk_level"] = "LOW"
        decision_data["decision"] = "APPROVED"
        decision_data["reason"] = "Meets all criteria"

    return decision_data

if __name__ == "__main__":
    import requests
    # Simulate a decision
    decision = generate_loan_decision()
    print(json.dumps(decision, indent=2))
    
    # Send to MetaGuardian Webhook
    try:
        response = requests.post("http://localhost:5000/webhook", json=decision)
        print(f"Webhook Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed to send webhook: {e}")
