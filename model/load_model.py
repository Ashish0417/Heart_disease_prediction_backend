import os
import joblib


def load_model(model_path='heart_model_ensemble.pkl'):
    """Load the trained model components from disk"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    return joblib.load(model_path)
