import streamlit as st
import cv2
import numpy as np
import time
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.vision.camera import Camera
from app.vision.detector import EmotionDetector
from app.audio.recorder import AudioRecorder
from app.audio.transcriber import Transcriber
from app.logic.symptoms import SymptomAnalyzer
from app.logic.scoring import UrgencyScorer
from app.components.dashboard import render_header, render_metrics, render_patient_list

from app.audio.converter import convert_to_wav
from app.audio.speaker import Speaker
from app.database import init_db, add_patient, get_patients, clear_patients

# Initialize modules
if 'detector' not in st.session_state:
    st.session_state.detector = EmotionDetector()
if 'recorder' not in st.session_state:
    st.session_state.recorder = AudioRecorder()
if 'transcriber' not in st.session_state:
    st.session_state.transcriber = Transcriber()
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = SymptomAnalyzer()
if 'scorer' not in st.session_state:
    st.session_state.scorer = UrgencyScorer()
if 'speaker' not in st.session_state:
    st.session_state.speaker = Speaker()

# Initialize patient list (Load from DB)
if 'patients' not in st.session_state:
    st.session_state.patients = get_patients()

def main():
    init_db()
    render_header()
    
    # Refresh patients from DB
    st.session_state.patients = get_patients()
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Triage Settings")
        input_source = st.radio("Input Source", ["Live Camera/Mic", "Upload Files"])
        
        st.divider()
        st.header("New Patient Scan")
        patient_name = st.text_input("Patient Name")

        st.divider()

    # Logic based on input source
    if input_source == "Live Camera/Mic":
        with st.sidebar:
            start_scan = st.button("Start Live Scan")
        
        render_patient_list(st.session_state.patients)
        
        if start_scan:
            if not patient_name:
                st.error("Please enter patient name.")
            else:
                run_live_scan(patient_name)
                
    elif input_source == "Upload Files":
        render_upload_interface(patient_name)
        render_patient_list(st.session_state.patients)

def render_upload_interface(patient_name):
    st.markdown("### 📂 Upload Patient Data")
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded_video = st.file_uploader("Upload Video/Image", type=['jpg', 'png', 'jpeg', 'mp4'])
    with col2:
        uploaded_audio = st.file_uploader("Upload Audio", type=['wav', 'mp3', 'mp4', 'm4a'])
        
    if st.button("Diagnose Patient", type="primary"):
        if not patient_name:
            st.error("Please enter patient name in the sidebar.")
            return
        
        if not uploaded_video and not uploaded_audio:
            st.error("Please upload at least one file.")
            return
            
        run_file_scan(patient_name, uploaded_video, uploaded_audio)

def run_live_scan(name):
    st.divider()
    st.write(f"### Scanning Patient: {name} (Live)...")
    
    col1, col2 = st.columns(2)
    
    # 1. Vision Scan
    with col1:
        st.info("Recording Video (5s) for Smart Scan...")
        cam = Camera()
        temp_live_path = "temp_live_video.mp4"
        success = cam.record_video(temp_live_path, duration=5)
        cam.release()
        
        if success:
            # Use smart video processing
            visual_score, emotion, best_frame, emotion_dict = st.session_state.detector.process_video(temp_live_path)
            
            if best_frame is not None:
                # Convert to RGB for display
                frame_rgb = cv2.cvtColor(best_frame, cv2.COLOR_BGR2RGB)
                st.image(frame_rgb, caption=f"Best Frame (Emotion: {emotion})", width=300)
                st.success(f"Detected Emotion: {emotion.upper()}")
                
                # Show emotion probability
                if emotion_dict:
                    st.bar_chart(emotion_dict)
            else:
                st.error("Could not analyze video.")
                visual_score = 0
                emotion = "N/A"
        else:
            st.error("Camera failed to record.")
            visual_score = 0
            emotion = "N/A"

    # 2. Audio Scan
    with col2:
        st.info("Listening for Symptoms (5s)...")
        audio_data = st.session_state.recorder.listen(timeout=5, phrase_time_limit=5)
        
        if audio_data:
            text, error = st.session_state.transcriber.transcribe(audio_data)
            
            if error:
                st.error(f"Transcription Failed: {error}")
                text = ""
            else:
                st.write(f"**Transcript:** \"{text}\"")
            
            symptom_score, keywords = st.session_state.analyzer.calculate_symptom_score(text)
            if keywords:
                st.warning(f"Detected Keywords: {', '.join(keywords)}")
            else:
                st.write("No critical keywords detected.")
        else:
            st.error("No audio detected.")
            text = ""
            symptom_score = 0
            keywords = []

    finalize_scan(name, visual_score, symptom_score, emotion, text)

