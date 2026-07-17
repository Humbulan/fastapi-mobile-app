import os
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException
import uvicorn

app = FastAPI()
SECRET_KEY = os.getenv("YOCO_SECRET_KEY")

@app.post("/yoco-webhook")
async def yoco_webhook(request: Request):
    # Logic to verify payload and update MariaDB will go here
    print("Webhook received!")
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

