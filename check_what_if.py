import glob
import json

from governance.what_if.evaluator import evaluate_what_if

SHOW = ("S2_", "S5_")

for f in sorted(glob.glob("fixtures/*.json")):
    d = json.load(open(f, encoding="utf-8"))
    if not d["name"].startswith(SHOW):
        continue
    print(d["name"], "(criticality:", d["incident"]["asset_criticality"] + ")")
    for o in evaluate_what_if(d["incident"]):
        print(f"   {o['option']:<20} security={o['security']:<9} evidence={o['evidence']:<7} business={o['business']:<9} policy={o['policy']}")