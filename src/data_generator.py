# src/data_generator.py
import numpy as np
import pandas as pd
import os

def generate_fab_dataset(num_lots=120, output_csv="src/data/lot_telemetry.csv"):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    np.random.seed(42)
    
    records = []
    patterns = ["None", "Edge-Ring", "Center", "Scratch", "Donut", "Random"]
    
    for i in range(1, num_lots + 1):
        lot_id = f"LOT-{3000 + i}"
        pattern = np.random.choice(patterns, p=[0.45, 0.18, 0.12, 0.10, 0.08, 0.07])
        
        # Baseline process parameters for 3nm node
        euv_dose = np.random.normal(45.0, 0.7)          # mJ/cm2
        euv_focus = np.random.normal(0.0, 0.015)        # um
        etch_rf_power = np.random.normal(1200, 12)      # Watts
        etch_ref_power = np.random.normal(14, 1.5)      # Watts
        etch_pressure = np.random.normal(10.0, 0.25)    # mTorr
        cmp_downforce = np.random.normal(2.4, 0.08)     # psi
        cmp_slurry_flow = np.random.normal(200, 4.0)    # ml/min
        hotplate_temp = np.random.normal(110.0, 0.15)   # deg C
        
        # Inject physical failure modes
        if pattern == "Edge-Ring":
            etch_ref_power += np.random.uniform(12, 26)  # Focus ring erosion
            etch_rf_power += np.random.uniform(45, 85)
            yield_pct = np.clip(np.random.normal(76.5, 2.5), 62.0, 83.0)
            primary_cause = "Etch_Bias_RF_Power_Drift"
        elif pattern == "Center":
            euv_focus += np.random.uniform(0.07, 0.14)   # Scanner focal tilt
            hotplate_temp -= np.random.uniform(1.4, 2.8)
            yield_pct = np.clip(np.random.normal(78.5, 2.0), 66.0, 82.5)
            primary_cause = "Litho_Focus_PEB_Gradient"
        elif pattern == "Scratch":
            cmp_downforce += np.random.uniform(1.8, 3.2) # CMP pressure spike
            cmp_slurry_flow -= np.random.uniform(35, 65)
            yield_pct = np.clip(np.random.normal(70.5, 3.5), 54.0, 79.0)
            primary_cause = "CMP_Downforce_Spike"
        elif pattern == "Donut":
            etch_pressure += np.random.uniform(2.2, 4.5)
            yield_pct = np.clip(np.random.normal(80.5, 1.8), 73.0, 84.5)
            primary_cause = "CVD_Showerhead_Pressure_Imbalance"
        elif pattern == "Random":
            yield_pct = np.clip(np.random.normal(83.0, 3.0), 71.0, 87.0)
            primary_cause = "Airborne_Particle_Contamination"
        else:
            yield_pct = np.clip(np.random.normal(95.8, 1.2), 92.5, 99.2)
            primary_cause = "Nominal_Baseline"

        records.append({
            "lot_id": lot_id,
            "yield_pct": round(yield_pct, 2),
            "defect_pattern": pattern,
            "primary_cause": primary_cause,
            "euv_dose": round(euv_dose, 3),
            "euv_focus": round(euv_focus, 4),
            "etch_rf_power": round(etch_rf_power, 2),
            "etch_ref_power": round(etch_ref_power, 2),
            "etch_pressure": round(etch_pressure, 3),
            "cmp_downforce": round(cmp_downforce, 3),
            "cmp_slurry_flow": round(cmp_slurry_flow, 2),
            "hotplate_temp": round(hotplate_temp, 2)
        })
        
    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    print(f"Success: Fab dataset generated at {output_csv} with {len(df)} lots.")

if __name__ == "__main__":
    generate_fab_dataset()