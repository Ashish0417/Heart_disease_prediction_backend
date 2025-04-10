from dataclasses import Field
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, field_validator
from pydantic.fields import Field

class PatientData(BaseModel):
    age: int = Field(..., example=63, description="Age in years")
    sex: int = Field(..., example=1, description="0 = female, 1 = male")
    cp: int = Field(..., example=3, description="Chest pain type (0-3)")
    trestbps: int = Field(..., example=145, description="Resting blood pressure (mm Hg)")
    chol: int = Field(..., example=233, description="Serum cholesterol (mg/dl)")
    fbs: int = Field(..., example=1, description="Fasting blood sugar > 120 mg/dl (1 = true)")
    restecg: int = Field(..., example=0, description="Resting ECG results (0-2)")
    thalach: int = Field(..., example=150, description="Maximum heart rate achieved")
    exang: int = Field(..., example=0, description="Exercise induced angina (1 = yes)")
    oldpeak: float = Field(..., example=2.3, description="ST depression induced by exercise")
    slope: int = Field(..., example=0, description="Slope of peak exercise ST segment (0-2)")
    ca: int = Field(..., example=0, description="Number of major vessels colored by fluoroscopy (0-4)")
    thal: int = Field(..., example=1, description="Thalassemia (0-3)")

    @field_validator('sex')
    def sex_must_be_valid(cls, v):
        if v not in [0, 1]:
            raise ValueError('sex must be 0 (female) or 1 (male)')
        return v
    
    @field_validator('cp')
    def cp_must_be_valid(cls, v):
        if v not in [0, 1, 2, 3]:
            raise ValueError('cp must be between 0 and 3')
        return v
    
    @field_validator('restecg')
    def restecg_must_be_valid(cls, v):
        if v not in [0, 1, 2]:
            raise ValueError('restecg must be between 0 and 2')
        return v
    
    @field_validator('fbs', 'exang')
    def binary_must_be_valid(cls, v):
        if v not in [0, 1]:
            raise ValueError('value must be 0 or 1')
        return v
    
    @field_validator('slope')
    def slope_must_be_valid(cls, v):
        if v not in [0, 1, 2]:
            raise ValueError('slope must be between 0 and 2')
        return v
    
    @field_validator('ca')
    def ca_must_be_valid(cls, v):
        if v not in [0, 1, 2, 3, 4]:
            raise ValueError('ca must be between 0 and 4')
        return v
    
    @field_validator('thal')
    def thal_must_be_valid(cls, v):
        if v not in [0, 1, 2, 3]:
            raise ValueError('thal must be between 0 and 3')
        return v

class PredictionResponse(BaseModel):
    prediction: Dict[str, Any]
    uncertainty: Dict[str, Any]
    abnormal_features: Dict[str, Dict[str, Any]]
    key_contributors: Dict[str, Dict[str, Any]]
    report_date: str
    clinical_insights: Dict[str, List[str]]
    visualization: Optional[str] = None