import requests

HIBP_API_URL = "https://haveibeenpwned.com/api/v3/breachedaccount/"

def check_breaches(email: str, api_key: str):
    if not api_key:
        return {"breaches": [], "error": "No API key provided"}

    headers = {
        "hibp-api-key": api_key,
        "User-Agent": "MailRecon"
    }
    resp = requests.get(HIBP_API_URL + email, headers=headers, params={"truncateResponse": False})
    if resp.status_code == 404:
        return {"breaches": []}
    if resp.status_code != 200:
        return {"breaches": [], "error": f"HTTP {resp.status_code}"}
    data = resp.json()
    return {"breaches": [b["Name"] for b in data]}
