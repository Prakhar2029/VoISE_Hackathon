# The Sentinel: Multimodal ER Triage System

**"Patients lie, Biometrics don't."**

The Sentinel is an AI-powered kiosk designed for Emergency Room triage. It prioritizes patients based on **Biometric Urgency** by analyzing three independent signals:
1.  **Visual Pain Analysis** (Facial Micro-expressions)
2.  **Audio Stress Analysis** (Voice Pitch/Jitter)
3.  **Semantic Symptom Analysis** (Verbal "Kill Words")

## Key Features

### 1. Multimodal Analysis
- **The Eyes**: Uses `DeepFace` to detect facial micro-expressions (Fear, Pain, Sadness).
- **The Ears**: Uses `SpeechRecognition` to transcribe patient complaints.
- **The Brain**: Analyzes keywords against a weighted medical dictionary to calculate urgency.

### 2. Flexible Input Modes
- **Live Mode**: Real-time scanning using Webcam and Microphone.
- **Upload Mode**: Support for pre-recorded Video (`.mp4`, `.mov`) and Audio (`.wav`, `.mp3`, `.m4a`) files.
- **Smart Video Scan**: Automatically scans uploaded videos to find the frame with the highest emotional intensity.

### 3. Intelligent Feedback
- **Text-to-Speech Diagnosis**: The system announces the triage priority verbally.
- **Transparency**: View the "Critical Symptom Keywords" used by the AI.
- **Confidence Charts**: Visual bar charts showing the probability of detected emotions.

## Project Structure

This project is designed for a 4-person team to work in parallel:

-   **`app/vision/`**: Computer Vision module (DeepFace).
-   **`app/audio/`**: Audio processing and speech-to-text.
-   **`app/logic/`**: Scoring algorithms and symptom weights.
-   **`app/components/`**: Shared Streamlit UI components.
-   **`app/main.py`**: Main application entry point.

## Setup & Installation

1.  **Clone the repository**
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application**:
    ```bash
    streamlit run app/main.py
    ```
    *Or use the provided `run.bat` script on Windows.*

## Dependencies

-   `streamlit`: UI framework
-   `deepface`: Facial emotion analysis
-   `opencv-python`: Camera handling
-   `SpeechRecognition`: Audio transcription
-   `pyttsx3`: Text-to-Speech engine
-   `moviepy` / `imageio-ffmpeg`: Audio conversion
-   `pandas`: Data management
