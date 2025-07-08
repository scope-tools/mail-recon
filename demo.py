#!/usr/bin/env python3
"""
MailRecon Demo - Email & Phone Privacy Analysis
Demonstrates both email and phone number privacy scanning capabilities.
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def demo_email_analysis():
    """Demonstrate email privacy analysis."""
    print("=" * 60)
    print("📧 EMAIL PRIVACY ANALYSIS DEMO")
    print("=" * 60)
    
    test_emails = [
        "test@example.com",
        "demo@gmail.com"
    ]
    
    for email in test_emails:
        print(f"\n🔍 Analyzing: {email}")
        print("-" * 40)
        
        # Activate virtual environment and run scan
        cmd = f"source .venv/bin/activate && python3 main.py --email {email}"
        output = run_command(cmd)
        
        # Print relevant lines (skip full output for demo)
        lines = output.split('\n')
        for line in lines:
            if any(keyword in line for keyword in ['[+]', 'BreachDirectory:', 'EmailRep', 'Privacy Assessment:', 'Reports generated:']):
                print(line)

def demo_phone_analysis():
    """Demonstrate phone privacy analysis."""
    print("\n" + "=" * 60)
    print("📱 PHONE PRIVACY ANALYSIS DEMO")
    print("=" * 60)
    
    test_phones = [
        "+1-555-123-4567",  # High risk (VoIP, sequential)
        "2025551234",       # Medium risk (sequential)
        "+1-202-867-5309",  # Lower risk
        "8005551234"        # Toll-free (high risk)
    ]
    
    for phone in test_phones:
        print(f"\n🔍 Analyzing: {phone}")
        print("-" * 40)
        
        # Activate virtual environment and run scan
        cmd = f"source .venv/bin/activate && python3 main.py --phone '{phone}'"
        output = run_command(cmd)
        
        # Print relevant lines
        lines = output.split('\n')
        for line in lines:
            if any(keyword in line for keyword in ['[+]', 'Privacy Assessment:', 'Spam Score:', 'Privacy Risks:', 'Reports generated:']):
                print(line)

def show_reports():
    """Show generated report files."""
    print("\n" + "=" * 60)
    print("📊 GENERATED REPORTS")
    print("=" * 60)
    
    if os.path.exists("reports"):
        files = os.listdir("reports")
        if files:
            print("Generated report files:")
            for file in sorted(files):
                print(f"  📄 {file}")
        else:
            print("No reports found.")
    else:
        print("Reports directory not found.")

def main():
    """Run the complete demo."""
    print("🛡️  MAILRECON - PRIVACY ANALYSIS TOOL DEMO")
    print("Email and Phone Privacy Protection")
    print()
    
    # Check if virtual environment exists
    if not os.path.exists(".venv"):
        print("❌ Virtual environment not found. Please run:")
        print("   python3 -m venv .venv")
        print("   source .venv/bin/activate") 
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    try:
        # Run demos
        demo_email_analysis()
        demo_phone_analysis()
        show_reports()
        
        print("\n" + "=" * 60)
        print("✅ DEMO COMPLETE")
        print("=" * 60)
        print("Your privacy analysis reports have been generated in the 'reports/' directory.")
        print("Both JSON and PDF formats are available for detailed analysis.")
        print()
        print("🔒 All analysis runs locally - no data is sent to external services")
        print("   except for the specific API calls configured in your keys.json")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")

if __name__ == "__main__":
    main()