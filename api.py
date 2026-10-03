from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(
    title="Hotel Cancellation Prediction API",
    description="API for predicting the probability that a hotel reservation will be canceled.",
    version="1.0.0",
)

MODEL_PATH = "hotel_cancellation_predictor.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    model_load_error = str(e)


class Reservation(BaseModel):
    lead_time: float
    stays_in_weekend_nights: float
    stays_in_week_nights: float
    num_adults: float
    num_children: float
    num_babies: float


@app.get("/")
def home():
    return {
        "message": "Hotel Cancellation Prediction API is running",
        "model_loaded": model is not None,
    }


@app.get("/health")
def health():
    if model is None:
        raise HTTPException(
            status_code=503,
            detail=f"Model is not available: {model_load_error}",
        )

    return {
        "status": "ok",
        "model_loaded": True,
    }


@app.post("/predict")
def predict(reservation: Reservation):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail=f"Model is not available: {model_load_error}",
        )

    try:
        data = pd.DataFrame(
            [{
                "lead_time": reservation.lead_time,
                "stays_in_weekend_nights": reservation.stays_in_weekend_nights,
                "stays_in_week_nights": reservation.stays_in_week_nights,
                "num_adults": reservation.num_adults,
                "num_children": reservation.num_children,
                "num_babies": reservation.num_babies,
            }]
        )

        probability = float(model.predict_proba(data)[:, 1][0])

        return {
            "cancellation_probability": probability,
            "cancellation_percentage": round(probability * 100, 1),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
