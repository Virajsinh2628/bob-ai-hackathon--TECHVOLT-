import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import shap
import os

FEATURE_COLS = [
    "euv_dose", "euv_focus", "etch_rf_power", "etch_ref_power",
    "etch_pressure", "cmp_downforce", "cmp_slurry_flow", "hotplate_temp"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA_PATH = os.path.join(BASE_DIR, "data", "lot_telemetry.csv")

class YieldAnalysisEngine:
    def __init__(self, data_path=DEFAULT_DATA_PATH):
        self.data_path = data_path
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.explainer = None
        self.df = None
        self._initialize_engine()
        
    def _initialize_engine(self):
        if not os.path.exists(self.data_path):
            try:
                from data_generator import generate_fab_dataset
            except ImportError:
                from src.data_generator import generate_fab_dataset
            generate_fab_dataset(output_csv=self.data_path)
            
        self.df = pd.read_csv(self.data_path)
        X = self.df[FEATURE_COLS]
        y = self.df["yield_pct"]
        self.model.fit(X, y)
        self.explainer = shap.TreeExplainer(self.model)
        
    def explain_lot(self, lot_id: str):
        subset = self.df[self.df["lot_id"].str.upper() == lot_id.upper()]
        if subset.empty:
            return None
            
        X_sample = subset[FEATURE_COLS]
        shap_values = self.explainer.shap_values(X_sample)[0]
        
        feature_impacts = []
        for feature, recorded_val, shap_val in zip(FEATURE_COLS, X_sample.values[0], shap_values):
            feature_impacts.append({
                "parameter": feature,
                "value": round(recorded_val, 3),
                "shap_impact": round(shap_val, 3),
                "yield_penalty": bool(shap_val < 0)
            })
            
        feature_impacts.sort(key=lambda item: item["shap_impact"])
        return {
            "lot_id": lot_id,
            "actual_yield": float(subset["yield_pct"].values[0]),
            "defect_pattern": str(subset["defect_pattern"].values[0]),
            "ranked_factors": feature_impacts
        }

    def predict_upcoming_risk(self, recipe_parameters: dict) -> dict:
        df_input = pd.DataFrame([recipe_parameters])[FEATURE_COLS]
        pred_yield = self.model.predict(df_input)[0]
        
        if pred_yield < 80.0:
            risk = "CRITICAL"
            hold = True
        elif pred_yield < 87.0:
            risk = "ELEVATED"
            hold = False
        else:
            risk = "NOMINAL"
            hold = False
            
        return {
            "predicted_yield": round(pred_yield, 2),
            "risk_level": risk,
            "hold_recommended": hold
        }