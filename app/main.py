import requests
from fastapi import FastAPI, Depends, HTTPException
from schema import User, InputModel, Login
from helpers import (
    JWTBearer, create_jwt_token, 
    decode_jwt, configure_firebase,
    get_current_active_user,
    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI
)

import tensorflow as tf
import numpy as np
import pickle



# service_account_path
service_account_path = "./helpers/serviceAccountKey.json"

# Inisialisasi Firebase
db = None
try:
    db = configure_firebase(service_account_path)
    db = db.collection("users")
except Exception as e:
    print(f"Gagal menginisialisasi Firebase: {e}")
    db = None


# Dependency Instance
jwt_bearer = JWTBearer()

# Inisialisasi FastAPI
app = FastAPI()

# Load TensorFlow Model
model = tf.keras.models.load_model("model/obesity_prediction_model.h5")

# ------------------- Endpoints ------------------- #

@app.post("/auth/register")
async def create_user(user: User):
    # Check if user exists
    if db.document(user.username).get().exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Add user to Firebase
    db.document(user.username).set({
        "username": user.username,
        "password": user.password,
        "email": user.email,
        "age": user.age,
        "gender": user.gender,
        "height": user.height,
        "weight": user.weight
    })
    return {"message": "User created successfully"}


@app.post("/auth/login")
async def login(user: Login):
    # Check credentials
    user_data = db.document(user.username).get()
    if not user_data.exists or user_data.to_dict().get("password") != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate JWT token
    token = create_jwt_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/auth/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }

@app.get("/auth/google")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    return user_info.json()


@app.get("/users/list")
async def get_users(
    token: str = Depends(jwt_bearer),
):
    try:
        users = db.stream()
        # Konversi setiap dokumen ke dictionary
        all_users = [user.to_dict() for user in users]

        if not all_users:
            raise HTTPException(status_code=404, detail="Tidak ada data pengguna yang ditemukan.")

        return {"users": all_users}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kesalahan server: {e}")

    

@app.get("/profile")
async def get_profile(
    token: str = Depends(jwt_bearer),
    current_user: dict = Depends(get_current_active_user)
    ):
    """
    Mendapatkan profil pengguna berdasarkan JWT token.
    """
    email = current_user.get('sub')
    try:
        # Ambil data pengguna dari Firestore
        user_doc = db.document(email).get()

        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan.")

        return user_doc.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kesalahan server: {e}")


@app.put("/profile")
async def update_profile(
    profile: User, 
    token: str = Depends(jwt_bearer),
    current_user: dict = Depends(get_current_active_user)
    ):
    """
    Memperbarui profil pengguna berdasarkan JWT token.
    """
    email = current_user.get('sub')
    try:
        # Perbarui data pengguna di Firestore
        user_ref = db.document(email)
        user_doc = user_ref.get()

        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan.")

        # Perbarui data pengguna
        user_ref.update(profile.dict())
        return {"message": "Profil berhasil diperbarui."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kesalahan server: {e}")


@app.post("/predict/", dependencies=[Depends(JWTBearer())])
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
