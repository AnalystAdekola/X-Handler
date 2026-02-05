import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import os
import random

# --- 1. SETTINGS & CONFIG ---
st.set_page_config(page_title="HAC Digital Assistant", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .stSidebar { background-color: #161b22; }
    h1 { color: #58a6ff; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background-color: #238636 !important; color: white !important; width: 100%; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. AI SETUP ---
# Replace with your actual key or use st.secrets["GOOGLE_API_KEY"]
API_KEY = "YOUR_GOOGLE_API_KEY_HERE" 
genai.configure(api_key=API_KEY)

# --- 3. NAVIGATION MENU ---
menu = st.sidebar.radio("CHOOSE TOOL", ["📊 Data Viz Tool", "🐦 X-Handler AI"])

# ---------------------------------------------------------
# TOOL 1: DATA VISUALIZATION
# ---------------------------------------------------------
if menu == "📊 Data Viz Tool":
    st.title("📊 SMART DATA VIZ")
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("📍 Data Preview")
        st.dataframe(df.head(3), use_container_width=True)

        all_cols = df.columns.tolist()
        
        # 3 Analysis Slots
        slots = []
        for i in range(1, 4):
            with st.sidebar.expander(f"CHART {i} SETTINGS"):
                cols = st.multiselect(f"Columns {i}", options=all_cols, key=f"c{i}")
                viz = st.selectbox(f"Style {i}", ["None", "Bar Chart", "Line Chart", "Pie Chart", "Histogram"], key=f"v{i}")
                slots.append({"cols": cols, "viz": viz})

        if st.sidebar.button("Show Dashboard"):
            active_slots = [s for s in slots if s["viz"] != "None"]
            display_cols = st.columns(len(active_slots))
            
            for idx, slot in enumerate(active_slots):
                with display_cols[idx]:
                    try:
                        if slot["viz"] == "Bar Chart":
                            fig = px.bar(df, x=slot["cols"][0], y=slot["cols"][1] if len(slot["cols"])>1 else None, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Prism)
                        elif slot["viz"] == "Line Chart":
                            fig = px.line(df, x=slot["cols"][0], y=slot["cols"][1] if len(slot["cols"])>1 else slot["cols"][0], template="plotly_dark")
                        
                        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error in Chart {idx+1}")

# ---------------------------------------------------------
# TOOL 2: X-HANDLER AI
# ---------------------------------------------------------
elif menu == "🐦 X-Handler AI":
    st.title("🐦 X CONTENT HANDLER")
    
    # Creativity Control to stop repetitive responses
    creativity = st.sidebar.slider("Human Creativity Level", 0.1, 1.0, 0.8)
    model = genai.GenerativeModel('gemini-pro', generation_config={"temperature": creativity})

    STRICT_RULES = """
    Rules: Use Simple English. No big grammar. Sound like a real person, not a bot.
    Use line breaks for space. No words like 'delve' or 'unleash'.
    """

    tab1, tab2 = st.tabs(["✨ Craft Post", "💬 Smart Reply"])

    with tab1:
        topic = st.text_input("Topic for today?")
        style = random.choice(["Story-based", "Short & Punchy", "Question for the audience"])
        
        if st.button("Generate Post"):
            if topic:
                prompt = f"{STRICT_RULES}\nStyle: {style}\nTopic: {topic}\nWrite a post for X (Twitter):"
                response = model.generate_content(prompt)
                st.subheader("Your Draft:")
                st.write(response.text)

    with tab2:
        others_post = st.text_area("Paste the post you want to reply to:")
        if st.button("Generate Reply"):
            if others_post:
                prompt = f"{STRICT_RULES}\nGenerate a natural, simple human response to this: {others_post}"
                response = model.generate_content(prompt)
                st.subheader("Suggested Reply:")
                st.write(response.text)
