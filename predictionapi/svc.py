# #UNCOMMENT BELOW 2 LINES IF RUNNING LOCALLY
# from dotenv import load_dotenv
# load_dotenv(dotenv_path = '.env')
import os
print(os.listdir('.'))
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

# from fastapi import FastAPI

# app = FastAPI()

# def add(a,b):
