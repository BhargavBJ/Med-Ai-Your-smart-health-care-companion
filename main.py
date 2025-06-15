from diagnosis_agent import diagnose_patient
from diet_agent import suggest_diet
from routine_agent import suggest_routine
import streamlit as st
MONGO_URI = st.secrets["MONGO_URI"]


def login_page():
    st.title("🧑‍⚕️ Patient Login")
    name = st.text_input("Enter your name")
    email = st.text_input("Enter your email")
    if st.button("Login"):
        if name and email:
            st.session_state.logged_in = True
            st.session_state.name = name
            st.session_state.email = email
        else:
            st.warning("Please enter both name and email.")

def main_page():
    st.title("AI Health Assistant")
    st.markdown(f"👤 Logged in as: **{st.session_state.name}**  \n📧 **{st.session_state.email}**")

    col1, col2, col3 = st.columns(3)

    if col1.button("🧪 Diagnose Patient"):
        st.markdown(diagnose_patient(st.session_state.name, st.session_state.email), unsafe_allow_html=True)

    if col2.button("🥗 Suggest Diet"):
        st.markdown(suggest_diet(st.session_state.name, st.session_state.email), unsafe_allow_html=True)

    if col3.button("🏃 Recommend Routine"):
        st.markdown(suggest_routine(st.session_state.name, st.session_state.email), unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    main_page()
else:
    login_page()
