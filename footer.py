import streamlit as st

def show_footer():
    st.markdown(
        """
        <div style="position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; padding: 0px;">
            <p style="color: #f1f1f1; font-family: 'Karla', sans-serif; font-size: 14px; display: inline-block;">For any issues using the product or your account, contact us at</p>
            <p style="color: #71eea8; font-family: 'Karla', sans-serif; font-size: 14px; display: inline-block;"> hello@kathalyst.ai</p>
            <p style="color: #f1f1f1; font-family: 'Karla', sans-serif; font-size: 12px; position: inline-block; bottom: 0; right: 0;">© 2023 Kathalyst. All Rights Reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

show_footer()