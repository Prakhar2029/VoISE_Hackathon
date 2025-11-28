import sqlite3
import os
import pandas as pd
from datetime import datetime

DB_FILE = "patients.db"

def init_db():
    """Initialize the database with the patients table."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            complaint TEXT,
            visual_score REAL,
            symptom_score REAL,
            urgency_score REAL,
            emotion TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_patient(patient_data):
    """Add a new patient record."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO patients (name, complaint, visual_score, symptom_score, urgency_score, emotion, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        patient_data["Name"],
        patient_data["Complaint"],
        patient_data["Visual Score"],
        patient_data["Symptom Score"],
        patient_data["Urgency Score"],
        patient_data["Emotion"],
        patient_data["Time"]
    ))
    conn.commit()
    conn.close()

def get_patients():
    """Retrieve all patients as a list of dictionaries."""
    if not os.path.exists(DB_FILE):
        return []
    
    conn = sqlite3.connect(DB_FILE)
    # Use pandas for easy conversion to list of dicts
    try:
        df = pd.read_sql_query("SELECT * FROM patients", conn)
        # Rename columns to match the app's expected format
        df = df.rename(columns={
            "name": "Name",
            "complaint": "Complaint",
            "visual_score": "Visual Score",
            "symptom_score": "Symptom Score",
            "urgency_score": "Urgency Score",
            "emotion": "Emotion",
            "timestamp": "Time"
        })
        return df.to_dict('records')
    except Exception:
        return []
    finally:
        conn.close()

def clear_patients():
    """Clear all patient records."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM patients")
    conn.commit()
    conn.close()
