from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import joblib
import pandas as pd
import logging
from functools import lru_cache
from schema import Employee

# -----------------------------
# Logging Configuration
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("attrition_api.log")
    ]
)
logger = logging.getLogger(__name__)

# -----------------------------
# FastAPI App Configuration
# -----------------------------

app = FastAPI(
    title="Employee Attrition Prediction API",
    description="API to predict whether an employee is likely to leave the company.",
    version="1.0.0"
)

# -----------------------------
# Load Model Once at Startup
# -----------------------------

@lru_cache(maxsize=1)
def load_model():
    logger.info("Loading model from disk...")
    model = joblib.load("attrition_model.pkl")
    logger.info("Model loaded successfully and cached")
    return model

# Load model when app starts — not on every request
model = load_model()

# -----------------------------
# Startup Event
# -----------------------------

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI server started successfully")
    logger.info("Model is ready for predictions")

# -----------------------------
# Shutdown Event
# -----------------------------

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI server is shutting down")

# -----------------------------
# Validation Error Handler
# -----------------------------

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Invalid input data",
            "details": str(exc)
        }
    )

# -----------------------------
# Health Check Endpoint
# -----------------------------

@app.get("/", tags=["Health Check"])
def health_check():
    logger.info("Health check endpoint called")
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Employee Attrition API is running"
        }
    )

# -----------------------------
# Model Info Endpoint
# -----------------------------

@app.get("/model-info", tags=["Health Check"])
def model_info():
    logger.info("Model info endpoint called")
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": {
                "model_type": "Random Forest Classifier",
                "recall_score": 0.596,
                "roc_auc_score": 0.723,
                "accuracy_score": 0.809,
                "total_features": 29,
                "class_imbalance_handling": "class_weight=balanced"
            }
        }
    )

# -----------------------------
# Single Prediction Endpoint
# -----------------------------

@app.post("/predict", tags=["Prediction"])
def predict_attrition(employee: Employee):
    try:
        logger.info(
            f"Single prediction request — "
            f"Age={employee.Age}, "
            f"Department={employee.Department}, "
            f"OverTime={employee.OverTime}, "
            f"MonthlyIncome={employee.MonthlyIncome}"
        )

        # Convert validated input to DataFrame
        input_df = pd.DataFrame([employee.model_dump()])

        # Get probability of attrition
        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(input_df)[0][1]
            prediction = 1 if probability > 0.5 else 0
        else:
            prediction = int(model.predict(input_df)[0])
            probability = float(prediction)

        # Confidence level
        if probability >= 0.75:
            confidence = "High"
        elif probability >= 0.50:
            confidence = "Medium"
        else:
            confidence = "Low"

        # Prediction label
        prediction_label = (
            "Likely to Leave" if prediction == 1
            else "Likely to Stay"
        )

        logger.info(
            f"Prediction result — "
            f"{prediction_label}, "
            f"Probability={round(float(probability), 4)}, "
            f"Confidence={confidence}"
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": {
                    "prediction": prediction,
                    "prediction_label": prediction_label,
                    "attrition_probability": round(float(probability), 4),
                    "confidence_level": confidence
                }
            }
        )

    except Exception as e:
        logger.error(f"Single prediction failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

# -----------------------------
# Batch Prediction Endpoint
# -----------------------------

@app.post("/predict/batch", tags=["Prediction"])
def predict_batch(employees: list[Employee]):
    try:
        logger.info(f"Batch prediction request — {len(employees)} employees")

        # Convert list of employees to DataFrame
        input_df = pd.DataFrame([e.model_dump() for e in employees])

        # Get probabilities for all employees
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df)[:, 1]
            predictions = (probabilities > 0.5).astype(int)
        else:
            predictions = model.predict(input_df).astype(int)
            probabilities = predictions.astype(float)

        # Build results list
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):

            # Confidence level per employee
            if prob >= 0.75:
                confidence = "High"
            elif prob >= 0.50:
                confidence = "Medium"
            else:
                confidence = "Low"

            results.append({
                "employee_index": i,
                "prediction": int(pred),
                "prediction_label": "Likely to Leave" if pred == 1 else "Likely to Stay",
                "attrition_probability": round(float(prob), 4),
                "confidence_level": confidence
            })

        # Summary stats
        at_risk = sum(1 for r in results if r["prediction"] == 1)
        safe = len(results) - at_risk

        logger.info(
            f"Batch prediction complete — "
            f"{at_risk} at risk, "
            f"{safe} likely to stay, "
            f"out of {len(employees)} total"
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "summary": {
                    "total_employees": len(results),
                    "at_risk_count": at_risk,
                    "safe_count": safe,
                    "attrition_rate": f"{round((at_risk / len(results)) * 100, 2)}%"
                },
                "data": results
            }
        )

    except Exception as e:
        logger.error(f"Batch prediction failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}"
        )
