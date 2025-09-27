from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pandas as pd
import os

# --- 1. Pydantic model for request validation ---
class CheckRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

# --- 2. Create the FastAPI App and Enable CORS ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. Load data ONCE when the app starts, not on every request ---
try:
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "q-vercel-latency.json")
    telemetry_df = pd.read_json(file_path)
except Exception as e:
    print(f"Error loading data file: {e}")
    telemetry_df = pd.DataFrame()

# --- 4. The API Endpoint (now at the root "/") ---
@app.post("/")
async def get_latency_stats(data: CheckRequest):
    if telemetry_df.empty:
        return {"error": "Server is missing the telemetry data file."}, 500

    results_list = []

    for region in data.regions:
        region_df = telemetry_df[telemetry_df['region'] == region]

        if not region_df.empty:
            # Using pandas is much cleaner and more efficient
            avg_latency = round(region_df['latency_ms'].mean(), 2)
            p95_latency = round(region_df['latency_ms'].quantile(0.95), 2)
            avg_uptime = round(region_df['uptime_pct'].mean(), 3)
            breaches = int((region_df['latency_ms'] > data.threshold_ms).sum())

            # --- 5. The response format must be a LIST of objects ---
            results_list.append({
                "region": region,
                "avg_latency": avg_latency,
                "p95_latency": p95_latency,
                "avg_uptime": avg_uptime,
                "breaches": breaches,
            })

    return {"regions": results_list}
