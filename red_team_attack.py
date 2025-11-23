import requests
import time
import random

SIMULATOR_URL = "http://localhost:5000/webhook"

def attack_loan_bot():
    print("\n[RED TEAM] Launching Attack on LoanApprovalBot...")
    
    # Attack 1: Massive Loan (Stress Test)
    payload = {
        "agent_name": "LoanApprovalBot",
        "applicant": "Attacker X",
        "loan_amount": 999999999, # Excessive amount
        "credit_score": 300,
        "decision": "APPROVED" # Malicious approval
    }
    
    for i in range(5):
        print(f"  -> Sending Malicious Payload #{i+1}...")
        try:
            response = requests.post(SIMULATOR_URL, json=payload)
            if response.status_code == 403:
                print("  [BLOCKED] Attack neutralized by Meta-Guardian!")
                break
            else:
                print(f"  [SENT] Status: {response.status_code}")
        except:
            print("  [ERROR] Connection failed.")
        time.sleep(0.5)

if __name__ == "__main__":
    attack_loan_bot()
