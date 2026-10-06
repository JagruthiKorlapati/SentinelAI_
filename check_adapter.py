from agents import ALL_AGENTS
from incident_parser import parse_incident
from governance.action_map import ACTION_MAP
from governance.adapter import assess_m1
from governance.constants import AGENTS

# 1. Every action string M1's agents can emit must be in the map
emitted = {rule[0] for a in ALL_AGENTS for rule in a.rules.values()}
missing = emitted - set(ACTION_MAP)
print("M1 actions emitted:", len(emitted), "| unmapped:", sorted(missing) or "none")

# 2. Agent names must match governance names
from governance.action_map import map_agent_name
names = [map_agent_name(a.name) for a in ALL_AGENTS]
print("Agent names OK:", names == AGENTS, names)

# 3. Run one scenario per attack type through the real pipeline
TEXTS = [
    "Ransomware encrypted files on the database server",
    "Payment server down, transactions failing",
    "DDoS traffic flood against the web server",
    "Malware found on the file server",
    "Data exfiltration from the database",
    "SQL injection attack on the website",
    "Phishing emails hitting the email server",
    "Brute force login attempts on the VPN",
    "Insider employee copying files",
    "Data loss: records deleted from the database",
    "Something odd happened",
]
for text in TEXTS:
    incident = parse_incident(text)
    recs = [a.analyse(incident) for a in ALL_AGENTS]
    out = assess_m1({"incident": incident, "recommendations": recs})
    a = out["assessment"]
    acts = [o["action"] for o in out["agent_outputs"]]
    print(f"\n{text}")
    print("  attack:", incident["attack_type"], "| actions:", acts)
    print("  conflict:", a["conflict_types"], a["conflict_severity"],
          "| risk:", a["risk_score"], a["risk_level"],
          "| approval:", a["policy_results"]["requires_approval"])