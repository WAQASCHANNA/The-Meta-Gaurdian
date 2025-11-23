def check_financial_compliance(decision_data):
    """
    Validates Loan and Expense decisions.
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
