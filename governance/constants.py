# Single source of truth for action names.
# Must match what M1's agents output. Never type these strings by hand elsewhere.

ISOLATE = "ISOLATE"
PRESERVE_EVIDENCE = "PRESERVE_EVIDENCE"
COMPLETE_BACKUP = "COMPLETE_BACKUP"
KEEP_ONLINE = "KEEP_ONLINE"
MONITOR = "MONITOR"
CONTINUE = "CONTINUE"
DELETE_DATA = "DELETE_DATA"
UNKNOWN = "UNKNOWN"

ALL_ACTIONS = {
    ISOLATE, PRESERVE_EVIDENCE, COMPLETE_BACKUP, KEEP_ONLINE,
    MONITOR, CONTINUE, DELETE_DATA, UNKNOWN,
}

AGENTS = ["ThreatDetection", "Forensics", "Backup", "BusinessContinuity"]