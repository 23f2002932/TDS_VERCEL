import json
from http.server import BaseHTTPRequestHandler
import numpy as np

# The JSON data is now embedded directly in the code
telemetry_data = [
  {
    "region": "apac", "service": "analytics", "latency_ms": 225.55,
    "uptime_pct": 98.427, "timestamp": 20250301
  },
  {
    "region": "apac", "service": "analytics", "latency_ms": 197.32,
    "uptime_pct": 99.212, "timestamp": 20250302
  },
  {
    "region": "apac", "service": "support", "latency_ms": 183.88,
    "uptime_pct": 99.072, "timestamp": 20250303
  },
  {
    "region": "apac", "service": "payments", "latency_ms": 183.52,
    "uptime_pct": 98.291, "timestamp": 20250304
  },
  {
    "region": "apac", "service": "catalog", "latency_ms": 164.73,
    "uptime_pct": 98.234, "timestamp": 20250305
  },
  {
    "region": "apac", "service": "payments", "latency_ms": 174.03,
    "uptime_pct": 97.972, "timestamp": 20250306
  },
  {
    "region": "apac", "service": "support", "latency_ms": 224.51,
    "uptime_pct": 98.665, "timestamp": 20250307
  },
  {
    "region": "apac", "service": "checkout", "latency_ms": 184.65,
    "uptime_pct": 98.221, "timestamp": 20250308
  },
  {
    "region": "apac", "service": "analytics", "latency_ms": 130.37,
    "uptime_pct": 97.592, "timestamp": 20250309
  },
  {
    "region": "apac", "service": "support", "latency_ms": 165.67,
    "uptime_pct": 98.896, "timestamp": 20250310
  },
  {
    "region": "apac", "service": "payments", "latency_ms": 188.97,
    "uptime_pct": 97.718, "timestamp": 20250311
  },
  {
    "region": "apac", "service": "payments", "latency_ms": 123.37,
    "uptime_pct": 97.731, "timestamp": 20250312
  },
  {
    "region": "emea", "service": "checkout", "latency_ms": 133.02,
    "uptime_pct": 98.028, "timestamp": 20250301
  },
  {
    "region": "emea", "service": "catalog", "latency_ms": 169.84,
    "uptime_pct": 99.109, "timestamp": 20250302
  },
  {
    "region": "emea", "service": "payments", "latency_ms": 154.18,
    "uptime_pct": 97.394, "timestamp": 20250303
  },
  {
    "region": "emea", "service": "checkout", "latency_ms": 195.82,
    "uptime_pct": 98.972, "timestamp": 20250304
  },
  {
    "region": "emea", "service": "support", "latency_ms": 144.93,
    "uptime_pct": 97.49, "timestamp": 20250305
  },
  {
    "region": "emea", "service": "analytics", "latency_ms": 160.15,
    "uptime_pct": 97.653, "timestamp": 20250306
  },
  {
    "region": "emea", "service": "payments", "latency_ms": 100.9,
    "uptime_pct": 97.399, "timestamp": 20250307
  },
  {
    "region": "emea", "service": "analytics", "latency_ms": 164.21,
    "uptime_pct": 98.377, "timestamp": 20250308
  },
  {
    "region": "emea", "service": "checkout", "latency_ms": 165.87,
    "uptime_pct": 98.908, "timestamp": 20250309
  },
  {
    "region": "emea", "service": "analytics", "latency_ms": 196.88,
    "uptime_pct": 97.614, "timestamp": 20250310
  },
  {
    "region": "emea", "service": "analytics", "latency_ms": 145.07,
    "uptime_pct": 98.827, "timestamp": 20250311
  },
  {
    "region": "emea", "service": "checkout", "latency_ms": 232.59,
    "uptime_pct": 99.194, "timestamp": 20250312
  },
  {
    "region": "amer", "service": "analytics", "latency_ms": 195.24,
    "uptime_pct": 97.459, "timestamp": 20250301
  },
  {
    "region": "amer", "service": "payments", "latency_ms": 176.28,
    "uptime_pct": 98.3, "timestamp": 20250302
  },
  {
    "region": "amer", "service": "payments", "latency_ms": 153.44,
    "uptime_pct": 97.598, "timestamp": 20250303
  },
  {
    "region": "amer", "service": "checkout", "latency_ms": 132.69,
    "uptime_pct": 98.214, "timestamp": 20250304
  },
  {
    "region": "amer", "service": "recommendations", "latency_ms": 194.49,
    "uptime_pct": 97.514, "timestamp": 20250305
  },
  {
    "region": "amer", "service": "recommendations", "latency_ms": 175.57,
    "uptime_pct": 97.756, "timestamp": 20250306
  },
  {
    "region": "amer", "service": "payments", "latency_ms": 107.35,
    "uptime_pct": 98.311, "timestamp": 20250307
  },
  {
    "region": "amer", "service": "support", "latency_ms": 104.89,
    "uptime_pct": 98.197, "timestamp": 20250308
  },
  {
    "region": "amer", "service": "analytics", "latency_ms": 224.83,
    "uptime_pct": 98.185, "timestamp": 20250309
  },
  {
    "region": "amer", "service": "catalog", "latency_ms": 173.78,
    "uptime_pct": 97.919, "timestamp": 20250310
  },
  {
    "region": "amer", "service": "catalog", "latency_ms": 136.74,
    "uptime_pct": 99.219, "timestamp": 20250311
  },
  {
    "region": "amer", "service": "recommendations", "latency_ms": 117.76,
    "uptime_pct": 98.919, "timestamp": 20250312
  }
]

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # This handles the pre-flight request for CORS
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
        self.end_headers()

    def do_POST(self):
        # Read the body of the POST request
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_body = json.loads(post_data)

        regions_to_process = request_body.get("regions", [])
        threshold = request_body.get("threshold_ms", 0)

        results = []

        for region in regions_to_process:
            region_data = [d for d in telemetry_data if d['region'] == region]
            
            if region_data:
                latencies = [d['latency_ms'] for d in region_data]
                uptimes = [d['uptime_pct'] for d in region_data]
                
                avg_latency = round(np.mean(latencies), 2)
                p95_latency = round(np.percentile(latencies, 95), 2)
                avg_uptime = round(np.mean(uptimes), 3)
                breaches = sum(1 for lat in latencies if lat > threshold)

                results.append({
                    "region": region,
                    "avg_latency": avg_latency,
                    "p95_latency": p95_latency,
                    "avg_uptime": avg_uptime,
                    "breaches": breaches,
                })
        
        # Prepare and send the response
        response_data = json.dumps({"regions": results})
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response_data.encode('utf-8'))
