# FastAPI microservice that exposes a /predict endpoint
from fastapi import FastAPI
from pydantic import BaseModel
import math

app = FastAPI(title="Dynamic Pricing API")

class RequestBody(BaseModel):
    base_price: float
    demand: float
    inventory_level: int
    time_of_day: int  # 0-23

class ResponseBody(BaseModel):
    recommended_price: float
    metadata: dict

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/predict", response_model=ResponseBody)
async def predict(body: RequestBody):
    # simple heuristic + placeholder for ML model
    demand_factor = 1 + (body.demand - 0.5) * 0.5
    inventory_factor = 1.0 if body.inventory_level > 50 else 1.2
    hour_factor = 1.1 if 18 <= body.time_of_day <= 22 else 1.0

    price = body.base_price * demand_factor * inventory_factor * hour_factor

    # floor and round
    price = max(0.01, round(price, 2))

    return ResponseBody(
        recommended_price=price,
        metadata={
            "demand_factor": demand_factor,
            "inventory_factor": inventory_factor,
            "hour_factor": hour_factor
        }
    )

if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
