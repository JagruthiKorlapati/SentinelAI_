import json
import shutil
from pathlib import Path

import pytest
import yaml

import governance.policy.engine as policy_engine
from governance.assess import assess
from governance.risk.engine import load_risk_config

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_FILES = sorted((ROOT / "fixtures").glob("*.json"))

REQUIRED_FIELDS = [
    "conflict", "conflict_types", "conflict_severity", "risk_score", "risk_level",
    "action_sensitivity", "policy_results", "authority", "trust", "risk_breakdown",
]


def load_fixture(name_part):
    for f in FIXTURE_FILES:
        if name_part in f.name:
            return json.loads(f.read_text(encoding="utf-8"))
    raise FileNotFoundError(name_part)


@pytest.mark.parametrize("path", FIXTURE_FILES, ids=lambda p: p.name)
def test_fixture_matches_expected(path):
    d = json.loads(path.read_text(encoding="utf-8"))
    a = assess(d["agents"], d["incident"])
    e = d["expected"]
    assert a["conflict"] == e["conflict"]
    assert set(a["conflict_types"]) == set(e["conflict_types"])
    assert a["policy_results"]["hard_block"] == e["hard_block"]
    assert a["risk_level"] == e["risk_level"]


@pytest.mark.parametrize("path", FIXTURE_FILES, ids=lambda p: p.name)
def test_no_missing_fields(path):
    d = json.loads(path.read_text(encoding="utf-8"))
    a = assess(d["agents"], d["incident"])
    for field in REQUIRED_FIELDS:
        assert field in a, f"missing field: {field}"


@pytest.mark.parametrize("path", FIXTURE_FILES, ids=lambda p: p.name)
def test_breakdown_sums_to_score(path):
    d = json.loads(path.read_text(encoding="utf-8"))
    a = assess(d["agents"], d["incident"])
    total = sum(x["contribution"] for x in a["risk_breakdown"].values())
    assert total == a["risk_score"]


def test_s1_agents_agree_means_no_conflict():
    d = load_fixture("s1_")
    a = assess(d["agents"], d["incident"])
    assert a["conflict"] is False
    assert a["conflict_types"] == []


def test_s4_hard_block_beats_high_confidence():
    # ThreatDetection is 0.91 confident about DELETE_DATA, but mandatory policy wins.
    d = load_fixture("s4_")
    a = assess(d["agents"], d["incident"])
    assert a["policy_results"]["hard_block"] is True


def test_risk_weights_sum_to_one():
    cfg = load_risk_config()
    assert abs(sum(cfg["weights"].values()) - 1.0) < 1e-9


def test_editing_policy_file_changes_behaviour_without_code(tmp_path, monkeypatch):
    """The live demo: same input, edit one YAML value, different result."""
    d = load_fixture("s4_")
    before = assess(d["agents"], d["incident"])
    assert before["policy_results"]["hard_block"] is True

    # Work on a temporary copy so your real policy files are never touched
    tmp_policies = tmp_path / "policies"
    shutil.copytree(ROOT / "policies", tmp_policies)
    pol_file = tmp_policies / "policies.yaml"
    pol = yaml.safe_load(pol_file.read_text(encoding="utf-8"))
    pol["hard_block_actions"] = []  # remove the DELETE_DATA hard block
    pol_file.write_text(yaml.safe_dump(pol), encoding="utf-8")

    monkeypatch.setattr(policy_engine, "POLICY_DIR", tmp_policies)
    after = assess(d["agents"], d["incident"])
    assert after["policy_results"]["hard_block"] is False