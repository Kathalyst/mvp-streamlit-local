import streamlit as st

def show_footer():
    with st.sidebar:
        st.markdown(
            """
            <div style="position: fixed; bottom: 0; left: 25; text-align: center; padding: 0;">
                <p style="color: #f1f1f1; font-size: 14px; display: inline-block;">For any issues, contact:</p>
                <a style="color: #71eea8; font-size: 14px; text-decoration: none; display: inline-block;" href="mailto:hello@kathalyst.ai"> hello@kathalyst.ai</a>
                <p style="color: #f1f1f1; font-size: 12px; position: inline-block; bottom: 0; right: 0;">© 2023 Kathalyst. All Rights Reserved.</p>
            </div>
            """,
            unsafe_allow_html=True
            )


show_footer()