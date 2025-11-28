import streamlit as st
import pandas as pd

def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        /* Main Background with subtle gradient */
        .stApp {
            background: linear-gradient(135deg, #0e1117 0%, #161b22 100%);
            color: #e6edf3;
            font-family: 'Inter', sans-serif;
        }
        
        /* Glassmorphism Card Styling */
        .metric-card {
            background: rgba(22, 27, 34, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 24px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
            border-color: rgba(255, 255, 255, 0.2);
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            letter-spacing: -0.5px;
        }
        
        /* Pulse Animation for Header */
        @keyframes pulse-glow {
            0% { transform: scale(1); filter: drop-shadow(0 0 0px rgba(255, 75, 75, 0)); }
            50% { transform: scale(1.05); filter: drop-shadow(0 0 10px rgba(255, 75, 75, 0.5)); }
            100% { transform: scale(1); filter: drop-shadow(0 0 0px rgba(255, 75, 75, 0)); }
        }
        .pulse-icon {
            display: inline-block;
            animation: pulse-glow 3s infinite ease-in-out;
        }
        
        /* Custom Button Styling */
        .stButton button {
            background: linear-gradient(90deg, #238636 0%, #2ea043 100%);
            border: none;
            color: white;
            font-weight: 600;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            transition: all 0.2s;
        }
        .stButton button:hover {
            box-shadow: 0 4px 12px rgba(46, 160, 67, 0.4);
            transform: scale(1.02);
        }
        </style>
    """, unsafe_allow_html=True)

def setup_page():
    st.set_page_config(page_title="Emerge", page_icon="🏥", layout="wide")
    load_css()

def render_brand():
    st.markdown("""
        <div style='text-align: center; padding-bottom: 20px;'>
            <h1 style='color: #ff4b4b;'>
                <span class='pulse-icon'>🏥</span> Emerge
            </h1>
            <h3 style='color: #a0a0a0; font-style: italic;'>
                "AI-Powered Patient Prioritization."
            </h3>
        </div>
    """, unsafe_allow_html=True)

def render_metrics(visual_score, symptom_score, final_score):
    col1, col2, col3 = st.columns(3)
    
    # Determine color for final score
    if final_score > 8:
        score_color = "#ff4b4b" # Red
        status = "CRITICAL"
    elif final_score > 5:
        score_color = "#ffa500" # Orange
        status = "MEDIUM"
    else:
        score_color = "#00cc96" # Green
        status = "LOW"
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <h4 style="margin:0; color:#a0a0a0;">Visual Pain</h4>
                <h2 style="margin:0; font-size: 2.5rem;">{visual_score}/10</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <h4 style="margin:0; color:#a0a0a0;">Symptom Score</h4>
                <h2 style="margin:0; font-size: 2.5rem;">{symptom_score}/10</h2>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="metric-card" style="border-color: {score_color};">
                <h4 style="margin:0; color:{score_color};">Urgency Score</h4>
                <h2 style="margin:0; font-size: 3rem; color: {score_color};">{final_score}/10</h2>
                <p style="margin:0; color: {score_color}; font-weight: bold;">{status}</p>
            </div>
        """, unsafe_allow_html=True)

def render_patient_list(patients):
    st.markdown("### 📋 Live ER Waiting List")
    
    if not patients:
        st.info("Waiting room is empty.")
        return

    df = pd.DataFrame(patients)
    
    # Sort by urgency descending
    df = df.sort_values(by="Urgency Score", ascending=False)
    
    # Reset index for display
    df = df.reset_index(drop=True)
    
    # Style the dataframe
    def highlight_critical(row):
        if row['Urgency Score'] > 8:
            return ['background-color: rgba(255, 75, 75, 0.2); color: white'] * len(row)
        elif row['Urgency Score'] > 5:
            return ['background-color: rgba(255, 165, 0, 0.2); color: white'] * len(row)
        else:
            return [''] * len(row)

    st.dataframe(df.style.apply(highlight_critical, axis=1), use_container_width=True)
