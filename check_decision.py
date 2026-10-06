import glob
import json

from governance.assess import assess
from governance.decision.engine import decide

for f in sorted(glob.glob("fixtures/*.json")):
    d = json.load(open(f, encoding="utf-8"))
    a = assess(d["agents"], d["incident"])
    r = decide(d["agents"], d["incident"], a)
    print(f"{d['name']:<28} {r['decision']:<20} {r['reason_codes']}")
    if r["steps"]:
        print("   steps:", r["steps"])