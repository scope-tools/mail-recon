import requests

BD_API_URL = "https://breachdirectory.org/api"

def check_breachdirectory(email: str):
    """
    Free breach lookup via BreachDirectory.
    Returns a dict with 'breaches' list and optional 'error'.
    """
    try:
        resp = requests.get(BD_API_URL, params={"email": email}, timeout=10)
    except Exception as e:
        return {"breaches": [], "error": f"Request failed: {e}"}

    if resp.status_code == 403:
        return {"breaches": [], "error": "BreachDirectory forbade the request (403)"}
    if resp.status_code != 200:
        return {"breaches": [], "error": f"HTTP {resp.status_code}"}

    data = resp.json().get("response", [])
    return {"breaches": data}
