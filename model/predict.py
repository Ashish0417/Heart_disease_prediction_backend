from model.feature_info import FEATURE_INFO
import pandas as pd
import numpy as np
import datetime
from model.clinical_insights import get_clinical_insights

def predict_heart_disease(patient_data, model_components, num_bootstrap_samples=50, z_score_threshold=1.5):
    """
    Predict heart disease risk with uncertainty quantification and clinical insights.
    
    Args:
        patient_data: Dictionary or DataFrame with patient features 
        model_components: Dictionary containing trained model components
        num_bootstrap_samples: Number of bootstrap samples for uncertainty estimation
        z_score_threshold: Threshold for flagging abnormal features
        
    Returns:
        Dictionary with prediction results and clinical insights
    """
    # Extract components
    ensemble = model_components['ensemble']
    rf_model1 = model_components['rf_model1']
    rf_model2 = model_components['rf_model2']
    gb_model1 = model_components['gb_model1']
    gb_model2 = model_components['gb_model2']
    scaler = model_components['scaler']
    feature_means = model_components['feature_means']
    feature_stds = model_components['feature_stds']
    
    # Convert dict to DataFrame if needed
    if isinstance(patient_data, dict):
        patient_data = pd.DataFrame([patient_data])
    
    # Ensure all required features are present
    expected_features = feature_means.index.tolist()
    for feature in expected_features:
        if feature not in patient_data.columns:
            raise ValueError(f"Missing required feature: {feature}")
    
    # Scale patient data
    patient_data_scaled = pd.DataFrame(
        scaler.transform(patient_data),
        columns=patient_data.columns
    )
    
    # Basic prediction with the ensemble
    prediction_proba = ensemble.predict_proba(patient_data_scaled)[0, 1]
    prediction = 1 if prediction_proba >= 0.22 else 0
    
    # --- Enhanced uncertainty estimation ---
    # 1. Bootstrap sampling with noise
    bootstrap_probs = []
    for _ in range(num_bootstrap_samples):
        # Create bootstrapped sample with noise
        bootstrap_sample = patient_data_scaled.copy()
        for col in bootstrap_sample.columns:
            noise = np.random.normal(0, 0.05)  # Small gaussian noise
            if bootstrap_sample[col].dtype in [np.float64, np.int64]:
                bootstrap_sample[col] = bootstrap_sample[col] + noise
        
        # Get predictions from all individual models
        rf1_prob = rf_model1.predict_proba(bootstrap_sample)[0, 1]
        rf2_prob = rf_model2.predict_proba(bootstrap_sample)[0, 1]
        gb1_prob = gb_model1.predict_proba(bootstrap_sample)[0, 1]
        gb2_prob = gb_model2.predict_proba(bootstrap_sample)[0, 1]
        
        # Average the predictions
        avg_prob = (rf1_prob + rf2_prob + gb1_prob + gb2_prob) / 4
        bootstrap_probs.append(avg_prob)
    
    # 2. Calculate variance across models for this sample
    model_probs = [
        rf_model1.predict_proba(patient_data_scaled)[0, 1],
        rf_model2.predict_proba(patient_data_scaled)[0, 1],
        gb_model1.predict_proba(patient_data_scaled)[0, 1],
        gb_model2.predict_proba(patient_data_scaled)[0, 1]
    ]
    model_variance = np.var(model_probs)
    
    # 3. Combine both uncertainty measures (bootstrap and model variance)
    bootstrap_std = np.std(bootstrap_probs)
    combined_uncertainty = np.sqrt(bootstrap_std**2 + model_variance)
    
    # Scale to percentage (0-100%)
    # The scaling factor 4.0 is chosen to make typical uncertainty values range from 0-100%
    # Higher values might exceed 100% for extremely uncertain predictions
    uncertainty_percent = min(combined_uncertainty * 400, 100)
    reliability_percent = 100 - uncertainty_percent
    
    # --- Abnormal feature detection ---
    # Calculate z-scores using original (unscaled) data
    z_scores = (patient_data - feature_means) / feature_stds
    
    # Identify abnormal features
    abnormal_features = {}
    for col in z_scores.columns:
        z_val = z_scores.iloc[0][col]
        if abs(z_val) >= z_score_threshold:
            abnormal_features[col] = {
                'feature_name': FEATURE_INFO[col]['name'],
                'value': patient_data.iloc[0][col],
                'z_score': z_val,
                'direction': 'high' if z_val > 0 else 'low',
                'severity': 'severe' if abs(z_val) > 2.5 else 'moderate',
                'clinical_context': FEATURE_INFO[col]['clinical_context']
            }
            
            # Add human-readable value for categorical features
            if 'values' in FEATURE_INFO[col]:
                value = int(patient_data.iloc[0][col])
                if value in FEATURE_INFO[col]['values']:
                    abnormal_features[col]['readable_value'] = FEATURE_INFO[col]['values'][value]
            
            # Add units where applicable
            if 'unit' in FEATURE_INFO[col] and FEATURE_INFO[col]['unit']:
                abnormal_features[col]['unit'] = FEATURE_INFO[col]['unit']
    
    # Sort abnormal features by severity (absolute z-score)
    abnormal_features = dict(sorted(
        abnormal_features.items(), 
        key=lambda x: abs(x[1]['z_score']), 
        reverse=True
    ))
    
    # --- Feature importance for this prediction ---
    # Calculate feature importances
    feature_importances = ensemble.named_estimators_['rf1'].feature_importances_
    
    feature_contributions = {}
    for i, col in enumerate(feature_means.index):
        # Calculate personalized feature importance
        importance = feature_importances[i]
        contribution = importance * (1 + 0.5 * abs(z_scores.iloc[0][col]))
        
        if importance > 0.02:  # Only include significant contributions
            feature_contributions[col] = {
                'feature_name': FEATURE_INFO[col]['name'],
                'importance': round(importance, 3),
                'contribution': round(contribution, 3)
            }
            
            # Add human-readable value for categorical features
            if 'values' in FEATURE_INFO[col]:
                value = int(patient_data.iloc[0][col])
                if value in FEATURE_INFO[col]['values']:
                    feature_contributions[col]['value'] = FEATURE_INFO[col]['values'][value]
            else:
                feature_contributions[col]['value'] = float(patient_data.iloc[0][col])
                
                # Add units where applicable
                if 'unit' in FEATURE_INFO[col] and FEATURE_INFO[col]['unit']:
                    feature_contributions[col]['unit'] = FEATURE_INFO[col]['unit']
    
    # Sort feature contributions
    feature_contributions = dict(sorted(
        feature_contributions.items(),
        key=lambda x: x[1]['contribution'],
        reverse=True
    ))
    
    # --- Format results for clinical use ---
    risk_levels = {
        (0, 0.05): "Very Low",
        (0.05, 0.2): "Low", 
        (0.2, 0.4): "Moderate",
        (0.4, 0.6): "High",
        (0.6, 1.0): "Very High"
    }
    
    risk_level = next(level for range_vals, level in risk_levels.items() 
                     if range_vals[0] <= prediction_proba < range_vals[1] or range_vals[1] == 1.0)
    
    # Format date for the report
    today = datetime.datetime.now().strftime("%B %d, %Y")

    
    # Generate clinical insights
    clinical_insights = get_clinical_insights(prediction_proba, uncertainty_percent/100, 
                                             abnormal_features, feature_contributions)
    
    # Format final results
    return {
        "prediction": {
            "heart_disease_probability": round(prediction_proba, 3),
            "binary_prediction": int(prediction),
            "risk_level": risk_level,
            "risk_category": "High Risk" if prediction_proba >= 0.5 else "Low Risk"
        },
        "uncertainty": {
            "uncertainty_percent": round(uncertainty_percent, 1),
            "reliability_percent": round(reliability_percent, 1),
            "assessment": "Prediction is " + (
                "highly reliable" if uncertainty_percent < 20 else
                "moderately reliable" if uncertainty_percent < 50 else
                "uncertain - consider additional tests"
            )
        },
        "abnormal_features": abnormal_features,
        "key_contributors": feature_contributions,
        "report_date": today,
        "clinical_insights": clinical_insights
    }
