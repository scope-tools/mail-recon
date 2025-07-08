import re
import requests
import hashlib

def check_phone_privacy(phone_number: str):
    """
    Phone number privacy and intelligence analysis.
    Returns a dict with privacy analysis results.
    """
    # Normalize phone number
    normalized = re.sub(r'[^\d+]', '', phone_number)
    if not normalized:
        return {"error": "Invalid phone number format"}
    
    # Basic validation
    if len(normalized) < 10:
        return {"error": "Phone number too short"}
    
    result = {
        "original": phone_number,
        "normalized": normalized,
        "privacy_risks": [],
        "carrier_info": None,
        "disposable": False,
        "spam_score": 0
    }
    
    # Check for known spam/scam patterns
    spam_patterns = [
        r'^(\+1)?8(00|44|55|66|77|88)\d{7}$',  # Toll-free numbers
        r'^(\+1)?9(00|07)\d{7}$',  # Premium rate numbers
    ]
    
    for pattern in spam_patterns:
        if re.match(pattern, normalized):
            result["privacy_risks"].append("Premium or toll-free number")
            result["spam_score"] += 30
    
    # Check length patterns for different countries/regions
    country_info = analyze_country_code(normalized)
    result.update(country_info)
    
    # Check for sequential or repetitive numbers (privacy risk indicators)
    if has_sequential_digits(normalized):
        result["privacy_risks"].append("Sequential digit pattern detected")
        result["spam_score"] += 20
    
    if has_repetitive_digits(normalized):
        result["privacy_risks"].append("Repetitive digit pattern detected")
        result["spam_score"] += 15
    
    # Check against known VoIP/disposable providers (basic patterns)
    if is_likely_voip(normalized):
        result["disposable"] = True
        result["privacy_risks"].append("Likely VoIP/disposable number")
        result["spam_score"] += 25
    
    # Overall privacy assessment
    if result["spam_score"] > 50:
        result["privacy_assessment"] = "high_risk"
    elif result["spam_score"] > 25:
        result["privacy_assessment"] = "medium_risk"
    else:
        result["privacy_assessment"] = "low_risk"
    
    return result

def analyze_country_code(phone_number: str):
    """Analyze country code and provide basic location info."""
    country_codes = {
        "+1": {"country": "US/Canada", "length_range": [11, 11]},
        "+44": {"country": "United Kingdom", "length_range": [11, 13]},
        "+49": {"country": "Germany", "length_range": [11, 12]},
        "+33": {"country": "France", "length_range": [10, 10]},
        "+86": {"country": "China", "length_range": [11, 13]},
        "+91": {"country": "India", "length_range": [10, 12]},
        "+81": {"country": "Japan", "length_range": [10, 11]},
        "+7": {"country": "Russia", "length_range": [10, 11]},
    }
    
    for code, info in country_codes.items():
        if phone_number.startswith(code):
            return {
                "country_code": code,
                "country": info["country"],
                "expected_length": info["length_range"]
            }
    
    # Default for numbers without country code (assume US)
    if phone_number.startswith("+"):
        return {"country_code": "unknown", "country": "Unknown"}
    else:
        return {"country_code": "+1", "country": "US (assumed)", "expected_length": [10, 10]}

def has_sequential_digits(phone_number: str):
    """Check for sequential digit patterns."""
    digits = re.sub(r'[^\d]', '', phone_number)
    for i in range(len(digits) - 3):
        if digits[i:i+4] in ['0123', '1234', '2345', '3456', '4567', '5678', '6789']:
            return True
        if digits[i:i+4] in ['9876', '8765', '7654', '6543', '5432', '4321', '3210']:
            return True
    return False

def has_repetitive_digits(phone_number: str):
    """Check for repetitive digit patterns."""
    digits = re.sub(r'[^\d]', '', phone_number)
    for i in range(len(digits) - 3):
        if len(set(digits[i:i+4])) <= 2:  # 4 digits with 2 or fewer unique chars
            return True
    return False

def is_likely_voip(phone_number: str):
    """Basic check for VoIP/disposable number patterns."""
    # This is a simplified check - in practice you'd use a comprehensive database
    voip_area_codes = ['555', '800', '844', '855', '866', '877', '888']
    digits = re.sub(r'[^\d]', '', phone_number)
    
    if len(digits) >= 10:
        area_code = digits[-10:-7]  # Get area code from 10-digit format
        return area_code in voip_area_codes
    
    return False

def generate_phone_hash(phone_number: str):
    """Generate a privacy-safe hash of the phone number for lookup purposes."""
    normalized = re.sub(r'[^\d+]', '', phone_number)
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]