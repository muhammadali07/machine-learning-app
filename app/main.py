import requests
from fastapi import FastAPI, Depends, HTTPException
from api import api_predict, api_auth, api_users, api_system

# Inisialisasi FastAPI
app = FastAPI(
    title="Obesity Classification API",
    description="API for obesity prediction, meal time reminders, history, and barcode scanning.",
    version="1.0.0"
)

app.include_router(api_auth.router)
app.include_router(api_predict.router)
app.include_router(api_users.router)
app.include_router(api_system.router)