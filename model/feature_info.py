FEATURE_INFO = {
    'age': {
        'name': 'Age',
        'unit': 'years',
        'normal_range': (30, 70),
        'clinical_context': 'Age is a risk factor for heart disease, increasing with age'
    },
    'sex': {
        'name': 'Sex',
        'unit': '',
        'values': {0: 'Female', 1: 'Male'},
        'clinical_context': 'Males have higher risk of heart disease than females'
    },
    'cp': {
        'name': 'Chest Pain Type',
        'unit': '',
        'values': {0: 'Typical angina', 1: 'Atypical angina', 2: 'Non-anginal pain', 3: 'Asymptomatic'},
        'clinical_context': 'Type of chest pain experienced; atypical symptoms may still indicate heart issues'
    },
    'trestbps': {
        'name': 'Resting Blood Pressure',
        'unit': 'mm Hg',
        'normal_range': (90, 120),
        'clinical_context': 'Elevated blood pressure increases cardiac workload and risk'
    },
    'chol': {
        'name': 'Serum Cholesterol',
        'unit': 'mg/dl',
        'normal_range': (125, 200),
        'clinical_context': 'High cholesterol contributes to plaque formation in arteries'
    },
    'fbs': {
        'name': 'Fasting Blood Sugar',
        'unit': '',
        'values': {0: 'FBS < 120 mg/dl', 1: 'FBS > 120 mg/dl'},
        'clinical_context': 'Elevated blood sugar may indicate diabetes, a heart disease risk factor'
    },
    'restecg': {
        'name': 'Resting ECG Results',
        'unit': '',
        'values': {0: 'Normal', 1: 'ST-T wave abnormality', 2: 'Left ventricular hypertrophy'},
        'clinical_context': 'ECG abnormalities may indicate existing heart conditions'
    },
    'thalach': {
        'name': 'Maximum Heart Rate',
        'unit': 'bpm',
        'normal_range': (120, 180),
        'clinical_context': 'Lower max heart rate may indicate reduced cardiac capacity'
    },
    'exang': {
        'name': 'Exercise Induced Angina',
        'unit': '',
        'values': {0: 'No', 1: 'Yes'},
        'clinical_context': 'Angina during exercise strongly associated with coronary artery disease'
    },
    'oldpeak': {
        'name': 'ST Depression',
        'unit': 'mm',
        'normal_range': (0, 0.5),
        'clinical_context': 'Depression induced by exercise relative to rest; indicates ischemia'
    },
    'slope': {
        'name': 'Peak Exercise ST Segment',
        'unit': '',
        'values': {0: 'Upsloping', 1: 'Flat', 2: 'Downsloping'},
        'clinical_context': 'Slope of peak exercise ST segment; downsloping indicates abnormality'
    },
    'ca': {
        'name': 'Major Vessels Colored by Fluoroscopy',
        'unit': '',
        'normal_range': (0, 0),
        'clinical_context': 'Number of major vessels with calcium deposits; more vessels indicate advanced disease'
    },
    'thal': {
        'name': 'Thalassemia',
        'unit': '',
        'values': {0: 'Normal', 1: 'Fixed defect', 2: 'Reversible defect', 3: 'Unknown'},
        'clinical_context': 'Blood disorder affecting oxygen carrying capacity; defects may indicate abnormal blood supply'
    }
}