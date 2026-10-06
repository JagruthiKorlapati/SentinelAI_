import glob
import json

from governance.assess import assess

REQUIRED = [
    "conflict", "conflict_types", "conflict_severity", "risk_score", "risk_level",
    "action_sensitivity", "policy_results", "authority", "trust",
]

for f in sorted(glob.glob("fixtures/*.json")):
    d = json.load(open(f, encoding="utf-8"))
    a = assess(d["agents"], d["incident"])
    e = d["expected"]

    missing = [k for k in REQUIRED if k not in a]
    checks = {
        "fields": not missing,
        "conflict": a["conflict"] == e["conflict"],
        "types": set(a["conflict_types"]) == set(e["conflict_types"]),
        "hard_block": a["policy_results"]["hard_block"] == e["hard_block"],
        "risk_level": a["risk_level"] == e["risk_level"],
    }
    status = "ALL OK" if all(checks.values()) else "MISMATCH " + str([k for k, v in checks.items() if not v])
    print(d["name"], a["risk_score"], a["risk_level"], "->", status)

    if d["name"] == "S2_payment_server_malware":
        with open("contracts/governance_assessment_example.json", "w", encoding="utf-8") as out:
            json.dump(a, out, indent=2)