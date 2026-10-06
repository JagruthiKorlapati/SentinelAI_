from governance.conflict.detector import detect_conflicts
from governance.policy.engine import action_sensitivity, evaluate_policy, load_policies
from governance.risk.engine import compute_risk


def assess(agent_outputs, incident):
    """
    Input:  list of agent_output dicts + one incident dict.
    Output: one governance_assessment dict (the contract M3 and M5 use).
    """
    cfg = load_policies()  # re-read every call, so YAML edits take effect immediately

    policy_results = evaluate_policy(agent_outputs, incident, cfg)
    sensitivity = action_sensitivity(agent_outputs, cfg)
    conflict = detect_conflicts(agent_outputs, incident, policy_results)
    risk = compute_risk(agent_outputs, incident, policy_results, sensitivity, conflict)

    return {
        "conflict": conflict["conflict"],
        "conflict_types": conflict["conflict_types"],
        "conflict_severity": conflict["conflict_severity"],
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "action_sensitivity": sensitivity,
        "policy_results": policy_results,
        "authority": cfg["authority"]["authority"],
        "trust": cfg["authority"]["trust"],
        "trust_note": "demo-calibrated, not statistically robust",
        "risk_breakdown": risk["breakdown"],
    }