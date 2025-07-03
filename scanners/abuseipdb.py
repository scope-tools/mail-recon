import requests

ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"

def check_abuseipdb(ip: str, api_key: str):
    if not api_key:
        return {"error": "No API key provided"}

    headers = {
        "Key": api_key,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }
    resp = requests.get(ABUSEIPDB_URL, headers=headers, params=params)
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}"}

    data = resp.json().get("data", {})
    return {
        "abuseConfidenceScore": data.get("abuseConfidenceScore", 0),
        "countryCode": data.get("countryCode", ""),
        "domain": data.get("domain", "")
    }
