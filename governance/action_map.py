"""Translate M1's agent vocabulary into the governance vocabulary (constants.py)."""
from governance.constants import (
    ISOLATE, PRESERVE_EVIDENCE, COMPLETE_BACKUP, KEEP_ONLINE, MONITOR, UNKNOWN,
    TARGETED_BLOCK,
)
ACTION_MAP = {
        # Threat Detection
    "ISOLATE_SERVER": ISOLATE,
    "BLOCK_TRAFFIC": TARGETED_BLOCK,
    "BLOCK_TRANSFER": TARGETED_BLOCK,
    "BLOCK_MALICIOUS_REQUESTS": TARGETED_BLOCK,
    "LOCK_ACCOUNTS_AND_BLOCK_IP": TARGETED_BLOCK,
    "REVOKE_ACCESS": TARGETED_BLOCK,
    "QUARANTINE_EMAILS": TARGETED_BLOCK,
    "INVESTIGATE_ALERTS": MONITOR,
    # Forensics
    "PRESERVE_EVIDENCE": PRESERVE_EVIDENCE,
    "COLLECT_LOGS": PRESERVE_EVIDENCE,
    # Backup
    "COMPLETE_BACKUP": COMPLETE_BACKUP,
    "VERIFY_BACKUP": COMPLETE_BACKUP,
    "RESTORE_BACKUP": COMPLETE_BACKUP,
    "RESTRICT_BACKUP_ACCESS": COMPLETE_BACKUP,
    # Business Continuity
    "KEEP_UNAFFECTED_SERVICES_ONLINE": KEEP_ONLINE,
    "MAINTAIN_SERVICE": KEEP_ONLINE,
    "SWITCH_TO_BACKUP": KEEP_ONLINE,
    "SWITCH_TO_READ_ONLY_MODE": KEEP_ONLINE,
    # Fallback used by M1's agents
    "ESCALATE_TO_ANALYST": UNKNOWN,
}


def map_action(m1_action: str) -> str:
    """Unknown strings become UNKNOWN instead of crashing."""
    return ACTION_MAP.get(m1_action, UNKNOWN)


def map_agent_name(name: str) -> str:
    """'Threat Detection' -> 'ThreatDetection'."""
    return name.replace(" ", "")