def get_clinical_insights(risk_prob, uncertainty, abnormal_features, key_contributors):
    """Generate clinical insights and recommendations based on prediction results"""
    
    insights = []
    recommendations = []
    
    # Risk level assessment
    if risk_prob < 0.2:
        insights.append("Patient shows minimal indicators of heart disease.")
        recommendations.append("Standard preventive care and lifestyle counseling advised.")
    elif risk_prob < 0.4:
        insights.append("Patient shows some risk factors for heart disease.")
        recommendations.append("Consider lifestyle modifications and monitoring of risk factors.")
    elif risk_prob < 0.6:
        insights.append("Patient shows moderate risk factors for heart disease.")
        recommendations.append("Further cardiac assessment recommended. Consider non-invasive testing.")
    elif risk_prob < 0.8:
        insights.append("Patient shows significant risk factors for heart disease.")
        recommendations.append("Comprehensive cardiac evaluation indicated. Consider stress test and echocardiogram.")
    else:
        insights.append("Patient shows strong indicators of heart disease.")
        recommendations.append("Urgent cardiology referral advised. Consider cardiac catheterization if symptomatic.")
    
    # Uncertainty insights
    if uncertainty > 0.5:
        insights.append("Model shows significant uncertainty in this prediction.")
        recommendations.append("Consider additional diagnostic tests to confirm cardiovascular status.")
    
    # Feature-specific insights
    for feature, details in abnormal_features.items():
        if feature == 'cp' and details['value'] in [0, 1, 2]:
            insights.append(f"Patient reports {details.get('readable_value', details['value'])}, which may indicate angina.")
            if details['value'] == 0:  # Typical angina
                recommendations.append("Evaluate for stable coronary artery disease.")
        
        elif feature == 'thalach' and details['direction'] == 'low':
            insights.append("Maximum heart rate during exercise is abnormally low, suggesting reduced cardiac capacity.")
            recommendations.append("Consider evaluation for chronotropic incompetence or ischemic heart disease.")
        
        elif feature == 'oldpeak' and details['direction'] == 'high':
            insights.append("Significant ST depression observed during exercise, suggesting myocardial ischemia.")
            recommendations.append("ECG monitoring during exercise recommended to assess for ischemic changes.")
        
        elif feature == 'chol' and details['direction'] == 'high':
            insights.append("Elevated cholesterol levels may contribute to atherosclerotic disease.")
            recommendations.append("Lipid management indicated. Consider statin therapy if appropriate.")
        
        elif feature == 'trestbps' and details['direction'] == 'high':
            insights.append("Elevated resting blood pressure increases cardiac workload and stroke risk.")
            recommendations.append("Blood pressure management recommended. Target <130/80 mmHg.")
        
        elif feature == 'ca' and details['value'] > 0:
            insights.append(f"Fluoroscopy shows {int(details['value'])} major vessel(s) with calcium deposits.")
            recommendations.append("Presence of calcified vessels indicates atherosclerotic disease.")
        
        elif feature == 'exang' and details['value'] == 1:
            insights.append("Patient experiences angina during exercise, strongly associated with CAD.")
            recommendations.append("Anti-anginal medication may be indicated.")
            
        elif feature == 'thal' and details['value'] in [1, 2]:
            thal_value = details.get('readable_value', details['value'])
            insights.append(f"Thallium scan shows {thal_value}, indicating abnormal blood flow.")
            recommendations.append("Consider myocardial perfusion imaging to assess for reversible ischemia.")
    
    # Return combined insights
    return {
        "key_insights": insights[:5],  # Limit to top 5 insights
        "recommendations": recommendations[:5]  # Limit to top 5 recommendations
    }