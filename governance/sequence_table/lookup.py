from pathlib import Path

import yaml

from governance.constants import PRESERVE_EVIDENCE
from governance.policy.engine import load_policies

SEQ_FILE = Path(__file__).resolve().parents[2] / "policies" / "sequences.yaml"


def load_sequences():
    with open(SEQ_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _first_policy_failure(steps, incident, cfg, step_actions):
    """Return a reason string if any step breaks policy, else None."""
    pol = cfg["policies"]
    hard_block = set(pol.get("hard_block_actions", []))
    approval = set(pol.get("requires_approval_actions", []))
    approval_by_asset = pol.get("requires_approval_if_asset_criticality", {})
    evidence_required = set(pol.get("evidence_required_before", []))
    criticality = incident.get("asset_criticality", "LOW")

    seen_actions = []
    for step in steps:
        action = step_actions.get(step)
        if action is None:
            return f"UNKNOWN_STEP:{step}"
        if action in hard_block:
            return f"HARD_BLOCK:{step}"
        if action in approval:
            return f"APPROVAL_REQUIRED:{step}"
        if criticality in approval_by_asset.get(action, []):
            return f"APPROVAL_REQUIRED_CRITICAL_ASSET:{step}"
        if action in evidence_required and PRESERVE_EVIDENCE not in seen_actions:
            return f"EVIDENCE_NOT_PRESERVED_BEFORE:{step}"
        seen_actions.append(action)
    return None


def find_safe_coordinated_action(conflict_types, incident, config=None, table=None):
    """
    Returns {"safe": bool, "steps": [...], "reason": str}.
    No table entry, or any step failing policy -> safe False (the decision engine
    then falls through to HUMAN_REVIEW).
    """
    cfg = config or load_policies()
    table = table or load_sequences()

    key = "+".join(sorted(conflict_types))
    steps = table["sequences"].get(key)
    if not steps:
        return {"safe": False, "steps": [], "reason": "NO_SAFE_SEQUENCE:NO_TABLE_ENTRY"}

    failure = _first_policy_failure(steps, incident, cfg, table["step_actions"])
    if failure:
        return {"safe": False, "steps": [], "reason": f"NO_SAFE_SEQUENCE:{failure}"}

    return {"safe": True, "steps": list(steps), "reason": f"SEQUENCE_FOUND:{key}"}