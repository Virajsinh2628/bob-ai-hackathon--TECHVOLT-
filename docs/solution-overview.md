# Solution Overview

## What We Built

WaferPulse is an autonomous semiconductor yield diagnostics and pre-dispatch gatekeeping platform designed for advanced 3nm and 5nm fabrication environments.

The platform combines wafer defect pattern analysis, equipment telemetry analytics, explainable machine learning, and IBM Bob integration to help process engineers rapidly identify root causes of yield loss and prevent future wafer scrap.

Instead of manually analyzing thousands of sensor readings and defect maps, engineers can use WaferPulse to receive explainable diagnostics, batch risk assessments, and recommended corrective actions through an interactive dashboard and IBM Bob agent workflows.

---

## How It Works

1. Wafer telemetry and equipment sensor data are collected and normalized.
2. Defect patterns across wafer maps are analyzed and classified into known semiconductor failure signatures.
3. A machine learning model predicts yield performance and identifies at-risk wafer lots.
4. Tree-SHAP explainability techniques rank the sensor parameters contributing most strongly to yield degradation.
5. IBM Bob accesses diagnostic tools through FastMCP integration.
6. Engineers receive automated recommendations and maintenance actions.
7. Upcoming batches are evaluated before processing and high-risk lots are flagged.

---

## Architecture Diagram

> See `architecture.md` for the detailed architecture.

```text
Wafer Telemetry
        |
        v
Data Processing Layer
        |
        v
Machine Learning Engine
        |
        v
Tree-SHAP Attribution
        |
        v
FastMCP Server
        |
        v
IBM Bob
        |
        v
Fab Engineer Dashboard
```

---

## Analytical Pipeline Flow

| Stage | Input | Processing | Output |
|---------|---------|---------|---------|
| Data Collection | Sensor Telemetry | Data Cleaning | Structured Dataset |
| Defect Analysis | Wafer Maps | Pattern Classification | Defect Category |
| Yield Prediction | Process Parameters | Machine Learning | Yield Score |
| Root Cause Analysis | Sensor Data | Tree-SHAP Attribution | Ranked Root Causes |
| Agent Integration | Diagnostic Requests | FastMCP Processing | IBM Bob Responses |
| Pre-Run Validation | New Batch Recipes | Risk Evaluation | Batch Risk Assessment |

---

## Key Design Decisions

| Decision | Rationale |
|-----------|-----------|
| Tree-SHAP Explainability | Provides interpretable explanations for yield degradation rather than black-box predictions |
| IBM Bob + MCP Architecture | Enables conversational diagnostic workflows through a standardized protocol |
| Streamlit Dashboard | Rapid development with strong visualization support |
| Pre-Dispatch Risk Evaluation | Prevents scrap before production instead of reacting afterward |
| Synthetic Semiconductor Dataset | Enables prototyping without requiring proprietary fab data |

---

## IBM Technologies Used

### IBM Bob

IBM Bob serves as the conversational engineering assistant. Engineers can interact with Bob to review yield excursions, investigate equipment behavior, and receive recommended corrective procedures.

### Model Context Protocol (MCP)

FastMCP is used to expose diagnostic semiconductor tools directly to IBM Bob.

The MCP implementation provides the following operational tools:

- `get_lot_yield_summary`
- `rank_root_causes`
- `recommend_corrective_action`
- `predict_upcoming_batches`

These tools allow IBM Bob to retrieve wafer yield summaries, identify root causes, recommend maintenance actions, and predict risk for future manufacturing lots.

---

## Expected Outcomes

WaferPulse helps semiconductor manufacturers:

- Reduce yield loss investigation time.
- Improve root cause identification accuracy.
- Detect equipment degradation earlier.
- Prevent unnecessary wafer scrap.
- Improve manufacturing efficiency through AI-assisted diagnostics.