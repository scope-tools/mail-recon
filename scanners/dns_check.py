import dns.resolver

def check_dns(domain: str):
    result = {"a": [], "mx": []}
    try:
        for rd in dns.resolver.resolve(domain, "A"):
            result["a"].append(rd.to_text())
    except Exception:
        pass

    try:
        for mx in dns.resolver.resolve(domain, "MX"):
            result["mx"].append(str(mx.exchange).rstrip("."))
    except Exception:
        pass

    return result
