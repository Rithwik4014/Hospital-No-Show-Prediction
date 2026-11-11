import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "carepredict.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT,
            age INTEGER,
            neighbourhood TEXT,
            appointment_date TEXT,
            waiting_days INTEGER,
            prediction TEXT,
            probability REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_prediction(patient, prediction, probability):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (gender, age, neighbourhood, appointment_date,
         waiting_days, prediction, probability)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        patient["Gender"],
        patient["Age"],
        patient["Neighbourhood"],
        patient["AppointmentDay"],
        patient["WaitingDays"],
        prediction,
        probability
    ))

    connection.commit()
    connection.close()


def get_predictions():
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM predictions ORDER BY id DESC")
    records = cursor.fetchall()

    connection.close()
    return records


def get_analytics():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_predictions,

            SUM(CASE
                WHEN prediction = 'High No-Show Risk' THEN 1
                ELSE 0
            END) AS high_risk,

            SUM(CASE
                WHEN prediction = 'Low No-Show Risk' THEN 1
                ELSE 0
            END) AS low_risk,

            COALESCE(AVG(probability), 0) AS average_probability

        FROM predictions
    """)

    result = cursor.fetchone()
    connection.close()

    return {
        "total_predictions": result[0],
        "high_risk": result[1] or 0,
        "low_risk": result[2] or 0,
        "average_probability": round(result[3], 2)
    }