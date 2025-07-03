````markdown
# MailRecon

MailRecon is a lightweight email and domain profiling tool designed for inbox safety, OSINT workflows, and digital threat awareness. It runs passive lookups on email addresses and their domains using public data sources, then outputs a risk-rated report in PDF and JSON format.

Runs locally. No cloud. No data collection.

## Features

- Free breach lookup via BreachDirectory (breachdirectory.org)  
  may return “service denied” (403) under heavy use

- EmailRep.io reputation checks (requires API key)

- Gravatar presence detection (public profile image)

- Whois and domain age lookup

- DNS A and MX record resolution

- AbuseIPDB scoring (requires API key)

- DNSBL blacklist checks against:  
  - zen.spamhaus.org  
  - bl.spamcop.net  
  - b.barracudacentral.org  

## Installation

Clone the repository and install dependencies

```bash
git clone https://github.com/scope-tools/mail-recon.git
cd mail-recon
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
````

## Usage

To scan an email address and generate a full report

```bash
python3 main.py --email someone@example.com
```

Example output

```text
[+] Scan complete for someone@example.com

BreachDirectory: 2 breaches
  • Adobe
  • LinkedIn

EmailRep reput.: low
Gravatar: False
Whois: created 1995-08-14 (10915 days ago)
A records: 23.215.0.136, …
AbuseIPDB score: 7%

Blacklist hits:
  - zen.spamhaus.org: False
  - bl.spamcop.net: False
  - b.barracudacentral.org: False

Reports generated:
- JSON: reports/someone_at_example_com_report.json
- PDF:  reports/someone_at_example_com_report.pdf
```

## Configuration (API Keys)

Create a file at `config/keys.json` containing only the keys you have:

```json
{
  "emailrep_key": "YOUR_EMAILREP_KEY",
  "abuseipdb_key": "YOUR_ABUSEIPDB_KEY"
}
```

No key is required for BreachDirectory or blacklist checks. If a key is missing, that feature is skipped or reports an error.

## Reports

JSON report saved as `reports/<email>_report.json`
PDF report saved as `reports/<email>_report.pdf`

## Roadmap

- Manual scanning with PDF and JSON output
- BreachDirectory free breach lookup
- EmailRep and AbuseIPDB API integrations
- Gravatar, Whois, DNS and DNSBL checks
- Gmail inbox auto-scanning (OAuth)
- Phone number intelligence module
- LLM-powered summaries via Ollama

## Privacy

Scans run fully offline
No telemetry, logging or cloud processing
API keys used only if configured
All reports saved locally

## License

MIT License — see `LICENSE`

## Maintainer

Built and maintained by scope-tools ([https://github.com/scope-tools](https://github.com/scope-tools))
Pull requests, issues and feature suggestions are welcome.

```
```
