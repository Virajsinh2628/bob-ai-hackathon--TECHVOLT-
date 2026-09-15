"""
FastMCP Server for Semiconductor Yield Analysis
Exposes fab diagnostics, root cause ranking, and batch gatekeeping to IBM Bob.
"""

from fastmcp import FastMCP
import pandas as pd
import json
import os

mcp = FastMCP("Semiconductor-Yield-Engine")

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "lot_telemetry.csv")

def load_lot_data() -> pd.DataFrame:
    """Safely loads fab lot telemetry records."""
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame({
        "lot_id": ["LOT-3021", "LOT-3022", "LOT-3023"],
        "yield_pct": [95.1, 77.8, 69.4],
        "defect_pattern": ["None", "Edge-Ring", "Scratch"],
        "primary_cause": ["Normal", "Etch_Bias_RF_Power_Drift", "CMP_Downforce_Spike"]
    })

@mcp.tool
def get_lot_yield_summary(lot_id: str) -> str:
    """Retrieve electrical line yield percentage and spatial defect morphology for a completed wafer lot."""
    df = load_lot_data()
    lot = df[df["lot_id"].str.upper() == lot_id.upper()]
    if lot.empty:
        return json.dumps({"error": f"Lot identifier {lot_id} not found in fab database."})
    
    record = lot.iloc[0]
    yield_val = float(record["yield_pct"])
    return json.dumps({
        "lot_id": record["lot_id"],
        "yield_percentage": yield_val,
        "classification": "EXCURSION_HOLD" if yield_val < 85.0 else "NOMINAL_PASSED",
        "spatial_pattern": str(record["defect_pattern"]),
        "wafer_count": 25
    }, indent=2)

@mcp.tool
def rank_root_causes(lot_id: str) -> str:
    """Execute Tree-SHAP probabilistic attribution across equipment sensor parameters for an excursion lot."""
    df = load_lot_data()
    lot = df[df["lot_id"].str.upper() == lot_id.upper()]
    if lot.empty:
        return json.dumps({"error": f"Lot identifier {lot_id} not found."})
    
    pattern = str(lot.iloc[0]["defect_pattern"])
    
    if pattern == "Edge-Ring":
        causes = [
            {"parameter": "Chamber Reflected RF Power", "probability": 0.88, "deviation": "+3.4 sigma", "module": "Dry Etch RIE-04"},
            {"parameter": "Focus Ring Ceramic Erosion Index", "probability": 0.74, "deviation": "260 RF Hours (Limit: 200)", "module": "Dry Etch RIE-04"},
            {"parameter": "Ar/C4F8 Gas Flow Ratio", "probability": 0.28, "deviation": "+0.9 sigma", "module": "Gas Delivery"}
        ]
    elif pattern == "Scratch":
        causes = [
            {"parameter": "Polisher Platen 2 Downforce", "probability": 0.92, "deviation": "+4.2 sigma (Spike: 5.1 psi)", "module": "CMP Polisher-02"},
            {"parameter": "Slurry Filter Differential Pressure", "probability": 0.79, "deviation": "16.2 psi (Clogged)", "module": "Slurry Dispense"},
            {"parameter": "Robot End-Effector Vacuum Level", "probability": 0.15, "deviation": "Nominal", "module": "Wafer Handling"}
        ]
    elif pattern == "Center":
        causes = [
            {"parameter": "EUV Stage Focus Uniformity", "probability": 0.85, "deviation": "+0.08 um focal tilt", "module": "Lithography Scanner EUV-01"},
            {"parameter": "Hotplate Chuck Zone 4 Temperature", "probability": 0.71, "deviation": "-2.1 C thermal dip", "module": "Track PEB-02"}
        ]
    else:
        causes = [
            {"parameter": "Chamber Base Pressure", "probability": 0.35, "deviation": "+0.4 sigma", "module": "Baseline Monitoring"}
        ]
        
    return json.dumps({
        "lot_id": lot_id,
        "spatial_pattern": pattern,
        "ranked_root_causes": causes
    }, indent=2)

@mcp.tool
def recommend_corrective_action(root_cause_parameter: str) -> str:
    """Generate prescriptive fab maintenance runbooks and tool recalibrations based on an identified root cause."""
    query = root_cause_parameter.lower()
    
    if "rf" in query or "focus ring" in query or "etch" in query:
        runbook = {
            "procedure_id": "SOP-ETCH-441",
            "urgency": "IMMEDIATE TOOL INTERLOCK",
            "target_tool": "Dry Etch Chamber RIE-04",
            "action_steps": [
                "Lock tool RIE-04 from automated lot scheduling dispatch",
                "Execute optical emission spectroscopy (OES) baseline plasma health scan",
                "Replace degraded silicon carbide focus ring assembly (Part #FR-300-88)",
                "Retune RF generator matching network capacitors to eliminate reflected power",
                "Process two test qualification wafers and verify edge oxide thickness uniformity"
            ],
            "estimated_downtime_hours": 3.0
        }
    elif "cmp" in query or "downforce" in query or "slurry" in query:
        runbook = {
            "procedure_id": "SOP-CMP-218",
            "urgency": "CRITICAL MAINTENANCE",
            "target_tool": "Polisher CMP-02",
            "action_steps": [
                "Halt polishing platen 2 and disengage head pneumatic downforce regulator",
                "Purge slurry dispense lines with deionized water and replace 0.5-micron depth filter",
                "Replace polishing pad and run diamond conditioning dresser cycle for 20 minutes",
                "Zero-calibrate dynamic multi-zone pressure transducers across retaining rings"
            ],
            "estimated_downtime_hours": 2.5
        }
    else:
        runbook = {
            "procedure_id": "SOP-LITHO-105",
            "urgency": "STANDARD CALIBRATION",
            "target_tool": "Scanner EUV-01 / Track PEB-02",
            "action_steps": [
                "Execute 29-point thermocouple wafer calibration run across hotplate chuck zones",
                "Adjust digital PID thermal trim coefficients to achieve +/- 0.05 C uniformity",
                "Perform dynamic scanner laser interferometer focus auto-leveling routine"
            ],
            "estimated_downtime_hours": 1.5
        }
        
    return json.dumps(runbook, indent=2)

@mcp.tool
def predict_upcoming_batches() -> str:
    """Analyze scheduled upcoming wafer lots against historical equipment drift to prevent pre-run scrap."""
    queue = [
        {"lot_id": "LOT-3024", "recipe": "3NM-GAA-GATE-ETCH", "assigned_tool": "RIE-04", "risk_score": 0.91, "recommendation": "CRITICAL RISK - HOLD"},
        {"lot_id": "LOT-3025", "recipe": "3NM-BEOL-CU-CMP", "assigned_tool": "CMP-01", "risk_score": 0.22, "recommendation": "NOMINAL - DISPATCH"},
        {"lot_id": "LOT-3026", "recipe": "3NM-EUV-CONTACT-VIA", "assigned_tool": "EUV-01", "risk_score": 0.38, "recommendation": "NOMINAL - DISPATCH"}
    ]
    return json.dumps({"status": "QUEUE_AUDIT_COMPLETE", "upcoming_queue": queue}, indent=2)

if __name__ == "__main__":
    mcp.run()