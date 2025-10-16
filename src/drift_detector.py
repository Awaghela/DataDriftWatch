import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import os, json
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'metadata', 'air_quality.csv')
META_PATH = os.path.join(os.path.dirname(__file__), '..', 'metadata', 'run_log.jsonl')
os.makedirs(os.path.dirname(META_PATH), exist_ok=True)

def calculate_drift(df):
    scores = {}
    for col in df.columns:
        if col != 'timestamp' and pd.api.types.is_numeric_dtype(df[col]):
            new = df[col].iloc[-500:]
            old = df[col].iloc[:-500]
            stat, p = ks_2samp(new, old)
            scores[col] = round(1 - p, 4)
    return scores

def detect_drift():
    df = pd.read_csv(DATA_PATH)
    drift_scores = calculate_drift(df)
    run_info = {
        "timestamp": datetime.now().isoformat(),
        "n_records": len(df),
        "drift_scores": drift_scores
    }
    with open(META_PATH, 'a') as f:
        f.write(json.dumps(run_info) + "\n")
    print(f"✅ Drift detection complete. Logged metadata to {META_PATH}")

if __name__ == "__main__":
    detect_drift()