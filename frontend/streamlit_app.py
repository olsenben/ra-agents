import streamlit as st
import requests
import os
from dotenv import load_dotenv
from streamlit_utils import *
import pyrebase


load_dotenv()
"""
known issues: results don't display until selected from sidebar after initial run
something about the session state is clearing the selected query, breaking the delete button
"""

# password = st.text_input("Password", type="password")
# if password != st.secrets["STREAMLIT_PASSWORD"]:
#     st.stop()



#API_URL = "https://ra-agents.fly.dev"
API_URL = "http://backend:8000"
#FLY_API_KEY = os.environ.get("FLY_API_TOKEN") 
FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY") 



firebase_config = {
    'apiKey': FIREBASE_API_KEY,
    'authDomain': "ra-agents-c9e4b.firebaseapp.com",
    'databaseURL': "https://ra-agents-c9e4b-default-rtdb.firebaseio.com/",
    'projectId': "ra-agents-c9e4b",
    'storageBucket': "ra-agents-c9e4b.firebasestorage.app",
    'messagingSenderId': "993522025814",
    'appId': "1:993522025814:web:3b34c4f28162d6d2c402f7",
    'measurementId': "G-NMBRFZ9DBW"
 }

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()



if 'id_token' not in st.session_state:

    st.title("Welcome – Please Log In or Sign Up")

    # Initialize control flags if not already present
    if 'auth_choice' not in st.session_state:
        st.session_state.auth_choice = "Login"
    if 'just_logged_in' not in st.session_state:
        st.session_state.just_logged_in = False

    #use a form to ensure atomicity and avoid partial reruns
    with st.form(key='auth_form'):
        auth_choice = st.radio("Choose action", ["Login", "Sign Up"], key="auth_choice")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Submit")

        if submit:
            try:
                if auth_choice == "Login":
                    user = auth.sign_in_with_email_and_password(email, password)
                else:
                    auth.create_user_with_email_and_password(email, password)
                    user = auth.sign_in_with_email_and_password(email, password)

                st.session_state['id_token'] = user['idToken']
                st.session_state['just_logged_in'] = True
                st.rerun()

            except Exception as e:
                st.error("Authentication failed.")
                st.exception(e)

#after rerun: if user has just logged in, clear flags
elif st.session_state.get("just_logged_in", False):
    st.session_state.just_logged_in = True
    st.success("Logged in successfully!")


    headers = {
        "Authorization" : f"Bearer {st.session_state['id_token']}"
    }

    #remove top padding
    st.markdown("""
        <style>
        .main > div:first-child {
            padding-top: 0rem;
        }
        .block-container {
            padding-top: 0rem;
        }
        </style>
    """, unsafe_allow_html=True)

    #inject custom CSS
    st.markdown("""
        <style>
        .sticky-container {
            position: -webkit-sticky;
            position: sticky;
            top: 0;
            background-color: black;
            padding: 1rem;
            z-index: 999;
            border-bottom: 1px solid #ddd;
        }
        </style>
    """, unsafe_allow_html=True)

    #sticky header block
    st.markdown('<div class="sticky-container">', unsafe_allow_html=True)

    st.title("Multi-Agent Research Assistant")
    query = st.text_input("Enter a research topic", "glioblastoma")
    limit = st.slider("Number of papers to analyze", 1, 20, 5)
    analyze_button = st.button("Analyze")

    st.markdown('</div>', unsafe_allow_html=True)

    #load history and update sidebar
    update_sidebar(API_URL, headers, limit=20)

    if "selected_query" in st.session_state and st.session_state["selected_query"]:
        #only show matching result if selected
        runs = fetch_history(API_URL, headers, limit=20)
        selected_query = st.session_state["selected_query"]
        selected_run = next((run for run in runs if run["query"] == selected_query), None)

        if selected_run:
            display_data(selected_run)
            if st.button("Delete this entry"):
                url = f"{API_URL}/delete/{selected_run['id']}"
                response = requests.delete(f"{API_URL}/delete/{selected_run['id']}", headers=headers)
                if response.status_code == 200:
                    st.success("Entry deleted successfully")
                    st.session_state["selected_query"] = ""
                    st.rerun()
                else:
                    st.error("Failed to delete entry")
    else:
        st.write("Analyze or select a previous query from the sidebar.")

    if analyze_button:
        with st.spinner("Running multi-agent pipeline..."):
            try:
                data = fetch_data(query, API_URL, headers, limit=limit)
                st.session_state["selected_query"] = data["query"]
                st.rerun()
                #display_data(data)

            except requests.exceptions.RequestException as e:
                st.error(f"API request failed: {e}")
                

    logout_button = st.button("Logout")
    if logout_button:
        del st.session_state['id_token']
        st.rerun()