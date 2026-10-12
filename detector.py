import re
from urllib.parse import urlparse

SUSPICIOUS_PHRASES = [
    "verify your account",
    "urgent action required",
    "your account has been suspended",
    "confirm your password",
    "click here immediately",
    "unusual login activity",
    "your account will be closed",
    "update your payment information",
    "you habe won",
    "limited time offer"
]

def analyze_email(email):
    email_lower = email.lower()
    score = 0
    warnings = []

    #check for suspicious phrases
    for phrase in SUSPICIOUS_PHRASES:
        if phrase in email_lower:
            score = score + 10
            warnings.append(f"Suspicious phrase: {phrase}")


    #extract URLs from the email
    urls = re.findall(r'https?://[^\s<>"\']+', email)

    for url in urls:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""

        #check for IP-based links
        if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", hostname):
            score = score + 25
            warnings.append("Link uses an IP address")

        #check for insecure HTTP links
        if parsed.scheme == "http":
            score = score + 10
            warnings.append("Link uses HTPP instead of HTTPS")

    #check for excessive exclamation marks
    if email.count("!") >= 3:
        score = score + 10
        warnings.append("Excessive exclamation marks")

    score = min(score, 100)

    if score >= 60:
        risk = "High Risk"
    elif score >= 30:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    return {
        "score": score,
        "risk": risk,
        "warnings": warnings
    }