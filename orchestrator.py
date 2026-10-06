from concurrent.futures import ThreadPoolExecutor

from incident_parser import parse_incident
from llm_parser import parse_incident_llm
from agents import ALL_AGENTS

RISK_ORDER = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


def _safe_analyse(agent, incident):
    """One broken agent must never crash the whole analysis."""
    try:
        return agent.analyse(incident)
    except Exception as e:
        print(f"[orchestrator] {agent.name} failed: {e}")
        return {
            "agent": agent.name,
            "recommendation": "ESCALATE_TO_ANALYST",
            "confidence": 0,
            "risk_level": "MEDIUM",
            "reason": "This agent could not complete its analysis; manual review needed.",
        }


def analyse_incident(text: str, use_llm: bool = True) -> dict:
    incident = parse_incident_llm(text) if use_llm else parse_incident(text)

    # All 4 agents run at the same time; map keeps agent order.
    with ThreadPoolExecutor(max_workers=len(ALL_AGENTS)) as executor:
        recs = list(executor.map(lambda a: _safe_analyse(a, incident), ALL_AGENTS))

    return {
        "incident": incident,
        "recommendations": recs,
        "overall_risk": max((r["risk_level"] for r in recs), key=RISK_ORDER.index),
        "average_confidence": round(sum(r["confidence"] for r in recs) / len(recs)),
    }