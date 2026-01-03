import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
# This looks for your key in .streamlit/secrets.toml (locally) 
# or in the Streamlit Cloud "Secrets" settings (when live)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("API Key not found. Please add 'GEMINI_API_KEY' to your secrets.")
    st.stop()

# --- 2. UI DESIGN ---
st.set_page_config(page_title="Pitch Vision AI", page_icon="📈")
st.title("🚀 Pitch Vision AI")
st.markdown("""
    Welcome to your AI Pitch Consultant. 
    Enter your idea below to get a professional analysis.
""")

# Input area
user_input = st.text_area("What is your pitch idea?", height=150, placeholder="e.g. A subscription service for organic dog treats...")

# --- 3. AI LOGIC ---
if st.button("Analyze My Pitch"):
    if user_input:
        with st.spinner("🤖 Gemini is analyzing your pitch..."):
            try:
                # Initializing the model (Flash is faster and cost-effective)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Sending the prompt to Google AI
                response = model.generate_content(f"Analyze the following pitch and provide feedback on its strengths, weaknesses, and potential: {user_input}")
                
                # Displaying the output
                st.success("Analysis Complete!")
                st.subheader("Professional Feedback")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred with the AI: {e}")
    else:
        st.warning("Please enter a pitch idea first!")

# --- 4. SIDEBAR (Optional) ---
with st.sidebar:
    st.info("Built with Google Gemini & Streamlit")
    if st.button("Clear Chat"):
        st.rerun()