\# Cyber Incident Agents (Member 1)



Takes an incident description, runs 4 agents in parallel, returns 4 recommendations.



\## Run



&#x20;   pip install -r requirements.txt

&#x20;   uvicorn api:app --host 0.0.0.0 --port 8000



Docs: http://<ip>:8000/docs



\## API



`POST /analyze`



Request:



&#x20;   {"text": "Ransomware detected on payment server", "use\_llm": true}



Response:



&#x20;   {

&#x20;     "incident": {

&#x20;       "incident\_id": "INC-001",

&#x20;       "attack\_type": "RANSOMWARE",

&#x20;       "target": "PAYMENT\_SERVER",

&#x20;       "severity": "CRITICAL",

&#x20;       "business\_impact": "HIGH",

&#x20;       "description": "..."

&#x20;     },

&#x20;     "recommendations": \[

&#x20;       {

&#x20;         "agent": "Threat Detection",

&#x20;         "recommendation": "ISOLATE\_SERVER",

&#x20;         "confidence": 96,

&#x20;         "risk\_level": "CRITICAL",

&#x20;         "reason": "..."

&#x20;       }

&#x20;       // Forensics, Backup, Business Continuity (always 4, always this order)

&#x20;     ],

&#x20;     "overall\_risk": "CRITICAL",

&#x20;     "average\_confidence": 93

&#x20;   }



`GET /scenarios` returns demo scenario texts.



\## Possible values



\- attack\_type: RANSOMWARE, DATA\_EXFILTRATION, SQL\_INJECTION, MALWARE, PHISHING,

&#x20; BRUTE\_FORCE, INSIDER\_THREAT, DDOS, DATA\_LOSS, PAYMENT\_SERVER\_FAILURE, UNKNOWN

\- target: PAYMENT\_SERVER, DATABASE\_SERVER, WEB\_SERVER, EMAIL\_SERVER, FILE\_SERVER,

&#x20; AUTH\_SERVER, UNKNOWN

\- severity / business\_impact / risk\_level / overall\_risk: LOW, MEDIUM, HIGH, CRITICAL

&#x20; (business\_impact is LOW, MEDIUM or HIGH)

\- agents (fixed order): Threat Detection, Forensics, Backup, Business Continuity

\- confidence: integer 0-99

\- recommendation: ISOLATE\_SERVER, BLOCK\_TRAFFIC, BLOCK\_TRANSFER, QUARANTINE\_EMAILS,

&#x20; BLOCK\_MALICIOUS\_REQUESTS, LOCK\_ACCOUNTS\_AND\_BLOCK\_IP, REVOKE\_ACCESS,

&#x20; INVESTIGATE\_ALERTS, PRESERVE\_EVIDENCE, COLLECT\_LOGS, COMPLETE\_BACKUP,

&#x20; VERIFY\_BACKUP, RESTORE\_BACKUP, RESTRICT\_BACKUP\_ACCESS,

&#x20; KEEP\_UNAFFECTED\_SERVICES\_ONLINE, SWITCH\_TO\_BACKUP, MAINTAIN\_SERVICE,

&#x20; SWITCH\_TO\_READ\_ONLY\_MODE, ESCALATE\_TO\_ANALYST (fallback)



\## Notes



\- Without ANTHROPIC\_API\_KEY the rule-based parser is used (always works).

\- With a valid key, an LLM parses free-form text; any failure falls back to rules.

\- The response shape never changes, even for unknown input.

