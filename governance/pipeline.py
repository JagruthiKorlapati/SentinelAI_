"""Full flow: incident text -> M1 agents -> adapter -> governance assessment -> M3 decision."""
from governance.adapter import assess_m1
from governance.decision.engine import decide


def run_pipeline(text: str, use_llm: bool = True) -> dict:
    # imported here so governance can be used without M1's LLM dependencies loaded
    from orchestrator import analyse_incident

    m1 = analyse_incident(text, use_llm=use_llm)
    gov = assess_m1(m1)
    decision = decide(gov["agent_outputs"], gov["incident"], gov["assessment"])
    return {"m1": m1, **gov, "decision": decision}