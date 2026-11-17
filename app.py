from pathlib import Path
import joblib
import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"
model = joblib.load(MODEL_PATH)

app = FastAPI(title="Iris ML Predictor", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

SPECIES = {0: "Iris Setosa", 1: "Iris Versicolor", 2: "Iris Virginica"}

class FlowerInput(BaseModel):
    sepal_length: float = Field(..., gt=0, description="Sepal length in cm")
    sepal_width: float = Field(..., gt=0, description="Sepal width in cm")
    petal_length: float = Field(..., gt=0, description="Petal length in cm")
    petal_width: float = Field(..., gt=0, description="Petal width in cm")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
def predict(payload: FlowerInput):
    values = np.array([[
        payload.sepal_length, payload.sepal_width,
        payload.petal_length, payload.petal_width
    ]])
    prediction = int(model.predict(values)[0])
    probabilities = model.predict_proba(values)[0]
    return {
        "prediction": prediction,
        "species": SPECIES[prediction],
        "confidence": round(float(np.max(probabilities)) * 100, 2)
    }
