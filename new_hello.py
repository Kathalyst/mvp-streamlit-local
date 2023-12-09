import streamlit as st

placeholder = st.empty()
placeholder.header("Sign Up Page")
placeholder.text("After header")

if placeholder.button("Submit"):
    i = 3
    placeholder.empty()

    st.sidebar.header("After Sign In")
    st.balloons()
    st.header("Application page")
    if st.button("Testing Button"):
        st.text("Great! you clicked the Test button")
