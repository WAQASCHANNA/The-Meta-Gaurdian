def check_hr_compliance(decision_data):
    """
    Validates Hiring decisions.
    """
    agent_name = decision_data.get("agent_name")
    compliance_result = {
        "compliant": True,
        "violation_type": None,
        "message": "Compliant with policy."
    }

    if agent_name == "HiringBot":
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

    return compliance_result
