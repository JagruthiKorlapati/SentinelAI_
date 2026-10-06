"""Convert M1's orchestrator data into the shapes assess() expects."""
from governance.action_map import map_action, map_agent_name
from governance.assess import assess


def adapt_incident(m1_incident: dict) -> dict:
    return {
        "incident_id": m1_incident.get("incident_id"),
        "asset": m1_incident["target"],
        "asset_criticality": m1_incident["business_impact"],  # LOW / MEDIUM / HIGH
        "threat_type": m1_incident["attack_type"],
        "severity": m1_incident["severity"],
        "data_involved": "unknown",
        "description": m1_incident.get("description", ""),
    }


def adapt_agent_outputs(m1_recs: list, m1_incident: dict) -> list:
    return [
        {
            "agent": map_agent_name(r["agent"]),
            "action": map_action(r["recommendation"]),
            "raw_action": r["recommendation"],   # kept so the UI can show M1's wording
            "target": m1_incident["target"],
            "reason": r["reason"],
            "confidence": r["confidence"] / 100,  # M1: 0-99, governance: 0-1
            "risk_level": r["risk_level"],
        }
        for r in m1_recs
    ]


def assess_m1(m1_result: dict) -> dict:
    """Takes the dict returned by M1's analyse_incident() and returns the governance assessment."""
    incident = adapt_incident(m1_result["incident"])
    outputs = adapt_agent_outputs(m1_result["recommendations"], m1_result["incident"])
    return {
        "incident": incident,
        "agent_outputs": outputs,
        "assessment": assess(outputs, incident),
    }