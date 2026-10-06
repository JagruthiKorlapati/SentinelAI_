from .base import BaseAgent


class BackupAgent(BaseAgent):
    name = "Backup"
    rules = {
        "RANSOMWARE": ("COMPLETE_BACKUP", 85, "Make sure a clean, complete backup of {target} exists before any recovery attempt."),
        "DATA_LOSS": ("RESTORE_BACKUP", 90, "Restore {target} from the latest verified backup to recover lost data."),
        "MALWARE": ("VERIFY_BACKUP", 82, "Verify that backups of {target} are not infected before relying on them."),
        "DATA_EXFILTRATION": ("VERIFY_BACKUP", 68, "Confirm backups of {target} are intact and access to them is secured."),
        "DDOS": ("VERIFY_BACKUP", 60, "DDoS rarely destroys data, but confirm {target} backups are healthy."),
        "PAYMENT_SERVER_FAILURE": ("RESTORE_BACKUP", 80, "Be ready to restore {target} from backup if repair fails."),
        "PHISHING": ("VERIFY_BACKUP", 65, "Confirm {target} backups are clean in case the phishing led to a compromise."),
        "SQL_INJECTION": ("VERIFY_BACKUP", 82, "Check {target} backups to confirm data was not tampered with before the attack."),
        "BRUTE_FORCE": ("VERIFY_BACKUP", 62, "Ensure {target} backups are intact and their access credentials are changed."),
        "INSIDER_THREAT": ("RESTRICT_BACKUP_ACCESS", 80, "Limit access to {target} backups so an insider cannot delete or copy them."),
    }