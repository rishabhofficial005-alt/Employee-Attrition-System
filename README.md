# Employee Attrition Prediction System

A complete end-to-end Machine Learning project that predicts whether an employee is likely to leave the company. Built with Scikit-learn, FastAPI, and Streamlit.

---

## Problem Statement

Employee attrition is a critical challenge for organizations. Losing an employee unexpectedly results in significant costs — recruitment, onboarding, and lost productivity. This project builds a machine learning system to predict attrition risk early so HR teams can take proactive retention actions.

> **Key metric: Recall** — It is more costly to miss an at-risk employee than to flag a false alarm.

---

## Demo

| Streamlit UI | FastAPI Swagger |
|---|---|
| Fill employee details → Get instant prediction | Test all endpoints at `/docs` |

Run locally:
```bash
# Terminal 1 — Start API
uvicorn main:app --reload

# Terminal 2 — Start UI
streamlit run web.py
```

Then open:
- Streamlit UI → http://localhost:8501
- API Docs → http://127.0.0.1:8000/docs

---

## Project Structure

```
Employee-Attrition/
│
├── EmployeeAttrition.ipynb     # EDA, feature engineering, model training
├── main.py                     # FastAPI server with prediction endpoints
├── schema.py                   # Pydantic input validation schema
├── web.py                      # Streamlit frontend UI
├── attrition_model.pkl         # Trained Random Forest model
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

---

## Dataset

**IBM HR Analytics Employee Attrition Dataset**

| Property | Value |
|---|---|
| Source | IBM / Kaggle |
| Rows | 1,470 employees |
| Features | 35 columns |
| Target | Attrition (Yes / No) |
| Class distribution | 83% No, 17% Yes (imbalanced) |

---

## Exploratory Data Analysis

Key findings from EDA:

- **Overtime** — Employees working overtime had ~30% attrition rate vs ~10% for those who did not
- **Monthly Income** — Employees who left had significantly lower median income
- **Age** — Younger employees showed higher turnover tendencies
- **Job Satisfaction** — Level 1 satisfaction had 23% attrition vs 11% for level 4
- **Marital Status** — Single employees had ~25% attrition vs ~12% for married employees
- **Sales Department** — Highest attrition rate at ~20% across all departments

---

## Models Trained

| Model | Accuracy | Recall | Precision | ROC-AUC |
|---|---|---|---|---|
| Logistic Regression | 0.864 | 0.340 | 0.640 | 0.652 |
| SVM | 0.857 | 0.149 | 0.778 | 0.570 |
| KNN | 0.847 | 0.043 | 1.000 | 0.521 |
| Decision Tree | 0.759 | 0.489 | 0.329 | 0.650 |
| **Random Forest** ✅ | **0.810** | **0.596** | **0.431** | **0.723** |
| AdaBoost | 0.833 | 0.255 | 0.462 | 0.599 |

**Random Forest** selected as the best model based on highest Recall and ROC-AUC score.

---

## Handling Class Imbalance

The dataset is imbalanced — 1,233 No vs 237 Yes (83:17 ratio).

- `stratify=y` used in train/test split to preserve class ratio
- `class_weight='balanced'` applied to all models that support it
- For AdaBoost — `class_weight='balanced'` passed to base `DecisionTreeClassifier`
- KNN does not support class weighting — noted as a limitation

---

## Top Attrition Drivers (Feature Importance)

Based on Random Forest feature importances:

1. **MonthlyIncome** — Lowest paid employees leave most
2. **OverTime** — Overtime employees are 3x more likely to leave
3. **TotalWorkingYears** — Less experienced employees show higher turnover
4. **Age** — Younger employees leave more frequently
5. **YearsWithCurrManager** — Shorter tenure with manager indicates instability
6. **YearsAtCompany** — Employees in early tenure years are highest risk

---

## API Endpoints

Base URL: `http://127.0.0.1:8000`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/model-info` | Model metrics and details |
| POST | `/predict` | Single employee prediction |
| POST | `/predict/batch` | Batch prediction for multiple employees |

### Sample Request — `/predict`

```json
{
  "Age": 28,
  "BusinessTravel": "Travel_Frequently",
  "DailyRate": 500,
  "Department": "Sales",
  "DistanceFromHome": 15,
  "Education": 3,
  "EducationField": "Marketing",
  "EnvironmentSatisfaction": 2,
  "Gender": "Male",
  "HourlyRate": 45,
  "JobInvolvement": 2,
  "JobLevel": 1,
  "JobRole": "Sales Representative",
  "JobSatisfaction": 1,
  "MaritalStatus": "Single",
  "MonthlyIncome": 2500,
  "MonthlyRate": 8000,
  "NumCompaniesWorked": 4,
  "OverTime": "Yes",
  "PercentSalaryHike": 11,
  "RelationshipSatisfaction": 2,
  "StockOptionLevel": 0,
  "TotalWorkingYears": 3,
  "TrainingTimesLastYear": 1,
  "WorkLifeBalance": 1,
  "YearsAtCompany": 1,
  "YearsInCurrentRole": 1,
  "YearsSinceLastPromotion": 0,
  "YearsWithCurrManager": 1
}
```

### Sample Response

```json
{
  "status": "success",
  "data": {
    "prediction": 1,
    "prediction_label": "Likely to Leave",
    "attrition_probability": 0.823,
    "confidence_level": "High"
  }
}
```

---

## Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-username/employee-attrition.git
cd employee-attrition
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Place dataset in project folder**
```
WA_Fn-UseC_-HR-Employee-Attrition.csv
```

**5. Run the notebook to train and save the model**
```
Run all cells in EmployeeAttrition.ipynb
This saves attrition_model.pkl in the project folder
```

**6. Start FastAPI server**
```bash
uvicorn main:app --reload
```

**7. Start Streamlit UI**
```bash
streamlit run web.py
```

---

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.10+ |
| ML Library | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| API Framework | FastAPI |
| Input Validation | Pydantic |
| Model Serialization | Joblib |
| Frontend UI | Streamlit |
| API Client | Requests |

---

## Business Recommendations

Based on model insights, HR should focus retention efforts on:

- Young employees (under 30) in their first 1-2 years at the company
- Employees working overtime consistently
- Low-income employees especially in the Sales department
- Teams with high manager turnover (low YearsWithCurrManager)
- Employees with low job satisfaction (level 1 or 2)

