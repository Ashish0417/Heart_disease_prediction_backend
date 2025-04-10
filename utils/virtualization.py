import matplotlib.pyplot as plt
import io
import pandas as pd
import base64
from model.feature_info import FEATURE_INFO

def visualize_patient_data(patient_data, feature_means, feature_stds, result):
    """Create visualization of patient data relative to population norms"""
    if not isinstance(patient_data, pd.DataFrame):
        patient_data = pd.DataFrame([patient_data])
    
    # Calculate z-scores
    z_scores = (patient_data - feature_means) / feature_stds
    
    # Select numerical features for visualization
    num_features = [col for col in z_scores.columns 
                   if col not in ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']]
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Create bar plot of z-scores
    bars = plt.bar(range(len(num_features)), z_scores[num_features].iloc[0], color='skyblue')
    
    # Color bars based on abnormality
    for i, feature in enumerate(num_features):
        z_val = z_scores[feature].iloc[0]
        if abs(z_val) > 1.5:
            bars[i].set_color('salmon' if z_val > 0 else 'lightgreen')
    
    # Add reference lines
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.axhline(y=1.5, color='red', linestyle='--', alpha=0.5)
    plt.axhline(y=-1.5, color='red', linestyle='--', alpha=0.5)
    
    # Set labels and title
    plt.xticks(range(len(num_features)), [FEATURE_INFO[f]['name'] for f in num_features], rotation=45, ha='right')
    plt.ylabel('Standard Deviations from Mean')
    plt.title(f'Patient Feature Profile (Risk Level: {result["prediction"]["risk_level"]})')
    
    # Add risk probability and reliability
    plt.text(0.02, 0.95, f'Heart Disease Risk: {result["prediction"]["heart_disease_probability"]:.1%}', 
             transform=plt.gca().transAxes, fontsize=12, 
             bbox=dict(facecolor='white', alpha=0.8))
    
    plt.text(0.02, 0.89, f'Prediction Reliability: {result["uncertainty"]["reliability_percent"]:.1f}%', 
             transform=plt.gca().transAxes, fontsize=12, 
             bbox=dict(facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    
    # Convert plot to base64 for embedding in web applications
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_str