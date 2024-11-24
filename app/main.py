from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from typing import Optional
from firebase_admin import credentials, firestore, initialize_app
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle


# Inisialisasi Firebase
cred = credentials.Certificate("serviceAccountKey.json")

import os

print(os.path.exists("serviceAccountKey.json"))


initialize_app(cred)
db = firestore.client()
user_ref = db.collection('users')

# Konfigurasi JWT
# Konfigurasi JWT
SECRET_KEY = "your_jwt_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Inisialisasi FastAPI
app = FastAPI()

# Load TensorFlow Model
model = tf.keras.models.load_model("model/obesity_prediction_model.h5")


# ------------------- Models ------------------- #
class User(BaseModel):
    username: str
    password: str


class InputModel(BaseModel):
    gender: str
    age: float
    height: float
    weight: float
    family_history: int
    high_calorie_food: int
    vegetable_freq: int
    meals_per_day: float
    food_between_meals: str
    smoking: int
    water_consumption: float
    calorie_monitoring: int
    physical_activity: float
    tech_usage: int
    alcohol_consumption: str
    transportation: str


# ------------------- Auth Utils ------------------- #
# Helper: Membuat token JWT
def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dependency: Validasi token JWT
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, credentials: HTTPAuthorizationCredentials = Depends()):
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Credentials not provided"
            )
        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        except PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token"
            )
        return payload

# Dependency Instance
jwt_bearer = JWTBearer()


# read dataset
def read_csv_file(file_path: str):
    """
    Membaca file dataset CSV dan mengembalikan DataFrame.

    Parameters:
        file_path (str): Path ke file CSV.

    Returns:
        pd.DataFrame: Data dari file CSV dalam bentuk DataFrame.
    """
    try:
        # Membaca file CSV
        data = pd.read_csv(file_path)
        label = data["NObeyesdad"].unique().tolist()



        print(f"Dataset berhasil dibaca. Jumlah baris: {len(data)}, Jumlah kolom: {len(data.columns)}")
        return data, label
    except FileNotFoundError:
        print(f"File tidak ditemukan di lokasi: {file_path}")
    except pd.errors.EmptyDataError:
        print("File CSV kosong.")
    except pd.errors.ParserError as e:
        print(f"Terjadi kesalahan saat memparsing file CSV: {e}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# ------------------- Endpoints ------------------- #

@app.post("/create-user/")
async def create_user(user: User):
    # Check if user exists
    if user_ref.document(user.username).get().exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Add user to Firebase
    user_ref.document(user.username).set({"password": user.password})
    return {"message": "User created successfully"}


@app.post("/login/")
async def login(user: User):
    # Check credentials
    user_data = user_ref.document(user.username).get()
    if not user_data.exists or user_data.to_dict().get("password") != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate JWT token
    token = create_jwt_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/predict/")
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


@app.get("/secure-endpoint/")
async def secure_endpoint(current_user: str = Depends(jwt_bearer)):
    return {"message": f"Hello {current_user}, this is a secure endpoint!"}
