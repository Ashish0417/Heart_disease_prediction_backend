# ❤️ Heart Disease Prediction Backend API

A machine learning-powered FastAPI backend that predicts the likelihood of heart disease based on patient medical attributes. This backend offers not only predictions but also interpretable results with confidence scores, key contributing factors, and clinical insights.


---

## 🚀 Features

- **Accurate Predictions**: Heart disease risk assessment using ensemble machine learning
- **Uncertainty Quantification**: Reliability scores and confidence intervals
- **Interpretable Results**: Comprehensive JSON response including:
  - ✅ Prediction value and probability
  - 📊 Uncertainty estimation and reliability score
  - 🔍 Abnormal features with severity and explanations
  - 📈 Key contributors with SHAP-like feature importance
  - 💡 Clinical insights and health recommendations
  - 🖼️ Interactive data visualization (base64-encoded)
- **Developer-Friendly**: Full Swagger/OpenAPI documentation
- **Deployment-Ready**: Docker support for seamless deployment

---

## 🔧 Installation

### ✅ Requirements

- Python 3.8 or newer
- [pip](https://pip.pypa.io/en/stable/)
- Docker (optional)

### 🧪 Local Setup (Without Docker)

```bash
# 1. Clone the repository
git clone https://github.com/Ashish0417/Heart_disease_prediction_backend.git
cd Heart_disease_prediction_backend

# 2. (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Run the API
uvicorn main:app --reload
```

Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 🐳 Docker Setup

```bash
# 1. Build the image
docker build -t heart-disease-backend .

# 2. Run the container
docker run -d -p 8000:8000 heart-disease-backend
```

---

## 📨 API Usage

### Endpoint: `POST /predict`

#### Request Format
- **Content-Type:** `application/json`
- **Request Body Example:**

```json
{
  "age": 63,
  "sex": 1,
  "cp": 3,
  "trestbps": 145,
  "chol": 233,
  "fbs": 1,
  "restecg": 0,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 2.3,
  "slope": 0,
  "ca": 0,
  "thal": 1
}
```

#### Parameter Details

| Parameter | Description | Range |
|-----------|-------------|-------|
| `age` | Patient's age in years | Integer |
| `sex` | Gender (0=female, 1=male) | 0 or 1 |
| `cp` | Chest pain type | 0-3 |
| `trestbps` | Resting blood pressure (mm Hg) | Integer |
| `chol` | Serum cholesterol (mg/dl) | Integer |
| `fbs` | Fasting blood sugar > 120 mg/dl | 0 or 1 |
| `restecg` | Resting ECG results | 0-2 |
| `thalach` | Maximum heart rate achieved | Integer |
| `exang` | Exercise induced angina | 0 or 1 |
| `oldpeak` | ST depression induced by exercise | Float |
| `slope` | Slope of peak exercise ST segment | 0-2 |
| `ca` | Number of major vessels colored by fluoroscopy | 0-4 |
| `thal` | Thalassemia | 0-3 |

### ✅ Sample Response

```json
{
  "prediction": {
    "value": 1,
    "probability": 76.5,
    "risk_category": "High Risk"
  },
  "uncertainty": {
    "level": 23.5,
    "reliability": 76.5
  },
  "abnormal_features": {
    "age": {
      "value": 63,
      "z_score": 1.87,
      "severity": "Moderate",
      "note": "Age is a risk factor for heart disease, increasing with age"
    },
    "cp": {
      "value": 3,
      "z_score": 2.03,
      "severity": "Significant",
      "label": "Asymptomatic",
      "note": "Type of chest pain experienced; atypical symptoms may still indicate heart issues"
    },
    "trestbps": {
      "value": 145,
      "z_score": 1.65,
      "severity": "Moderate",
      "note": "Elevated blood pressure is a risk factor for heart disease"
    },
    "chol": {
      "value": 233,
      "z_score": 1.58,
      "severity": "Moderate",
      "note": "Elevated cholesterol is a risk factor for heart disease"
    },
    "fbs": {
      "value": 1,
      "z_score": 2.35,
      "severity": "Significant",
      "label": "FBS > 120 mg/dl",
      "note": "Elevated blood sugar may indicate diabetes, a heart disease risk factor"
    }
  },
  "key_contributors": {
    "cp": {
      "contribution": 0.2354,
      "original_value": 3,
      "mean_value": 1.37
    },
    "thal": {
      "contribution": 0.1876,
      "original_value": 1,
      "mean_value": 1.53
    },
    "age": {
      "contribution": 0.1453,
      "original_value": 63,
      "mean_value": 54.37
    },
    "ca": {
      "contribution": 0.1235,
      "original_value": 0,
      "mean_value": 0.73
    },
    "oldpeak": {
      "contribution": 0.1122,
      "original_value": 2.3,
      "mean_value": 1.04
    }
  },
  "report_date": "April 10, 2025",
  "clinical_insights": {
    "general": [
      "Patient shows elevated risk factors for heart disease.",
      "Model shows significant uncertainty in this prediction."
    ],
    "recommendations": [
      "Consider lifestyle modifications and monitoring of risk factors.",
      "Consider additional diagnostic tests to confirm cardiovascular status."
    ]
  },
  "visualization": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA..."
}
```

---

## 🧠 Response Field Explanations

| Field | Description |
|-------|-------------|
| `prediction.value` | Binary classification result (1 = heart disease likely, 0 = heart disease unlikely) |
| `prediction.probability` | Probability percentage of heart disease risk |
| `prediction.risk_category` | Categorized risk level (Low/Moderate/High/Very High Risk) |
| `uncertainty.level` | Model uncertainty percentage (lower is better) |
| `uncertainty.reliability` | Confidence in prediction (higher is better) |
| `abnormal_features` | Patient features that deviate significantly from normal ranges |
| `key_contributors` | Top features that most influenced the prediction outcome |
| `clinical_insights` | General observations and recommended medical actions |
| `visualization` | Base64-encoded PNG image showing patient feature profile |

---

## 🔄 API Performance

- **Average Response Time**: ~200ms
- **Parallelized Processing**: Concurrent feature analysis and visualization generation
- **Model Ensemble**: Multiple predictors for improved reliability
- **Memory Efficient**: Optimized for low resource usage

---

## 📘 License

MIT License © 2025

---

## 👨‍⚕️ Author

Developed by [Ashish0417](https://github.com/Ashish0417)  
With ❤️ for healthcare and AI.

---

## 📚 References

- Heart Disease UCI Dataset: [Kaggle](https://www.kaggle.com/ronitf/heart-disease-uci)
- FastAPI Documentation: [FastAPI](https://fastapi.tiangolo.com/)
- Scikit-learn Documentation: [Scikit-learn](https://scikit-learn.org/)
