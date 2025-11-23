import json
from datetime import datetime, timedelta

# Generate sample audit log data for demo purposes
sample_data = []

# Sample 1: Compliant Loan
sample_data.append({
    "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
    "original_decision": {
        "agent_name": "LoanApprovalBot",
        "applicant": "John Doe",
        "loan_amount": 15000,
        "credit_score": 720,
        "decision": "APPROVED"
    },
    "compliance_check": {
        "compliant": True,
        "violation_type": None,
        "message": "Decision complies with credit policy."
    }
})

# Sample 2: High Risk Loan (Violation)
sample_data.append({
    "timestamp": (datetime.now() - timedelta(hours=1, minutes=30)).isoformat(),
    "original_decision": {
        "agent_name": "LoanApprovalBot",
        "applicant": "Jane Smith",
        "loan_amount": 75000,
        "credit_score": 580,
        "decision": "APPROVED"
    },
    "compliance_check": {
        "compliant": False,
        "violation_type": "High Risk Loan",
        "message": "Credit score 580 is below minimum threshold of 600."
    }
})

# Sample 3: Compliant Hiring
sample_data.append({
    "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
    "original_decision": {
        "agent_name": "HiringBot",
        "candidate": "Alice Johnson",
        "years_experience": 5,
        "education": "Masters",
        "decision": "INTERVIEW"
    },
    "compliance_check": {
        "compliant": True,
        "violation_type": None,
        "message": "Decision complies with hiring policy."
    }
})

# Sample 4: Bias Detection (Violation)
sample_data.append({
    "timestamp": (datetime.now() - timedelta(minutes=45)).isoformat(),
    "original_decision": {
        "agent_name": "HiringBot",
        "candidate": "Bob Chen",
        "years_experience": 3,
        "education": "Bachelors",
        "decision": "REJECT"
    },
    "compliance_check": {
        "compliant": False,
        "violation_type": "Potential Bias",
        "message": "Candidate name 'Bob Chen' may indicate demographic bias in rejection pattern."
    }
})

# Sample 5: Excessive Expense (Violation)
sample_data.append({
    "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat(),
    "original_decision": {
        "agent_name": "ExpenseApprovalBot",
        "employee": "Marketing Team",
        "expense_amount": 12000,
        "category": "Conference",
        "decision": "APPROVED"
    },
    "compliance_check": {
        "compliant": False,
        "violation_type": "Excessive Expense",
        "message": "Expense amount $12000 exceeds limit of $10000."
    }
})

# Sample 6: Compliant Expense
sample_data.append({
    "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
    "original_decision": {
        "agent_name": "ExpenseApprovalBot",
        "employee": "Sales Team",
        "expense_amount": 3500,
        "category": "Client Dinner",
        "decision": "APPROVED"
    },
    "compliance_check": {
        "compliant": True,
        "violation_type": None,
        "message": "Decision complies with expense policy."
    }
})

# Write to sample file
with open("sample_audit_log.json", "w") as f:
    json.dump(sample_data, f, indent=2)

print("Created sample_audit_log.json with 6 sample decisions")
print("   - 3 Compliant decisions")
print("   - 3 Violations (High Risk Loan, Bias, Excessive Expense)")
