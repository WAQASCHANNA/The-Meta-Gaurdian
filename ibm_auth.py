import requests
from ibm_config import API_KEY

IAM_URL = "https://iam.cloud.ibm.com/identity/token"

def get_access_token():
    if not API_KEY:
        raise ValueError("API Key not found in configuration.")
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }
    
    try:
        response = requests.post(IAM_URL, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Authentication Failed: {e}")
        if response:
            print(f"Response: {response.text}")
        return None
