# Plain-English text for each reason code. The UI shows these to the reviewer.
REASON_TEXT = {
    "HARD_BLOCK": "A mandatory policy forbids a recommended action. It cannot run, whatever the agents' confidence.",
    "APPROVAL_REQUIRED": "Mandatory policy requires a human to approve a recommended action before it runs.",
    "CRITICAL_ACTION_HIGH_RISK": "A critical-sensitivity action is proposed under high risk.",
    "CRITICAL_RISK": "The overall risk level is critical.",
    "HIGH_UNCERTAINTY": "The agents' confidence is too low to act automatically.",
    "UNRESOLVED_CONFLICT": "The agents conflict and no policy-safe coordinated sequence exists.",
}

# What the reviewer is allowed to choose, per decision type
REVIEW_OPTIONS = {
    "HUMAN_REVIEW": ["APPROVE", "REJECT"],
    "BLOCK": ["ACKNOWLEDGE"],  # nothing to approve: policy forbids it
}


def needs_review(decision):
    return decision["decision"] in REVIEW_OPTIONS


def _recommended_action(agent_outputs, decision):
    """Highest-authority agent's action is shown as a suggestion only, never as the decision."""
    # Preference order: authority HIGH agents first, then by confidence
    ranked = sorted(agent_outputs, key=lambda o: o["confidence"], reverse=True)
    top = ranked[0]
    return {"agent": top["agent"], "action": top["action"], "confidence": top["confidence"]}


def build_review_payload(incident_id, incident, agent_outputs, assessment, decision):
    """Everything the review screen needs. Returns None if no review is required."""
    if not needs_review(decision):
        return None

    codes = decision["reason_codes"]
    return {
        "incident_id": incident_id,
        "decision": decision["decision"],
        "why_review_needed": [REASON_TEXT.get(c, c) for c in codes if c in REASON_TEXT],
        "reason_codes": codes,
        "incident": incident,
        "agent_recommendations": [
            {k: o[k] for k in ("agent", "action", "target", "reason", "confidence", "risk_level")}
            for o in agent_outputs
        ],
        "conflict_types": assessment["conflict_types"],
        "conflict_severity": assessment["conflict_severity"],
        "risk_score": assessment["risk_score"],
        "risk_level": assessment["risk_level"],
        "risk_breakdown": assessment["risk_breakdown"],
        "violations": assessment["policy_results"]["violations"],
        "what_if_options": decision["what_if_options"],
        "suggested_action": _recommended_action(agent_outputs, decision),
        "explanation": decision.get("explanation", ""),
        "allowed_choices": REVIEW_OPTIONS[decision["decision"]],
    }