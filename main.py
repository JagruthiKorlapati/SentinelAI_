import json

from orchestrator import analyse_incident
from scenarios import SCENARIOS


def print_summary(result: dict) -> None:
    inc = result["incident"]
    print("\n" + "=" * 70)
    print(f"{inc['incident_id']} | {inc['attack_type']} | {inc['target']} | "
          f"{inc['severity']} | impact: {inc['business_impact']}")
    print("=" * 70)
    for r in result["recommendations"]:
        print(f"{r['agent']:<22} -> {r['recommendation']:<34} "
              f"{r['confidence']:>3}%  [{r['risk_level']}]")
        print(f"    {r['reason']}")
    print("-" * 70)
    print(f"Overall risk: {result['overall_risk']} | "
          f"Avg confidence: {result['average_confidence']}%")


if __name__ == "__main__":
    print("Demo scenarios:", ", ".join(SCENARIOS))
    text = input("\nEnter incident text (or scenario name): ").strip()
    text = SCENARIOS.get(text.upper(), text)
    result = analyse_incident(text)
    print_summary(result)
    print("\nRaw JSON:")
    print(json.dumps(result, indent=2))