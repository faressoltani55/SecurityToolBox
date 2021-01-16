import utils.enc_functions as enc
import streamlit as st


def process_input(encoding, input, file=False):
    right, left = st.beta_columns(2)
    with right:
        encode = st.button('Encode')
    with left:
        decode = st.button('Decode')
    if encode:
        return enc.encode_text(encoding, input)
    elif decode:
        return enc.decode_text(encoding, input)

def write():
    st.title("Encode/Decode text or file: ")
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    input_type = st.radio("Pick input type: ", ["Text input", "File input"])

    if input_type == "Text input":
        input = st.text_area("Write your message here")
    elif input_type == "File input":
        input = st.file_uploader("Choose a file to process", accept_multiple_files=False)

    encoding_type = st.selectbox("Start by choosing the type of encoding to deal with: ", ["Standard text encoding", "Base64", "URL"])

    if encoding_type == "Standard text encoding":
        encoding = st.selectbox("Pick the encoding: ", enc.get_standard_text_encodings())
        result = process_input(encoding, input)
        st.text(result)
    elif encoding_type == "Base64":
        return
    elif encoding_type == "URL":
        return