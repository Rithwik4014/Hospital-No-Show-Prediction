from flask import Flask, render_template, request
import pandas as pd
import joblib
import sys
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

# Import database functions
sys.path.insert(0, str(BASE_DIR))

from database import (
    create_table,
    save_prediction,
    get_predictions,
    get_analytics
)

# Initialize database
create_table()

# Load dataset
data_path = BASE_DIR / "data" / "cleaned_hospital_appointments.csv"
df = pd.read_csv(data_path)

neighbourhoods = sorted(df["Neighbourhood"].unique())

# Load trained model
model_path = BASE_DIR / "models" / "best_gradient_boosting.pkl"
model = joblib.load(model_path)

# Load preprocessing pipeline
artifacts_path = BASE_DIR / "models" / "preprocessing_artifacts.pkl"
artifacts = joblib.load(artifacts_path)

preprocessor = artifacts["preprocessor"]

THRESHOLD = 0.20


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/prediction')
def prediction():
    return render_template(
        'prediction.html',
        neighbourhoods=neighbourhoods
    )


@app.route('/history')
def history():
    records = get_predictions()

    return render_template(
        'history.html',
        records=records
    )


# Analytics Dashboard
@app.route('/dashboard')
def dashboard():
    analytics = get_analytics()

    return render_template(
        'dashboard.html',
        analytics=analytics
    )


@app.route('/predict', methods=['POST'])
def predict():

    try:
        # Collect patient information
        gender = request.form.get("Gender", "")
        age = int(request.form.get("Age", ""))
        neighbourhood = request.form.get("Neighbourhood", "")

        scholarship = int(request.form.get("Scholarship", ""))
        hypertension = int(request.form.get("Hipertension", ""))
        diabetes = int(request.form.get("Diabetes", ""))
        alcoholism = int(request.form.get("Alcoholism", ""))
        handicap = int(request.form.get("Handcap", ""))
        sms_received = int(request.form.get("SMS_received", ""))

        # Receive dates
        scheduled_date = datetime.strptime(
            request.form.get("ScheduledDay", ""), "%Y-%m-%d"
        )

        appointment_date = datetime.strptime(
            request.form.get("AppointmentDay", ""), "%Y-%m-%d"
        )

        # Validate gender
        if gender not in ["F", "M"]:
            raise ValueError("Invalid gender.")

        # Validate age
        if not 0 <= age <= 100:
            raise ValueError("Age must be between 0 and 100.")

        # Validate neighbourhood
        if neighbourhood not in neighbourhoods:
            raise ValueError("Invalid neighbourhood.")

        # Validate binary fields
        binary_fields = [
            scholarship,
            hypertension,
            diabetes,
            alcoholism,
            sms_received
        ]

        if any(value not in [0, 1] for value in binary_fields):
            raise ValueError("Invalid yes/no selection.")

        # Validate handicap
        if handicap not in [0, 1, 2, 3, 4]:
            raise ValueError("Invalid handicap level.")

        # Validate dates
        if appointment_date < scheduled_date:
            raise ValueError(
                "Appointment date cannot be before scheduled date."
            )

        # Calculate appointment features
        waiting_days = (appointment_date - scheduled_date).days
        appointment_day = appointment_date.weekday()

        # Prepare patient data
        patient_data = {
            "Gender": gender,
            "Age": age,
            "Neighbourhood": neighbourhood,
            "Scholarship": scholarship,
            "Hipertension": hypertension,
            "Diabetes": diabetes,
            "Alcoholism": alcoholism,
            "Handcap": handicap,
            "SMS_received": sms_received,
            "WaitingDays": waiting_days,
            "AppointmentDayOfWeek": appointment_day,
            "AppointmentDay": appointment_date.strftime("%Y-%m-%d")
        }

        # Prepare model input
        input_df = pd.DataFrame([{
            key: value
            for key, value in patient_data.items()
            if key != "AppointmentDay"
        }])

        # Apply preprocessing
        processed_input = preprocessor.transform(input_df)

        # Predict probability
        probability = model.predict_proba(processed_input)[0][1]

        probability_percentage = round(probability * 100, 2)

        # Determine risk level
        if probability >= THRESHOLD:
            prediction_result = "High No-Show Risk"
            risk_level = "high"
        else:
            prediction_result = "Low No-Show Risk"
            risk_level = "low"

        # Save prediction to database
        save_prediction(
            patient_data,
            prediction_result,
            probability_percentage
        )

        # Display prediction result
        return render_template(
            'results.html',
            prediction=prediction_result,
            risk_level=risk_level,
            probability=probability_percentage
        )

    except (KeyError, ValueError, TypeError) as error:
        return f"Invalid patient information: {error}", 400


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)