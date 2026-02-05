import streamlit as st
import google.generativeai as genai
import random

# --- 1. SETTINGS & CONFIG ---
st.set_page_config(page_title="My X-Handler AI", page_icon="🐦")

# Sleek Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    h1 { color: #1d9bf0; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { 
        background-color: #1d9bf0 !important; 
        color: white !important; 
        border-radius: 20px; 
        font-weight: bold;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. API SETUP ---
# It is safer to use st.secrets for the key on Streamlit Cloud
# If running locally, you can replace this with your actual string: "AIza..."
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    API_KEY = "YOUR_ACTUAL_GOOGLE_API_KEY_HERE"

genai.configure(api_key=API_KEY)

# --- 3. THE "HUMAN" ENGINE ---
st.title("🐦 X-Handler AI")
st.write("Craft posts and replies in simple, human language.")

# Creativity slider to prevent repetitive responses
creativity = st.sidebar.slider("Creativity Level", 0.1, 1.0, 0.8)

# Initialize the model
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash', # Using Flash for faster response
    generation_config={"temperature": creativity}
)

# These rules are sent with every single request
STRICT_RULES = """
Role: You are a grounded, authentic human building in public.
Style: 
- Use Simple English. No 'big grammar' or academic words.
- Use line breaks between sentences. 
- Avoid bot-like words: 'delve', 'unleash', 'transformative', 'landscape'.
- Be helpful and slightly witty.
- Sound like a peer, not a lecturer.
"""

tab1, tab2 = st.tabs(["✨ Craft New Post", "💬 Smart Reply"])

# --- TAB 1: NEW POSTS ---
with tab1:
    topic = st.text_input("What's on your mind?", placeholder="e.g. Learning Python is hard but fun")
    
    if st.button("Generate Post Draft"):
        if topic:
            with st.spinner("Thinking..."):
                try:
                    style_hint = random.choice(["share a personal observation", "ask a question", "give a simple tip"])
                    prompt = f"{STRICT_RULES}\nTopic: {topic}\nInstruction: Write a short X post. {style_hint}."
                    
                    response = model.generate_content(prompt)
                    st.subheader("Draft:")
                    st.write(response.text)
                    st.caption(f"Character Count: {len(response.text)}")
                except Exception as e:
                    st.error(f"API Error: {e}. Check if your API Key is correct.")

# --- TAB 2: REPLIES ---
with tab2:
    others_post = st.text_area("Paste the post you want to reply to:", height=150)
    
    if st.button("Generate Human Reply"):
        if others_post:
            with st.spinner("Analyzing tone..."):
                try:
                    prompt = f"{STRICT_RULES}\nReply to this post in a natural way: {others_post}"
                    response = model.generate_content(prompt)
                    st.subheader("Suggested Reply:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"API Error: {e}")
