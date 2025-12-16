from typing import List

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/aggregate")
def aggregate(updates: List[dict]):
    if len(updates) == 0:
        raise HTTPException(status_code=400, detail="No updates provided")
    w_avg = sum(u["w"] for u in updates) / len(updates)
    b_avg = sum(u["b"] for u in updates) / len(updates)
    return {"w": w_avg, "b": b_avg}
