import streamlit as st
import requests

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Employee Attrition Predictor",
    page_icon="👔",
    layout="wide"
)

# -----------------------------
# Cache the API call
# -----------------------------

@st.cache_data(show_spinner=False)
def get_prediction(employee_tuple):
    employee_data = dict(employee_tuple)
    try:
        response = requests.post(
            "https://employee-attrition-system-2.onrender.com/predict/",
            json=employee_data,
            timeout=66        # stops waiting after 60 seconds
        )
        return response
    except requests.exceptions.ConnectionError:
        return None

# -----------------------------
# Title Section
# -----------------------------

st.title("👔 Employee Attrition Predictor")
st.markdown("Fill in the employee details below to predict whether they are likely to leave the company.")
st.divider()

# -----------------------------
# Personal Information
# -----------------------------

st.subheader("Personal Information")
col1, col2, col3 = st.columns(3)

with col1:
    Age = st.slider("Age", min_value=18, max_value=60, value=30)
    Gender = st.selectbox("Gender", ["Male", "Female"])
    MaritalStatus = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])

with col2:
    Education = st.selectbox("Education Level", [1, 2, 3, 4, 5],
                             help="1=Below College, 2=College, 3=Bachelor, 4=Master, 5=Doctor")
    EducationField = st.selectbox("Education Field", [
        "Life Sciences", "Medical", "Marketing",
        "Technical Degree", "Human Resources", "Other"
    ])
    NumCompaniesWorked = st.number_input("Number of Companies Worked", min_value=0, max_value=20, value=1)

with col3:
    DistanceFromHome = st.number_input("Distance From Home (km)", min_value=0, max_value=100, value=5)
    BusinessTravel = st.selectbox("Business Travel", [
        "Travel_Rarely", "Travel_Frequently", "Non-Travel"
    ])
    OverTime = st.selectbox("OverTime", ["Yes", "No"])

st.divider()

# -----------------------------
# Job Information
# -----------------------------

st.subheader("Job Information")
col4, col5, col6 = st.columns(3)

with col4:
    Department = st.selectbox("Department", [
        "Sales", "Research & Development", "Human Resources"
    ])
    JobRole = st.selectbox("Job Role", [
        "Sales Executive", "Research Scientist", "Laboratory Technician",
        "Manufacturing Director", "Healthcare Representative", "Manager",
        "Sales Representative", "Research Director", "Human Resources"
    ])
    JobLevel = st.selectbox("Job Level", [1, 2, 3, 4, 5],
                            help="1=Entry, 2=Junior, 3=Mid, 4=Senior, 5=Director")

with col5:
    JobInvolvement = st.selectbox("Job Involvement", [1, 2, 3, 4],
                                  help="1=Low, 2=Medium, 3=High, 4=Very High")
    JobSatisfaction = st.selectbox("Job Satisfaction", [1, 2, 3, 4],
                                   help="1=Low, 2=Medium, 3=High, 4=Very High")
    EnvironmentSatisfaction = st.selectbox("Environment Satisfaction", [1, 2, 3, 4],
                                           help="1=Low, 2=Medium, 3=High, 4=Very High")

with col6:
    RelationshipSatisfaction = st.selectbox("Relationship Satisfaction", [1, 2, 3, 4],
                                            help="1=Low, 2=Medium, 3=High, 4=Very High")
    WorkLifeBalance = st.selectbox("Work Life Balance", [1, 2, 3, 4],
                                   help="1=Bad, 2=Good, 3=Better, 4=Best")
    PerformanceRating = st.selectbox("Performance Rating", [1, 2, 3, 4],
                                     help="1=Low, 2=Good, 3=Excellent, 4=Outstanding")

st.divider()

# -----------------------------
# Compensation & Experience
# -----------------------------

st.subheader("Compensation & Experience")
col7, col8, col9 = st.columns(3)

with col7:
    MonthlyIncome = st.number_input("Monthly Income", min_value=1000, max_value=100000, value=5000)
    DailyRate = st.number_input("Daily Rate", min_value=100, max_value=1500, value=800)
    HourlyRate = st.number_input("Hourly Rate", min_value=30, max_value=100, value=65)

