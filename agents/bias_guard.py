def check_bias(decision_data):
    """
    Analyzes hiring decisions for potential bias.
    """
    agent_name = decision_data.get("agent_name")
    compliance_result = {
        "compliant": True,
        "violation_type": None,
        "message": "No bias detected."
    }

    if agent_name == "HiringBot":
        location = decision_data.get("location", "")
        # Mock Bias Logic: Flag if "Unknown" location is rejected (already covered by HR guard, but this adds a specific bias flag)
        # Or flag if a specific demographic is rejected (mocking this by flagging very young candidates as potential age bias if rejected)
        
        experience = decision_data.get("experience_years", 0)
        decision = decision_data.get("decision", "")
        
        if decision == "REJECTED" and experience > 10:
             # Suspicious rejection of highly experienced candidate
             compliance_result["compliant"] = False
             compliance_result["violation_type"] = "Potential Age Bias"
             compliance_result["message"] = "Highly experienced candidate rejected. Review for age bias."

    return compliance_result
