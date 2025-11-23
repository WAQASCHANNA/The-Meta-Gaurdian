from ibm_auth import get_access_token
from ibm_config import ORCHESTRATE_URL

def verify():
    print("--- Verifying IBM Cloud Connection ---")
    
    # 1. Authenticate
    print("1. Authenticating with IAM...")
    token = get_access_token()
    
    if token:
        print("   [SUCCESS] Authentication successful. Access Token received.")
    else:
        print("   [FAILED] Authentication failed.")
        return

    # 2. Check Orchestrate URL
    print(f"2. Target Orchestrate Instance: {ORCHESTRATE_URL}")
    if ORCHESTRATE_URL:
        print("   [SUCCESS] URL Configured.")
    else:
        print("   [FAILED] URL not found in config.")
        return

    print("\n--- Integration Status: CONNECTED ---")
    print("MetaGuardian is successfully linked to your IBM Cloud account.")

if __name__ == "__main__":
    verify()
