import re

def check_policy(decision_data):
    """
    Simulates NLU policy checking.
    Input: Decision JSON
    Output: Compliance Result JSON
    """
    agent_name = decision_data.get("agent_name")
    compliance_result = {
        "compliant": True,
        "violation_type": None,
        "message": "Compliant with policy."
    }

    if agent_name == "LoanApprovalBot":
        amount = decision_data.get("loan_amount", 0)
        score = decision_data.get("credit_score", 0)
        if amount > 50000:
            compliance_result["compliant"] = False
            compliance_result["violation_type"] = "High Risk Loan"
            compliance_result["message"] = f"Loan amount ${amount} exceeds $50k auto-approval limit."
        elif score < 600:
            compliance_result["compliant"] = False
            compliance_result["violation_type"] = "Credit Risk"
            compliance_result["message"] = f"Credit score {score} is below minimum 600."

    elif agent_name == "HiringBot":
        location = decision_data.get("location", "")
        experience = decision_data.get("experience_years", 0)
        if location == "Unknown":
            compliance_result["compliant"] = False
            compliance_result["violation_type"] = "Missing Data"
            compliance_result["message"] = "Candidate location is unknown."
        elif experience < 2:
             compliance_result["compliant"] = False
             compliance_result["violation_type"] = "Experience Gap"
             compliance_result["message"] = "Candidate has less than 2 years experience."

    elif agent_name == "ExpenseApprovalBot":
        amount = decision_data.get("amount", 0)
        expense_type = decision_data.get("expense_type", "")
        if amount > 10000:
            compliance_result["compliant"] = False
            compliance_result["violation_type"] = "High Value Expense"
            compliance_result["message"] = f"Expense ${amount} exceeds $10k limit."
        elif expense_type == "Software" and amount > 5000:
            compliance_result["compliant"] = False
            compliance_result["violation_type"] = "IT Approval Required"
            compliance_result["message"] = "Software expense > $5k requires IT approval."

    return compliance_result
