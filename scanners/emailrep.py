import requests

EMAILREP_API_URL = "https://emailrep.io/"

def check_emailrep(email: str, api_key: str):
    headers = {
        "User-Agent": "MailRecon"
    }
    if api_key:
        headers["Key"] = api_key

    resp = requests.get(EMAILREP_API_URL + email, headers=headers)
    if resp.status_code == 429:
        return {"error": "Rate limited by EmailRep.io"}
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}"}
    data = resp.json()

    # Pick out a few key fields
    reputation = data.get("reputation", "unknown")
    disposable = data.get("disposable", False)
    badges = data.get("details", {}).get("badges", [])

    return {
        "reputation": reputation,
        "disposable": disposable,
        "badges": badges
    }
