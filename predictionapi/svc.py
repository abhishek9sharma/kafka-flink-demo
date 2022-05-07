import os
from fastapi import FastAPI
from predictionapi.routers import prediction_router

app = FastAPI()


@app.get("/")
def start_svc():
    return {"Info": "Prediction Service is running"}


app.include_router(
    prediction_router.router,
    tags=['make predictions']
)
