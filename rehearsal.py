from orchestrator import analyse_incident
from scenarios import SCENARIOS

print(f"{'SCENARIO':<11} {'ATTACK':<18} {'TARGET':<16} {'RISK':<9} CONF")
print("-" * 65)
for name, text in SCENARIOS.items():
    r = analyse_incident(text)
    inc = r["incident"]
    print(f"{name:<11} {inc['attack_type']:<18} {inc['target']:<16} "
          f"{r['overall_risk']:<9} {r['average_confidence']}%")
    for rec in r["recommendations"]:
        print(f"    {rec['agent']:<20} -> {rec['recommendation']}")