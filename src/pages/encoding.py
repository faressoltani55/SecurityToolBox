import streamlit as st

from src.logic.encoding.constants import ASCII_BINARY_ENCODINGS
import src.logic.encoding.functions as enc


def process_input(message, encoding):
    right, left = st.beta_columns(2)
    with right:
        encode = st.button('Encode')
    with left:
        decode = st.button('Decode')
    if encode:
        return enc.encode(message, encoding)
    elif decode:
        return enc.decode(message, encoding)


def write():
    st.title("Encode/Decode text")
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    message = st.text_area("Write your message here")

    encoding = st.selectbox("Start by choosing the type of Binary-ASCII encoding: ", ASCII_BINARY_ENCODINGS)
    result = process_input(message, encoding)
    if result is not None:
        st.text(result)

