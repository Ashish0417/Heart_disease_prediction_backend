def generate_report(results, include_visualization=False):
    """
    Generate a formatted clinical report from prediction results
    
    Args:
        results: Dictionary of prediction results
        include_visualization: Whether to include plots in the report
        
    Returns:
        String containing the formatted report
    """
    report = []
    
    # Header
    report.append("=" * 60)
    report.append("CARDIAC RISK ASSESSMENT REPORT")
    report.append("=" * 60)
    report.append(f"Report Date: {results['report_date']}")
    report.append("")
    
    # Risk assessment
    report.append("RISK ASSESSMENT")
    report.append("-" * 30)
    report.append(f"Heart Disease Risk: {results['prediction']['risk_level']} ({results['prediction']['heart_disease_probability']*100:.1f}%)")
    report.append(f"Risk Category: {results['prediction']['risk_category']}")
    report.append(f"Prediction Reliability: {results['uncertainty']['reliability_percent']:.1f}%")
    report.append(f"Uncertainty Level: {results['uncertainty']['uncertainty_percent']:.1f}%")
    report.append(f"Assessment: {results['uncertainty']['assessment']}")
    report.append("")
    
    # Key insights
    report.append("CLINICAL INSIGHTS")
    report.append("-" * 30)
    for i, insight in enumerate(results['clinical_insights']['key_insights'], 1):
        report.append(f"{i}. {insight}")
    report.append("")
    
    # Abnormal findings
    report.append("ABNORMAL CLINICAL FINDINGS")
    report.append("-" * 30)
    if results['abnormal_features']:
        for feature, details in results['abnormal_features'].items():
            direction = "↑" if details['direction'] == 'high' else "↓"
            
            if 'readable_value' in details:
                value_text = f"{details['readable_value']}"
            elif 'unit' in details:
                value_text = f"{details['value']} {details['unit']}"
            else:
                value_text = f"{details['value']}"
                
            report.append(f"- {details['feature_name']}: {value_text} {direction}")
            report.append(f"  Severity: {details['severity'].title()} (z-score: {details['z_score']:.2f})")
            report.append(f"  Note: {details['clinical_context']}")
            report.append("")
    else:
        report.append("- No significantly abnormal features detected")
        report.append("")
    
    # Recommendations
    report.append("CLINICAL RECOMMENDATIONS")
    report.append("-" * 30)
    for i, rec in enumerate(results['clinical_insights']['recommendations'], 1):
        report.append(f"{i}. {rec}")
    report.append("")
    
    # Return the formatted report
    return "\n".join(report)
