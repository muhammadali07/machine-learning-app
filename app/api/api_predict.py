import numpy as np
import pickle

from fastapi import APIRouter, Depends, HTTPException
from helpers import LoadModel, JWTBearer
from schema import InputModel, NutritionAnalyzeRequest, Reminder, ScanInput
from typing import List

router = APIRouter(prefix="/v2/predict", tags=["Prediction"])

model = LoadModel()
reminders = []


@router.post("/", dependencies=[Depends(JWTBearer())])
async def predict(input_data: InputModel):
    # Prepare input for the TensorFlow model
    input_array = np.array([[
        1 if input_data.gender.lower() == "male" else 0,
        input_data.age,
        input_data.height,
        input_data.weight,
        input_data.family_history,
        input_data.high_calorie_food,
        input_data.vegetable_freq,
        input_data.meals_per_day,
        1 if input_data.food_between_meals.lower() == "yes" else 0,
        input_data.smoking,
        input_data.water_consumption,
        input_data.calorie_monitoring,
        input_data.physical_activity,
        input_data.tech_usage,
        1 if input_data.alcohol_consumption.lower() == "frequent" else 0,
        1 if input_data.transportation.lower() == "car" else 0
    ]])

    # Get prediction
    prediction = model.predict(input_array)
    res = np.array(prediction[0]).argmax()
    resList = pickle.load(open("./dataset/label.pkl", "rb"))

    return {"prediction": resList[res]}


@router.post("/nutrition/analyze", dependencies=[Depends(JWTBearer())])
async def predict(input_data: NutritionAnalyzeRequest):
    food_data = {
        "Chicken Breast": [31, 3.6, 0, 165],  # Example: [protein, fat, carbohydrates, calories]
        "Rice": [2.7, 0.3, 28, 130]
    }
    if input_data.food_name not in food_data:
        raise HTTPException(status_code=404, detail="Food item not found in the database")

    base_value = np.array([[food_data[input_data.food_name]]])
    service_ration = input_data.serving_size / 100
    features = base_value * service_ration

    if model:
        prediction = model.predict(features.reshape(1, -1))
    else:
        prediction = features

    return {
        "food_name": data.food_name,
        "serving_size": data.serving_size,
        "nutrition": {
            "calories": round(prediction[3], 2),
            "protein": round(prediction[0], 2),
            "carbohydrates": round(prediction[2], 2),
            "fat": round(prediction[1], 2)
        }
    }

@router.get("/reminder")
async def reminder():
    return {"message": "Reminder"}

@router.post("/reminder/add")
async def reminder_add(reminder: Reminder):
    reminders.append(reminder)
    return {"message": "Reminder added"}


# In-memory storage for simplicity
history = []

@router.get("/history/list", response_model=List[dict])
async def get_history():
    return history

@router.post("/history/add")
async def add_to_history(record: dict):
    history.append(record)
    return {"message": "Record added to history"}

@router.post("/scan/barcode")
async def scan_barcode(scan: ScanInput):
    # Dummy implementation: Simulate barcode lookup
    return {
        "barcode": scan.barcode,
        "item_name": "Sample Food Item",
        "calories": 250
    }