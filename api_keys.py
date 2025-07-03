import json
import os

def load_api_keys():
    """
    Load API keys from config/keys.json.
    Returns a dict with any keys found, or an empty dict if the file is missing or invalid.
    """
    key_path = os.path.join("config", "keys.json")
    if not os.path.exists(key_path):
        print("[!] Warning: config/keys.json not found. API-dependent features will be skipped.")
        return {}

    try:
        with open(key_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("[!] Error: config/keys.json contains invalid JSON.")
        return {}
