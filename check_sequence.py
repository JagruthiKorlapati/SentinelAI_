import glob
import json

from governance.assess import assess
from governance.sequence_table.lookup import find_safe_coordinated_action

for f in sorted(glob.glob("fixtures/*.json")):
    d = json.load(open(f, encoding="utf-8"))
    a = assess(d["agents"], d["incident"])
    r = find_safe_coordinated_action(a["conflict_types"], d["incident"])
    print(d["name"], r["safe"], r["reason"])
    if r["safe"]:
        print("   steps:", r["steps"])