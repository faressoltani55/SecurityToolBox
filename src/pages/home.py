import pathlib

import streamlit as st


def write():
    st.title("Welcome to Security Tool Box")
    st.text("The needed tools for basic security measures and protection")
    st.markdown(
        """
        <div style="width:100%;height:0;padding-bottom:56%;position:relative;">
            <iframe src="https://giphy.com/embed/115BJle6N2Av0A" width="100%" height="100%" style="position:absolute" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )
