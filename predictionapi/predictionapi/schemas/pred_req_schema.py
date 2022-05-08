from pydantic import BaseModel
from datetime import datetime, date


class PredictionReq(BaseModel):
    transaction_time_since_first_april_2022_00am_in_seconds: int
    transaction_amount: float
    beneficiary: str
    type: str
    country : str