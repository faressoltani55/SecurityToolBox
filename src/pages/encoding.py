import utils.enc_functions as enc
import streamlit as st


def process_input(encoding, text):
    right, left = st.beta_columns(2)
    with right:
        encode = st.button('Encode')
    with left:
        decode = st.button('Decode')
    if encode:
        return enc.encode_text(encoding, text)
    elif decode:
        return enc.decode_text(encoding, text)


def write():
    st.title("Encode/Decode text")
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    input_text = st.text_area("Write your message here")

   # encoding_type = st.selectbox("Start by choosing the type of encoding to deal with: ",["Standard text encoding", "Base64", "URL"])
    encoding_type = st.selectbox("Start by choosing the type of Binary-ASCII encoding: ",  )
    if encoding_type == "Standard text encoding":
        encoding = st.selectbox("Pick the encoding: ", enc.get_standard_text_encodings())
        result = process_input(encoding, input_text)
        st.text(result)

