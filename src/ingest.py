import pandas as pd
import numpy as np
from datetime import datetime
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'metadata', 'air_quality.csv')
SOURCE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'AirQualityUCI.csv')
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

def fetch_data():
    df = pd.read_csv(SOURCE_PATH, sep=';', decimal=',')
    df = df.dropna(axis=1, how='all').dropna()
    df = df.select_dtypes(include=[np.number])

    # --- inject small random noise each run ---
    drift_factor = np.random.normal(1.0, 0.05)  # ±5% change
    df *= drift_factor

    df = df.sample(2000, random_state=None)
    df['timestamp'] = datetime.now().isoformat()
    df.to_csv(DATA_PATH, index=False)
    print(f"Air quality data saved with drift factor {drift_factor:.3f}")

if __name__ == "__main__":
    fetch_data()