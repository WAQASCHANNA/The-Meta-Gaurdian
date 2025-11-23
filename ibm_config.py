import json
import os

DATA_FILE = "data.json"

def load_config():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"{DATA_FILE} not found.")
    
    with open(DATA_FILE, "r") as f:
        # The file content is a JSON string inside a string, or just JSON.
        # Based on the view_file output: "{\"apikey\":...}"
        content = f.read().strip()
        
        # Handle double encoding if present (starts and ends with quotes)
        if content.startswith('"') and content.endswith('"'):
            content = json.loads(content) # Decode the outer string
            
        return json.loads(content) # Parse the inner JSON

try:
    config = load_config()
    API_KEY = config.get("apikey")
    ORCHESTRATE_URL = config.get("url")
except Exception as e:
    print(f"Error loading config: {e}")
    API_KEY = None
    ORCHESTRATE_URL = None
