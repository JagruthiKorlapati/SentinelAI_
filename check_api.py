from fastapi.testclient import TestClient

from api import app

client = TestClient(app)

r = client.post("/govern", json={"text": "Ransomware encrypted files on the database server", "use_llm": False})
print("status:", r.status_code)
body = r.json()
print("keys:", sorted(body))
print("decision:", body["decision"]["decision"], body["decision"]["reason_codes"])
print("risk:", body["assessment"]["risk_score"], body["assessment"]["risk_level"])

r = client.post("/govern", json={"text": "   ", "use_llm": False})
print("empty text status (expect 422):", r.status_code)

r = client.post("/analyze", json={"text": "DDoS flood on the web server", "use_llm": False})
print("M1 /analyze still works (expect 200):", r.status_code)