with col8:
    MonthlyRate = st.number_input("Monthly Rate", min_value=2000, max_value=27000, value=14000)
    PercentSalaryHike = st.slider("Percent Salary Hike", min_value=0, max_value=25, value=15)
    StockOptionLevel = st.selectbox("Stock Option Level", [0, 1, 2, 3],
                                    help="0=None, 1=Low, 2=Medium, 3=High")

with col9:
    TotalWorkingYears = st.number_input("Total Working Years", min_value=0, max_value=40, value=8)
    TrainingTimesLastYear = st.number_input("Training Times Last Year", min_value=0, max_value=10, value=3)

st.divider()

# -----------------------------
# Tenure Information
# -----------------------------

st.subheader("Tenure Information")
col10, col11, col12 = st.columns(3)

with col10:
    YearsAtCompany = st.number_input("Years At Company", min_value=0, max_value=40, value=5)

with col11:
    YearsInCurrentRole = st.number_input("Years In Current Role", min_value=0, max_value=20, value=3)

with col12:
    YearsSinceLastPromotion = st.number_input("Years Since Last Promotion", min_value=0, max_value=15, value=1)

col13, col14 = st.columns(2)
with col13:
    YearsWithCurrManager = st.number_input("Years With Current Manager", min_value=0, max_value=20, value=3)

st.divider()

# -----------------------------
# Predict Button
# -----------------------------

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    predict_button = st.button("🔍 Predict Attrition", use_container_width=True)

# -----------------------------
# Prediction Result
# -----------------------------

if predict_button:

    # Build input as tuple so it can be cached
    # st.cache_data requires hashable input — dict is not hashable, tuple is
    employee_tuple = tuple({
        "Age": Age,
        "BusinessTravel": BusinessTravel,
        "DailyRate": int(DailyRate),
        "Department": Department,
        "DistanceFromHome": int(DistanceFromHome),
        "Education": Education,
        "EducationField": EducationField,
        "EnvironmentSatisfaction": EnvironmentSatisfaction,
        "Gender": Gender,
        "HourlyRate": int(HourlyRate),
        "JobInvolvement": JobInvolvement,
        "JobLevel": JobLevel,
        "JobRole": JobRole,
        "JobSatisfaction": JobSatisfaction,
        "MaritalStatus": MaritalStatus,
        "MonthlyIncome": int(MonthlyIncome),
        "MonthlyRate": int(MonthlyRate),
        "NumCompaniesWorked": int(NumCompaniesWorked),
        "OverTime": OverTime,
        "PercentSalaryHike": PercentSalaryHike,
        "RelationshipSatisfaction": RelationshipSatisfaction,
        "StockOptionLevel": StockOptionLevel,
        "TotalWorkingYears": int(TotalWorkingYears),
        "TrainingTimesLastYear": int(TrainingTimesLastYear),
        "WorkLifeBalance": WorkLifeBalance,
        "YearsAtCompany": int(YearsAtCompany),
        "YearsInCurrentRole": int(YearsInCurrentRole),
        "YearsSinceLastPromotion": int(YearsSinceLastPromotion),
        "YearsWithCurrManager": int(YearsWithCurrManager)
    }.items())

    with st.spinner("Predicting..."):
        response = get_prediction(employee_tuple)

    if response is None:
        st.error("Cannot connect to FastAPI server. Make sure it is running on http://127.0.0.1:8000")

    elif response.status_code == 200:
        result = response.json()
        prediction_label = result['data']['prediction_label']
        probability = result['data']['attrition_probability']
        confidence = result['data']['confidence_level']

        st.divider()
        st.subheader("Prediction Result")

        if prediction_label == "Likely to Leave":
            st.error(f"⚠️ {prediction_label}")
        else:
            st.success(f"✅ {prediction_label}")

        col_r1, col_r2, col_r3 = st.columns(3)

        with col_r1:
            st.metric(label="Prediction", value=prediction_label)
        with col_r2:
            st.metric(label="Attrition Probability", value=f"{round(probability * 100, 2)}%")
        with col_r3:
            st.metric(label="Confidence Level", value=confidence)

    else:
        st.error(f"API Error: {response.status_code} — {response.text}")