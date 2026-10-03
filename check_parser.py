from incident_parser import parse_incident

TESTS = [
    ("Ransomware detected on payment server",                     "RANSOMWARE",   "PAYMENT_SERVER",  "CRITICAL"),
    ("Ransomware on payment server, system is slow",              "RANSOMWARE",   "PAYMENT_SERVER",  "CRITICAL"),
    ("Payment server down and ransomware detected",               "RANSOMWARE",   "PAYMENT_SERVER",  "CRITICAL"),
    ("Someone encrypted our files on the file server",            "RANSOMWARE",   "FILE_SERVER",     "CRITICAL"),
    ("Someone encrypted all files in our payment infrastructure", "RANSOMWARE",   "PAYMENT_SERVER",  "CRITICAL"),
    ("Hackers exfiltrating customer data from database",          "DATA_EXFILTRATION", "DATABASE_SERVER", "CRITICAL"),
    ("Botnet flooding our website",                               "DDOS",         "WEB_SERVER",      "HIGH"),
    ("Malware found on database server, high severity",           "MALWARE",      "DATABASE_SERVER", "HIGH"),
    ("Payment gateway outage",                                    "PAYMENT_SERVER_FAILURE", "PAYMENT_SERVER", "CRITICAL"),
    ("hello",                                                     "UNKNOWN",      "UNKNOWN",         "MEDIUM"),
    ("",                                                          "UNKNOWN",      "UNKNOWN",         "MEDIUM"),
    ("Phishing email sent to employees",                          "PHISHING",     "EMAIL_SERVER",    "HIGH"),
    ("SQL injection attack on our database",                      "SQL_INJECTION", "DATABASE_SERVER", "CRITICAL"),
    ("Brute force login attempts on admin panel",                 "BRUTE_FORCE",  "AUTH_SERVER",     "HIGH"),
    ("Disgruntled employee deleted files from file server",       "INSIDER_THREAT", "FILE_SERVER",   "HIGH"),
    ("Our staff portal is flooded with bogus password guesses from overseas",
                                                                  "BRUTE_FORCE",  "AUTH_SERVER",     "HIGH"),
]

fails = 0
for text, attack, target, sev in TESTS:
    r = parse_incident(text)
    got = (r["attack_type"], r["target"], r["severity"])
    ok = got == (attack, target, sev)
    fails += not ok
    print("PASS" if ok else "FAIL", "|", repr(text), "->", got)

print(f"\n{len(TESTS) - fails}/{len(TESTS)} passed")