import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
from typing import Dict, Final, Optional, Sequence
from footer import show_footer
import psycopg2
import hashlib
import re
from datetime import datetime

def home():
    show_pages([
        Page("home.py","Home"),
        Page("app.py","App")
    ])

    hide_pages(['App'])

    st.sidebar.empty()
    #hide sidebar in streamlit app

    custom_css = """
    <style>
        /* Set color for text */
        body {
            color: #71eea8 !important;
        }

        /* Set color for button text */
        .css-1oktun7.e1m5b4gh0:hover {
            color: #71eea8 !important;
        }

        /* Set color for button background on hover */
        .css-1oktun7.e1m5b4gh0:hover:not([disabled]) {
            background-color: #71eea8 !important;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    TITLE: Final = "Welcome to Kathalyst"

    def pretty_title(title: str) -> None:
        """Make a centered title, and give it a red line. Adapted from
        'streamlit_extras.colored_headers' package.
        Parameters:
        -----------
        title : str
            The title of your page.
        """
        st.markdown(
            f"<h2 style='text-align: center'>{title}</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            (
                '<hr style="background-color: #71eea8; margin-top: 0;'
                ' margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">'
            ),
            unsafe_allow_html=True,
        )

    pretty_title(TITLE)

    try:
        conn = psycopg2.connect(
            host="kserver-mvp.postgres.database.azure.com",
            database="postgres",
            user="dev_mvp",
            password="katha@0b0bc56"
        )

    except psycopg2.OperationalError:
        st.error("Failed to connect to the database.")
        exit()

    # Create a cursor to execute queries
    cur = conn.cursor()

    def login_form():
        with st.form("Login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.form_submit_button("Log In"):
                if not username or not password:
                    st.error("Please enter both username and password.")
                else:
                    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

                    # Check if the username and password exist in the database
                    cur.execute("SELECT * FROM mvp.users WHERE username = %s AND password = %s", (username, hashed_password))
                    result = cur.fetchone()

                    if result:
                        cur.execute("UPDATE mvp.users SET login_count = login_count + 1 WHERE username = %s", (username,))
                        conn.commit()

                        st.session_state.logged_in = True
                        st.success("Login successful.")
                        #st.snow()
                        switch_page("App")
                    else:
                        st.error("Invalid username or password.")


    def is_valid_email(email):
        #Simple email validation using regex
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, email)

    def is_valid_password(password):
        # Password must be at least 8 characters and contain both letters and numbers
        return len(password) >= 8 and any(char.isalpha() for char in password) and any(char.isdigit() for char in password)


    # Signup page
    def register_user_form():
        with st.form("Signup"):
            email = st.text_input("Email")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            
            
            if st.form_submit_button("Sign Up"):
                if username and password and email:
                    cur.execute("SELECT * FROM mvp.users WHERE username = %s", (username,))
                    result = cur.fetchone()

                    if result:
                        st.error("Username already exists.")
                    elif not is_valid_email(email):
                        st.error("Please enter a valid email address.")
                    elif not is_valid_password(password):
                        st.error("Password must be at least 8 characters long and contain both letters and numbers.")
                    elif password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        # Hash the password for security
                        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

                        # Insert the new user into the database
                        cur.execute("INSERT INTO mvp.users (username, password, email, created_at) VALUES (%s, %s, %s, %s)", (username, hashed_password, email, datetime.now()))
                        conn.commit()

                        st.session_state.logged_in = True
                        st.success("Login successful.")
                        #st.snow()
                        switch_page("App")

    login_tabs = st.empty()
    with login_tabs:
        login_tab1, login_tab2 = st.tabs(
            ["Login", "Register"]
        )
        with login_tab1:
            login_form()
        with login_tab2:
            register_user_form()


home()