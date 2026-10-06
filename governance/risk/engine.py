from pathlib import Path

import yaml

POLICY_DIR = Path(__file__).resolve().parents[2] / "policies"

FACTORS = [
    "threat_severity", "business_impact", "policy_severity",
    "action_sensitivity", "uncertainty", "agent_disagreement",
]


def _load(filename):
    with open(POLICY_DIR / filename, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_risk_config():
    cfg = {}
    cfg.update(_load("risk_weights.yaml"))
    cfg.update(_load("risk_factors.yaml"))
    total = sum(cfg["weights"].values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Risk weights must sum to 1.0, got {total}")
    return cfg


def _policy_value(policy_results, cfg):
    s = cfg["policy_scores"]
    if policy_results["hard_block"]:
        return s["hard_block"]
    if policy_results["requires_approval"]:
        return s["requires_approval"]
    if policy_results["violations"]:
        return s["violations_only"]
    return s["none"]


def _band(score, bands):
    for level, upper in bands.items():  # LOW, MEDIUM, HIGH, CRITICAL in file order
        if score <= upper:
            return level
    return list(bands)[-1]


def _round_to_total(raw, total):
    """Whole-number contributions that add up exactly to the total."""
    floors = {k: int(v) for k, v in raw.items()}
    remainder = total - sum(floors.values())
    by_fraction = sorted(raw, key=lambda k: raw[k] - floors[k], reverse=True)
    for k in by_fraction[:remainder]:
        floors[k] += 1
    return floors


def compute_risk(agent_outputs, incident, policy_results, sensitivity, conflict, config=None):
    """
    Returns {"risk_score": int, "risk_level": str, "breakdown": {factor: {...}}}.
    `sensitivity` comes from action_sensitivity(); `conflict` comes from detect_conflicts().
    """
    cfg = config or load_risk_config()
    lv = cfg["level_scores"]
    w = cfg["weights"]

    avg_conf = sum(o["confidence"] for o in agent_outputs) / len(agent_outputs)
    n_types = min(len(conflict["conflict_types"]), 4)

    values = {
        "threat_severity": lv[incident["severity"]],
        "business_impact": lv[incident["asset_criticality"]],
        "policy_severity": _policy_value(policy_results, cfg),
        "action_sensitivity": lv[sensitivity],
        "uncertainty": round(100 * (1 - avg_conf), 2),
        "agent_disagreement": cfg["disagreement_scores"][n_types],
    }

    raw = {f: w[f] * values[f] for f in FACTORS}
    score = int(sum(raw.values()) + 0.5)
    score = max(0, min(100, score))
    contributions = _round_to_total(raw, score)

    breakdown = {
        f: {"value": values[f], "weight": w[f], "contribution": contributions[f]}
        for f in FACTORS
    }
    return {
        "risk_score": score,
        "risk_level": _band(score, cfg["bands"]),
        "breakdown": breakdown,
    }