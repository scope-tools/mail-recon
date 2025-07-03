import argparse
from api_keys import load_api_keys
from scanners.breachdirectory import check_breachdirectory
from scanners.emailrep import check_emailrep
from scanners.gravatar import check_gravatar
from scanners.whois_lookup import check_whois
from scanners.dns_check import check_dns
from scanners.abuseipdb import check_abuseipdb
from scanners.blacklist_check import check_blacklists
from utils.report_writer import save_json_report, save_pdf_report

def run_scan(email, keys):
    domain = email.split("@")[1]
    report = {}

    # 1) BreachDirectory
    bd = check_breachdirectory(email)
    report["breaches"] = bd.get("breaches", [])
    report["breachdirectory_error"] = bd.get("error")

    # 2) EmailRep
    er = check_emailrep(email, keys.get("emailrep_key"))
    report.update({
        "reputation": er.get("reputation"),
        "disposable": er.get("disposable"),
        "badges": er.get("badges", []),
        "emailrep_error": er.get("error")
    })

    # 3) Gravatar
    grav = check_gravatar(email)
    report["has_gravatar"] = grav["has_gravatar"]

    # 4) Whois
    who = check_whois(domain)
    report["whois"] = who

    # 5) DNS
    dnsr = check_dns(domain)
    report["dns"] = dnsr

    # 6) AbuseIPDB
    ip = dnsr.get("a", [None])[0]
    abuse = check_abuseipdb(ip, keys.get("abuseipdb_key")) if ip else {"error": "No IP"}
    report["abuseipdb"] = abuse

    # 7) DNSBL blacklist checks
    bl = check_blacklists(ip)
    report["blacklists"] = bl

    # Save reports
    json_path = save_json_report(email, report)
    pdf_path = save_pdf_report(email, report)

    # Print summary
    print(f"[+] Scan complete for {email}\n")
    print(f"BreachDirectory: {len(report['breaches'])} breaches" +
          (f" (error: {report['breachdirectory_error']})" if report['breachdirectory_error'] else ""))
    print(f"EmailRep reput.: {report['reputation']} (error: {report['emailrep_error']})")
    print(f"Gravatar: {report['has_gravatar']}")
    print(f"Whois: created {who.get('creation_date')} ({who.get('age_days')}d ago)")
    print(f"A records: {', '.join(dnsr['a']) or 'None'}")
    print(f"AbuseIPDB score: {abuse.get('abuseConfidenceScore', 'N/A')}%\n")
    print("Blacklist hits:")
    for zone, hit in bl.items():
        print(f"  - {zone}: {hit}")
    print(f"\nReports generated:\n- JSON: {json_path}\n- PDF:  {pdf_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MailRecon - Email threat profiler")
    parser.add_argument("--email", required=True, help="Email address to scan")
    args = parser.parse_args()

    keys = load_api_keys()
    run_scan(args.email, keys)
