import hashlib
import requests

GRAVATAR_BASE = "https://www.gravatar.com/avatar/"

def check_gravatar(email: str):
    h = hashlib.md5(email.strip().lower().encode("utf-8")).hexdigest()
    url = f"{GRAVATAR_BASE}{h}?d=404"
    resp = requests.get(url)
    return {"has_gravatar": resp.status_code != 404}
