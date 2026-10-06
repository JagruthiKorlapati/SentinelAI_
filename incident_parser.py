import re
from itertools import count

_counter = count(1)

# ORDER MATTERS: real attacks first, failure last
ATTACK_KEYWORDS = {
    "RANSOMWARE": ["ransom", "encrypt", "locked files", "files locked"],
    "DATA_EXFILTRATION": ["exfiltrat", "data leak", "data breach", "data theft",
                          "stolen data", "data stolen", "unauthorized transfer"],
    "SQL_INJECTION": ["sql injection", "sqli", "injection attack", "malicious query"],
    "MALWARE": ["malware", "trojan", "virus", "worm", "backdoor", "spyware", "keylogger"],
    "PHISHING": ["phish", "spear", "suspicious email", "fake email", "fake login",
                 "credential harvest"],
    "BRUTE_FORCE": ["brute force", "brute-force", "password spray", "credential stuffing",
                    "failed login", "repeated login", "password guess", "guessing password",
                    "login attempts", "bogus password"],
    "INSIDER_THREAT": ["insider", "employee", "disgruntled", "privilege abuse",
                       "rogue admin", "unauthorized access by"],
    "DDOS": ["ddos", "dos attack", "denial of service", "traffic flood",
             "botnet", "flood"],
    "DATA_LOSS": ["data loss", "deleted", "wiped", "corrupt"],
    "PAYMENT_SERVER_FAILURE": ["payment server down", "payment failure", "payment outage",
                               "payments down", "payment fail", "outage", "is down",
                               "went down", "not working", "unavailable"],
}

TARGET_KEYWORDS = {
    "PAYMENT_SERVER": ["payment"],
    "DATABASE_SERVER": ["database", "db server", "db"],
    "WEB_SERVER": ["web server", "website", "web app", "webapp"],
    "EMAIL_SERVER": ["email", "mail server"],
    "FILE_SERVER": ["file server"],
    "AUTH_SERVER": ["login", "authentication", "auth server", "vpn", "admin panel",
                    "portal", "sso", "password"],
}

DEFAULT_SEVERITY = {
    "RANSOMWARE": "CRITICAL",
    "DATA_EXFILTRATION": "CRITICAL",
    "SQL_INJECTION": "CRITICAL",
    "PAYMENT_SERVER_FAILURE": "CRITICAL",
    "MALWARE": "HIGH",
    "PHISHING": "HIGH",
    "BRUTE_FORCE": "HIGH",
    "INSIDER_THREAT": "HIGH",
    "DDOS": "HIGH",
    "DATA_LOSS": "HIGH",
    "UNKNOWN": "MEDIUM",
}

TARGET_IMPACT = {
    "PAYMENT_SERVER": "HIGH",
    "DATABASE_SERVER": "HIGH",
    "WEB_SERVER": "MEDIUM",
    "EMAIL_SERVER": "MEDIUM",
    "FILE_SERVER": "MEDIUM",
    "AUTH_SERVER": "HIGH",
    "UNKNOWN": "LOW",
}

SEVERITY_WORDS = ["critical", "high", "medium", "low"]


def _has_prefix(text, word):
    """Word-start match: 'encrypt' matches 'encrypted', but 'db' won't match 'feedback'."""
    return re.search(r"\b" + re.escape(word), text) is not None


def _has_word(text, word):
    """Whole-word match: 'low' will NOT match 'slow' or 'allowed'."""
    return re.search(r"\b" + re.escape(word) + r"\b", text) is not None


def _match(text, table, default="UNKNOWN"):
    for label, words in table.items():
        if any(_has_prefix(text, w) for w in words):
            return label
    return default


def parse_incident(text: str) -> dict:
    text = (text or "").strip()
    t = text.lower()

    attack = _match(t, ATTACK_KEYWORDS)
    target = _match(t, TARGET_KEYWORDS)

    severity = next((s.upper() for s in SEVERITY_WORDS if _has_word(t, s)),
                    DEFAULT_SEVERITY[attack])
    impact = TARGET_IMPACT[target]
    if severity == "CRITICAL":  # critical attack = impact at least HIGH
        impact = "HIGH"

    return {
        "incident_id": f"INC-{next(_counter):03d}",
        "attack_type": attack,
        "target": target,
        "severity": severity,
        "business_impact": impact,
        "description": text,
    }