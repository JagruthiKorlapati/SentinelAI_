from .threat_detection import ThreatDetectionAgent
from .forensics import ForensicsAgent
from .backup import BackupAgent
from .business_continuity import BusinessContinuityAgent

ALL_AGENTS = [
    ThreatDetectionAgent(),
    ForensicsAgent(),
    BackupAgent(),
    BusinessContinuityAgent(),
]