import dns.resolver

BLACKLISTS = [
    "zen.spamhaus.org",
    "bl.spamcop.net",
    "b.barracudacentral.org",
]

def check_blacklists(ip: str):
    """
    Check an IP address against a set of DNSBL zones.
    Returns a dict mapping zone → True/False/"error: …"
    """
    results = {}
    if not ip:
        return results
    for zone in BLACKLISTS:
        query = ".".join(reversed(ip.split("."))) + f".{zone}"
        try:
            dns.resolver.resolve(query, "A")
            results[zone] = True
        except dns.resolver.NXDOMAIN:
            results[zone] = False
        except Exception as e:
            results[zone] = f"error: {e}"
    return results
