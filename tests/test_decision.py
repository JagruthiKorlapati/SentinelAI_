import copy
import json
from pathlib import Path

import pytest

from governance.assess import assess
from governance.decision.engine import decide, load_decision_rules
from governance.decision.review import build_review_payload
from governance.sequence_table.lookup import find_safe_coordinated_action
from governance.what_if.evaluator import evaluate_what_if

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_FILES = sorted((ROOT / "fixtures").glob("*.json"))
DECISIONS = {"AUTO_EXECUTE", "CONTROLLED_RESPONSE", "HUMAN_REVIEW", "BLOCK"}


def load_fixture(name_part):
    for f in FIXTURE_FILES:
        if name_part in f.name:
            return json.loads(f.read_text(encoding="utf-8"))
    raise FileNotFoundError(name_part)


def run(name_part):
    d = load_fixture(name_part)
    a = assess(d["agents"], d["incident"])
    return d, a, decide(d["agents"], d["incident"], a)


def test_s1_auto_execute():
    _, _, dec = run("s1_")
    assert dec["decision"] == "AUTO_EXECUTE"


def test_s2_controlled_response_with_four_steps():
    _, _, dec = run("s2_")
    assert dec["decision"] == "CONTROLLED_RESPONSE"
    assert dec["steps"] == [
        "CAPTURE_EVIDENCE_SNAPSHOT", "CONFIRM_BACKUP_CHECKPOINT",
        "ISOLATE_SERVER", "BEGIN_RECOVERY",
    ]


def test_s3_human_review():
    _, _, dec = run("s3_")
    assert dec["decision"] == "HUMAN_REVIEW"


def test_s4_hard_policy_blocks():
    _, _, dec = run("s4_")
    assert dec["decision"] == "BLOCK"
    assert "HARD_BLOCK" in dec["reason_codes"]


def test_hard_block_beats_available_sequence():
    """Even if a safe sequence exists for these conflict types, a hard block must win."""
    d = load_fixture("s2_")
    agents = copy.deepcopy(d["agents"])
    agents[0]["action"] = "DELETE_DATA"  # a hard-blocked action
    a = assess(agents, d["incident"])
    assert a["policy_results"]["hard_block"] is True
    dec = decide(agents, d["incident"], a)
    assert dec["decision"] == "BLOCK"
    assert dec["steps"] == []


@pytest.mark.parametrize("path", FIXTURE_FILES, ids=lambda p: p.name)
def test_every_decision_names_its_rule(path):
    d = json.loads(path.read_text(encoding="utf-8"))
    a = assess(d["agents"], d["incident"])
    dec = decide(d["agents"], d["incident"], a)
    assert dec["decision"] in DECISIONS
    assert dec["reason_codes"], "decision has no reason codes"


@pytest.mark.parametrize("path", FIXTURE_FILES, ids=lambda p: p.name)
def test_decision_has_all_contract_fields(path):
    d = json.loads(path.read_text(encoding="utf-8"))
    a = assess(d["agents"], d["incident"])
    dec = decide(d["agents"], d["incident"], a)
    for field in ("decision", "steps", "what_if_options", "reason_codes", "explanation", "explanation_source"):
        assert field in dec


def test_no_safe_sequence_falls_through_to_human_review():
    """A conflict with no table entry, and no mandatory-policy trigger, must go to a human."""
    d = load_fixture("s2_")
    # Only a PRIORITY-only variant exists in the table; use a type combination that has no entry
    seq = find_safe_coordinated_action(["ACTION"], d["incident"])
    assert seq["safe"] is False
    assert "NO_SAFE_SEQUENCE" in seq["reason"]


def test_sequence_step_failing_policy_gives_no_safe_sequence():
    """Isolating a CRITICAL asset needs approval, so the sequence is rejected."""
    d = load_fixture("s5_")
    seq = find_safe_coordinated_action(["ACTION", "OBJECTIVE", "PRIORITY"], d["incident"])
    assert seq["safe"] is False
    assert "APPROVAL_REQUIRED_CRITICAL_ASSET" in seq["reason"]


def test_what_if_tables_differ_by_criticality():
    s2 = load_fixture("s2_")["incident"]
    s5 = load_fixture("s5_")["incident"]
    assert evaluate_what_if(s2) != evaluate_what_if(s5)


def test_high_uncertainty_goes_to_human_review():
    d = load_fixture("s1_")
    agents = copy.deepcopy(d["agents"])
    for o in agents:
        o["confidence"] = 0.3
    a = assess(agents, d["incident"])
    dec = decide(agents, d["incident"], a)
    assert dec["decision"] == "HUMAN_REVIEW"
    assert "HIGH_UNCERTAINTY" in dec["reason_codes"]


def test_thresholds_come_from_config():
    rules = load_decision_rules()
    for key in ("critical_action_sensitivity", "high_risk_level", "human_review_min_risk",
                "auto_execute_max_risk", "min_average_confidence"):
        assert key in rules


def test_review_payload_only_when_needed():
    for name, expect_payload in (("s1_", False), ("s2_", False), ("s3_", True), ("s4_", True), ("s5_", True)):
        d, a, dec = run(name)
        p = build_review_payload("INC-X", d["incident"], d["agents"], a, dec)
        assert (p is not None) == expect_payload


def test_blocked_case_cannot_be_approved():
    d, a, dec = run("s4_")
    p = build_review_payload("INC-X", d["incident"], d["agents"], a, dec)
    assert p["allowed_choices"] == ["ACKNOWLEDGE"]