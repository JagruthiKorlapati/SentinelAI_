from .base import BaseAgent


class BusinessContinuityAgent(BaseAgent):
    name = "Business Continuity"
    rules = {
        "RANSOMWARE": ("KEEP_UNAFFECTED_SERVICES_ONLINE", 86, "Contain the damage to {target} while other services keep serving customers."),
        "PAYMENT_SERVER_FAILURE": ("SWITCH_TO_BACKUP", 92, "Fail over transactions to the backup system so payments continue."),
        "DDOS": ("MAINTAIN_SERVICE", 85, "Use rate limiting and scaling so customers can still reach {target}."),
        "MALWARE": ("KEEP_UNAFFECTED_SERVICES_ONLINE", 80, "Keep clean systems running while {target} is cleaned."),
        "DATA_EXFILTRATION": ("KEEP_UNAFFECTED_SERVICES_ONLINE", 72, "Limit disruption; only restrict the compromised path on {target}."),
        "DATA_LOSS": ("SWITCH_TO_BACKUP", 78, "Serve users from a replica or backup while {target} is recovered."),
        "PHISHING": ("KEEP_UNAFFECTED_SERVICES_ONLINE", 75, "Keep business running; only reset credentials of affected users on {target}."),
        "SQL_INJECTION": ("SWITCH_TO_READ_ONLY_MODE", 84, "Run {target} in read-only mode so customers can still browse while it is secured."),
        "BRUTE_FORCE": ("MAINTAIN_SERVICE", 78, "Keep {target} available for real users while attack traffic is rate-limited."),
        "INSIDER_THREAT": ("KEEP_UNAFFECTED_SERVICES_ONLINE", 74, "Restrict only the suspect's access; other staff and services on {target} continue."),
    }