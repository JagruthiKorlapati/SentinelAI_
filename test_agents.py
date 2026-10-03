from incident_parser import parse_incident
from orchestrator import analyse_incident
from agents import ALL_AGENTS
from incident_parser import ATTACK_KEYWORDS


def test_ransomware_payment():
    r = analyse_incident("Ransomware detected on payment server")
    inc = r["incident"]
    assert inc["attack_type"] == "RANSOMWARE"
    assert inc["target"] == "PAYMENT_SERVER"
    assert inc["severity"] == "CRITICAL"
    recs = {x["agent"]: x["recommendation"] for x in r["recommendations"]}
    assert recs["Threat Detection"] == "ISOLATE_SERVER"
    assert recs["Forensics"] == "PRESERVE_EVIDENCE"
    assert recs["Backup"] == "COMPLETE_BACKUP"
    assert recs["Business Continuity"] == "KEEP_UNAFFECTED_SERVICES_ONLINE"


def test_natural_language():
    r = analyse_incident("Someone encrypted all files in our payment infrastructure")
    assert r["incident"]["attack_type"] == "RANSOMWARE"
    assert r["incident"]["target"] == "PAYMENT_SERVER"


def test_all_agents_same_structure():
    r = analyse_incident("DDoS attack on web server")
    keys = {"agent", "recommendation", "confidence", "risk_level", "reason"}
    assert all(set(x) == keys for x in r["recommendations"])


def test_unknown_input_does_not_crash():
    r = analyse_incident("something weird happened")
    assert len(r["recommendations"]) == 4


def test_slow_does_not_trigger_low_severity():
    inc = parse_incident("Ransomware on payment server, system is slow")
    assert inc["severity"] == "CRITICAL"


def test_real_attack_beats_failure_keyword():
    inc = parse_incident("Payment server down and ransomware detected")
    assert inc["attack_type"] == "RANSOMWARE"


def test_payment_gateway_outage():
    inc = parse_incident("Payment gateway outage")
    assert inc["attack_type"] == "PAYMENT_SERVER_FAILURE"
    assert inc["target"] == "PAYMENT_SERVER"


def test_unknown_reason_is_clean():
    r = analyse_incident("something weird happened")
    assert all("unknown" not in x["reason"].lower() for x in r["recommendations"])


def test_empty_input_does_not_crash():
    r = analyse_incident("")
    assert len(r["recommendations"]) == 4


def test_all_attack_types_have_rules():
    for agent in ALL_AGENTS:
        for attack in ATTACK_KEYWORDS:
            assert attack in agent.rules, f"{agent.name} missing rule for {attack}"
def test_rules_only_mode_works():
    r = analyse_incident("Ransomware detected on payment server", use_llm=False)
    assert r["incident"]["attack_type"] == "RANSOMWARE"


def test_llm_failure_falls_back(monkeypatch):
    import llm_parser
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake")
    monkeypatch.setattr(llm_parser, "_call_llm", lambda t: (_ for _ in ()).throw(RuntimeError("boom")))
    r = analyse_incident("Ransomware detected on payment server")
    assert r["incident"]["attack_type"] == "RANSOMWARE"
def test_broken_agent_does_not_crash(monkeypatch):
    monkeypatch.setattr(ALL_AGENTS[0], "analyse",
                        lambda incident: (_ for _ in ()).throw(RuntimeError("boom")))
    r = analyse_incident("Ransomware detected on payment server", use_llm=False)
    assert len(r["recommendations"]) == 4
    assert r["recommendations"][0]["recommendation"] == "ESCALATE_TO_ANALYST"
    assert r["recommendations"][1]["agent"] == "Forensics"