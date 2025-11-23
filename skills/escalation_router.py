def route_escalation(decision_data, compliance_result):
    """
    Simulates routing high-risk items to a human.
    """
    if not compliance_result["compliant"]:
        print("\n[!!!] ESCALATION ALERT [!!!]")
        print(f"Agent: {decision_data.get('agent_name')}")
        print(f"Violation: {compliance_result['violation_type']}")
        print(f"Message: {compliance_result['message']}")
        print(f"Decision Context: {json.dumps(decision_data, indent=2)}")
        print("[!!!] END ALERT [!!!]\n")
        return True
    return False

import json
