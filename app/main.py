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
        print(f"Dataset berhasil dibaca. Jumlah baris: {len(data)}, Jumlah kolom: {len(data.columns)}")
        return data
    except FileNotFoundError:
        print(f"File tidak ditemukan di lokasi: {file_path}")
    except pd.errors.EmptyDataError:
        print("File CSV kosong.")
    except pd.errors.ParserError as e:
        print(f"Terjadi kesalahan saat memparsing file CSV: {e}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


def compare_numpy_prediction_with_dataset(predicted_array: np.ndarray, dataset: pd.DataFrame, threshold: float = 0.9):
    """
    Membandingkan hasil prediksi numpy array dengan dataset untuk mencari kemiripan.

    Parameters:
        predicted_array (np.ndarray): Array hasil prediksi.
        dataset (pd.DataFrame): Dataset dalam bentuk DataFrame.
        threshold (float): Ambang batas kemiripan (0-1), default adalah 0.9.

    Returns:
        list: Daftar indeks baris dalam dataset yang mirip dengan data prediksi.
    """
    if len(predicted_array) != dataset.shape[1]:
        raise ValueError("Panjang array prediksi tidak sesuai dengan jumlah kolom dataset.")

    similar_rows = []
    for index, row in dataset.iterrows():
        similarity_score = 0
        for i, pred_value in enumerate(predicted_array):
            dataset_value = row[i]
            # Perbandingan data numerik dengan toleransi
            if isinstance(dataset_value, (int, float)) and isinstance(pred_value, (int, float)):
                diff = abs(dataset_value - pred_value)
                if diff <= threshold * max(abs(dataset_value), abs(pred_value), 1):  # Toleransi threshold
                    similarity_score += 1
            # Perbandingan data string
            elif isinstance(dataset_value, str) and isinstance(pred_value, str):
                if dataset_value.lower() == pred_value.lower():
                    similarity_score += 1

        # Hitung skor kemiripan sebagai persentase
        score_percentage = similarity_score / len(predicted_array)
        if score_percentage >= threshold:
            similar_rows.append((index, score_percentage))

    if not similar_rows:
        print("Tidak ada data dalam dataset yang mirip dengan data prediksi.")
    return similar_rows

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
    datasetPath = "dataset/ObesityDataSet_raw_and_data_sinthetic.csv"
    dataset = read_csv_file(datasetPath)

    similar_rows = compare_numpy_prediction_with_dataset(prediction, dataset, threshold=0.8)
    if similar_rows:
        print("Baris yang mirip ditemukan:")
        for index, score in similar_rows:
            print(f"Indeks: {index}, Skor Kemiripan: {score:.2f}")
    print("tipe data hasil model")
    print(type(prediction))


    result = prediction[0][0]  # Assuming binary classification

    return {"prediction": "Overweight" if result > 0.5 else "Not Overweight"}


@app.get("/secure-endpoint/")
async def secure_endpoint(current_user: str = Depends(jwt_bearer)):
    return {"message": f"Hello {current_user}, this is a secure endpoint!"}