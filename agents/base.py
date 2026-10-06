class BaseAgent:
    name = "Base"
    rules = {}  # attack_type -> (recommendation, base_confidence, reason_template)
    default = (
        "ESCALATE_TO_ANALYST",
        60,
        "No specific playbook for this attack; manual review needed on {target}.",
    )

    def analyse(self, incident: dict) -> dict:
        rec, conf, reason = self.rules.get(incident["attack_type"], self.default)
        target = incident["target"].replace("_", " ").lower()
        if target == "unknown":
            target = "the affected system"
        return {
            "agent": self.name,
            "recommendation": rec,
            "confidence": self._confidence(conf, incident),
            "risk_level": self._risk_level(incident),
            "reason": reason.format(target=target),
        }

    @staticmethod
    def _confidence(base, incident):
        bonus = {"CRITICAL": 4, "HIGH": 2}.get(incident["severity"], 0)
        bonus += 2 if incident["business_impact"] == "HIGH" else 0
        if incident["attack_type"] == "UNKNOWN":
            bonus -= 10
        return max(0, min(99, base + bonus))

    @staticmethod
    def _risk_level(incident):
        score = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}[incident["severity"]]
        score += {"LOW": 0, "MEDIUM": 1, "HIGH": 2}[incident["business_impact"]]
        if score >= 6:
            return "CRITICAL"
        if score >= 4:
            return "HIGH"
        if score >= 3:
            return "MEDIUM"
        return "LOW"