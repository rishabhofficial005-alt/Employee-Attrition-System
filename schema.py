from pydantic import BaseModel,Field
from typing import Literal
class Employee(BaseModel):
    
    Age: int = Field(..., ge=18, le=60)
    BusinessTravel: Literal["Travel_Rarely", "Travel_Frequently", "Non-Travel"]
    DailyRate: int = Field(..., gt=0)
    Department: Literal["Sales", "Research & Development", "Human Resources"]
    DistanceFromHome: int = Field(..., ge=0)
    Education: int = Field(..., ge=1, le=5)
    EducationField: Literal[
        "Life Sciences",
        "Medical",
        "Marketing",
        "Technical Degree",
        "Human Resources",
        "Other"
    ]
    EnvironmentSatisfaction: int = Field(..., ge=1, le=4)
    Gender: Literal["Male", "Female"]
    HourlyRate: int = Field(..., gt=0)
    JobInvolvement: int = Field(..., ge=1, le=4)
    JobLevel: int = Field(..., ge=1, le=5)
    JobRole: Literal[
        "Sales Executive",
        "Research Scientist",
        "Laboratory Technician",
        "Manufacturing Director",
        "Healthcare Representative",
        "Manager",
        "Sales Representative",
        "Research Director",
        "Human Resources"
    ]
    JobSatisfaction: int = Field(..., ge=1, le=4)
    MaritalStatus: Literal["Single", "Married", "Divorced"]
    MonthlyIncome: int = Field(..., gt=0)
    MonthlyRate: int = Field(..., gt=0)
    NumCompaniesWorked: int = Field(..., ge=0)
    OverTime: Literal["Yes", "No"]
    PercentSalaryHike: int = Field(..., ge=0)
    PerformanceRating: int = Field(..., ge=1, le=4)
    RelationshipSatisfaction: int = Field(..., ge=1, le=4)
    StockOptionLevel: int = Field(..., ge=0, le=3)
    TotalWorkingYears: int = Field(..., ge=0)
    TrainingTimesLastYear: int = Field(..., ge=0)
    WorkLifeBalance: int = Field(..., ge=1, le=4)
    YearsAtCompany: int = Field(..., ge=0)
    YearsInCurrentRole: int = Field(..., ge=0)
    YearsSinceLastPromotion: int = Field(..., ge=0)
    YearsWithCurrManager: int = Field(..., ge=0)
    