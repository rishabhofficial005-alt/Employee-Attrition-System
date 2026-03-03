from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import joblib
import pandas as pd
from schema import Employee

# -----------------------------
# FastAPI App Configuration
# -----------------------------

app = FastAPI(
    title="Employee Attrition Prediction API",
    description="API to predict whether an employee is likely to leave the company.",
    version="1.0.0"
)

# -----------------------------
# Load Trained Model
# -----------------------------

try:
    model = joblib.load("attrition_model.pkl")
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# -----------------------------
# Health Check Endpoint
# -----------------------------

@app.get("/", tags=["Health Check"])
def health_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Employee Attrition API is running 🚀"
        }
    )

# -----------------------------
# Prediction Endpoint
# -----------------------------

@app.post("/predict", tags=["Prediction"])
def predict_attrition(employee: Employee):

    try:
        # Convert validated input to DataFrame
        input_df = pd.DataFrame([employee.dict()])

        # Get probability of attrition (class 1)
        probability = model.predict_proba(input_df)[0][1]

        # Apply threshold
        prediction = 1 if probability > 0.5 else 0

        prediction_label = (
            "Likely to Leave ⚠️" if prediction == 1
            else "Likely to Stay ✅"
        )

        response = {
            "status": "success",
            "data": {
                "prediction": prediction,
                "prediction_label": prediction_label,
                "attrition_probability": round(float(probability), 4)
            }
        }

        return JSONResponse(status_code=200, content=response)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )