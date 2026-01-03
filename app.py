import streamlit as st
import google.generativeai as genai
import time
import os

# --- 1. INITIAL SETUP ---
st.set_page_config(page_title="MatchVision AI", page_icon="⚽", layout="wide")

# Securely load API Key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("API Key not found. Please add 'GEMINI_API_KEY' to your secrets.")
    st.stop()

# Define a deeper Tactical Persona
SYSTEM_PROMPT = (
    "You are an elite football tactical analyst. For every video segment, you must provide "
    "a detailed breakdown. Use Markdown headers for: 'Formation Analysis', 'Off-the-Ball Movement', "
    "'Defensive Transition', and 'Key Player Observations'. Be specific and professional."
)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=SYSTEM_PROMPT
)

# --- 2. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/football.png", width=80)
    st.title("MatchVision Pro")
    st.write("---")
    analysis_focus = st.multiselect(
        "Focus Areas", 
        ["Pressing Traps", "Counter-Attacking", "Low Block Integrity", "Space Creation"],
        default=["Space Creation"]
    )
    st.info("The AI will prioritize these areas in the analysis.")

# --- 3. MAIN DASHBOARD ---
st.title("⚽ MatchVision AI: Tactical Lab")

uploaded_video = st.file_uploader("Upload match footage", type=['mp4', 'mov', 'avi'])

if uploaded_video:
    # Top Section: Video Player
    st.video(uploaded_video)
    
    if st.button("🚀 Run AI Tactical Breakdown", use_container_width=True):
        with st.spinner("AI is analyzing frames..."):
            try:
                # Save temp file
                temp_path = "temp_match.mp4"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_video.read())

                # Upload to Gemini
                video_file = genai.upload_file(path=temp_path)
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)

                # Generate Content
                prompt = f"Analyze this clip focusing on: {', '.join(analysis_focus)}."
                response = model.generate_content([video_file, prompt])
                
                # Store result in session state
                st.session_state.raw_analysis = response.text
                os.remove(temp_path)
                
            except Exception as e:
                st.error(f"Analysis failed: {e}")

    # Bottom Section: Organized Insights using Tabs
    if 'raw_analysis' in st.session_state:
        st.divider()
        tab1, tab2 = st.tabs(["📊 Full Analysis", "📋 Quick Summary"])
        
        with tab1:
            st.markdown(st.session_state.raw_analysis)
        
        with tab2:
            # We ask the AI to summarize its own previous output
            with st.expander("See Key Takeaways"):
                st.write("Click the button above to regenerate a fresh analysis.")
                st.info("This is where your scout's 'Bottom Line' will appear.")

else:
    st.warning("Please upload a video file to begin.")