def run_file_scan(name, uploaded_video, uploaded_audio):
    st.divider()
    st.write(f"### Scanning Patient: {name} (File Upload)...")
    
    col1, col2 = st.columns(2)
    
    visual_score = 0
    emotion = "N/A"
    symptom_score = 0
    text = ""

    # 1. Vision Scan (File)
    with col1:
        if uploaded_video:
            st.info("Analyzing Visual Data (Smart Scan)...")
            # Save temp file
            temp_video_path = "temp_video.mp4"
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_video.getbuffer())
            
            # If it's an image, just read it
            if uploaded_video.type.startswith('image'):
                # DeepFace can read from path
                visual_score, emotion, emotion_dict = st.session_state.detector.analyze_frame(temp_video_path)
                st.image(uploaded_video, caption="Uploaded Image", width=300)
            else:
                # Use smart video processing
                visual_score, emotion, best_frame, emotion_dict = st.session_state.detector.process_video(temp_video_path)
                
                if best_frame is not None:
                    frame_rgb = cv2.cvtColor(best_frame, cv2.COLOR_BGR2RGB)
                    st.image(frame_rgb, caption=f"Best Frame (Emotion: {emotion})", width=300)
            
            st.success(f"Detected Emotion: {emotion.upper()}")
            
            # Show emotion probability
            if emotion_dict:
                st.bar_chart(emotion_dict)

    # 2. Audio Scan (File)
    with col2:
        if uploaded_audio:
            st.info("Analyzing Audio Data...")
            # Save temp file
            temp_audio_path = "temp_audio_input" + os.path.splitext(uploaded_audio.name)[1]
            with open(temp_audio_path, "wb") as f:
                f.write(uploaded_audio.getbuffer())
            
            # Convert to WAV
            wav_path = "temp_audio.wav"
            if convert_to_wav(temp_audio_path, wav_path):
                # Transcribe from file
                text, error = st.session_state.transcriber.transcribe_file(wav_path)
                
                if error:
                    st.error(f"Transcription Failed: {error}")
                    text = ""
                else:
                    st.write(f"**Transcript:** \"{text}\"")
                
                symptom_score, keywords = st.session_state.analyzer.calculate_symptom_score(text)
                if keywords:
                    st.warning(f"Detected Keywords: {', '.join(keywords)}")
                else:
                    st.write("No critical keywords detected.")
            else:
                st.error("Failed to convert audio file.")

    cleanup_temp_files()
    finalize_scan(name, visual_score, symptom_score, emotion, text)

def cleanup_temp_files():
    """Removes temporary files created during upload."""
    temp_files = ["temp_video.mp4", "temp_audio.wav", "temp_live_video.mp4"]
    for file in temp_files:
        if os.path.exists(file):
            try:
                os.remove(file)
            except Exception:
                pass
    
    # Also clean up any temp_audio_input.* files
    for file in os.listdir():
        if file.startswith("temp_audio_input"):
            try:
                os.remove(file)
            except Exception:
                pass

def finalize_scan(name, visual_score, symptom_score, emotion, text):
    # 3. Final Calculation
    final_score = st.session_state.scorer.calculate_final_score(visual_score, symptom_score)
    
    render_metrics(visual_score, symptom_score, final_score)
    
    # Speak result
    if final_score > 8:
        diagnosis = f"Critical Priority. Score {final_score}. Immediate attention required."
    elif final_score > 5:
        diagnosis = f"Medium Priority. Score {final_score}. Please wait."
    else:
        diagnosis = f"Low Priority. Score {final_score}."
        
    st.session_state.speaker.speak(diagnosis)
    
    # Add to list
    new_patient = {
        "Name": name,
        "Complaint": text if text else "N/A",
        "Visual Score": visual_score,
        "Symptom Score": symptom_score,
        "Urgency Score": final_score,
        "Emotion": emotion,
        "Time": time.strftime("%H:%M:%S")
    }
    
    add_patient(new_patient)
    st.session_state.patients = get_patients()
    st.success("Patient added to triage list.")
    time.sleep(3)
    st.rerun()

if __name__ == "__main__":
    main()
