from pathlib import Path

import yaml

RULES_FILE = Path(__file__).resolve().parents[2] / "policies" / "conflict_rules.yaml"

SEVERITY_LEVELS = ["NONE", "LOW", "MEDIUM", "HIGH"]

# One line per rule. This goes straight onto a slide.
CONFLICT_DEFINITIONS = {
    "ACTION": "Agents recommend actions that cannot both happen (e.g. isolate vs keep online).",
    "PRIORITY": "An urgent action is recommended while others say something must happen first.",
    "POLICY": "A recommended action is blocked by, or needs approval under, mandatory policy.",
    "OBJECTIVE": "A containment-focused agent clashes with an uptime-focused agent.",
}


def load_rules():
    with open(RULES_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _action_conflict(actions, rules):
    return any(a in actions and b in actions for a, b in rules["incompatible_pairs"])


def _priority_conflict(actions, rules):
    p = rules["priority"]
    return bool(actions & set(p["urgent_actions"])) and bool(actions & set(p["prerequisite_actions"]))


def _policy_conflict(policy_results):
    return bool(policy_results["hard_block"] or policy_results["requires_approval"])


def _objective_conflict(agent_outputs, rules):
    obj = rules["objective"]
    roles = obj["agent_objectives"]
    containment = any(
        roles.get(o["agent"]) == "CONTAINMENT" and o["action"] in obj["containment_actions"]
        for o in agent_outputs
    )
    uptime = any(
        roles.get(o["agent"]) == "UPTIME" and o["action"] in obj["uptime_actions"]
        for o in agent_outputs
    )
    return containment and uptime


def _severity(types, incident, policy_results, rules):
    if not types:
        return "NONE"
    level = min(len(types), 3)  # 1 LOW, 2 MEDIUM, 3+ HIGH
    bump_assets = rules["severity"]["bump_if_asset_criticality"]
    if incident.get("asset_criticality") in bump_assets or policy_results["hard_block"]:
        level += 1
    return SEVERITY_LEVELS[min(level, 3)]


def detect_conflicts(agent_outputs, incident, policy_results, rules=None):
    """Returns {"conflict": bool, "conflict_types": [...], "conflict_severity": str}."""
    rules = rules or load_rules()
    actions = {o["action"] for o in agent_outputs}

    types = []
    if _action_conflict(actions, rules):
        types.append("ACTION")
    if _priority_conflict(actions, rules):
        types.append("PRIORITY")
    if _policy_conflict(policy_results):
        types.append("POLICY")
    if _objective_conflict(agent_outputs, rules):
        types.append("OBJECTIVE")

    return {
        "conflict": len(types) > 0,
        "conflict_types": types,
        "conflict_severity": _severity(types, incident, policy_results, rules),
    }