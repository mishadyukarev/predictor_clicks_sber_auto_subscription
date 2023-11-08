from typing import Optional

import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
pipeline = joblib.load('data/main_pipeline')

border_for_prediction_1 = 0.05

class Form(BaseModel):
    visit_date: str
    visit_time: str
    visit_number: int
    utm_source: str
    utm_medium: str
    utm_campaign: str
    utm_adcontent: str
    utm_keyword: Optional[str]
    device_category: str
    device_os: Optional[str]
    device_brand: str
    device_model: Optional[str]
    device_screen_resolution: str
    device_browser: str
    geo_country: str
    geo_city: str


class Prediction(BaseModel):
    result: float


@app.post('/predict', response_model=Prediction)
def predict(form: Form):
    X = pd.DataFrame.from_dict([form.dict()])

    predict_proba = pipeline.predict_proba(X)[:, 1]
    y = [1 if value >= border_for_prediction_1 else 0 for value in predict_proba][0]

    return {
        'result': y
    }
