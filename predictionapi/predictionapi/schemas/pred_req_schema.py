from pydantic import BaseModel
from datetime import datetime, date


class PredictionReq(BaseModel):
    id: int
    name: str