from governance.pipeline import run_pipeline

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
    r = run_pipeline(text, use_llm=False)
    a, d = r["assessment"], r["decision"]
    print(f"\n{text}")
    print("  risk:", a["risk_score"], a["risk_level"], "| conflict:", a["conflict_types"] or "none")
    print("  DECISION:", d["decision"], "|", d["reason_codes"])
    print("  steps:", d["steps"] or "-", "| what-if options:", len(d["what_if_options"]))

unknown = run_pipeline("Something odd happened", use_llm=False)["decision"]["decision"]
print("\nUnknown incident goes to a human:", unknown == "HUMAN_REVIEW")