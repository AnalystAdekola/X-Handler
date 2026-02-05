import streamlit as st
import google.generativeai as genai
import random

# --- 1. SETTINGS ---
st.set_page_config(page_title="X-Handler AI", page_icon="🐦")

# API KEY SETUP
# Try to get from secrets first, then fallback to manual entry for testing
API_KEY = st.secrets.get("GOOGLE_API_KEY", "YOUR_ACTUAL_API_KEY_HERE")

try:
    genai.configure(api_key=API_KEY)
    # Using 'gemini-pro' as it is the most widely supported name across all versions
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. THE HUMAN ENGINE RULES ---
STRICT_RULES = """
Role: You are a grounded, authentic human building in public.
Tone: Simple English, no 'big grammar', no academic words.
Format: Use line breaks. No 'AI-speak' like 'delve' or 'transformative'.
Instructions: Sound like a peer chatting on X, not an AI bot.
"""

st.title("🐦 X-Handler AI")

tab1, tab2 = st.tabs(["✨ Craft New Post", "💬 Smart Reply"])

with tab1:
    topic = st.text_input("What's on your mind?", placeholder="e.g. My journey into tech")
    
    if st.button("Generate Post"):
        if topic:
            with st.spinner("Writing..."):
                try:
                    # Adding a bit of randomness to the prompt to keep it fresh
                    style = random.choice(["as a short story", "as a bold opinion", "as a quick tip"])
                    prompt = f"{STRICT_RULES}\nTopic: {topic}\nStyle: Write this {style} for an X post."
                    
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.subheader("Your Draft:")
                        st.write(response.text)
                        st.info(f"Character Count: {len(response.text)}")
                except Exception as e:
                    st.error("Model Error: Try checking your API key or the model name.")
                    st.info("Tip: Make sure you have 'google-generativeai' in your requirements.txt")

with tab2:
    others_post = st.text_area("Paste the post you want to reply to:")
    if st.button("Generate Reply"):
        if others_post:
            with st.spinner("Analyzing..."):
                try:
                    prompt = f"{STRICT_RULES}\nGenerate a simple, human-sounding reply to this: {others_post}"
                    response = model.generate_content(prompt)
                    st.subheader("Suggested Reply:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Reply Error: {e}")
