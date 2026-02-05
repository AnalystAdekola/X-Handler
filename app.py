import streamlit as st
import google.generativeai as genai
import random

# --- SETUP ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- ADD CREATIVITY CONTROLS ---
st.sidebar.header("Level of Creativity")
creativity = st.sidebar.slider("How 'human' should I be?", 0.1, 1.0, 0.7)

# Create the model with the dynamic temperature
model = genai.GenerativeModel(
    model_name='gemini-pro',
    generation_config={
        "temperature": creativity, # This stops the repetitive answers
        "top_p": 0.95,
        "top_k": 40,
    }
)

# --- REFINED PROMPT ---
# We add a 'random seed' or instruction to keep it fresh
def generate_fresh_post(topic):
    rules = f"""
    Write a post about {topic}. 
    Use a fresh perspective. Do not use the same opening as previous posts.
    Keep it simple, human, and conversational.
    Random style hint: {random.choice(['question-based', 'story-style', 'bold-statement', 'list-format'])}
    """
    response = model.generate_content(rules)
    return response.text
