from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import uvicorn

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import utils

app = FastAPI()

# ✅ ADD CORS MIDDLEWARE HERE (before any endpoints)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

utils.load_model()

class HouseData(BaseModel):
    location: str
    sqft: float
    bhk: int
    bath: int
    
@app.get('/')
def index():
    return {"message": 'Hello, Friends!'}

@app.get("/locations")
def get_locations():
    locations = utils.get_location_names()
    return {"locations": locations}

@app.post("/predict")
def predict_price(data: HouseData):
    price = utils.get_estimated_price(
        location=data.location,
        sqft=data.sqft,
        bhk=data.bhk,
        bath=data.bath
    )
    return {
        "estimated_price": price
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)