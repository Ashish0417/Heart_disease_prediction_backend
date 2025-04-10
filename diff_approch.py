from dataclasses import Field
from http.client import HTTPException
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, UploadFile, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import uuid
import os
import concurrent.futures
from pydantic import BaseModel
from schema import PredictionResponse, PatientData
from model.predict import predict_heart_disease
from model.load_model import load_model
from utils.report_gen import generate_report
from utils.virtualization import visualize_patient_data

app = FastAPI(
    title="Heart Disease Prediction API",
    description="API for predicting heart disease risk with clinical insights",
    version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_components = None

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global model_components
    model_path = 'heart_model_ensemble.pkl'
    if os.path.exists(model_path):
        print("Loading pre-trained model...")
        model_components = load_model(model_path)
    else:
        raise Exception("Model file not found. Please train the model first.")

@app.post("/predict", response_model=PredictionResponse)
async def predict(patient: PatientData, background_tasks: BackgroundTasks):
    """
    Predict heart disease risk with uncertainty estimation
    This endpoint processes patient data to predict cardiovascular risk,
    estimate prediction uncertainty, and provide clinical insights.
    """
    global model_components
    
    if model_components is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please try again later.")
    
    # Convert Pydantic model to dict
    patient_dict = patient.model_dump()
    
    # Get prediction result
    result = predict_heart_disease(patient_dict, model_components)
    
    # Create visualization and generate report in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Start visualization task
        visualization_future = executor.submit(
            visualize_patient_data,
            patient_dict,
            model_components['feature_means'],
            model_components['feature_stds'],
            result
        )
        
        # Start report generation in parallel
        report_future = executor.submit(generate_report, result)
        
        # Get visualization result
        img_base64 = visualization_future.result()
        
        # Get report result if you want to use it
        report = report_future.result()
        # You can store or use the report if needed
        # For example, save it to a file or database
        # Or add it to the result if you want to include it in the response
    
    # Add visualization to result
    result['visualization'] = f"data:image/png;base64,{img_base64}"
    
    # Optionally add the report to the result
    # result['report_text'] = report
    
    return result