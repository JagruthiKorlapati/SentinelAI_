import json
import os

from incident_parser import (
    ATTACK_KEYWORDS,
    TARGET_IMPACT,
    DEFAULT_SEVERITY,
    parse_incident as rule_parse,
)
from itertools import count

_llm_counter = count(1)

ATTACKS = list(ATTACK_KEYWORDS.keys())
TARGETS = [t for t in TARGET_IMPACT.keys() if t != "UNKNOWN"]
SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

SYSTEM_PROMPT = f"""You classify cybersecurity incident reports.
Reply with ONLY a JSON object, no markdown, no extra text:
{{"attack_type": one of {ATTACKS} or "UNKNOWN",
 "target": one of {TARGETS} or "UNKNOWN",
 "severity": one of {SEVERITIES}}}
Choose the closest match. Use UNKNOWN only if nothing fits."""


def _call_llm(text: str) -> dict:
    import anthropic

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    msg = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        max_tokens=200,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": text}],
        timeout=8,
    )
    raw = msg.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def parse_incident_llm(text: str) -> dict:
    """LLM first; any failure falls back to the rule-based parser."""
    text = (text or "").strip()
    if not text or not os.getenv("ANTHROPIC_API_KEY"):
        return rule_parse(text)

    try:
        data = _call_llm(text)
        attack = str(data.get("attack_type", "UNKNOWN")).upper()
        target = str(data.get("target", "UNKNOWN")).upper()
        severity = str(data.get("severity", "")).upper()

        if attack not in ATTACKS:
            attack = "UNKNOWN"
        if target not in TARGETS:
            target = "UNKNOWN"
        if severity not in SEVERITIES:
            severity = DEFAULT_SEVERITY.get(attack, "MEDIUM")

        # LLM understood nothing -> let rules try
        if attack == "UNKNOWN" and target == "UNKNOWN":
            return rule_parse(text)

        impact = TARGET_IMPACT.get(target, "LOW")
        if severity == "CRITICAL":
            impact = "HIGH"

        return {
            "incident_id": f"INC-{next(_llm_counter):03d}",
            "attack_type": attack,
            "target": target,
            "severity": severity,
            "business_impact": impact,
            "description": text,
        }
    except Exception as e:
        print(f"[llm_parser] fallback to rules: {e}")
        return rule_parse(text)