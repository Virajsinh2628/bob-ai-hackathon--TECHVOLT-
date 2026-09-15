import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from model_engine import YieldAnalysisEngine

st.set_page_config(page_title="FabOps AI - Wafer Yield Analyser", layout="wide")

st.title("Semiconductor Wafer Yield & Root Cause Analyser")
st.caption("3nm/5nm Sub-Node Defect Pattern Classifier & Batch Interlock Engine")

@st.cache_resource
def load_engine():
    return YieldAnalysisEngine()

engine = load_engine()
df = engine.df

st.sidebar.header("Wafer Lot Selector (Historical)")
lot_ids = df["lot_id"].tolist()
selected_lot = st.sidebar.selectbox("Select Processed Lot ID", lot_ids, index=1)

lot_row = df[df["lot_id"] == selected_lot].iloc[0]
k1, k2, k3, k4 = st.columns(4)
k1.metric("Lot ID", str(lot_row["lot_id"]))
k2.metric("Line Yield", f"{lot_row['yield_pct']}%", delta=f"{round(lot_row['yield_pct'] - 92.0, 1)}% vs target")
k3.metric("Defect Topology", str(lot_row["defect_pattern"]))
k4.metric("Status", "HOLD EXCURSION" if lot_row["yield_pct"] < 85.0 else "NOMINAL PASSED")

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"Wafer Map: {lot_row['defect_pattern']} ({lot_row['lot_id']})")
    grid_size = 40
    wafer_map = np.zeros((grid_size, grid_size))
    y_coords, x_coords = np.ogrid[-grid_size//2:grid_size//2, -grid_size//2:grid_size//2]
    circular_mask = x_coords**2 + y_coords**2 <= (grid_size//2 - 1)**2
    wafer_map[circular_mask] = 1
    
    current_pattern = str(lot_row["defect_pattern"])
    if current_pattern == "Edge-Ring":
        edge_ring_mask = (x_coords**2 + y_coords**2 >= (grid_size//2 - 5)**2) & circular_mask
        wafer_map[edge_ring_mask] = 0
    elif current_pattern == "Center":
        center_mask = (x_coords**2 + y_coords**2 <= (grid_size//5)**2) & circular_mask
        wafer_map[center_mask] = 0
    elif current_pattern == "Scratch":
        for pos in range(8, 32):
            if pos < grid_size:
                wafer_map[pos, pos] = 0
    elif current_pattern == "Donut":
        donut_mask = (x_coords**2 + y_coords**2 >= (grid_size//6)**2) & (x_coords**2 + y_coords**2 <= (grid_size//3)**2) & circular_mask
        wafer_map[donut_mask] = 0
    elif current_pattern == "Random":
        np.random.seed(int(str(lot_row["lot_id"]).split("-")[-1]))
        rand_pts = (np.random.rand(grid_size, grid_size) < 0.08) & circular_mask
        wafer_map[rand_pts] = 0
            
    fig_map, ax_map = plt.subplots(figsize=(4, 4))
    ax_map.imshow(wafer_map, cmap="RdYlGn", vmin=0, vmax=1)
    ax_map.axis("off")
    st.pyplot(fig_map)

with col2:
    st.subheader("Tree-SHAP Root Cause Attribution")
    analysis = engine.explain_lot(selected_lot)
    if analysis:
        df_shap = pd.DataFrame(analysis["ranked_factors"])
        fig_shap, ax_shap = plt.subplots(figsize=(6, 4))
        bar_colors = ["#d9534f" if val < 0 else "#5cb85c" for val in df_shap["shap_impact"]]
        ax_shap.barh(df_shap["parameter"], df_shap["shap_impact"], color=bar_colors)
        ax_shap.set_xlabel("Marginal Yield Impact (% Delta)")
        st.pyplot(fig_shap)

st.divider()
st.subheader("Upcoming Batch Pre-Run Gatekeeper (Pre-Dispatch Simulator)")

s1, s2, s3 = st.columns(3)
val_dose = s1.slider("EUV Scanner Dose (mJ/cm2)", 35.0, 55.0, 45.0)
val_focus = s2.slider("EUV Stage Focus (um)", -0.2, 0.2, 0.0)
val_ref_power = s3.slider("Chamber Reflected RF Power (W)", 10.0, 50.0, 15.0)

incoming_recipe = {
    "euv_dose": val_dose,
    "euv_focus": val_focus,
    "etch_ref_power": val_ref_power,
    "etch_rf_power": 1200.0 + (val_ref_power - 15.0) * 3.5,
    "etch_pressure": 10.0,
    "cmp_downforce": 2.4,
    "cmp_slurry_flow": 200.0,
    "hotplate_temp": 110.0
}

risk_result = engine.predict_upcoming_risk(incoming_recipe)
pred_val = risk_result["predicted_yield"]

if pred_val < 85.0:
    st.error(f"PRE-RUN INTERLOCK ACTIVE: Predicted Yield is {pred_val}% (CRITICAL RISK). Chamber RF reflected power drift indicates degraded focus ring. Scrap hold applied before dispatch!")
elif pred_val < 91.0:
    st.warning(f"ELEVATED DRIFT DETECTED: Predicted Yield is {pred_val}% (ELEVATED RISK). Process engineer review recommended before lot entry.")
else:
    st.success(f"PRE-RUN CHECK PASSED: Predicted Yield is {pred_val}% (NOMINAL). Recipe approved for automated dispatch.")