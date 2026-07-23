import streamlit as st
import base64
import os
from dotenv import load_dotenv
load_dotenv()

# Works locally (.env) and on Streamlit Cloud (st.secrets)
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
    os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]

from crew import run_trip_planner

st.set_page_config(page_title="AI Trip Planner", page_icon="✈️", layout="centered")

def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: 
                linear-gradient(rgba(255,255,255,0.88), rgba(255,255,255,0.88)),
                url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        [data-testid="stAppViewContainer"] {{
            background: transparent;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        .block-container {{
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 16px;
            padding: 2.5rem;
            margin-top: 1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_background("background.jpg")

st.title("✈️ AI Trip Planner")
# ... rest of your app
st.write("Enter your trip details and let AI agents build your itinerary.")

with st.form("trip_form"):
    destination = st.text_input("Destination", placeholder="e.g. Kyoto, Japan")
    duration_days = st.number_input("Number of days", min_value=1, max_value=30, value=4)
    num_people = st.number_input("Number of people", min_value=1, max_value=20, value=1)
    budget_level = st.selectbox("Budget level", ["budget", "mid-range", "luxury"])
    interests = st.text_input("Interests", placeholder="e.g. history, food, hiking")

    submitted = st.form_submit_button("Plan My Trip")

if submitted:
    if not destination or not interests:
        st.warning("Please fill in destination and interests.")
    else:
        with st.spinner("Your AI travel agents are working on it... this can take a minute or two."):
            outputs = run_trip_planner(destination, duration_days, num_people, budget_level, interests)

        st.success("Here's your itinerary!")
        st.markdown(outputs["itinerary"])

        st.divider()
        st.subheader("How the agents got there")

        with st.expander("🔍 Destination Research"):
            st.markdown(outputs["research"])

        with st.expander("💰 Budget Breakdown"):
            st.markdown(outputs["budget"])