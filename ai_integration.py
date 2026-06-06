from fastapi import FastAPI, HTTPException
import httpx
from datetime import datetime

app = FastAPI(title="Imperial AI Proxy", version="2.0.0")

AI_AGENT_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"

async def fetch_imperial_truth():
    return {
        "valuation": 269903984698.71,
        "villages": 18,
        "target": 900,
        "status": "operational"
    }

@app.get("/")
async def root():
    return {"service": "Imperial AI Proxy", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/ai/health")
async def ai_health_check():
    return {"ai_status": "connected", "model": MODEL_NAME}

@app.get("/integration/status")
async def integration_status():
    truth = await fetch_imperial_truth()
    return {
        "valuation": truth["valuation"],
        "villages": truth["villages"],
        "target": truth["target"],
        "status": truth["status"]
    }

@app.post("/ai/proxy")
async def ai_proxy(payload: dict):
    prompt = payload.get("prompt", "")
    if not prompt:
        raise HTTPException(status_code=400, detail="Missing 'prompt' field")
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            AI_AGENT_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
        )
        if resp.status_code != 200:
            return {"response": f"Error: {resp.text}", "model": MODEL_NAME, "timestamp": datetime.utcnow().isoformat()}
        result = resp.json()
        return {"response": result.get("response", ""), "model": MODEL_NAME, "timestamp": datetime.utcnow().isoformat()}

@app.post("/ai/imperial-chat")
async def imperial_ai_chat(user_message: str):
    truth = await fetch_imperial_truth()
    context = f"Villages: {truth['villages']}/{truth['target']}, Valuation: R{truth['valuation']:,.2f}"
    prompt = f"{context}\n\nUser: {user_message}\nAssistant:"
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            AI_AGENT_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
        )
        if resp.status_code != 200:
            return {"imperial_response": "AI service temporarily unavailable", "error": resp.text, "timestamp": datetime.utcnow().isoformat()}
        result = resp.json()
        return {"imperial_response": result.get("response", ""), "timestamp": datetime.utcnow().isoformat()}

@app.post("/ai/business-chat")
async def ai_business_chat(user_message: str):
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            AI_AGENT_URL,
            json={"model": MODEL_NAME, "prompt": user_message, "stream": False}
        )
        if resp.status_code != 200:
            return {"response": "AI service temporarily unavailable", "error": resp.text, "timestamp": datetime.utcnow().isoformat()}
        result = resp.json()
        return {"response": result.get("response", ""), "model": MODEL_NAME, "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8118)
