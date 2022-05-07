#import numpy
#import pandas as pd
import os

from fastapi import APIRouter
from predictionapi.schemas.pred_req_schema import PredictionReq



router = APIRouter()

@router.post("/predict")
def predict(pred_req: PredictionReq):

    pred_response = {}

    id = pred_req.id
    pred_response = {"id": id, "name": 'hello'}

    return pred_response
