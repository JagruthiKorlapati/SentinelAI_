from pathlib import Path

import yaml

from governance.constants import PRESERVE_EVIDENCE

# policies/ folder sits two levels above this file
POLICY_DIR = Path(__file__).resolve().parents[2] / "policies"

SENSITIVITY_ORDER = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


def _load(filename):
    with open(POLICY_DIR / filename, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_policies():
    """Read all policy files. Editing a YAML file changes behaviour, no code edits needed."""
    return {
        "policies": _load("policies.yaml"),
        "sensitivity": _load("sensitivity.yaml"),
        "authority": _load("authority.yaml"),
    }


def evaluate_policy(agent_outputs, incident, config=None):
    """
    Check every recommended action against the mandatory policies.
    Returns {"hard_block": bool, "requires_approval": bool, "violations": [...]}.
    """
    cfg = config or load_policies()
    pol = cfg["policies"]

    hard_block_actions = set(pol.get("hard_block_actions", []))
    approval_actions = set(pol.get("requires_approval_actions", []))
    approval_by_asset = pol.get("requires_approval_if_asset_criticality", {})
    evidence_required = set(pol.get("evidence_required_before", []))

    criticality = incident.get("asset_criticality", "LOW")
    evidence_planned = any(o["action"] == PRESERVE_EVIDENCE for o in agent_outputs)

    hard_block = False
    requires_approval = False
    violations = []

    for out in agent_outputs:
        action = out["action"]
        agent = out["agent"]

        if action in hard_block_actions:
            hard_block = True
            violations.append({
                "rule": "HARD_BLOCK", "agent": agent, "action": action,
                "detail": f"{action} is blocked by mandatory policy",
            })

        if action in approval_actions:
            requires_approval = True
            violations.append({
                "rule": "APPROVAL_REQUIRED", "agent": agent, "action": action,
                "detail": f"{action} needs human approval",
            })

        if criticality in approval_by_asset.get(action, []):
            requires_approval = True
            violations.append({
                "rule": "APPROVAL_REQUIRED_CRITICAL_ASSET", "agent": agent, "action": action,
                "detail": f"{action} on a {criticality} asset needs human approval",
            })

        if action in evidence_required and not evidence_planned:
            violations.append({
                "rule": "EVIDENCE_REQUIRED", "agent": agent, "action": action,
                "detail": f"{action} needs evidence preserved first",
            })

    return {
        "hard_block": hard_block,
        "requires_approval": requires_approval,
        "violations": violations,
    }


def action_sensitivity(agent_outputs, config=None):
    """Highest sensitivity among all recommended actions (LOW..CRITICAL)."""
    cfg = config or load_policies()
    table = cfg["sensitivity"]
    levels = [table.get(o["action"], "MEDIUM") for o in agent_outputs]
    return max(levels, key=SENSITIVITY_ORDER.index)