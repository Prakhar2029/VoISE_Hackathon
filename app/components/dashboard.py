import streamlit as st
import pandas as pd

def render_header():
    st.set_page_config(page_title="The Sentinel", page_icon="🏥", layout="wide")
    st.title("🏥 The Sentinel: AI-Powered ER Triage")
    st.markdown("### 'Patients lie, Biometrics don't.'")

def render_metrics(visual_score, symptom_score, final_score):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Visual Pain Score", value=f"{visual_score}/10")
    
    with col2:
        st.metric(label="Symptom Score", value=f"{symptom_score}/10")
        
    with col3:
        st.metric(label="Final Urgency Score", value=f"{final_score}/10", delta_color="inverse")

def render_patient_list(patients):
    st.subheader("Live ER Waiting List (Prioritized by AI)")
    
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
            return ['background-color: #ff4b4b; color: white'] * len(row)
        elif row['Urgency Score'] > 5:
            return ['background-color: #ffa500; color: black'] * len(row)
        else:
            return [''] * len(row)

    st.dataframe(df.style.apply(highlight_critical, axis=1), use_container_width=True)
