import { useState } from "react";
import "./App.css";

const mockAgents = [
  {
    name: "Threat Detection",
    icon: "TD",
    recommendation: "ISOLATE SERVER",
    confidence: 94,
    reason: "Active ransomware indicators detected on production infrastructure."
  },
  {
    name: "Forensics",
    icon: "FR",
    recommendation: "PRESERVE EVIDENCE",
    confidence: 91,
    reason: "Memory, process and network evidence should be preserved."
  },
  {
    name: "Backup",
    icon: "BK",
    recommendation: "COMPLETE BACKUP",
    confidence: 87,
    reason: "Create a recovery point before containment actions."
  },
  {
    name: "Business Continuity",
    icon: "BC",
    recommendation: "KEEP UNAFFECTED SERVICES ONLINE",
    confidence: 89,
    reason: "Maintain critical business services where isolation is not required."
  }
];

function App() {
  const [attackType, setAttackType] = useState("Ransomware");
  const [target, setTarget] = useState("Production Server");
  const [severity, setSeverity] = useState("Critical");
  const [businessImpact, setBusinessImpact] = useState("High");

  const [description, setDescription] = useState(
    "Ransomware detected on production infrastructure."
  );

  const [analyzing, setAnalyzing] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [decisionStatus, setDecisionStatus] = useState("");
  const [selectedScenario, setSelectedScenario] = useState(null);
  const [activeTab, setActiveTab] = useState("dashboard");

  const [auditLogs, setAuditLogs] = useState([]);

  const [governanceData, setGovernanceData] = useState({
    riskScore: 91,
    conflicts: 3,
    policyViolations: 0,
    riskLevel: "CRITICAL",
    priority: "SECURITY",
    decision: "COORDINATED RESPONSE"
  });

  const navItems = [
    { id: "dashboard", label: "Dashboard" },
    { id: "agents", label: "Agents" },
    { id: "governance", label: "Governance" },
    { id: "audit", label: "Audit" }
  ];

  const scrollToSection = (id) => {
    setActiveTab(id);

    const element = document.getElementById(id);

    if (element) {
      element.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    }
  };

  const addAuditLog = (title, description) => {
    const now = new Date();

    const time = now.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit"
    });

    setAuditLogs((previousLogs) => [
      ...previousLogs,
      {
        time,
        title,
        description
      }
    ]);
  };

  const calculateGovernance = () => {
    let riskScore = 50;
    let conflicts = 1;
    let policyViolations = 0;

    if (severity === "Critical") {
      riskScore += 35;
      conflicts += 2;
    } else if (severity === "High") {
      riskScore += 25;
      conflicts += 1;
    } else if (severity === "Medium") {
      riskScore += 12;
    } else {
      riskScore += 5;
    }

    if (businessImpact === "High") {
      riskScore += 10;
    } else if (businessImpact === "Medium") {
      riskScore += 5;
    }

    if (attackType === "Ransomware") {
      riskScore += 5;
    }

    if (attackType === "Data Exfiltration") {
      riskScore += 8;
      policyViolations += 1;
    }

    if (attackType === "Insider Threat") {
      riskScore += 7;
      policyViolations += 1;
    }

    if (attackType === "DDoS") {
      riskScore += 4;
    }

    riskScore = Math.min(riskScore, 99);

    let riskLevel = "LOW";

    if (riskScore >= 85) {
      riskLevel = "CRITICAL";
    } else if (riskScore >= 70) {
      riskLevel = "HIGH";
    } else if (riskScore >= 45) {
      riskLevel = "MEDIUM";
    }

    let priority = "BALANCED";

    if (riskScore >= 80) {
      priority = "SECURITY";
    } else if (businessImpact === "High") {
      priority = "BUSINESS CONTINUITY";
    }

    let decision = "MONITOR + REVIEW";

    if (riskScore >= 85) {
      decision = "COORDINATED RESPONSE";
    } else if (riskScore >= 70) {
      decision = "CONTAIN + INVESTIGATE";
    }

    if (attackType === "Data Exfiltration") {
      decision = "CONTAIN + INVESTIGATE";
    }

    if (businessImpact === "High" && severity !== "Critical") {
      decision = "COORDINATED RESPONSE";
    }

    const result = {
      riskScore,
      conflicts,
      policyViolations,
      riskLevel,
      priority,
      decision
    };

    setGovernanceData(result);

    return result;
  };

  const handleAnalyze = () => {
    setAnalyzing(true);
    setShowResults(false);
    setDecisionStatus("");
    setSelectedScenario(null);
    setAuditLogs([]);

    addAuditLog(
      "Incident received",
      `${attackType} activity detected on ${target}.`
    );

    setTimeout(() => {
      const newGovernanceData = calculateGovernance();

      addAuditLog(
        "Agent analysis completed",
        "Four autonomous agents submitted recommendations."
      );

      addAuditLog(
        "Conflict detection completed",
        `${newGovernanceData.conflicts} conflicts identified between agent recommendations.`
      );

      addAuditLog(
        "Governance decision generated",
        `${newGovernanceData.decision} generated by SentinelAI.`
      );

      setAnalyzing(false);
      setShowResults(true);
    }, 1500);
  };

  const handleDecision = (decision) => {
    setDecisionStatus(decision);

    if (decision === "APPROVED") {
      addAuditLog(
        "Human approval recorded",
        "Human reviewer approved the governance decision."
      );
    } else {
      addAuditLog(
        "Human rejection recorded",
        "Human reviewer rejected the governance decision. Re-evaluation required."
      );
    }
  };

  const handleScenario = (scenario) => {
    setSelectedScenario(scenario);
  };

  const getScenarioData = () => {
    if (selectedScenario === "ISOLATE SERVER") {
      return {
        risk: "LOW",
        riskScore: Math.max(governanceData.riskScore - 25, 20),
        businessImpact: "HIGH",
        policy: "Security policy satisfied",
        outcome: "Threat contained and affected server isolated.",
        explanation:
          "Isolation reduces attack exposure but may temporarily interrupt the affected production server."
      };
    }

    if (selectedScenario === "KEEP SERVER ONLINE") {
      return {
        risk: "CRITICAL",
        riskScore: Math.min(governanceData.riskScore + 5, 99),
        businessImpact: "LOW",
        policy: "Security policy risk detected",
        outcome:
          "Business continuity maintained, but attack exposure remains.",
        explanation:
          "Keeping the server online protects availability but allows the threat to remain active."
      };
    }

    if (selectedScenario === "COORDINATED RESPONSE") {
      return {
        risk: "LOW",
        riskScore: Math.max(governanceData.riskScore - 20, 25),
        businessImpact: "MEDIUM",
        policy: "Security and continuity policies balanced",
        outcome:
          "Threat containment and business continuity coordinated.",
        explanation:
          "The governance layer combines containment, evidence preservation, backup and continuity actions."
      };
    }

    return null;
  };

  const getFinalStatus = () => {
    if (decisionStatus === "APPROVED") {
      return "HUMAN APPROVED";
    }

    if (decisionStatus === "REJECTED") {
      return "RE-EVALUATION REQUIRED";
    }

    return "AWAITING HUMAN APPROVAL";
  };

  const scenarioData = getScenarioData();

  return (
    <div className="app">
      <header className="navbar">
        <div className="navbar-inner">
          <button
            className="brand"
            onClick={() => scrollToSection("dashboard")}
          >
            <span className="logo-mark">S</span>

            <span className="brand-text">
              <strong>SentinelAI</strong>
              <small>GOVERNANCE SOC</small>
            </span>
          </button>

          <nav className="nav-links">
            {navItems.map((item) => (
              <button
                key={item.id}
                className={`nav-link ${
                  activeTab === item.id ? "active" : ""
                }`}
                onClick={() => scrollToSection(item.id)}
              >
                {item.label}
              </button>
            ))}
          </nav>

          <div className="system-status">
            <span className="status-dot"></span>
            <span>SYSTEM ONLINE</span>
          </div>
        </div>
      </header>

      <main className="dashboard">
        <section id="dashboard" className="hero">
          <div className="hero-content">
            <div className="eyebrow">
              SENTINELAI // AI GOVERNANCE SECURITY OPERATIONS
            </div>

            <h1>
              Autonomous Security.
              <br />
              <span>Governed Decisions.</span>
            </h1>

            <p className="hero-text">
              A governance layer that evaluates autonomous AI agent decisions,
              detects conflicts, applies security policies and keeps humans in
              control.
            </p>

            <div className="hero-tags">
              <span>LIVE SIMULATION</span>
              <span>4 AI AGENTS</span>
              <span>HUMAN OVERSIGHT</span>
            </div>
          </div>

          <div className="hero-console">
            <div className="console-header">
              <span>SECURITY CONSOLE</span>
              <span className="console-live">● LIVE</span>
            </div>

            <div className="console-body">
              <div>
                <span className="console-key">ENGINE</span>
                <strong>GOVERNANCE</strong>
              </div>

              <div>
                <span className="console-key">STATUS</span>
                <strong className="green-text">OPERATIONAL</strong>
              </div>

              <div>
                <span className="console-key">THREAT MODE</span>
                <strong>MONITORING</strong>
              </div>

              <div>
                <span className="console-key">HUMAN CONTROL</span>
                <strong className="cyan-text">ENABLED</strong>
              </div>
            </div>
          </div>
        </section>

        <section className="stats-grid">
          <div className="stat-card">
            <span className="stat-label">ACTIVE AGENTS</span>
            <strong>04</strong>
            <small>Autonomous security agents</small>
          </div>

          <div className="stat-card">
            <span className="stat-label">CONFLICTS</span>
            <strong>{governanceData.conflicts}</strong>
            <small>Detected during evaluation</small>
          </div>

          <div className="stat-card">
            <span className="stat-label">RISK SCORE</span>
            <strong>{governanceData.riskScore}</strong>
            <small>{governanceData.riskLevel} risk level</small>
          </div>

          <div className="stat-card">
            <span className="stat-label">HUMAN REVIEW</span>
            <strong>{decisionStatus ? "DONE" : "WAIT"}</strong>
            <small>
              {decisionStatus
                ? "Decision recorded"
                : "Awaiting approval"}
            </small>
          </div>
        </section>

        <section className="section">
          <div className="section-heading">
            <div>
              <span className="section-kicker">01 // ATTACK SIMULATOR</span>
              <h2>Incident Intake</h2>
            </div>

            <span className="section-status">READY</span>
          </div>

          <div className="attack-panel">
            <div className="panel-terminal">
              <span>SIMULATION MODE</span>
              <strong>SECURITY EVENT INPUT</strong>
              <p>
                Configure an attack scenario and submit it to the autonomous
                agent pipeline.
              </p>
            </div>

            <div className="form-grid">
              <div className="form-group">
                <label>ATTACK TYPE</label>

                <select
                  value={attackType}
                  onChange={(event) => setAttackType(event.target.value)}
                >
                  <option>Ransomware</option>
                  <option>DDoS</option>
                  <option>Data Exfiltration</option>
                  <option>Insider Threat</option>
                </select>
              </div>

              <div className="form-group">
                <label>TARGET</label>

                <input
                  type="text"
                  value={target}
                  onChange={(event) => setTarget(event.target.value)}
                />
              </div>

              <div className="form-group">
                <label>SEVERITY</label>

                <select
                  value={severity}
                  onChange={(event) => setSeverity(event.target.value)}
                >
                  <option>Critical</option>
                  <option>High</option>
                  <option>Medium</option>
                  <option>Low</option>
                </select>
              </div>

              <div className="form-group">
                <label>BUSINESS IMPACT</label>

                <select
                  value={businessImpact}
                  onChange={(event) =>
                    setBusinessImpact(event.target.value)
                  }
                >
                  <option>High</option>
                  <option>Medium</option>
                  <option>Low</option>
                </select>
              </div>

              <div className="form-group full-width">
                <label>INCIDENT DESCRIPTION</label>

                <textarea
                  value={description}
                  onChange={(event) => setDescription(event.target.value)}
                  rows="3"
                />
              </div>

              <div className="full-width">
                <button
                  className="analyze-button"
                  onClick={handleAnalyze}
                  disabled={analyzing}
                >
                  {analyzing
                    ? "ANALYZING SECURITY EVENT..."
                    : "RUN AI ANALYSIS →"}
                </button>
              </div>
            </div>
          </div>
        </section>

        <section id="agents" className="section">
          <div className="section-heading">
            <div>
              <span className="section-kicker">02 // AI AGENTS</span>
              <h2>Agent Analysis</h2>
            </div>

            <span className="section-status live">4 AGENTS ONLINE</span>
          </div>

          <div className="agent-grid">
            {mockAgents.map((agent) => (
              <div className="agent-card" key={agent.name}>
                <div className="agent-top">
                  <div className="agent-icon">{agent.icon}</div>

                  <div>
                    <h3>{agent.name}</h3>
                    <span className="agent-online">
                      ● ONLINE
                    </span>
                  </div>
                </div>

                <div className="agent-recommendation">
                  <span>RECOMMENDATION</span>
                  <strong>{agent.recommendation}</strong>
                </div>

                <div className="confidence-row">
                  <span>CONFIDENCE</span>
                  <strong>{agent.confidence}%</strong>
                </div>

                <div className="confidence-bar">
                  <span
                    style={{
                      width: `${agent.confidence}%`
                    }}
                  ></span>
                </div>

                <p className="agent-reason">{agent.reason}</p>
              </div>
            ))}
          </div>
        </section>

        <section id="governance" className="section">
          <div className="section-heading">
            <div>
              <span className="section-kicker">
                03 // GOVERNANCE ENGINE
              </span>
              <h2>Conflict & Policy Evaluation</h2>
            </div>

            <span className="section-status live">
              {showResults ? "EVALUATED" : "STANDBY"}
            </span>
          </div>

          <div className="governance-engine">
            <div className="governance-flow">
              <div className="governance-stage">
                <span className="stage-number">01</span>
                <div className="stage-icon">AI</div>
                <h3>Agent Decisions</h3>
                <p>4 recommendations submitted</p>
              </div>

              <div className="flow-arrow">→</div>

              <div className="governance-stage">
                <span className="stage-number">02</span>
                <div className="stage-icon">CF</div>
                <h3>Conflict Detection</h3>
                <p>{governanceData.conflicts} conflicts identified</p>
              </div>

              <div className="flow-arrow">→</div>

              <div className="governance-stage">
                <span className="stage-number">03</span>
                <div className="stage-icon">RP</div>
                <h3>Risk + Policy</h3>
                <p>{governanceData.riskScore}/100 risk score</p>
              </div>

              <div className="flow-arrow">→</div>

              <div className="governance-stage decision-stage">
                <span className="stage-number">04</span>
                <div className="stage-icon">GD</div>
                <h3>Governance Decision</h3>
                <p>{governanceData.decision}</p>
              </div>
            </div>
          </div>

          <div className="analysis-grid">
            <div className="analysis-card">
              <span>RISK LEVEL</span>
              <strong className="danger-text">
                {governanceData.riskLevel}
              </strong>
            </div>

            <div className="analysis-card">
              <span>RISK SCORE</span>
              <strong>{governanceData.riskScore}/100</strong>
            </div>

            <div className="analysis-card">
              <span>POLICY VIOLATIONS</span>
              <strong>{governanceData.policyViolations}</strong>
            </div>

            <div className="analysis-card">
              <span>PRIORITY</span>
              <strong>{governanceData.priority}</strong>
            </div>
          </div>

          <div className="sub-section">
            <div className="sub-heading">
              <span>04 // WHAT-IF ENGINE</span>
              <p>Compare possible governance actions</p>
            </div>

            <div className="what-if-grid">
              <button
                className={`what-if-card ${
                  selectedScenario === "ISOLATE SERVER"
                    ? "selected"
                    : ""
                }`}
                onClick={() => handleScenario("ISOLATE SERVER")}
              >
                <span className="what-if-number">01</span>
                <span className="what-if-label">SCENARIO</span>
                <strong>ISOLATE SERVER</strong>
                <p>Contain the affected production server.</p>
              </button>

              <button
                className={`what-if-card ${
                  selectedScenario === "KEEP SERVER ONLINE"
                    ? "selected"
                    : ""
                }`}
                onClick={() =>
                  handleScenario("KEEP SERVER ONLINE")
                }
              >
                <span className="what-if-number">02</span>
                <span className="what-if-label">SCENARIO</span>
                <strong>KEEP SERVER ONLINE</strong>
                <p>Prioritize business availability.</p>
              </button>

              <button
                className={`what-if-card ${
                  selectedScenario === "COORDINATED RESPONSE"
                    ? "selected"
                    : ""
                }`}
                onClick={() =>
                  handleScenario("COORDINATED RESPONSE")
                }
              >
                <span className="what-if-number">03</span>
                <span className="what-if-label">SCENARIO</span>
                <strong>COORDINATED RESPONSE</strong>
                <p>Balance containment and continuity.</p>
              </button>
            </div>

            {scenarioData && (
              <div className="scenario-result">
                <div className="scenario-result-header">
                  <div>
                    <span>WHAT-IF RESULT</span>
                    <h3>{selectedScenario}</h3>
                  </div>

                  <button
                    className="clear-scenario"
                    onClick={() => setSelectedScenario(null)}
                  >
                    CLEAR
                  </button>
                </div>

                <div className="scenario-metrics">
                  <div>
                    <span>RISK</span>
                    <strong>{scenarioData.risk}</strong>
                  </div>

                  <div>
                    <span>RISK SCORE</span>
                    <strong>{scenarioData.riskScore}</strong>
                  </div>

                  <div>
                    <span>BUSINESS IMPACT</span>
                    <strong>{scenarioData.businessImpact}</strong>
                  </div>

                  <div>
                    <span>POLICY</span>
                    <strong>{scenarioData.policy}</strong>
                  </div>
                </div>

                <div className="scenario-explanation">
                  <strong>OUTCOME</strong>
                  <p>{scenarioData.outcome}</p>

                  <strong>EXPLANATION</strong>
                  <p>{scenarioData.explanation}</p>
                </div>
              </div>
            )}
          </div>

          <div className="sub-section">
            <div className="sub-heading">
              <span>05 // HUMAN REVIEW</span>
              <p>Final governance decision requires human approval.</p>
            </div>

            <div className="review-panel">
              <div className="review-info">
                <span>RECOMMENDED ACTION</span>
                <h3>{governanceData.decision}</h3>
                <p>
                  SentinelAI has evaluated agent recommendations,
                  conflicts, risk and policy constraints.
                </p>
              </div>

              <div className="review-actions">
                <button
                  className="approve-button"
                  onClick={() => handleDecision("APPROVED")}
                  disabled={!showResults}
                >
                  ✓ APPROVE
                </button>

                <button
                  className="reject-button"
                  onClick={() => handleDecision("REJECTED")}
                  disabled={!showResults}
                >
                  ✕ REJECT
                </button>
              </div>

              <div className="decision-status">
                STATUS:{" "}
                <strong>
                  {decisionStatus || "WAITING FOR HUMAN REVIEW"}
                </strong>
              </div>
            </div>
          </div>

          <div className="final-decision">
            <div className="final-icon">
              {decisionStatus === "APPROVED" ? "✓" : "!"}
            </div>

            <div>
              <span>FINAL GOVERNANCE STATUS</span>
              <h3>{getFinalStatus()}</h3>
            </div>
          </div>
        </section>

        <section id="audit" className="section">
          <div className="section-heading">
            <div>
              <span className="section-kicker">
                06 // AUDIT TRAIL
              </span>
              <h2>Decision Trace</h2>
            </div>

            <span className="section-status live">
              TRACEABILITY ENABLED
            </span>
          </div>

          <div className="audit-panel">
            {auditLogs.length === 0 ? (
              <div className="audit-item">
                <span className="audit-dot"></span>

                <span className="audit-time">--:--:--</span>

                <div className="audit-content">
                  <strong>Audit engine ready</strong>
                  <p>
                    Run AI analysis to generate the live governance
                    audit trail.
                  </p>
                </div>
              </div>
            ) : (
              auditLogs.map((log, index) => (
                <div
                  className="audit-item"
                  key={`${log.time}-${index}`}
                >
                  <span className="audit-dot"></span>

                  <span className="audit-time">
                    {log.time}
                  </span>

                  <div className="audit-content">
                    <strong>{log.title}</strong>
                    <p>{log.description}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </section>

        <footer className="footer">
          <span>SENTINELAI</span>
          <span>AI GOVERNANCE // SECURITY // HUMAN OVERSIGHT</span>
          <span>LOCAL SIMULATION</span>
        </footer>
      </main>
    </div>
  );
}

export default App;