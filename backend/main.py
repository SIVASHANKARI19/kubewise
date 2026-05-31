from fastapi import FastAPI, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import random

app = FastAPI()

REQUEST_COUNT = Counter("kubewise_requests_total", "Total request count", ["endpoint"])
CPU_GAUGE = Gauge("kubewise_cpu_usage", "Simulated CPU usage")
MEMORY_GAUGE = Gauge("kubewise_memory_usage_mb", "Simulated memory usage")

@app.get("/")
def root():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return {"message": "KubeWise AI Backend Running"}

@app.get("/metrics")
def metrics():
    REQUEST_COUNT.labels(endpoint="/metrics").inc()
    cpu = round(random.uniform(0.2, 0.9), 2)
    mem = random.randint(400, 700)
    CPU_GAUGE.set(cpu)
    MEMORY_GAUGE.set(mem)
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/recommendation")
def recommendation():
    REQUEST_COUNT.labels(endpoint="/recommendation").inc()
    return {"cpu_requested": 4, "cpu_actual": 0.4, "recommended_cpu": 1, "savings_percent": 75}
