import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def save_json_report(email, data):
    fname = email.replace("@", "_at_").replace(".", "_") + "_report.json"
    path = os.path.join("reports", fname)
    os.makedirs("reports", exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path

def save_pdf_report(email, data):
    fname = email.replace("@", "_at_").replace(".", "_") + "_report.pdf"
    path = os.path.join("reports", fname)
    os.makedirs("reports", exist_ok=True)
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"MailRecon Report for {email}")
    y -= 30

    c.setFont("Helvetica", 12)
    for section, results in data.items():
        c.drawString(50, y, section + ":")
        y -= 20
        if isinstance(results, list):
            for item in results:
                c.drawString(70, y, f"• {item}")
                y -= 15
        elif isinstance(results, dict):
            for k, v in results.items():
                c.drawString(70, y, f"{k}: {v}")
                y -= 15
        else:
            c.drawString(70, y, str(results))
            y -= 15
        y -= 10
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    return path
