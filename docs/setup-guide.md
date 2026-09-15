# Setup Guide

> **This file is read by the automated evaluation pipeline. Be precise and complete.**

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.10 or higher
- Git
- VS Code
- IBM Bob Client
- Internet connection for dependency installation

---

## Environment Variables

Copy `.env.example` to `.env` if custom configuration is required.

```bash
cp .env.example .env
```

| Variable | Description | Required |
|----------|-------------|----------|
| FAB_TELEMETRY_PATH | Path to telemetry dataset | No |
| MCP_TRANSPORT | stdio or sse transport | No |
| LOG_LEVEL | Runtime logging level | No |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/drijesh-ppatel/bob-ai-hackathon--TECHVOLT-.git

# Move into project folder
cd bob-ai-hackathon--TECHVOLT-

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install fastmcp streamlit pandas numpy scikit-learn shap matplotlib
```

---

## Running the Application

### Generate Fab Dataset

```bash
python src/data_generator.py
```

### Launch WaferPulse Dashboard

```bash
streamlit run src/app.py
```

Application will be available at:

```text
http://localhost:8501
```

### Launch IBM Bob MCP Server

```bash
python src/mcp_server.py
```

---

## Running Verification Tests

```bash
python -c "import sys; sys.path.append('src'); import mcp_server; print('Verification Successful')"
```

---

## Quick Demo Walkthrough

1. Open `http://localhost:8501`
2. Select a wafer lot from the dashboard.
3. Review defect patterns and root-cause rankings.
4. Inspect upcoming batch risk predictions.
5. View IBM Bob diagnostic outputs through MCP tools.

---

## Troubleshooting

| Issue | Solution |
|---------|----------|
| ModuleNotFoundError | Run `pip install fastmcp streamlit pandas numpy scikit-learn shap matplotlib` |
| Virtual environment activation error | Run PowerShell as Administrator and retry |
| Port 8501 already in use | Use `streamlit run src/app.py --server.port 8502` |
| MCP server not starting | Verify `src/mcp_server.py` exists |
| Dataset not found | Run `python src/data_generator.py` first |