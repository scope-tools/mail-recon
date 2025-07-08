import argparse
from api_keys import load_api_keys
from scanners.breachdirectory import check_breachdirectory
from scanners.emailrep import check_emailrep
from scanners.gravatar import check_gravatar
from scanners.whois_lookup import check_whois
from scanners.dns_check import check_dns
from scanners.abuseipdb import check_abuseipdb
from scanners.blacklist_check import check_blacklists
from scanners.phone_intel import check_phone_privacy
from utils.report_writer import save_json_report, save_pdf_report

def run_email_scan(email, keys):
    """Run comprehensive email privacy and security scan."""
    domain = email.split("@")[1]
    report = {"scan_type": "email"}

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

    return report

def run_phone_scan(phone_number):
    """Run comprehensive phone number privacy analysis."""
    report = {"scan_type": "phone"}
    
    # Phone privacy analysis
    phone_intel = check_phone_privacy(phone_number)
    report["phone_analysis"] = phone_intel
    
    return report

def print_email_summary(email, report):
    """Print summary for email scan results."""
    print(f"[+] Email scan complete for {email}\n")
    print(f"BreachDirectory: {len(report['breaches'])} breaches" +
          (f" (error: {report['breachdirectory_error']})" if report['breachdirectory_error'] else ""))
    print(f"EmailRep reput.: {report['reputation']} (error: {report['emailrep_error']})")
    print(f"Gravatar: {report['has_gravatar']}")
    who = report["whois"]
    print(f"Whois: created {who.get('creation_date')} ({who.get('age_days')}d ago)")
    dnsr = report["dns"]
    print(f"A records: {', '.join(dnsr['a']) or 'None'}")
    abuse = report["abuseipdb"]
    print(f"AbuseIPDB score: {abuse.get('abuseConfidenceScore', 'N/A')}%\n")
    print("Blacklist hits:")
    bl = report["blacklists"]
    for zone, hit in bl.items():
        print(f"  - {zone}: {hit}")

def print_phone_summary(phone_number, report):
    """Print summary for phone scan results."""
    phone_data = report["phone_analysis"]
    print(f"[+] Phone scan complete for {phone_number}\n")
    
    if "error" in phone_data:
        print(f"Error: {phone_data['error']}")
        return
    
    print(f"Normalized: {phone_data['normalized']}")
    print(f"Country: {phone_data.get('country', 'Unknown')}")
    print(f"Privacy Assessment: {phone_data['privacy_assessment']}")
    print(f"Spam Score: {phone_data['spam_score']}/100")
    print(f"Disposable/VoIP: {phone_data['disposable']}")
    
    if phone_data['privacy_risks']:
        print("\nPrivacy Risks:")
        for risk in phone_data['privacy_risks']:
            print(f"  - {risk}")
    else:
        print("\nNo significant privacy risks detected.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MailRecon - Email & Phone Privacy Tool")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--email", help="Email address to scan")
    group.add_argument("--phone", help="Phone number to analyze")
    args = parser.parse_args()

    keys = load_api_keys()
    
    if args.email:
        report = run_email_scan(args.email, keys)
        
        # Save reports
        json_path = save_json_report(args.email, report)
        pdf_path = save_pdf_report(args.email, report)
        
        # Print summary
        print_email_summary(args.email, report)
        print(f"\nReports generated:\n- JSON: {json_path}\n- PDF:  {pdf_path}")
        
    elif args.phone:
        report = run_phone_scan(args.phone)
        
        # Save reports
        phone_safe = args.phone.replace("+", "plus").replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")
        json_path = save_json_report(f"phone_{phone_safe}", report)
        pdf_path = save_pdf_report(f"phone_{phone_safe}", report)
        
        # Print summary
        print_phone_summary(args.phone, report)
        print(f"\nReports generated:\n- JSON: {json_path}\n- PDF:  {pdf_path}")
