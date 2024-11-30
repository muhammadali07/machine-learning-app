import requests
from fastapi import APIRouter, Depends, HTTPException
from schema import User, Login
from helpers import (
    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI, configure_firebase,
    create_jwt_token
)
router = APIRouter(prefix="/v2/auth", tags=["Auth User"])


@router.post("/register", )
async def create_user(user: User):
    # Initialising connect to Firebase
    db = configure_firebase()
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


@router.post("/auth/login")
async def login(user: Login):
    # Check credentials
    db = configure_firebase()
    user_data = db.document(user.username).get()
    if not user_data.exists or user_data.to_dict().get("password") != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate JWT token
    token = create_jwt_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/auth/google/login")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }


@router.get("/auth/google/callback")
async def auth_google(code: str):
    db = configure_firebase()
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
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                             headers={"Authorization": f"Bearer {access_token}"})

    # create jwt token
    data = user_info.json()
    email = data.get("email")

    userInfoFirebase = db.document(email).get()
    if not userInfoFirebase.exists:
        dt = {
            "username": data.get(""),
            "password": "1234445",
            "email": email,
            "age": 0,
            "gender": "-",
            "height": 0,
            "weight": 0,
        }
        db.document(email).set(dt)
    jwtToken = create_jwt_token({"sub": email})
    return {"access_token": jwtToken, "token_type": "bearer", "user_info": data}
