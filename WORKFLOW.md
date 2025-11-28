# The Sentinel: Triage Workflow

This document outlines the end-to-end workflow of **The Sentinel**, an AI-powered Multimodal ER Triage System.

## 1. Patient Intake (The Input)
The process begins when a patient interacts with the kiosk.
*   **Scenario A (Live Kiosk)**: The patient stands in front of the kiosk. The camera captures their face, and the microphone records their complaint.
*   **Scenario B (Remote/Upload)**: A paramedic or nurse uploads a pre-recorded video and audio file of the patient to the system.

## 2. Multimodal Analysis (The Processing)
The system processes the inputs simultaneously using three independent AI modules:

### A. Visual Analysis ("The Eyes")
*   **Input**: Video feed or uploaded video file.
*   **Action**: The **Computer Vision Module** (`DeepFace`) scans the patient's face for micro-expressions.
*   **Detection**: It looks for specific emotions indicative of physical distress:
    *   **Fear/Agony**: High Urgency.
    *   **Sadness (Grimace)**: Medium Urgency.
    *   **Neutral/Happy**: Low Urgency.
*   **Output**: A `Visual_Pain_Score` (0-10).

### B. Audio Analysis ("The Ears")
*   **Input**: Voice recording or uploaded audio file.
*   **Action**: The **Audio Module** first converts the audio to a processable format (WAV) if necessary.
*   **Transcription**: It uses Speech-to-Text to transcribe the patient's spoken words into text.
*   **Output**: A text transcript (e.g., "My chest hurts and I can't breathe").

### C. Semantic Logic ("The Brain")
*   **Input**: The text transcript.
*   **Action**: The **Logic Module** scans the text for "Kill Words"—keywords associated with life-threatening conditions.
*   **Weighting**:
    *   "Chest", "Heart", "Stroke" → **Critical (10 points)**
    *   "Breath", "Bleeding" → **High (8-9 points)**
    *   "Headache", "Dizzy" → **Medium (3-4 points)**
*   **Output**: A `Symptom_Score` (0-10).

## 3. Risk Calculation (The Decision)
The system aggregates the signals to calculate the final **Biometric Urgency Score**:

> **Formula**: `Final_Score = (Visual_Score * 0.6) + (Symptom_Score * 0.4)`

*   *Why this matters*: A patient might say "I'm fine" (Low Symptom Score), but their face shows extreme agony (High Visual Score). The algorithm catches this discrepancy and prioritizes them.

## 4. Triage & Output (The Action)
The system takes immediate action based on the `Final_Score`:

1.  **Dashboard Update**: The patient is added to the **Live ER Waiting List**.
    *   **Critical (>8)**: Row flashes **RED**.
    *   **Medium (>5)**: Row turns **ORANGE**.
    *   **Low (<5)**: Row remains standard.
2.  **Auto-Sorting**: The list automatically re-orders, placing the highest-risk patient at the top, regardless of arrival time.
3.  **Voice Announcement**: The system uses **Text-to-Speech** to announce the triage result (e.g., *"Critical Priority. Immediate attention required."*).

---
**"Patients lie. Biometrics don't."**
