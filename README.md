# 🚀 WaferPulse: 3nm Fab Yield Root Cause & Batch Risk Analyser


---

## 👥 Team

| Field | Value |
|---|---|
| **Team Name** | TECHVOLT |
| **Track** | AI |
| **Team Lead** | Manan Pravinbhai Patel — 25ec082@charusat.edu.in |
| **Members** | Virajsinh Hemantsinh Dabhi, Hiral Harishkumar Shah, Liza Sohilbhai Vhora |

---

## 🎯 Problem Statement

>What problem does your project solve? Who experiences this problem?

At sub-5nm process nodes, a 1% yield drop costs semiconductor foundries tens of millions of dollars per month. Process integration engineers spend weeks manually correlating high-density inline defect inspection images against thousands of equipment sensor parameters across lithography, etch, and CMP chambers. Foundries lack automated tools to isolate root causes probabilistically and flag at-risk upcoming batches before chamber processing.

---

## 💡 Solution

>What did you build? How does it solve the problem above?

WaferPulse automates semiconductor fab triage by combining spatial wafer defect pattern classification with Tree-SHAP marginal telemetry attribution, isolating equipment root causes down to standard deviation drift. The engine exposes deterministic diagnostic endpoints to IBM Bob through a local FastMCP server, enabling conversational fab triage, prescriptive maintenance runbooks, and an automated pre-run safety interlock that prevents dispatching at-risk batches.
---

## ✨ Key Features

- **Feature 1:** Spatial Defect Pattern Classification: Classifies wafer die morphologies into canonical fab failure signatures (Edge-Ring, Center, Scratch, Donut, Random).
- **Feature 2:** Tree-SHAP Root Cause Attribution: Decomposes multivariate chamber sensor telemetry to rank physical equipment anomalies by marginal yield penalty.
- **Feature 3:** Pre-Dispatch Batch Gatekeeper: Evaluates recipe setpoints for upcoming uncommitted wafer lots and triggers automated safety interlocks to prevent scrap.
- **Feature 4:** Load-Bearing IBM Bob MCP Integration: FastMCP server running over STDIO transport providing JSON-RPC tools for autonomous agent diagnostic workflows.
- **Feature 5:** Interactive FabOps Operations UI: Real-time Streamlit dashboard providing engineers with visual wafer map slicing, SHAP charts, and recipe parameter simulators.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Languages** | Python 3.10+ |
| **Frameworks** | Streamlit, FastMCP, Scikit-Learn |
| **IBM Technologies** | IBM Bob, Model Context Protocol (MCP) |
| **Databases** | Pandas DataFrame, Structured Fab CSV Telemetry |
| **Other** | Tree-SHAP, NumPy, Matplotlib, GitHub Actions CI |

---

## 📁 Repository Structure

```
├── src/                  # All source code
├── docs/                 # Written documentation
│   ├── problem-statement.md
│   ├── solution-overview.md
│   ├── architecture.md
│   └── setup-guide.md
├── demo/                 # Demo artifacts
│   ├── screenshots/      # App screenshots
│   └── demo-video-link.txt  # Link to demo video
├── presentation/         # Slide deck
└── submission.yaml       # Structured submission metadata
```

---

## ⚡ How to Run

```bash
# Clone Repository
git clone https://github.com/drijesh-ppatel/bob-ai-hackathon--TECHVOLT-.git

cd bob-ai-hackathon--TECHVOLT-

# Create Virtual Environment
python -m venv venv

# Activate Virtual Environment (Windows)
.\venv\Scripts\activate

# Install Dependencies
pip install fastmcp streamlit pandas numpy scikit-learn shap matplotlib

# Generate Dataset
python src/data_generator.py

# Launch Dashboard
streamlit run src/app.py
```

---

## 🖥️ Demo

| Artifact | Link |
|---|---|
| 📹 Demo Video | [See demo/demo-video-link.txt](demo/demo-video-link.txt) |
| 🌐 Live Demo | [See demo/live-demo-url.txt](demo/live-demo-url.txt) |
| 🖼️ Screenshots | [See demo/screenshots/](demo/screenshots/) |
| 📊 Presentation | [See presentation/slides.pdf](presentation/) |

---

## ⚠️ Known Limitations


- Telemetry Scope: Currently models a limited set of lithography, etch, and CMP sensor variables, whereas production fabs ingest thousands of telemetry channels.

- Synthetic Calibration: Uses synthetic semiconductor telemetry datasets instead of proprietary foundry production data.
- Local MCP Deployment: FastMCP server currently runs locally and is not deployed as a distributed production-scale service.
Show more lines
---

## 🏅 What We're Most Proud Of

We are most proud of integrating semiconductor domain knowledge with IBM Bob MCP workflows. Rather than building a passive analytics dashboard, WaferPulse delivers actionable root-cause diagnostics, batch risk assessment, and conversational fab triage capabilities through IBM Bob integration.

---
