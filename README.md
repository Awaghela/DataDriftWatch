# DataDriftWatch

**DataDriftWatch** is a lightweight, observability-focused dashboard designed to track **data drift**, **dataset health**, and **quality changes over time**.  
It simulates a real data monitoring pipeline — similar to what modern orchestration platforms like **Dagster**, **Prefect**, or **Airflow** manage in production.

---

## 🔍 Overview

In real-world data systems, subtle changes in data distribution can silently break ML models, dashboards, or decision logic.  
**DataDriftWatch** helps monitor these shifts by:

✅ Ingesting data (batch or simulated streaming)  
✅ Detecting statistical drift using tests like KS-test  
✅ Logging each run with timestamped metadata  
✅ Visualizing drift trends in an interactive Streamlit dashboard

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📁 Data Ingestion | Pulls datasets or simulates time-series updates |
| 📊 Drift Detection | KS-test for distribution shifts across features |
| 📜 Run Logging | JSONL metadata with timestamps & drift metrics |
| 📈 Interactive Dashboard | Streamlit + Plotly visualizations & filters |
| 🚨 Future Ready | Supports alerts, scheduling, Dagster integration |

---

## 🧠 How It Works (Pipeline Concept)

```txt
Ingest Data       →   Validate & Detect Drift   →   Log Run      →   Visualize in UI
 (ingest.py)           (drift_detector.py)          (run_log)        (Streamlit Dashboard)


## 🛠️ Installation & Setup

```bash
# 1️⃣ Clone the Repository
git clone https://github.com/<your-username>/DataDriftWatch.git
cd DataDriftWatch

# 2️⃣ Create Virtual Environment (Optional but Recommended)
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# .\venv\Scripts\activate  # Windows

# 3️⃣ Install Dependencies
pip install -r requirements.txt

# 4️⃣ Run Ingestion (fetch / simulate dataset)
python src/ingest.py

# 5️⃣ Run Drift Detection
python src/drift_detector.py

# 6️⃣ Launch Dashboard
streamlit run dashboard/app.py
