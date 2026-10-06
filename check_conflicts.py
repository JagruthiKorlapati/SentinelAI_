import glob
import json

from governance.conflict.detector import detect_conflicts
from governance.policy.engine import evaluate_policy

for f in sorted(glob.glob("fixtures/*.json")):
    d = json.load(open(f, encoding="utf-8"))
    pol = evaluate_policy(d["agents"], d["incident"])
    r = detect_conflicts(d["agents"], d["incident"], pol)
    print(d["name"], r["conflict"], r["conflict_types"], r["conflict_severity"])