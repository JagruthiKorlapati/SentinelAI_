from pathlib import Path

import yaml

from governance.sequence_table.lookup import find_safe_coordinated_action
from governance.what_if.evaluator import evaluate_what_if

RULES_FILE = Path(__file__).resolve().parents[2] / "policies" / "decision_rules.yaml"
LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


def load_decision_rules():
    with open(RULES_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _at_least(level, minimum):
    return LEVELS.index(level) >= LEVELS.index(minimum)


def decide(agent_outputs, incident, assessment, rules=None):
    """
    Returns the decision object: decision, steps, what_if_options, reason_codes,
    plus explanation fields that M1's explanation layer fills in.
    """
    rules = rules or load_decision_rules()
    policy = assessment["policy_results"]
    risk_level = assessment["risk_level"]
    avg_conf = sum(o["confidence"] for o in agent_outputs) / len(agent_outputs)

    def result(decision, codes, steps=None):
        return {
            "decision": decision,
            "steps": steps or [],
            "what_if_options": evaluate_what_if(incident),
            "reason_codes": codes,
            "explanation": "",
            "explanation_source": "pending",
        }

    # 1. Hard policy block always wins
    if policy["hard_block"]:
        return result("BLOCK", ["HARD_BLOCK"])

    # 2. Mandatory approval policy
    if policy["requires_approval"]:
        return result("HUMAN_REVIEW", ["APPROVAL_REQUIRED"])

    # 3. Critical-sensitivity action with high risk
    if (_at_least(assessment["action_sensitivity"], rules["critical_action_sensitivity"])
            and _at_least(risk_level, rules["high_risk_level"])):
        return result("HUMAN_REVIEW", ["CRITICAL_ACTION_HIGH_RISK"])

    # 4. Critical risk level
    if _at_least(risk_level, rules["human_review_min_risk"]):
        return result("HUMAN_REVIEW", ["CRITICAL_RISK"])

    # 5. High uncertainty
    if avg_conf < rules["min_average_confidence"]:
        return result("HUMAN_REVIEW", ["HIGH_UNCERTAINTY"])

    # 6. Conflict: try a safe coordinated sequence, else a human decides
    if assessment["conflict"]:
        seq = find_safe_coordinated_action(assessment["conflict_types"], incident)
        if seq["safe"]:
            return result("CONTROLLED_RESPONSE", ["COORDINATED_SEQUENCE_FOUND", seq["reason"]], seq["steps"])
        return result("HUMAN_REVIEW", ["UNRESOLVED_CONFLICT", seq["reason"]])

    # 6b. Threat types that always need a human, even at low risk
    if incident.get("threat_type") in rules.get("human_review_threats", []):
        return result("HUMAN_REVIEW", ["THREAT_TYPE_NEEDS_HUMAN"])

    # 7. No conflict, low risk
    if not _at_least(risk_level, "MEDIUM") or LEVELS.index(risk_level) <= LEVELS.index(rules["auto_execute_max_risk"]):
        return result("AUTO_EXECUTE", ["AUTO_EXECUTE_LOW_RISK"])

    # 8. No conflict but above low risk: carry out the agreed actions in a controlled way
    agreed = list(dict.fromkeys(o["action"] for o in agent_outputs))
    return result("CONTROLLED_RESPONSE", ["NO_CONFLICT_ELEVATED_RISK"], agreed)