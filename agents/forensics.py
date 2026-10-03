from .base import BaseAgent


class ForensicsAgent(BaseAgent):
    name = "Forensics"
    rules = {
        "RANSOMWARE": ("PRESERVE_EVIDENCE", 87, "Keep disk images and memory of {target} to trace the entry point and ransomware strain."),
        "MALWARE": ("COLLECT_LOGS", 84, "Collect system and network logs from {target} to identify the malware source."),
        "DDOS": ("COLLECT_LOGS", 78, "Traffic logs for {target} help identify attacker IP ranges and attack pattern."),
        "DATA_EXFILTRATION": ("PRESERVE_EVIDENCE", 88, "Preserve transfer logs and artifacts to prove what data left {target}."),
        "DATA_LOSS": ("COLLECT_LOGS", 76, "Audit logs of {target} show who or what deleted or corrupted the data."),
        "PAYMENT_SERVER_FAILURE": ("COLLECT_LOGS", 72, "Gather logs from {target} to find the failure root cause."),
        "PHISHING": ("COLLECT_LOGS", 82, "Collect email headers and click logs for {target} to find who received and opened the message."),
        "SQL_INJECTION": ("PRESERVE_EVIDENCE", 88, "Preserve web and query logs of {target} to prove what the attacker accessed."),
        "BRUTE_FORCE": ("COLLECT_LOGS", 83, "Authentication logs of {target} reveal the attacker's IPs and any successful login."),
        "INSIDER_THREAT": ("PRESERVE_EVIDENCE", 90, "Preserve access logs and user activity on {target} for HR and legal action."),
    }