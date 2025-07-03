import whois
from datetime import datetime

def check_whois(domain: str):
    try:
        data = whois.whois(domain)
    except Exception as e:
        return {"error": str(e)}

    cd = data.creation_date
    if isinstance(cd, list):
        cd = cd[0]
    if not isinstance(cd, datetime):
        return {"error": "unable to parse creation date"}

    age_days = (datetime.now() - cd).days
    return {
        "creation_date": cd.strftime("%Y-%m-%d"),
        "age_days": age_days,
        "registrar": data.registrar or "unknown"
    }
