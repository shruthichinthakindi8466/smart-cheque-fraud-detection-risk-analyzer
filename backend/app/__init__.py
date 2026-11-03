from fastapi import FastAPI

app = FastAPI(title="Smart Cheque Fraud Detection API")

@app.get("/health")
def health_check():
    return {"status": "ok"}
