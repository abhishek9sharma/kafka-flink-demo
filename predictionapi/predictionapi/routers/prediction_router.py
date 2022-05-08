#import numpy
#import pandas as pd
import os

from fastapi import APIRouter
from predictionapi.schemas.pred_req_schema import PredictionReq
from predictionapi.model.predictor import *
#from predictionapi.model.predictor import model

router = APIRouter()

@router.post("/predict")
def predict(pred_req: PredictionReq):
    pred_req_dict = pred_req.dict()
    pred_response = get_transaction_prediction(pred_req_dict)
    return pred_response