# 🚀 Employee Attrition Prediction System

## 📌 Project Overview

Employee attrition is a major challenge for organizations, leading to financial losses, productivity gaps, and hiring costs.  

This project builds an end-to-end Machine Learning system to predict whether an employee is likely to leave the company using historical HR data.

The final solution includes:
- Exploratory Data Analysis (EDA)
- Multiple model comparison
- Hyperparameter tuning
- Model selection
- FastAPI deployment with live prediction endpoint

---

## 📊 Dataset Information

- Dataset: IBM HR Analytics Employee Attrition Dataset  
- Total Records: 1470 employees  
- Features: 30 employee attributes  
- Target Variable: Attrition (Yes / No)

---

## 🔍 Exploratory Data Analysis Insights

Key observations:

- Employees working overtime show significantly higher attrition rates.
- Sales department has comparatively higher turnover.
- Single employees have higher probability of leaving.
- Lower job satisfaction correlates with higher attrition.
- Work-life balance impacts retention.

---

## 🤖 Machine Learning Models Compared

| Model | Recall | ROC-AUC |
|-------|--------|----------|
| Logistic Regression | 0.34 | 0.65 |
| SVM | 0.15 | - |
| Decision Tree | 0.48 | 0.64 |
| AdaBoost | 0.25 | 0.59 |
| **Random Forest (Final Model)** | **0.61** | **0.73** |

### ✅ Final Model: Random Forest

The Random Forest model was selected based on:
- Highest recall (important to detect employees likely to leave)
- Strong ROC-AUC score
- Balanced performance

---

## 🛠 Tech Stack

- Python
- Pandas
- Scikit-Learn
- FastAPI
- Uvicorn
- Pydantic
- Joblib

---

## 🚀 API Deployment

The trained model is deployed using FastAPI.

### Run Locally

```bash
uvicorn main:app --reload
