from .base import BaseAgent


class ThreatDetectionAgent(BaseAgent):
    name = "Threat Detection"
    rules = {
        "RANSOMWARE": ("ISOLATE_SERVER", 90, "Active ransomware on {target} can encrypt and spread to connected systems."),
        "MALWARE": ("ISOLATE_SERVER", 86, "Malware on {target} may spread laterally or open a backdoor."),
        "DDOS": ("BLOCK_TRAFFIC", 88, "Malicious traffic flood against {target} must be filtered at the edge."),
        "DATA_EXFILTRATION": ("BLOCK_TRANSFER", 89, "Data is leaving {target}; outbound transfer must be stopped immediately."),
        "DATA_LOSS": ("ISOLATE_SERVER", 72, "Isolate {target} to stop further data damage while the cause is found."),
        "PAYMENT_SERVER_FAILURE": ("INVESTIGATE_ALERTS", 70, "Check whether the {target} failure is caused by an attack."),
        "PHISHING": ("QUARANTINE_EMAILS", 86, "Malicious emails hitting {target} must be quarantined and affected credentials reset."),
        "SQL_INJECTION": ("BLOCK_MALICIOUS_REQUESTS", 90, "Injection attempts against {target} must be blocked at the firewall or WAF."),
        "BRUTE_FORCE": ("LOCK_ACCOUNTS_AND_BLOCK_IP", 88, "Repeated login attempts on {target} should trigger account lockout and IP blocking."),
        "INSIDER_THREAT": ("REVOKE_ACCESS", 87, "Suspicious internal activity on {target}; revoke the user's access immediately."),
    }