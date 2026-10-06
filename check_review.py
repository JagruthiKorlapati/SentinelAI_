import glob
import json

from governance.assess import assess
from governance.decision.engine import decide
from governance.decision.review import build_review_payload

for i, f in enumerate(sorted(glob.glob("fixtures/*.json")), start=1):
    d = json.load(open(f, encoding="utf-8"))
    a = assess(d["agents"], d["incident"])
    dec = decide(d["agents"], d["incident"], a)
    p = build_review_payload(f"INC-00{i}", d["incident"], d["agents"], a, dec)
    if p is None:
        print(d["name"], "-> no human review needed (" + dec["decision"] + ")")
        continue
    print(d["name"], "->", p["decision"], "| choices:", p["allowed_choices"])
    for line in p["why_review_needed"]:
        print("   why:", line)
    print("   suggested:", p["suggested_action"])

    if d["name"].startswith("S5_"):
        with open("contracts/review_payload_example.json", "w", encoding="utf-8") as out:
            json.dump(p, out, indent=2)