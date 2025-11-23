import json
import random
from datetime import datetime

def generate_expense_decision():
    employees = ["E101", "E102", "E103", "E104"]
    expense_types = ["Travel", "Meals", "Software", "Equipment"]
    
    employee_id = random.choice(employees)
    expense_type = random.choice(expense_types)
    amount = random.randint(50, 15000)

    decision_data = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": "ExpenseApprovalBot",
        "employee_id": employee_id,
        "expense_type": expense_type,
        "amount": amount,
        "decision": "PENDING",
        "risk_level": "UNKNOWN",
        "reason": ""
    }

    # Logic
    if amount > 10000:
        decision_data["risk_level"] = "HIGH"
        decision_data["decision"] = "FLAGGED"
        decision_data["reason"] = "Expense exceeds $10k limit"
    elif expense_type == "Software" and amount > 5000:
        decision_data["risk_level"] = "MEDIUM"
        decision_data["decision"] = "FLAGGED"
        decision_data["reason"] = "Software purchase > $5k requires IT approval"
    else:
        decision_data["risk_level"] = "LOW"
        decision_data["decision"] = "APPROVED"
        decision_data["reason"] = "Within policy limits"

    return decision_data

if __name__ == "__main__":
    import requests
    decision = generate_expense_decision()
    print(json.dumps(decision, indent=2))

    # Send to MetaGuardian Webhook
    try:
        response = requests.post("http://localhost:5000/webhook", json=decision)
        print(f"Webhook Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed to send webhook: {e}")
