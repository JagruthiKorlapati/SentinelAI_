from pathlib import Path

import yaml

WHAT_IF_FILE = Path(__file__).resolve().parents[2] / "policies" / "what_if.yaml"

# Used if an unknown criticality appears: the most cautious table
FALLBACK_CRITICALITY = "CRITICAL"


def load_what_if():
    with open(WHAT_IF_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def evaluate_what_if(incident, table=None):
    """
    Returns a list of {"option", "security", "evidence", "business", "policy"},
    one per candidate action, using the consequence table for the asset's criticality.
    """
    table = table or load_what_if()
    criticality = incident.get("asset_criticality", FALLBACK_CRITICALITY)
    options = table.get(criticality) or table[FALLBACK_CRITICALITY]

    return [
        {"option": name, **consequences}
        for name, consequences in options.items()
    ]