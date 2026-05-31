from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "KubeWise AI Backend Running"}

@app.get("/metrics")
def metrics():
    return {
        "cpu_usage": 0.4,
        "memory_usage": 512,
        "status": "healthy"
    }

@app.get("/recommendation")
def recommend():
    return {
        "cpu_requested": 4,
        "cpu_actual": 0.4,
        "recommended_cpu": 1,
        "savings_percent": 75
    }