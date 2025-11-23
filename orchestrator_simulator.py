from flask import Flask, request, jsonify
from agents.financial_guard import check_financial_compliance
from agents.hr_guard import check_hr_compliance
from agents.bias_guard import check_bias
from skills.audit_logger import log_audit
from skills.escalation_router import route_escalation
import json

app = Flask(__name__)

# Self-Healing State
AGENT_VIOLATIONS = {}
BLOCKED_AGENTS = set()
MAX_VIOLATIONS = 3

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    agent_name = data.get('agent_name')
    
    # 0. Self-Healing Check
    if agent_name in BLOCKED_AGENTS:
        print(f"BLOCKED REQUEST from {agent_name}")
        return jsonify({
            "status": "blocked", 
            "message": "Agent is blocked due to excessive violations."
        }), 403

    print(f"Received webhook from {agent_name}")

    # 1. Route to Specialized Agent
    compliance = None
    
    if agent_name in ["LoanApprovalBot", "ExpenseApprovalBot"]:
        compliance = check_financial_compliance(data)
    elif agent_name == "HiringBot":
        # Check HR Policy
        compliance = check_hr_compliance(data)
        # Check Bias if HR check passed (or in parallel)
        if compliance["compliant"]:
             bias_check = check_bias(data)
             if not bias_check["compliant"]:
                 compliance = bias_check # Override with bias warning

    else:
        # Fallback or Error
        compliance = {
            "compliant": False, 
            "violation_type": "Unknown Agent", 
            "message": "Agent not registered."
        }

    # 2. Audit Log
    log_id = log_audit(data, compliance)

    # 3. Self-Healing Logic: Track Violations
    if not compliance["compliant"]:
        AGENT_VIOLATIONS[agent_name] = AGENT_VIOLATIONS.get(agent_name, 0) + 1
        print(f"Violation recorded for {agent_name}. Count: {AGENT_VIOLATIONS[agent_name]}")
        
        if AGENT_VIOLATIONS[agent_name] >= MAX_VIOLATIONS:
            BLOCKED_AGENTS.add(agent_name)
            print(f"[!!!] SELF-HEALING TRIGGERED: Blocking {agent_name} [!!!]")

    # 4. Escalate if needed
    escalated = route_escalation(data, compliance)

    response = {
        "status": "processed",
        "audit_id": log_id,
        "compliance_result": compliance,
        "escalated": escalated,
        "blocked": agent_name in BLOCKED_AGENTS
    }
    
    return jsonify(response)

@app.route('/resolve_decision', methods=['POST'])
def resolve_decision():
    """
    Human-in-the-Loop Resolution Endpoint
    """
    data = request.json
    audit_id = data.get("audit_id") # This would ideally be an ID, but we are using list index for simplicity in this mock
    action = data.get("action") # "APPROVE" or "REJECT"
    
    # In a real DB, we would update the record. 
    # Here we will just log the resolution action to a new file or append to audit log
    
    print(f"Human Resolution: {action} for Audit ID {audit_id}")
    
    return jsonify({"status": "resolved", "action": action})

@app.route('/unblock_agent', methods=['POST'])
def unblock_agent():
    data = request.json
    agent_name = data.get("agent_name")
    if agent_name in BLOCKED_AGENTS:
        BLOCKED_AGENTS.remove(agent_name)
        AGENT_VIOLATIONS[agent_name] = 0
        print(f"Agent {agent_name} unblocked by admin.")
        return jsonify({"status": "unblocked", "agent": agent_name})
    return jsonify({"status": "error", "message": "Agent not found or not blocked"}), 404

@app.route('/system_status', methods=['GET'])
def system_status():
    return jsonify({
        "blocked_agents": list(BLOCKED_AGENTS),
        "violation_counts": AGENT_VIOLATIONS
    })

if __name__ == '__main__':
    print("Starting MetaGuardian Orchestrator Simulator on port 5000...")
    
    # Mandatory Integration: Authenticate with IBM Cloud
    from ibm_auth import get_access_token
    from ibm_config import ORCHESTRATE_URL
    
    print("--- IBM Watsonx Integration ---")
    token = get_access_token()
    if token:
        print(f"Authenticated with IBM Cloud. Token acquired.")
        print(f"Linked to Orchestrate Instance: {ORCHESTRATE_URL}")
    else:
        print("Warning: IBM Cloud Authentication Failed. Running in offline mode.")
    print("-------------------------------")

    app.run(port=5000, debug=True)
