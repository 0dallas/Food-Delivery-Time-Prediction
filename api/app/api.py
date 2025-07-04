# app/api.py
import joblib
import os
import pandas as pd
import logging
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from app.schemas import DeliveryFeatures, PredictionResponse

## --- Configuración ---
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
PREPROCESSOR_PATH = os.path.join(BASE_DIR, "preprocessor.pkl")

## --- Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

## --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.model = joblib.load(MODEL_PATH)
        app.state.preprocessor = joblib.load(PREPROCESSOR_PATH)
        logger.info("Model and preprocessor loaded successfully.")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise RuntimeError(f"Missing model or preprocessor: {e}")
    except Exception as e:
        logger.error("Failed to load model/preprocessor", exc_info=True)
        raise RuntimeError(f"Unexpected loading error: {e}")

    yield
    logger.info("Application shutdown cleanup complete.")

# --- FastAPI App ---
app = FastAPI(
    title="Delivery Time Prediction API",
    description="Predicts food delivery time based on features.",
    version="1.0.0",
    lifespan=lifespan
)

# --- Endpoints ---
@app.get("/health", response_model=dict)
async def health_check():
    return {"status": "ok", "message": "API is running and model is loaded."}

@app.post("/predict_delivery_time", response_model=PredictionResponse)
async def predict_delivery_time(features: DeliveryFeatures):
    try:
        df = pd.DataFrame([features.model_dump()])
        processed = app.state.preprocessor.transform(df)
        prediction = app.state.model.predict(processed)[0]
        return {"predicted_delivery_time_min": round(float(prediction), 2)}
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
