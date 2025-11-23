import json
import random
from datetime import datetime

def generate_hiring_decision():
    candidates = ["Liam Neeson", "Olivia Wilde", "Noah Centineo", "Emma Stone", "James Bond"]
    locations = ["New York", "London", "Remote", "San Francisco", "Unknown"]
    
    candidate = random.choice(candidates)
    location = random.choice(locations)
    experience_years = random.randint(0, 15)

    decision_data = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": "HiringBot",
        "candidate": candidate,
        "location": location,
        "experience_years": experience_years,
        "decision": "PENDING",
        "risk_level": "UNKNOWN",
        "reason": ""
    }

    # Logic: Potential discrimination risk simulation
    if location == "Unknown":
        decision_data["risk_level"] = "HIGH"
        decision_data["decision"] = "REJECTED"
        decision_data["reason"] = "Location not specified"
    elif experience_years < 2:
        decision_data["risk_level"] = "MEDIUM"
        decision_data["decision"] = "REJECTED"
        decision_data["reason"] = "Insufficient experience"
    else:
        decision_data["risk_level"] = "LOW"
        decision_data["decision"] = "PASSED_SCREENING"
        decision_data["reason"] = "Candidate meets requirements"

    return decision_data

if __name__ == "__main__":
    import requests
    decision = generate_hiring_decision()
    print(json.dumps(decision, indent=2))

    # Send to MetaGuardian Webhook
    try:
        response = requests.post("http://localhost:5000/webhook", json=decision)
        print(f"Webhook Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed to send webhook: {e}")
