import glob
import json

from governance.conflict.detector import detect_conflicts
from governance.policy.engine import action_sensitivity, evaluate_policy
from governance.risk.engine import compute_risk

for f in sorted(glob.glob("fixtures/*.json")):
    d = json.load(open(f, encoding="utf-8"))
    pol = evaluate_policy(d["agents"], d["incident"])
    con = detect_conflicts(d["agents"], d["incident"], pol)
    sens = action_sensitivity(d["agents"])
    r = compute_risk(d["agents"], d["incident"], pol, sens, con)
    total = sum(x["contribution"] for x in r["breakdown"].values())
    print(d["name"], r["risk_score"], r["risk_level"], "| breakdown sums to score:", total == r["risk_score"])