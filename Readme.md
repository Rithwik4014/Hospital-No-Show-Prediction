# CarePredict – Hospital No-Show Prediction System

An AI-powered machine learning application that predicts the likelihood of patients missing their scheduled hospital appointments.

## Project Overview

CarePredict is a machine learning-based decision-support system developed to analyse historical hospital appointment data and estimate the risk of appointment no-shows.

The application allows users to enter patient and appointment details, receive a prediction with a probability score, view previous predictions, and monitor prediction statistics through an analytics dashboard.

## Problem Statement

Missed hospital appointments can lead to inefficient resource utilisation, scheduling difficulties, and reduced healthcare accessibility.

CarePredict explores how machine learning can help identify appointments with a higher estimated no-show risk.

## Objectives

- Analyse historical hospital appointment data.
- Identify patterns associated with missed appointments.
- Build and evaluate machine learning classification models.
- Integrate the selected model into a Flask web application.
- Store prediction records using SQLite.
- Display prediction history and analytics.

## Dataset

**Dataset:** Medical Appointment No Shows  
**Source:** Kaggle  
**Original records:** 110,527  
**Final cleaned records:** 110,521

The dataset contains appointment information such as:

- Gender
- Age
- Neighbourhood
- Scholarship
- Hypertension
- Diabetes
- Alcoholism
- Handicap
- SMS Received
- Appointment information
- No-show status

## Data Preprocessing

The following preprocessing operations were performed:

1. Removed invalid age records.
2. Converted appointment dates into datetime format.
3. Calculated waiting days between scheduling and appointment.
4. Removed records with negative waiting days.
5. Extracted appointment weekdays.
6. Removed unnecessary patient and appointment identifiers.
7. Encoded categorical variables using One-Hot Encoding.
8. Scaled numerical features using StandardScaler.
9. Split the dataset into training and testing sets using stratification.

## Machine Learning Models

The following models were trained and evaluated:

- Logistic Regression
- Balanced Logistic Regression
- Random Forest
- Decision Tree
- Gradient Boosting
- Tuned Random Forest
- Tuned Gradient Boosting

Gradient Boosting was selected for integration into the web application.

The application uses a probability threshold of 0.20 to classify predictions:

- Probability >= 20%: High No-Show Risk
- Probability < 20%: Low No-Show Risk

The threshold prioritises identifying more potential no-shows, but can also produce false positives.

## Application Features

### 1. Patient Prediction
Enter patient details and appointment information to estimate no-show probability.

### 2. Prediction Results
Displays:
- Predicted risk category
- No-show probability
- Visual probability indicator

### 3. Prediction History
Stores and displays previously generated predictions.

### 4. Analytics Dashboard
Displays:
- Total predictions
- High-risk predictions
- Low-risk predictions
- Average no-show probability
- Prediction distribution chart
- Risk overview chart

## Technology Stack

| Category | Technologies |

| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Data Visualisation | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Model Storage | Joblib |
| Development Environment | VS Code, Jupyter Notebook |

## Project Structure

```text
Hospital_No_Show_Prediction/
│
├── app/
│   ├── app.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── prediction.html
│   │   ├── results.html
│   │   ├── history.html
│   │   └── dashboard.html
│   │
│   └── static/
│       └── style.css
│
├── data/
│   ├── KaggleV2-May-2016.csv
│   └── cleaned_hospital_appointments.csv
│
├── models/
│   ├── preprocessing_artifacts.pkl
│   ├── best_random_forest.pkl
│   └── best_gradient_boosting.pkl
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering_preprocessing.ipynb
│   └── 04_model_training_evaluation.ipynb
│
├── database.py
├── requirements.txt
├── Readme.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Rithwik4014/Hospital-No-Show-Prediction.git
```

### 2. Navigate to the project directory

```bash
cd Hospital-No-Show-Prediction
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app/app.py
```

### 7. Open in your browser

```text
http://127.0.0.1:5000
```

## Model Evaluation

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

The project considers recall and F1-score important because the dataset contains fewer no-show cases than attended appointments.

## Limitations

- The model is trained on a historical dataset and may not generalise to every hospital.
- The classification threshold involves a trade-off between recall and precision.
- High-risk predictions can include false positives.
- The system is an academic prototype and has not been clinically validated.

## Future Improvements

- Improve model performance through additional feature engineering and model experimentation.
- Explore more effective class-imbalance handling techniques.
- Add user authentication and role-based access.
- Improve dashboard analytics.
- Deploy the application to a cloud platform.

## Disclaimer

CarePredict is an academic machine learning project developed for educational purposes. Predictions are estimates based on historical data and should not be treated as medical advice or clinical decisions.

## Author

**Thotamsetty Rithwik**  
B.Tech – Computer Science and Engineering

GitHub: https://github.com/Rithwik4014