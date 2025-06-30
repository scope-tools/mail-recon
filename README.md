# MailRecon

MailRecon is a lightweight email and domain profiling tool designed for inbox safety, OSINT workflows, and digital threat awareness. It runs passive lookups on email addresses and their domains using public data sources, then outputs a risk-rated report in PDF and JSON format.

Runs locally. No cloud. No data collection.

---

## Features

Email analysis:
- Breach history using HaveIBeenPwned
- Email reputation lookup via EmailRep.io
- Gravatar presence check (public profile image)
- Username footprinting (e.g. GitHub)

Domain and sender analysis:
- Whois data (registrar, creation date, privacy)
- DNS and MX record check
- Domain age detection
- Spam and abuse blacklist check (via AbuseIPDB)

Output:
- PDF report with threat summary and risk score
- JSON report for automation and scripting

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/scope-tools/mail-recon.git
cd mail-recon
pip install -r requirements.txt
```

---

## Usage

To scan an email address and generate a full report:

```bash
python main.py --email someone@example.com
```

Output files will be saved to the `reports/` directory as:

- `someone_example_com_report.pdf`
- `someone_example_com_report.json`

---

### Configuration (API Keys)

To enable breach and risk data, create a file at `config/keys.json` and add your API keys:

```json
{
  "hibp_key": "your-haveibeenpwned-api-key",
  "emailrep_key": "your-emailrep-api-key",
  "abuseipdb_key": "your-abuseipdb-api-key"
}
```

API key sources:

- HIBP: [https://haveibeenpwned.com/API/Key](https://haveibeenpwned.com/API/Key)
- EmailRep: [https://emailrep.io](https://emailrep.io)
- AbuseIPDB: [https://www.abuseipdb.com](https://www.abuseipdb.com)

If a key is missing, that feature will be skipped automatically.

---

### Example

```bash
python main.py --email ceo@trustme.click
```

This runs:

- Email breach and reputation checks
- Domain age and whois lookup
- MX record presence
- DNS blacklist scans

Sample result:

- Breach status: Found in 3 public breaches
- Reputation: Suspicious (disposable email service)
- Domain age: 11 days
- Blacklist: Flagged on AbuseIPDB
- Score: 🔴 Risky

---

## Roadmap

- [x] Basic scanning with PDF and JSON output
- [x] Support for EmailRep, AbuseIPDB, and HIBP APIs
- [ ] Gmail inbox scanning (OAuth only)
- [ ] Terminal UI and GUI version
- [ ] Phone number lookup module
- [ ] Self-updating threat definitions

---

## Privacy

- Scans run locally and offline
- No telemetry, logging, or cloud processing
- Optional APIs are used only if configured by the user
- All reports are stored on your device

---

## License

MIT License — see `LICENSE`

---

## Maintainer

Built and maintained by [scope-tools](https://github.com/scope-tools)
Pull requests, issues, and feature suggestions are welcome.

```


```



